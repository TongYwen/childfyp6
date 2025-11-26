"""
Flask Routes Integration for Purchasable Resources
Add these routes to app.py to enable e-commerce functionality
"""

from flask import request, redirect, url_for, render_template, jsonify, session, flash
from flask_login import login_required, current_user
from ecommerce_integration import EcommerceIntegration, format_resources_html
from config import Config


# ========================================
# IMPROVED RESOURCES HUB WITH PURCHASES
# ========================================

@app.route("/dashboard/resources-shop")
@login_required
def resources_shop():
    """
    Enhanced Resources Hub with purchasable items
    Replaces or supplements existing /dashboard/resources route
    """
    child_id = session.get("selected_child")
    if not child_id:
        return redirect(url_for("select_child"))

    conn = get_db_conn()
    cursor = conn.cursor(dictionary=True)

    # Get child info
    cursor.execute(
        "SELECT * FROM children WHERE id=%s AND parent_id=%s",
        (child_id, current_user.id),
    )
    child = cursor.fetchone()

    if not child:
        cursor.close()
        conn.close()
        flash("Child not found.", "danger")
        return redirect(url_for("dashboard"))

    # Get child's learning profile
    cursor.execute("""
        SELECT module, result, data
        FROM ai_results
        WHERE child_id=%s AND module IN ('learning', 'insights', 'tutoring')
        ORDER BY updated_at DESC
    """, (child_id,))

    ai_data = {row['module']: row for row in cursor.fetchall()}

    # Extract priorities from insights/tutoring
    priorities = []
    if 'tutoring' in ai_data:
        # Parse tutoring data for priority subjects
        import json
        try:
            tutoring_data = json.loads(ai_data['tutoring'].get('data', '{}'))
            priorities = [p.get('area', p.get('subject', ''))
                         for p in tutoring_data.get('priorities', [])[:3]]
        except:
            pass

    # Extract learning style
    learning_style = 'Visual'  # Default
    if 'learning' in ai_data:
        result_text = ai_data['learning']['result']
        for style in ['Visual', 'Auditory', 'Kinesthetic', 'Reading']:
            if style in result_text:
                learning_style = style
                break

    # Initialize e-commerce integration
    ecommerce = EcommerceIntegration(conn)

    # Get filters from query parameters
    resource_type = request.args.get('type')
    max_price = request.args.get('max_price', type=float)
    search_query = request.args.get('q', '').strip()

    # Get recommended resources
    if search_query:
        resources = ecommerce.search_resources(
            query=search_query,
            child_age=child.get('age'),
            type_filter=resource_type,
            max_price=max_price
        )
    else:
        resources = ecommerce.get_resources_for_child(
            child_age=child.get('age', 5),
            child_grade=child.get('grade_level', 'preschool'),
            learning_style=learning_style,
            priorities=priorities,
            limit=30
        )

    # Get popular resources for sidebar
    popular_resources = ecommerce.get_popular_resources(limit=5)

    # Get wishlist
    wishlist = ecommerce.get_wishlist(child_id)

    # Format resources HTML
    resources_html = format_resources_html(resources, ecommerce)

    cursor.close()
    conn.close()

    return render_template(
        "dashboard.html",
        content_template="dashboard/_resources_shop.html",
        selected_child=child,
        resources=resources,
        resources_html=resources_html,
        popular_resources=popular_resources,
        wishlist=wishlist,
        learning_style=learning_style,
        priorities=priorities,
        active="resources_shop",
    )


# ========================================
# PURCHASE TRACKING & REDIRECT
# ========================================

