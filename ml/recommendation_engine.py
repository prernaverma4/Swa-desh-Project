"""
AI/ML Recommendation Engine for Digital Catalyst Platform
=========================================================

This module implements a hybrid recommendation system combining multiple
filtering strategies to provide personalized heritage site recommendations.

Academic Context - Recommendation Systems:
-----------------------------------------
Recommendation systems are a class of information filtering systems that
predict user preferences. This implementation uses a hybrid approach combining:

1. Content-Based Filtering: Recommends items similar to user's past preferences
2. Collaborative Filtering: Recommends items liked by similar users
3. Popularity-Based Filtering: Recommends trending/popular items
4. Hybrid Approach: Combines multiple strategies for better results

Recommendation System Types:

Content-Based Filtering:
- Analyzes item features (category, state, etc.)
- Recommends items similar to user's history
- Pros: No cold start for items, explainable recommendations
- Cons: Limited diversity, requires feature engineering

Collaborative Filtering:
- Analyzes user behavior patterns
- Finds similar users and recommends their preferences
- Pros: Discovers unexpected items, no domain knowledge needed
- Cons: Cold start problem, sparsity issues

Popularity-Based:
- Recommends trending/popular items
- Pros: Simple, works for new users
- Cons: No personalization, filter bubble

Hybrid Approach:
- Combines multiple strategies
- Pros: Leverages strengths of each method
- Cons: More complex implementation

Cold Start Problem:
When new users/items have no history, recommendations are difficult.
Solution: Use popularity-based recommendations as fallback.

Complexity Analysis:
- Content-based: O(n) where n is number of items
- Collaborative: O(u*i) where u is users, i is items
- Popularity: O(n log n) for sorting
- Hybrid: O(n log n) dominant term

Pure Python Implementation:
No external dependencies (pandas, numpy, scikit-learn) for maximum compatibility.
"""

from collections import Counter, defaultdict


