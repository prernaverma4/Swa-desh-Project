# Deploying to Render

Since this project is a backend-heavy Python Flask application with an active MongoDB/SQL database, **Render** is the best deployment option (compared to Netlify). Your repository already contains the necessary configurations for Render.

## Steps to Deploy on Render
1. Go to your Render Dashboard via this link: [Deploy on Render](https://dashboard.render.com/web/new?onboarding=active).
2. Click **New +** and select **Web Service**.
3. Choose **Build and deploy from a Git repository**.
4. Connect your GitHub/GitLab account and select this repository.
5. In the configuration page, verify these settings:
   - **Name:** Choose a name for your app.
   - **Language:** Python 3
   - **Branch:** main
   - **Build Command:** `pip install -r requirements.txt` (or if it's already in `render.yaml` skip)
   - **Start Command:** `gunicorn app:app`
6. Click **Create Web Service**. 
7. Wait approx 5-10 minutes for the build to finish. Your app will then be live!

> [!TIP]
> **Environment Variables:**
> Don't forget to add your MongoDB URI or secret keys to the **Environment Variables** tab in your Render dashboard, just like in your `.env` file locally.