@app.route("/resource/purchase/<int:resource_id>/<int:link_id>")
@login_required
def purchase_redirect(resource_id, link_id):
    """Track click and redirect to e-commerce site"""
    child_id = session.get("selected_child")

    if not child_id:
        flash("Please select a child first.", "warning")
        return redirect(url_for("select_child"))

    conn = get_db_conn()
    ecommerce = EcommerceIntegration(conn)

    # Get link details
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT platform, url, affiliate_link
        FROM resource_purchase_links
        WHERE id = %s
    """, (link_id,))

    link = cursor.fetchone()
    cursor.close()

    if not link:
        conn.close()
        flash("Purchase link not found.", "danger")
        return redirect(url_for("resources_shop"))

    # Track the click
    device = 'mobile' if request.user_agent.platform in ['android', 'iphone'] else 'web'
    ecommerce.track_click(child_id, resource_id, link_id, link['platform'], device)

    conn.close()

    # Redirect to purchase URL (prefer affiliate link)
    redirect_url = link['affiliate_link'] if link['affiliate_link'] else link['url']

    return redirect(redirect_url)


# ========================================
# API ENDPOINTS
# ========================================

@app.route("/api/resource/track-click/<int:resource_id>/<int:link_id>", methods=["POST"])
@login_required
def api_track_click(resource_id, link_id):
    """API endpoint to track clicks"""
    child_id = session.get("selected_child")

    if not child_id:
        return jsonify({"success": False, "error": "No child selected"}), 400

    conn = get_db_conn()
    ecommerce = EcommerceIntegration(conn)

    try:
        device = request.json.get('device', 'web') if request.is_json else 'web'
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT platform FROM resource_purchase_links WHERE id=%s", (link_id,))
        link = cursor.fetchone()
        cursor.close()

        if link:
            click_id = ecommerce.track_click(
                child_id, resource_id, link_id, link['platform'], device
            )
            conn.close()
            return jsonify({"success": True, "click_id": click_id})
        else:
            conn.close()
            return jsonify({"success": False, "error": "Link not found"}), 404

    except Exception as e:
        conn.close()
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/resource/wishlist/add/<int:resource_id>", methods=["POST"])
@login_required
def api_wishlist_add(resource_id):
    """Add resource to wishlist"""
    child_id = session.get("selected_child")

    if not child_id:
        return jsonify({"success": False, "error": "No child selected"}), 400

    conn = get_db_conn()
    ecommerce = EcommerceIntegration(conn)

    try:
        data = request.json if request.is_json else {}
        priority = data.get('priority', 0)
        notes = data.get('notes', '')

        success = ecommerce.add_to_wishlist(child_id, resource_id, priority, notes)
        conn.close()

        return jsonify({"success": success})

    except Exception as e:
        conn.close()
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/resource/wishlist/remove/<int:resource_id>", methods=["POST"])
@login_required
def api_wishlist_remove(resource_id):
    """Remove resource from wishlist"""
    child_id = session.get("selected_child")

    if not child_id:
        return jsonify({"success": False, "error": "No child selected"}), 400

    conn = get_db_conn()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            DELETE FROM resource_wishlists
            WHERE child_id = %s AND resource_id = %s
        """, (child_id, resource_id))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"success": True})

    except Exception as e:
        cursor.close()
        conn.close()
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/dashboard/wishlist")
@login_required
def wishlist():
    """View child's resource wishlist"""
    child_id = session.get("selected_child")

    if not child_id:
        return redirect(url_for("select_child"))

    conn = get_db_conn()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM children WHERE id=%s AND parent_id=%s",
        (child_id, current_user.id),
    )
    child = cursor.fetchone()

    if not child:
        cursor.close()
        conn.close()
        return redirect(url_for("dashboard"))

    ecommerce = EcommerceIntegration(conn)
    wishlist_items = ecommerce.get_wishlist(child_id)

    # Get purchase links for each item
    for item in wishlist_items:
        item['purchase_links'] = ecommerce.get_purchase_links(item['resource_id'])

    # Calculate totals
    total_items = len(wishlist_items)
    total_original = sum(float(item['price_rm']) for item in wishlist_items)
    total_current = sum(float(item['current_best_price'] or item['price_rm']) for item in wishlist_items)
    total_savings = total_original - total_current

    cursor.close()
    conn.close()

    return render_template(
        "dashboard.html",
        content_template="dashboard/_wishlist.html",
        selected_child=child,
        wishlist=wishlist_items,
        total_items=total_items,
        total_original=total_original,
        total_current=total_current,
        total_savings=total_savings,
        active="wishlist",
    )