class RecommendationEngine:
    """
    AI-powered hybrid recommendation system for heritage sites and artisans.
    
    This engine implements multiple recommendation strategies and combines them
    for optimal results. Designed for academic evaluation with comprehensive
    documentation explaining algorithm choices and trade-offs.
    """

    def __init__(self):
        pass

    def recommend_heritage_sites(self, sites_data, top_n=5):
        """Recommend top heritage sites by visitor count."""
        if not sites_data:
            return []
        sorted_sites = sorted(
            sites_data,
            key=lambda s: s.get('annual_visitors') or 0,
            reverse=True
        )
        return sorted_sites[:top_n]

    def recommend_artisans_by_state(self, artisans_data, state_filter=None, top_n=5):
        """Recommend artisans, optionally filtered by state, sorted by price (affordable first)."""
        if not artisans_data:
            return []
        if state_filter:
            artisans_data = [
                a for a in artisans_data
                if (a.get('state') or '').lower() == state_filter.lower()
            ]
        sorted_artisans = sorted(
            artisans_data,
            key=lambda a: a.get('product_price') or 0
        )
        return sorted_artisans[:top_n]

    def recommend_by_category(self, sites_data, category, top_n=3):
        """Recommend heritage sites by category."""
        if not sites_data or not category:
            return []
        filtered = [
            s for s in sites_data
            if (s.get('category') or '').lower() == category.lower()
        ]
        sorted_sites = sorted(
            filtered,
            key=lambda s: s.get('annual_visitors') or 0,
            reverse=True
        )
        return sorted_sites[:top_n]

    def get_state_wise_distribution(self, artisans_data):
        """State-wise artisan counts."""
        if not artisans_data:
            return {}
        states = [a.get('state') or '' for a in artisans_data]
        return dict(Counter(states))

    def get_visitor_trends(self, sites_data):
        """Top 10 sites by visitors for charts."""
        if not sites_data:
            return {'labels': [], 'values': []}
        sorted_sites = sorted(
            sites_data,
            key=lambda s: s.get('annual_visitors') or 0,
            reverse=True
        )[:10]
        return {
            'labels': [s.get('name') or '' for s in sorted_sites],
            'values': [s.get('annual_visitors') or 0 for s in sorted_sites]
        }

    def calculate_economic_impact(self, sites_data, artisans_data):
        """Economic impact metrics."""
        total_visitors = sum(s.get('annual_visitors', 0) or 0 for s in (sites_data or []))
        prices = [a.get('product_price', 0) or 0 for a in (artisans_data or [])]
        avg_product_price = sum(prices) / len(prices) if prices else 0
        tourism_revenue = total_visitors * 500
        artisan_revenue = len(artisans_data or []) * avg_product_price * 50
        return {
            'total_visitors': total_visitors,
            'tourism_revenue': tourism_revenue,
            'artisan_revenue': artisan_revenue,
            'total_economic_impact': tourism_revenue + artisan_revenue,
            'avg_product_price': avg_product_price
        }

    # ========================================================================
    # CONTENT-BASED FILTERING METHODS
    # ========================================================================
    
    def get_user_preferred_categories(self, user_bookmarks, user_views):
        """
        Extract user's preferred heritage site categories from their history.
        
        Academic Note - Content-Based Filtering:
        ---------------------------------------
        Content-based filtering analyzes item features to find patterns in
        user preferences. This function extracts category preferences from:
        1. Bookmarks (strong signal - user explicitly saved)
        2. Views (weak signal - user browsed but may not have liked)
        
        Weighting Strategy:
        - Bookmarks: Weight 3x (explicit positive feedback)
        - Views: Weight 1x (implicit interest signal)
        
        Args:
            user_bookmarks: List of heritage sites user bookmarked
            user_views: List of heritage sites user viewed
            
        Returns:
            list: Ordered list of preferred categories (most to least preferred)
        """
        category_scores = defaultdict(int)
        
        # Weight bookmarks heavily (explicit preference)
        for site in user_bookmarks:
            category = site.get('category', '')
            if category:
                category_scores[category] += 3
        
        # Weight views lightly (implicit interest)
        for site in user_views:
            category = site.get('category', '')
            if category:
                category_scores[category] += 1
        
        # Sort by score descending
        sorted_categories = sorted(
            category_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        return [cat for cat, score in sorted_categories]
    
    def get_user_preferred_states(self, user_bookmarks, user_views):
        """
        Extract user's preferred states from their browsing history.
        
        Similar to category preferences but for geographic locations.
        Users may prefer sites in certain states due to:
        - Proximity to home
        - Cultural affinity
        - Travel plans
        
        Args:
            user_bookmarks: List of heritage sites user bookmarked
            user_views: List of heritage sites user viewed
            
        Returns:
            list: Ordered list of preferred states
        """
        state_scores = defaultdict(int)
        
        # Weight bookmarks heavily
        for site in user_bookmarks:
            state = site.get('state', '')
            if state:
                state_scores[state] += 3
        
        # Weight views lightly
        for site in user_views:
            state = site.get('state', '')
            if state:
                state_scores[state] += 1
        
        # Sort by score descending
        sorted_states = sorted(
            state_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        return [state for state, score in sorted_states]
    
    def find_sites_by_attributes(self, all_sites, preferred_categories, preferred_states, exclude_ids=None):
        """
        Find heritage sites matching user's preferred attributes.
        
        Academic Note - Attribute Matching:
        ----------------------------------
        This implements content-based filtering by matching item attributes
        to user preferences. Scoring formula:
        
        Score = (category_match * 2) + (state_match * 1)
        
        Category weighted higher because it indicates content type preference,
        while state is more about logistics/convenience.
        
        Args:
            all_sites: List of all available heritage sites
            preferred_categories: User's preferred categories (ordered)
            preferred_states: User's preferred states (ordered)
            exclude_ids: Set of site IDs to exclude (already seen/bookmarked)
            
        Returns:
            list: Sites sorted by relevance score
        """
        if not all_sites:
            return []
        
        exclude_ids = exclude_ids or set()
        scored_sites = []
        
        for site in all_sites:
            site_id = site.get('id')
            if site_id in exclude_ids:
                continue
            
            score = 0
            category = site.get('category', '')
            state = site.get('state', '')
            
            # Score based on category match (higher weight)
            if category in preferred_categories:
                # Earlier in preference list = higher score
                category_rank = preferred_categories.index(category)
                score += (len(preferred_categories) - category_rank) * 2
            
            # Score based on state match (lower weight)
            if state in preferred_states:
                state_rank = preferred_states.index(state)
                score += (len(preferred_states) - state_rank) * 1
            
            if score > 0:
                scored_sites.append((site, score))
        
        # Sort by score descending
        scored_sites.sort(key=lambda x: x[1], reverse=True)
        
        return [site for site, score in scored_sites]
    
    # ========================================================================
    # POPULARITY-BASED FILTERING METHODS
    # ========================================================================
    
    def calculate_engagement_score(self, site, view_count, bookmark_count, avg_rating, review_count):
        """
        Calculate engagement score for a heritage site.
        
        Academic Note - Weighted Scoring Formula:
        ----------------------------------------
        Engagement score combines multiple signals with different weights:
        
        Formula:
        Score = (avg_rating * 0.4) + (normalized_views * 0.3) + (normalized_bookmarks * 0.3)
        
        Rationale for Weights:
        - Rating (40%): Quality signal from user feedback
        - Views (30%): Popularity signal (many people interested)
        - Bookmarks (30%): Intent signal (people want to visit)
        
        Normalization:
        Raw counts are normalized to 0-5 scale to match rating scale.
        This prevents high-traffic sites from dominating purely by volume.
        
        Args:
            site: Heritage site dictionary
            view_count: Number of views
            bookmark_count: Number of bookmarks
            avg_rating: Average rating (1-5)
            review_count: Number of reviews
            
        Returns:
            float: Engagement score (0-5 scale)
        """
        # Handle missing ratings
        rating_score = avg_rating if avg_rating else 2.5  # Neutral default
        
        # Normalize view count to 0-5 scale
        # Assume 1000 views = max score of 5
        view_score = min(5.0, (view_count / 1000.0) * 5.0)
        
        # Normalize bookmark count to 0-5 scale
        # Assume 100 bookmarks = max score of 5
        bookmark_score = min(5.0, (bookmark_count / 100.0) * 5.0)
        
        # Weighted combination
        engagement_score = (rating_score * 0.4) + (view_score * 0.3) + (bookmark_score * 0.3)
        
        return round(engagement_score, 2)
    
    # ========================================================================
    # COLLABORATIVE FILTERING METHODS
    # ========================================================================
    
    def find_similar_users(self, user_id, all_user_bookmarks, min_common=2):
        """
        Find users with similar preferences using Jaccard similarity.
        
        Academic Note - Collaborative Filtering:
        ---------------------------------------
        Collaborative filtering finds users with similar tastes and recommends
        items they liked. This uses Jaccard similarity coefficient:
        
        Jaccard(A, B) = |A ∩ B| / |A ∪ B|
        
        Where A and B are sets of bookmarked sites for two users.
        
        Jaccard Similarity Properties:
        - Range: 0 to 1 (0 = no overlap, 1 = identical)
        - Symmetric: Jaccard(A, B) = Jaccard(B, A)
        - Simple and interpretable
        - Works well for binary data (bookmarked or not)
        
        Alternative Metrics:
        - Cosine similarity: Better for rating data
        - Pearson correlation: Better for continuous ratings
        - Euclidean distance: Sensitive to scale
        
        Args:
            user_id: Current user's ID
            all_user_bookmarks: Dict mapping user_id to set of bookmarked site IDs
            min_common: Minimum common bookmarks to consider similarity
            
        Returns:
            list: Tuples of (user_id, similarity_score) sorted by similarity
        """
        if user_id not in all_user_bookmarks:
            return []
        
        user_bookmarks = all_user_bookmarks[user_id]
        similar_users = []
        
        for other_user_id, other_bookmarks in all_user_bookmarks.items():
            if other_user_id == user_id:
                continue
            
            # Calculate Jaccard similarity
            intersection = user_bookmarks & other_bookmarks
            union = user_bookmarks | other_bookmarks
            
            if len(intersection) < min_common:
                continue
            
            if len(union) == 0:
                continue
            
            similarity = len(intersection) / len(union)
            similar_users.append((other_user_id, similarity))
        
        # Sort by similarity descending
        similar_users.sort(key=lambda x: x[1], reverse=True)
        
        return similar_users
    
    def get_recommendations_from_similar_users(self, similar_users, all_user_bookmarks, user_bookmarks, top_n=10):
        """
        Get recommendations from similar users' bookmarks.
        
        Academic Note - Recommendation Aggregation:
        ------------------------------------------
        Combines recommendations from multiple similar users using weighted voting:
        
        Score(item) = Σ(similarity_score * user_liked_item)
        
        Items liked by more similar users get higher scores.
        
        Args:
            similar_users: List of (user_id, similarity_score) tuples
            all_user_bookmarks: Dict mapping user_id to bookmarked site IDs
            user_bookmarks: Current user's bookmarked site IDs
            top_n: Number of recommendations to return
            
        Returns:
            list: Site IDs sorted by recommendation score
        """
        site_scores = defaultdict(float)
        
        for other_user_id, similarity in similar_users[:10]:  # Top 10 similar users
            other_bookmarks = all_user_bookmarks.get(other_user_id, set())
            
            # Recommend sites bookmarked by similar user but not by current user
            for site_id in other_bookmarks:
                if site_id not in user_bookmarks:
                    site_scores[site_id] += similarity
        
        # Sort by score descending
        sorted_sites = sorted(
            site_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        return [site_id for site_id, score in sorted_sites[:top_n]]
    
    # ========================================================================
    # HYBRID RECOMMENDATION METHOD
    # ========================================================================
    
    def recommend_for_user(self, user_id, user_bookmarks, user_views, all_sites, 
                          all_user_bookmarks, site_engagement_data, top_n=10):
        """
        Generate personalized recommendations using hybrid approach.
        
        Academic Note - Hybrid Recommendation System:
        --------------------------------------------
        This method combines three recommendation strategies:
        
        1. Content-Based (40% weight):
           - Analyzes user's preferred categories and states
           - Recommends similar sites
           - Pros: Personalized, explainable
           - Cons: Limited diversity
        
        2. Collaborative Filtering (30% weight):
           - Finds similar users
           - Recommends their bookmarks
           - Pros: Discovers unexpected items
           - Cons: Requires user data
        
        3. Popularity-Based (30% weight):
           - Recommends trending sites
           - Based on engagement metrics
           - Pros: Quality signal
           - Cons: Less personalized
        
        Hybrid Approach Benefits:
        - Leverages strengths of each method
        - Mitigates weaknesses
        - Better coverage (works for new and existing users)
        - More diverse recommendations
        
        Cold Start Handling:
        - New users: Rely more on popularity
        - Users with history: Rely more on content/collaborative
        
        Complexity: O(n log n) where n is number of sites
        
        Args:
            user_id: Current user's ID
            user_bookmarks: List of sites user bookmarked
            user_views: List of sites user viewed
            all_sites: List of all available sites
            all_user_bookmarks: Dict of all users' bookmarks
            site_engagement_data: Dict of engagement metrics per site
            top_n: Number of recommendations to return
            
        Returns:
            list: Recommended heritage sites (dictionaries)
        """
        # Extract user's bookmarked and viewed site IDs
        bookmarked_ids = {site.get('id') for site in user_bookmarks if site.get('id')}
        viewed_ids = {site.get('id') for site in user_views if site.get('id')}
        exclude_ids = bookmarked_ids | viewed_ids
        
        recommendations = {}
        
        # ====================================================================
        # STRATEGY 1: Content-Based Filtering (40% weight)
        # ====================================================================
        
        if user_bookmarks or user_views:
            # Extract preferences
            preferred_categories = self.get_user_preferred_categories(user_bookmarks, user_views)
            preferred_states = self.get_user_preferred_states(user_bookmarks, user_views)
            
            # Find matching sites
            content_based_sites = self.find_sites_by_attributes(
                all_sites, preferred_categories, preferred_states, exclude_ids
            )
            
            # Add to recommendations with weight
            for i, site in enumerate(content_based_sites[:top_n * 2]):
                site_id = site.get('id')
                if site_id:
                    # Score decreases with rank
                    score = (top_n * 2 - i) * 0.4
                    recommendations[site_id] = recommendations.get(site_id, 0) + score
        
        # ====================================================================
        # STRATEGY 2: Collaborative Filtering (30% weight)
        # ====================================================================
        
        if user_id and all_user_bookmarks:
            # Find similar users
            similar_users = self.find_similar_users(user_id, all_user_bookmarks)
            
            if similar_users:
                # Get their recommendations
                collab_site_ids = self.get_recommendations_from_similar_users(
                    similar_users, all_user_bookmarks, bookmarked_ids, top_n * 2
                )
                
                # Add to recommendations with weight
                for i, site_id in enumerate(collab_site_ids):
                    score = (len(collab_site_ids) - i) * 0.3
                    recommendations[site_id] = recommendations.get(site_id, 0) + score
        
        # ====================================================================
        # STRATEGY 3: Popularity-Based (30% weight)
        # ====================================================================
        
        # Score all sites by engagement
        popularity_scores = []
        for site in all_sites:
            site_id = site.get('id')
            if site_id in exclude_ids:
                continue
            
            engagement = site_engagement_data.get(site_id, {})
            engagement_score = self.calculate_engagement_score(
                site,
                engagement.get('view_count', 0),
                engagement.get('bookmark_count', 0),
                engagement.get('avg_rating'),
                engagement.get('review_count', 0)
            )
            
            popularity_scores.append((site_id, engagement_score))
        
        # Sort by engagement score
        popularity_scores.sort(key=lambda x: x[1], reverse=True)
        
        # Add to recommendations with weight
        for i, (site_id, eng_score) in enumerate(popularity_scores[:top_n * 2]):
            score = eng_score * 0.3
            recommendations[site_id] = recommendations.get(site_id, 0) + score
        
        # ====================================================================
        # COMBINE AND RANK
        # ====================================================================
        
        # Sort by combined score
        sorted_recommendations = sorted(
            recommendations.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        # Get top N site IDs
        recommended_ids = [site_id for site_id, score in sorted_recommendations[:top_n]]
        
        # Return full site objects
        recommended_sites = [
            site for site in all_sites
            if site.get('id') in recommended_ids
        ]
        
        # Sort by recommendation score order
        id_to_rank = {site_id: i for i, site_id in enumerate(recommended_ids)}
        recommended_sites.sort(key=lambda s: id_to_rank.get(s.get('id'), 999))
        
        return recommended_sites
