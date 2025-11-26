"""
E-Commerce Integration Module
Manages purchasable learning resources with direct links to Malaysian e-commerce platforms
"""

from typing import List, Dict, Optional, Any
from decimal import Decimal
import mysql.connector
from datetime import datetime, date
import urllib.parse


class EcommerceIntegration:
    """Handle purchasable learning resources and e-commerce links"""

    PLATFORMS = {
        'shopee': {
            'name': 'Shopee Malaysia',
            'icon': '🛒',
            'color': '#EE4D2D',
            'affiliate_base': 'https://shope.ee/affiliate/',
            'mobile_deeplink': 'shopee://'
        },
        'lazada': {
            'name': 'Lazada Malaysia',
            'icon': '🛍️',
            'color': '#0F156D',
            'affiliate_base': 'https://c.lazada.com.my/',
            'mobile_deeplink': 'lazada://'
        },
        'bookxcess': {
            'name': 'BookXcess',
            'icon': '📚',
            'color': '#D32F2F',
            'affiliate_base': 'https://www.bookxcess.com/',
            'mobile_deeplink': None
        },
        'kinokuniya': {
            'name': 'Kinokuniya',
            'icon': '📖',
            'color': '#2E7D32',
            'affiliate_base': 'https://malaysia.kinokuniya.com/',
            'mobile_deeplink': None
        },
        'popular': {
            'name': 'Popular Bookstore',
            'icon': '📕',
            'color': '#1976D2',
            'affiliate_base': 'https://www.popular.com.my/',
            'mobile_deeplink': None
        },
        'amazon': {
            'name': 'Amazon',
            'icon': '📦',
            'color': '#FF9900',
            'affiliate_base': 'https://www.amazon.com/',
            'mobile_deeplink': 'amazon://'
        }
    }

    def __init__(self, db_connection):
        self.conn = db_connection

    def get_resources_for_child(self, child_age: int, child_grade: str,
                                 learning_style: str, priorities: List[str],
                                 limit: int = 20) -> List[Dict]:
        """
        Get recommended purchasable resources for a child
        """
        cursor = self.conn.cursor(dictionary=True)

        # Build query based on priorities
        category_filter = ""
        if priorities:
            categories = "', '".join(priorities)
            category_filter = f"AND (pr.category IN ('{categories}') OR pr.category = 'Multiple')"

        # Build learning style filter
        style_filter = ""
        if learning_style:
            style_map = {
                'Visual': 'visual',
                'Auditory': 'auditory',
                'Kinesthetic': 'kinesthetic',
                'Reading': 'reading'
            }
            mapped_style = style_map.get(learning_style, learning_style.lower())
            style_filter = f"AND (pr.learning_style = '{mapped_style}' OR pr.learning_style IS NULL)"

        query = f"""
            SELECT
                pr.*,
                MIN(rpl.price_on_platform) as best_price,
                COUNT(DISTINCT rpl.id) as platform_count,
                COUNT(DISTINCT rr.id) as review_count_actual,
                AVG(rr.rating) as avg_user_rating,
                CASE
                    WHEN pr.category IN ('{("', '".join(priorities) if priorities else "")}') THEN 10
                    WHEN pr.learning_style = '{learning_style.lower() if learning_style else ""}' THEN 5
                    ELSE 0
                END as relevance_score
            FROM purchasable_resources pr
            LEFT JOIN resource_purchase_links rpl ON pr.id = rpl.resource_id AND rpl.in_stock = TRUE
            LEFT JOIN resource_reviews rr ON pr.id = rr.resource_id
            WHERE pr.min_age <= %s
              AND pr.max_age >= %s
              AND pr.in_stock = TRUE
              {category_filter}
              {style_filter}
            GROUP BY pr.id
            HAVING platform_count > 0
            ORDER BY relevance_score DESC, pr.quality_rating DESC, best_price ASC
            LIMIT %s
        """

        cursor.execute(query, (child_age, child_age, limit))
        resources = cursor.fetchall()

        # Get purchase links for each resource
        for resource in resources:
            resource['purchase_links'] = self.get_purchase_links(resource['id'])
            resource['best_link'] = self._get_best_link(resource['purchase_links'])

        cursor.close()
        return resources

    def get_purchase_links(self, resource_id: int) -> List[Dict]:
        """Get all purchase links for a resource"""
        cursor = self.conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                id,
                resource_id,
                platform,
                url,
                affiliate_link,
                price_on_platform,
                shipping_cost,
                free_shipping_threshold,
                in_stock,
                delivery_days,
                seller_name,
                seller_rating,
                promo_code,
                promo_description,
                promo_valid_until
            FROM resource_purchase_links
            WHERE resource_id = %s AND in_stock = TRUE
            ORDER BY price_on_platform ASC
        """, (resource_id,))

        links = cursor.fetchall()

        # Enhance with platform information
        for link in links:
            platform_info = self.PLATFORMS.get(link['platform'], {})
            link['platform_name'] = platform_info.get('name', link['platform'].title())
            link['platform_icon'] = platform_info.get('icon', '🛒')
            link['platform_color'] = platform_info.get('color', '#000000')

            # Calculate total cost
            link['total_cost'] = link['price_on_platform']
            if link['shipping_cost'] and link['price_on_platform'] < (link['free_shipping_threshold'] or 999):
                link['total_cost'] += link['shipping_cost']

            # Format promo
            if link['promo_code'] and link['promo_valid_until']:
                if isinstance(link['promo_valid_until'], date):
                    if link['promo_valid_until'] >= date.today():
                        link['promo_active'] = True
                    else:
                        link['promo_active'] = False
                        link['promo_code'] = None

        cursor.close()
        return links

    def _get_best_link(self, links: List[Dict]) -> Optional[Dict]:
        """Determine the best purchase link (lowest total cost, best rating)"""
        if not links:
            return None

        # Sort by total cost, then by seller rating
        best = sorted(links, key=lambda x: (x['total_cost'], -x.get('seller_rating', 0)))
        return best[0] if best else None

    def track_click(self, child_id: int, resource_id: int, link_id: int,
                    platform: str, device: str = 'web') -> int:
        """Track when a user clicks a purchase link"""
        cursor = self.conn.cursor()

        cursor.execute("""
            INSERT INTO resource_clicks
            (child_id, resource_id, link_id, platform, device, clicked_at)
            VALUES (%s, %s, %s, %s, %s, NOW())
        """, (child_id, resource_id, link_id, platform, device))

        self.conn.commit()

        # Update click count on the link
        cursor.execute("""
            UPDATE resource_purchase_links
            SET click_count = click_count + 1
            WHERE id = %s
        """, (link_id,))

        self.conn.commit()

        click_id = cursor.lastrowid
        cursor.close()

        return click_id

    def add_to_wishlist(self, child_id: int, resource_id: int,
                        priority: int = 0, notes: str = None) -> bool:
        """Add resource to child's wishlist"""
        cursor = self.conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO resource_wishlists
                (child_id, resource_id, priority, notes, added_at)
                VALUES (%s, %s, %s, %s, NOW())
                ON DUPLICATE KEY UPDATE
                    priority = VALUES(priority),
                    notes = VALUES(notes)
            """, (child_id, resource_id, priority, notes))

            self.conn.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"Error adding to wishlist: {e}")
            cursor.close()
            return False

    def get_wishlist(self, child_id: int) -> List[Dict]:
        """Get child's wishlist with resource details"""
        cursor = self.conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                w.*,
                pr.title,
                pr.type,
                pr.category,
                pr.price_rm,
                pr.image_url,
                MIN(rpl.price_on_platform) as current_best_price
            FROM resource_wishlists w
            JOIN purchasable_resources pr ON w.resource_id = pr.id
            LEFT JOIN resource_purchase_links rpl ON pr.id = rpl.resource_id AND rpl.in_stock = TRUE
            WHERE w.child_id = %s AND w.purchased = FALSE
            GROUP BY w.id
            ORDER BY w.priority DESC, w.added_at DESC
        """, (child_id,))

        wishlist = cursor.fetchall()

        # Calculate savings
        for item in wishlist:
            if item['current_best_price'] and item['current_best_price'] < item['price_rm']:
                item['savings'] = float(item['price_rm']) - float(item['current_best_price'])
                item['discount_percent'] = (item['savings'] / float(item['price_rm'])) * 100
            else:
                item['savings'] = 0
                item['discount_percent'] = 0

        cursor.close()
        return wishlist

    def add_review(self, resource_id: int, user_id: int, child_id: Optional[int],
                   rating: int, review_text: str, **kwargs) -> int:
        """Add a review for a resource"""
        cursor = self.conn.cursor()

        cursor.execute("""
            INSERT INTO resource_reviews
            (resource_id, user_id, child_id, rating, review_text,
             value_for_money, educational_value, engagement, quality,
             child_age_when_used, duration_used, would_recommend, verified_purchase)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            resource_id, user_id, child_id, rating, review_text,
            kwargs.get('value_for_money'), kwargs.get('educational_value'),
            kwargs.get('engagement'), kwargs.get('quality'),
            kwargs.get('child_age_when_used'), kwargs.get('duration_used'),
            kwargs.get('would_recommend', True), kwargs.get('verified_purchase', False)
        ))

        self.conn.commit()
        review_id = cursor.lastrowid

        # Update resource average rating
        self._update_resource_rating(resource_id)

        cursor.close()
        return review_id

    def _update_resource_rating(self, resource_id: int):
        """Recalculate and update resource rating"""
        cursor = self.conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT AVG(rating) as avg_rating, COUNT(*) as review_count
            FROM resource_reviews
            WHERE resource_id = %s
        """, (resource_id,))

        result = cursor.fetchone()

        if result and result['avg_rating']:
            cursor.execute("""
                UPDATE purchasable_resources
                SET quality_rating = %s, review_count = %s
                WHERE id = %s
            """, (result['avg_rating'], result['review_count'], resource_id))

            self.conn.commit()

        cursor.close()

    def get_popular_resources(self, category: Optional[str] = None,
                              limit: int = 10) -> List[Dict]:
        """Get most popular resources (by clicks and purchases)"""
        cursor = self.conn.cursor(dictionary=True)

        category_filter = f"AND pr.category = '{category}'" if category else ""

        cursor.execute(f"""
            SELECT
                pr.*,
                COUNT(DISTINCT rc.id) as click_count,
                SUM(CASE WHEN rc.purchased THEN 1 ELSE 0 END) as purchase_count,
                MIN(rpl.price_on_platform) as best_price
            FROM purchasable_resources pr
            LEFT JOIN resource_clicks rc ON pr.id = rc.resource_id
            LEFT JOIN resource_purchase_links rpl ON pr.id = rpl.resource_id AND rpl.in_stock = TRUE
            WHERE pr.in_stock = TRUE {category_filter}
            GROUP BY pr.id
            HAVING click_count > 0
            ORDER BY purchase_count DESC, click_count DESC
            LIMIT %s
        """, (limit,))

        resources = cursor.fetchall()
        cursor.close()
        return resources

    def search_resources(self, query: str, child_age: Optional[int] = None,
                        type_filter: Optional[str] = None, max_price: Optional[float] = None,
                        limit: int = 20) -> List[Dict]:
        """Search resources by keyword"""
        cursor = self.conn.cursor(dictionary=True)

        # Build filters
        filters = []
        params = []

        if child_age:
            filters.append("pr.min_age <= %s AND pr.max_age >= %s")
            params.extend([child_age, child_age])

        if type_filter:
            filters.append("pr.type = %s")
            params.append(type_filter)

        if max_price:
            filters.append("pr.price_rm <= %s")
            params.append(max_price)

        where_clause = " AND ".join(filters) if filters else "1=1"

        # Search in title, description, keywords
        search_query = f"""
            SELECT
                pr.*,
                MIN(rpl.price_on_platform) as best_price,
                MATCH(pr.title, pr.description) AGAINST (%s) as relevance
            FROM purchasable_resources pr
            LEFT JOIN resource_purchase_links rpl ON pr.id = rpl.resource_id AND rpl.in_stock = TRUE
            WHERE ({where_clause})
              AND (
                  MATCH(pr.title, pr.description) AGAINST (%s)
                  OR pr.title LIKE %s
                  OR pr.description LIKE %s
                  OR pr.keywords LIKE %s
              )
            GROUP BY pr.id
            ORDER BY relevance DESC, pr.quality_rating DESC
            LIMIT %s
        """

        like_query = f"%{query}%"
        params.extend([query, query, like_query, like_query, like_query, limit])

        cursor.execute(search_query, params)
        results = cursor.fetchall()
        cursor.close()

        return results

    def generate_affiliate_link(self, purchase_link_id: int, user_id: Optional[int] = None) -> str:
        """Generate tracked affiliate link"""
        cursor = self.conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT platform, url, affiliate_link
            FROM resource_purchase_links
            WHERE id = %s
        """, (purchase_link_id,))

        link = cursor.fetchone()
        cursor.close()

        if not link:
            return ""

        # If affiliate link exists, use it
        if link['affiliate_link']:
            base_url = link['affiliate_link']
        else:
            base_url = link['url']

        # Add tracking parameters
        tracking_params = {
            'ref': 'childgrowth',
            'link_id': purchase_link_id
        }

        if user_id:
            tracking_params['user'] = user_id

        # Append parameters
        separator = '&' if '?' in base_url else '?'
        tracked_url = base_url + separator + urllib.parse.urlencode(tracking_params)

        return tracked_url