@app.route("/resource/<int:resource_id>")
@login_required
def resource_detail(resource_id):
    """Detailed view of a single resource"""
    child_id = session.get("selected_child")

    conn = get_db_conn()
    cursor = conn.cursor(dictionary=True)

    # Get resource details
    cursor.execute("SELECT * FROM purchasable_resources WHERE id=%s", (resource_id,))
    resource = cursor.fetchone()

    if not resource:
        cursor.close()
        conn.close()
        flash("Resource not found.", "danger")
        return redirect(url_for("resources_shop"))

    # Get purchase links
    ecommerce = EcommerceIntegration(conn)
    purchase_links = ecommerce.get_purchase_links(resource_id)

    # Get reviews
    cursor.execute("""
        SELECT
            rr.*,
            u.name as reviewer_name
        FROM resource_reviews rr
        JOIN users u ON rr.user_id = u.id
        WHERE rr.resource_id = %s
        ORDER BY rr.created_at DESC
        LIMIT 10
    """, (resource_id,))
    reviews = cursor.fetchall()

    # Get child info if available
    child = None
    if child_id:
        cursor.execute("SELECT * FROM children WHERE id=%s", (child_id,))
        child = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template(
        "dashboard.html",
        content_template="dashboard/_resource_detail.html",
        selected_child=child,
        resource=resource,
        purchase_links=purchase_links,
        reviews=reviews,
        active="resources_shop",
    )


# ========================================
# ADMIN: MANAGE RESOURCES
# ========================================

@app.route("/admin/resources")
@login_required
@roles_required("admin")
def admin_resources():
    """Admin page to manage purchasable resources"""
    conn = get_db_conn()
    cursor = conn.cursor(dictionary=True)

    # Get search/filter parameters
    search = request.args.get('q', '').strip()
    resource_type = request.args.get('type')
    category = request.args.get('category')

    # Build query
    filters = ["1=1"]
    params = []

    if search:
        filters.append("(title LIKE %s OR description LIKE %s OR keywords LIKE %s)")
        like_query = f"%{search}%"
        params.extend([like_query, like_query, like_query])

    if resource_type:
        filters.append("type = %s")
        params.append(resource_type)

    if category:
        filters.append("category = %s")
        params.append(category)

    where_clause = " AND ".join(filters)

    cursor.execute(f"""
        SELECT
            pr.*,
            COUNT(DISTINCT rpl.id) as platform_count,
            MIN(rpl.price_on_platform) as lowest_price,
            COUNT(DISTINCT rc.id) as click_count
        FROM purchasable_resources pr
        LEFT JOIN resource_purchase_links rpl ON pr.id = rpl.resource_id
        LEFT JOIN resource_clicks rc ON pr.id = rc.resource_id
        WHERE {where_clause}
        GROUP BY pr.id
        ORDER BY pr.created_at DESC
    """, params)

    resources = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "admin/resources.html",
        resources=resources,
        search=search
    )


@app.route("/admin/resources/add", methods=["GET", "POST"])
@login_required
@roles_required("admin")
def admin_add_resource():
    """Add new purchasable resource"""
    if request.method == "POST":
        # Get form data
        title = request.form.get("title")
        description = request.form.get("description")
        resource_type = request.form.get("type")
        category = request.form.get("category")
        min_age = request.form.get("min_age", type=int)
        max_age = request.form.get("max_age", type=int)
        price_rm = request.form.get("price_rm", type=float)

        # Optional fields
        author = request.form.get("author")
        publisher = request.form.get("publisher")
        isbn = request.form.get("isbn")
        image_url = request.form.get("image_url")

        conn = get_db_conn()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO purchasable_resources
            (title, description, type, category, min_age, max_age, price_rm,
             author, publisher, isbn, image_url, created_by)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (title, description, resource_type, category, min_age, max_age, price_rm,
              author, publisher, isbn, image_url, current_user.id))

        resource_id = cursor.lastrowid

        # Add purchase links
        platforms = request.form.getlist("platforms[]")
        urls = request.form.getlist("urls[]")
        prices = request.form.getlist("prices[]")

        for platform, url, price in zip(platforms, urls, prices):
            if platform and url:
                cursor.execute("""
                    INSERT INTO resource_purchase_links
                    (resource_id, platform, url, price_on_platform)
                    VALUES (%s, %s, %s, %s)
                """, (resource_id, platform, url, float(price) if price else None))

        conn.commit()
        cursor.close()
        conn.close()

        flash("Resource added successfully!", "success")
        return redirect(url_for("admin_resources"))

    return render_template("admin/add_resource.html")


