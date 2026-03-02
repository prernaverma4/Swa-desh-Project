"""
Customer support chatbot for Digital Catalyst.
Answers questions about the platform, heritage sites, and artisans.
"""

import re


def get_chat_response(message, get_heritage_sites, get_artisans, is_authenticated):
    """
    Return a response string for the user message.
    get_heritage_sites() and get_artisans() are callables that return list of model instances.
    """
    if not message or not message.strip():
        return "Please type a question. I can help with heritage sites, artisans, and how to use the platform."

    text = message.strip().lower()
    sites = get_heritage_sites()
    artisans = get_artisans()

    # Greetings
    if re.search(r'\b(hi|hello|hey|namaste|good morning|good evening)\b', text):
        return (
            "Hello! I'm the Digital Catalyst assistant. I can help you with:\n"
            "• Heritage sites – search by state or category\n"
            "• Artisans – find by state or craft\n"
            "• How to register, login, add sites/artisans, or export data\n\n"
            "What would you like to know?"
        )

    # What is this platform / Digital Catalyst
    if any(w in text for w in ['what is digital catalyst', 'what is this', 'what is this platform', 'about the platform', 'about this site']):
        return (
            "**Digital Catalyst** is an AI-driven platform for Indian economic growth and heritage preservation. "
            "It helps you manage and explore heritage sites, support traditional artisans, view analytics, "
            "and export data. Use the Dashboard for insights, Heritage Sites and Artisans menus to browse or add data, "
            "and Export to download CSV."
        )

    # Register / sign up
    if any(w in text for w in ['how to register', 'how do i register', 'sign up', 'create account', 'register']):
        return (
            "To **register**: click **Register here** on the login page (or go to /register). "
            "Enter username, email, and password, then submit. After that, log in with your username and password."
        )

    # Login
    if any(w in text for w in ['how to login', 'how do i login', 'log in', 'sign in', 'login']):
        return (
            "To **log in**: use the login page and enter your username and password. "
            "Demo credentials: username **admin**, password **admin123**."
        )

    # Heritage sites in [state]
    state_match = re.search(
        r'heritage\s*(?:sites?)?\s*(?:in|at|of)?\s*([a-z\s]+?)(?:\?|$|\.)',
        text
    ) or re.search(r'(?:sites?|places?)\s*in\s*([a-z\s]+?)(?:\?|$|\.)', text)
    if state_match:
        state = state_match.group(1).strip()
        if len(state) > 1:
            state_title = state.title()
            found = [s for s in sites if (s.state or '').lower() == state.lower()]
            if found:
                lines = [f"Heritage sites in **{state_title}**:"]
                for s in found[:10]:
                    lines.append(f"• {s.name} ({s.category}) – {s.annual_visitors:,} visitors/year")
                if len(found) > 10:
                    lines.append(f"... and {len(found) - 10} more. Check the Heritage Sites page for the full list.")
                return "\n".join(lines)
            else:
                states = list(set((s.state or '').strip() for s in sites if (s.state or '').strip()))
                return f"No heritage sites found for **{state_title}**. Available states: {', '.join(sorted(states)[:15])}{'...' if len(states) > 15 else '.'}"

    # Artisans in [state]
    artisan_state = re.search(
        r'artisans?\s*(?:in|at|from)?\s*([a-z\s]+?)(?:\?|$|\.)',
        text
    ) or re.search(r'crafts?men?\s*(?:in|at|from)?\s*([a-z\s]+?)(?:\?|$|\.)', text)
    if artisan_state:
        state = artisan_state.group(1).strip()
        if len(state) > 1:
            state_title = state.title()
            found = [a for a in artisans if (a.state or '').lower() == state.lower()]
            if found:
                lines = [f"Artisans in **{state_title}**:"]
                for a in found[:10]:
                    lines.append(f"• {a.name} – {a.craft} (₹{a.product_price:,.0f})")
                if len(found) > 10:
                    lines.append(f"... and {len(found) - 10} more. See the Artisans page for the full list.")
                return "\n".join(lines)
            else:
                states = list(set((a.state or '').strip() for a in artisans if (a.state or '').strip()))
                return f"No artisans found for **{state_title}**. Available states: {', '.join(sorted(states)[:15])}{'...' if len(states) > 15 else '.'}"

    # How many heritage sites / artisans
    if re.search(r'how many\s*(heritage\s*)?sites?', text):
        return f"There are **{len(sites)}** heritage sites in the database. Open the Dashboard or Heritage Sites to explore them."
    if re.search(r'how many\s*artisans?', text):
        return f"There are **{len(artisans)}** artisans in the database. Open the Dashboard or Artisans page to explore them."

    # List all states / categories / crafts
    if any(w in text for w in ['which states', 'list states', 'what states', 'states covered']):
        site_states = set((s.state or '').strip() for s in sites if (s.state or '').strip())
        artisan_states = set((a.state or '').strip() for a in artisans if (a.state or '').strip())
        all_states = sorted(site_states | artisan_states)
        return f"States covered: **{', '.join(all_states[:20])}{'...' if len(all_states) > 20 else ''}**"
    if any(w in text for w in ['categories', 'heritage categories', 'types of sites']):
        cats = sorted(set((s.category or '').strip() for s in sites if (s.category or '').strip()))
        return f"Heritage categories: **{', '.join(cats)}**." if cats else "No categories in the database yet."
    if any(w in text for w in ['crafts', 'types of crafts', 'what crafts']):
        crafts = sorted(set((a.craft or '').strip() for a in artisans if (a.craft or '').strip()))
        return f"Crafts: **{', '.join(crafts)}**." if crafts else "No crafts in the database yet."

    # How to add heritage site
    if any(w in text for w in ['how to add heritage', 'add heritage site', 'add a site']):
        if not is_authenticated:
            return "Please **log in** first. Then go to **Heritage Sites** in the menu and click **Add Heritage Site** (or visit Heritage → Add). Fill in name, state, category, description, and annual visitors."
        return "Go to **Heritage Sites** in the menu, then click **Add Heritage Site**. Fill in name, state, category, description, and annual visitors, then save."

    # How to add artisan
    if any(w in text for w in ['how to add artisan', 'add artisan', 'add a artisan']):
        if not is_authenticated:
            return "Please **log in** first. Then go to **Artisans** and click **Add Artisan**. Fill in name, craft, state, product price, contact, and description."
        return "Go to **Artisans** in the menu, then click **Add Artisan**. Fill in name, craft, state, product price, contact, and description, then save."

    # Export / download
    if any(w in text for w in ['export', 'download', 'csv', 'download data']):
        if not is_authenticated:
            return "**Export** is available after you log in. From the Dashboard you can use **Export Heritage** or **Export Artisans** to download CSV files."
        return "After logging in, use the **Dashboard** → **Export Heritage** or **Export Artisans** to download CSV files of all heritage sites or artisans."

    # Dashboard / analytics
    if any(w in text for w in ['dashboard', 'analytics', 'statistics', 'stats']):
        total_visitors = sum((s.annual_visitors or 0) for s in sites)
        return (
            f"The **Dashboard** shows: number of heritage sites ({len(sites)}), artisans ({len(artisans)}), "
            f"states covered, total annual visitors ({total_visitors:,}), AI recommendations, economic impact, "
            "and charts. Log in and open the Dashboard to see it."
        )

    # Help / what can you do
    if any(w in text for w in ['help', 'what can you do', 'what do you do', 'options']):
        return (
            "I can help with:\n"
            "• **Heritage sites** – e.g. \"Heritage sites in Karnataka\"\n"
            "• **Artisans** – e.g. \"Artisans in Rajasthan\"\n"
            "• **Counts** – \"How many heritage sites?\" or \"How many artisans?\"\n"
            "• **Registration/Login** – \"How do I register?\" or \"How to login?\"\n"
            "• **Adding data** – \"How to add heritage site?\" or \"How to add artisan?\"\n"
            "• **Export** – \"How to export data?\"\n"
            "• **Platform** – \"What is Digital Catalyst?\""
        )

    # Default
    return (
        "I didn’t quite get that. Try asking:\n"
        "• \"Heritage sites in Maharashtra\"\n"
        "• \"Artisans in Gujarat\"\n"
        "• \"How many heritage sites?\"\n"
        "• \"How do I register?\" or \"What is Digital Catalyst?\"\n\n"
        "Or type **help** for more options."
    )