def format_resources_html(resources: List[Dict], ecommerce: EcommerceIntegration) -> str:
    """Format purchasable resources as HTML with purchase buttons"""

    if not resources:
        return "<p class='text-muted'>No resources found matching your criteria.</p>"

    html = """
    <div class="purchasable-resources">
    """

    for resource in resources:
        # Get purchase links
        links = ecommerce.get_purchase_links(resource['id'])
        best_link = ecommerce._get_best_link(links) if links else None

        # Calculate discount
        discount_html = ""
        if resource.get('original_price_rm') and resource['original_price_rm'] > resource['price_rm']:
            savings = float(resource['original_price_rm']) - float(resource['price_rm'])
            discount_pct = (savings / float(resource['original_price_rm'])) * 100
            discount_html = f"""
            <div class="discount-badge">
                <span class="save-amount">Save RM {savings:.2f}</span>
                <span class="save-percent">({discount_pct:.0f}% OFF)</span>
            </div>
            """

        # Best price display
        best_price = resource.get('best_price', resource['price_rm'])
        price_html = f"""
        <div class="resource-price">
            <span class="current-price">RM {float(best_price):.2f}</span>
            {f'<span class="original-price">RM {float(resource["original_price_rm"]):.2f}</span>' if resource.get('original_price_rm') else ''}
        </div>
        """

        # Rating display
        rating = resource.get('quality_rating', 0)
        stars_html = ''.join(['★' if i < rating else '☆' for i in range(5)])
        rating_html = f"""
        <div class="resource-rating">
            <span class="stars">{stars_html}</span>
            <span class="rating-value">{float(rating):.1f}</span>
            <span class="review-count">({resource.get('review_count', 0)} reviews)</span>
        </div>
        """

        # Purchase buttons
        buttons_html = ""
        if links:
            buttons_html += '<div class="purchase-links">'
            for link in links[:3]:  # Show top 3 platforms
                promo_badge = ""
                if link.get('promo_active') and link.get('promo_code'):
                    promo_badge = f'<span class="promo-badge">Code: {link["promo_code"]}</span>'

                buttons_html += f"""
                <a href="/resource/purchase/{resource['id']}/{link['id']}"
                   class="btn btn-purchase btn-{link['platform']}"
                   target="_blank"
                   data-resource-id="{resource['id']}"
                   data-link-id="{link['id']}">
                    {link['platform_icon']} Buy on {link['platform_name']}
                    <span class="platform-price">RM {float(link['price_on_platform']):.2f}</span>
                    {promo_badge}
                </a>
                """
            buttons_html += '</div>'

        # Wishlist button
        wishlist_btn = f"""
        <button class="btn btn-wishlist" data-resource-id="{resource['id']}">
            ♡ Add to Wishlist
        </button>
        """

        # Complete resource card
        html += f"""
        <div class="resource-card" data-resource-id="{resource['id']}">
            <div class="resource-image">
                <img src="{resource.get('image_url', '/static/images/placeholder.jpg')}"
                     alt="{resource['title']}" loading="lazy">
                {discount_html}
                <span class="resource-type-badge">{resource['type'].replace('_', ' ').title()}</span>
            </div>

            <div class="resource-details">
                <h4 class="resource-title">{resource['title']}</h4>

                {rating_html}

                <p class="resource-description">{resource.get('description', '')[:150]}...</p>

                <div class="resource-meta">
                    <span class="meta-item">📚 {resource['category']}</span>
                    <span class="meta-item">👶 Age {resource['min_age']}-{resource['max_age']}</span>
                    {f"<span class='meta-item'>✍️ {resource['author']}</span>" if resource.get('author') else ""}
                </div>

                {price_html}

                <div class="resource-actions">
                    {buttons_html}
                    {wishlist_btn}
                </div>
            </div>
        </div>
        """

    html += """
    </div>

    <script>
    // Track clicks
    document.querySelectorAll('.btn-purchase').forEach(btn => {
        btn.addEventListener('click', function(e) {
            const resourceId = this.dataset.resourceId;
            const linkId = this.dataset.linkId;

            // Send tracking request
            fetch(`/api/resource/track-click/${resourceId}/${linkId}`, {
                method: 'POST'
            });
        });
    });

    // Wishlist functionality
    document.querySelectorAll('.btn-wishlist').forEach(btn => {
        btn.addEventListener('click', function() {
            const resourceId = this.dataset.resourceId;

            fetch(`/api/resource/wishlist/add/${resourceId}`, {
                method: 'POST'
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    this.innerHTML = '♥ Added to Wishlist';
                    this.classList.add('added');
                }
            });
        });
    });
    </script>
    """

    return html