# ========================================
# CSS STYLES (add to static/style.css)
# ========================================

PURCHASABLE_RESOURCES_CSS = """
/* Purchasable Resources Styles */

.purchasable-resources {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 20px;
    margin: 20px 0;
}

.resource-card {
    background: white;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    transition: transform 0.2s, box-shadow 0.2s;
}

.resource-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 4px 16px rgba(0,0,0,0.15);
}

.resource-image {
    position: relative;
    width: 100%;
    height: 200px;
    overflow: hidden;
    background: #f5f5f5;
}

.resource-image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.discount-badge {
    position: absolute;
    top: 10px;
    right: 10px;
    background: #d32f2f;
    color: white;
    padding: 8px 12px;
    border-radius: 4px;
    font-weight: bold;
    font-size: 0.9em;
}

.resource-type-badge {
    position: absolute;
    bottom: 10px;
    left: 10px;
    background: rgba(0,0,0,0.7);
    color: white;
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 0.85em;
    text-transform: capitalize;
}

.resource-details {
    padding: 16px;
}

.resource-title {
    font-size: 1.1em;
    font-weight: 600;
    margin: 0 0 10px 0;
    color: #333;
}

.resource-rating {
    display: flex;
    align-items: center;
    gap: 6px;
    margin-bottom: 10px;
    font-size: 0.9em;
}

.stars {
    color: #ffa000;
    letter-spacing: 2px;
}

.rating-value {
    font-weight: 600;
}

.review-count {
    color: #666;
    font-size: 0.9em;
}

.resource-description {
    color: #666;
    font-size: 0.9em;
    margin-bottom: 12px;
    line-height: 1.5;
}

.resource-meta {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-bottom: 12px;
}

.meta-item {
    background: #f5f5f5;
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 0.85em;
    color: #555;
}

.resource-price {
    margin: 12px 0;
}

.current-price {
    font-size: 1.5em;
    font-weight: 700;
    color: #d32f2f;
}

.original-price {
    font-size: 1em;
    color: #999;
    text-decoration: line-through;
    margin-left: 8px;
}

.resource-actions {
    margin-top: 12px;
}

.purchase-links {
    display: flex;
    flex-direction: column;
    gap: 8px;
    margin-bottom: 10px;
}

.btn-purchase {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 10px 14px;
    border-radius: 6px;
    border: none;
    font-weight: 600;
    text-decoration: none;
    color: white;
    transition: opacity 0.2s;
}

.btn-purchase:hover {
    opacity: 0.9;
}

.btn-shopee { background: #EE4D2D; }
.btn-lazada { background: #0F156D; }
.btn-bookxcess { background: #D32F2F; }
.btn-popular { background: #1976D2; }

.platform-price {
    font-size: 0.95em;
}

.promo-badge {
    background: #4caf50;
    padding: 2px 6px;
    border-radius: 3px;
    font-size: 0.8em;
    margin-left: 6px;
}

.btn-wishlist {
    width: 100%;
    padding: 10px;
    border: 2px solid #ddd;
    background: white;
    border-radius: 6px;
    font-weight: 600;
    color: #666;
    cursor: pointer;
    transition: all 0.2s;
}

.btn-wishlist:hover {
    border-color: #f50057;
    color: #f50057;
}

.btn-wishlist.added {
    background: #f50057;
    color: white;
    border-color: #f50057;
}
"""
