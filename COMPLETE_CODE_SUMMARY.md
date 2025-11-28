# Complete Code Implementation Summary
## E-Commerce Product Recommendations for Tutoring Feature

This document contains all the code changes needed to implement the complete e-commerce product recommendation system with 4-way classification.

---

## 📁 File Structure

```
/home/user/childfyp6/
├── app.py                                    [MODIFIED]
├── db/
│   └── migrations/
│       ├── add_product_recommendations.sql   [NEW]
│       └── add_product_classifications.sql   [NEW]
├── static/
│   └── style.css                            [MODIFIED]
├── templates/
│   └── dashboard/
│       ├── _tutoring.html                   [MODIFIED]
│       └── _product_card.html               [NEW]
└── ECOMMERCE_FEATURE.md                     [NEW - Documentation]
```

---

## 🗄️ DATABASE MIGRATIONS

### 1. Create Product Recommendations Table

**File:** `db/migrations/add_product_recommendations.sql`

```sql
-- Migration: Add product recommendations for e-commerce integration
-- Created: 2025-11-28

-- Table to store recommended products with purchase links
CREATE TABLE IF NOT EXISTS `product_recommendations` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `child_id` INT(11) NOT NULL,
  `tutoring_result_id` INT(11) DEFAULT NULL,
  `product_name` VARCHAR(255) NOT NULL,
  `product_type` ENUM('book', 'learning_tool', 'stationery', 'toy', 'workbook', 'flashcard', 'game') NOT NULL,
  `description` TEXT,
  `age_range` VARCHAR(50) DEFAULT NULL,
  `price_myr` DECIMAL(10, 2) DEFAULT NULL,
  `amazon_url` VARCHAR(500) DEFAULT NULL,
  `shopee_url` VARCHAR(500) DEFAULT NULL,
  `lazada_url` VARCHAR(500) DEFAULT NULL,
  `popular_url` VARCHAR(500) DEFAULT NULL,
  `other_url` VARCHAR(500) DEFAULT NULL,
  `priority` ENUM('high', 'medium', 'low') DEFAULT 'medium',
  `reason` TEXT,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `child_id` (`child_id`),
  KEY `tutoring_result_id` (`tutoring_result_id`),
  CONSTRAINT `product_recommendations_ibfk_1` FOREIGN KEY (`child_id`) REFERENCES `children` (`id`) ON DELETE CASCADE,
  CONSTRAINT `product_recommendations_ibfk_2` FOREIGN KEY (`tutoring_result_id`) REFERENCES `ai_results` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Table to track product clicks/purchases (analytics)
CREATE TABLE IF NOT EXISTS `product_clicks` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `product_recommendation_id` INT(11) NOT NULL,
  `parent_id` INT(11) NOT NULL,
  `retailer` VARCHAR(50) NOT NULL,
  `clicked_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `product_recommendation_id` (`product_recommendation_id`),
  KEY `parent_id` (`parent_id`),
  CONSTRAINT `product_clicks_ibfk_1` FOREIGN KEY (`product_recommendation_id`) REFERENCES `product_recommendations` (`id`) ON DELETE CASCADE,
  CONSTRAINT `product_clicks_ibfk_2` FOREIGN KEY (`parent_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Add index for better query performance
CREATE INDEX idx_product_type_priority ON product_recommendations(product_type, priority);
CREATE INDEX idx_child_created ON product_recommendations(child_id, created_at DESC);
```

### 2. Add Classification Columns

**File:** `db/migrations/add_product_classifications.sql`

```sql
-- Migration: Add product classification fields
-- Created: 2025-11-28

-- Add classification columns to product_recommendations table
ALTER TABLE `product_recommendations`
ADD COLUMN `category` ENUM('books', 'art_craft', 'math_tools', 'stationery', 'educational_toys', 'digital_apps', 'other') DEFAULT 'other' AFTER `product_type`,
ADD COLUMN `subject` ENUM('mathematics', 'english', 'science', 'social_emotional', 'physical_development', 'general') DEFAULT 'general' AFTER `category`,
ADD COLUMN `learning_style` ENUM('visual', 'auditory', 'kinesthetic', 'reading_writing', 'mixed') DEFAULT 'mixed' AFTER `subject`,
ADD COLUMN `price_range` ENUM('budget', 'mid_range', 'premium') DEFAULT 'budget' AFTER `price_myr`;

-- Add indexes for better query performance on classification fields
CREATE INDEX idx_category ON product_recommendations(category);
CREATE INDEX idx_subject ON product_recommendations(subject);
CREATE INDEX idx_learning_style ON product_recommendations(learning_style);
CREATE INDEX idx_price_range ON product_recommendations(price_range);

-- Update price_range based on existing prices
UPDATE product_recommendations
SET price_range = CASE
    WHEN price_myr <= 20 THEN 'budget'
    WHEN price_myr > 20 AND price_myr <= 50 THEN 'mid_range'
    WHEN price_myr > 50 THEN 'premium'
    ELSE 'budget'
END;
```

---

## 🐍 BACKEND CODE (app.py)

### Key Functions Added/Modified

```python
# -------------------------------------------------
# Product Recommendation Helpers
# -------------------------------------------------
def generate_product_links(keywords, product_type):
    """
    Generate search URLs for multiple e-commerce platforms based on keywords.
    """
    import urllib.parse

    search_query = urllib.parse.quote_plus(keywords)

    links = {
        'amazon': f"https://www.amazon.com/s?k={search_query}",
        'shopee': f"https://shopee.com.my/search?keyword={search_query}",
        'lazada': f"https://www.lazada.com.my/catalog/?q={search_query}",
        'popular': f"https://www.popular.com.my/search?q={search_query}"
    }

    return links


def extract_products_from_response(full_response, child_id, cursor):
    """
    Extract product recommendations from AI response and store in database.
    Returns cleaned HTML (without product tags) and list of product dictionaries.
    """
    import re

    # Pattern to match product blocks
    product_pattern = r'\[PRODUCT_START\](.*?)\[PRODUCT_END\]'
    product_matches = re.findall(product_pattern, full_response, re.DOTALL)

    products = []
    tutoring_result_id = None

    for product_text in product_matches:
        # Parse product fields
        product_data = {}

        # Extract Name
        name_match = re.search(r'Name:\s*(.+?)(?:\n|$)', product_text)
        if name_match:
            product_data['name'] = name_match.group(1).strip()

        # Extract Type
        type_match = re.search(r'Type:\s*(.+?)(?:\n|$)', product_text)
        if type_match:
            product_data['type'] = type_match.group(1).strip().lower()

        # Extract Category
        category_match = re.search(r'Category:\s*(.+?)(?:\n|$)', product_text)
        if category_match:
            product_data['category'] = category_match.group(1).strip().lower()

        # Extract Subject
        subject_match = re.search(r'Subject:\s*(.+?)(?:\n|$)', product_text)
        if subject_match:
            product_data['subject'] = subject_match.group(1).strip().lower()

        # Extract Learning Style
        learning_style_match = re.search(r'Learning Style:\s*(.+?)(?:\n|$)', product_text)
        if learning_style_match:
            product_data['learning_style'] = learning_style_match.group(1).strip().lower()

        # Extract Age
        age_match = re.search(r'Age:\s*(.+?)(?:\n|$)', product_text)
        if age_match:
            product_data['age_range'] = age_match.group(1).strip()

        # Extract Price
        price_match = re.search(r'Price:\s*RM\s*([\d.]+)', product_text)
        if price_match:
            product_data['price'] = float(price_match.group(1))

        # Extract Why (description)
        why_match = re.search(r'Why:\s*(.+?)(?:\nKeywords:|$)', product_text, re.DOTALL)
        if why_match:
            product_data['why'] = why_match.group(1).strip()

        # Extract Keywords
        keywords_match = re.search(r'Keywords:\s*(.+?)(?:\nPriority:|$)', product_text, re.DOTALL)
        if keywords_match:
            product_data['keywords'] = keywords_match.group(1).strip()

        # Extract Priority
        priority_match = re.search(r'Priority:\s*(.+?)(?:\n|$)', product_text)
        if priority_match:
            product_data['priority'] = priority_match.group(1).strip().lower()

        # Only add if we have minimum required fields
        if 'name' in product_data and 'keywords' in product_data:
            products.append(product_data)

    # Remove product tags from HTML response
    cleaned_html = re.sub(product_pattern, '', full_response, flags=re.DOTALL)

    # Store products in database if any were found
    if products and cursor:
        for prod in products:
            # Generate product links
            links = generate_product_links(
                prod.get('keywords', prod['name']),
                prod.get('type', 'book')
            )

            # Calculate price range
            price = prod.get('price', 0.0)
            if price <= 20:
                price_range = 'budget'
            elif price <= 50:
                price_range = 'mid_range'
            else:
                price_range = 'premium'

            try:
                cursor.execute("""
                    INSERT INTO product_recommendations
                    (child_id, tutoring_result_id, product_name, product_type, category,
                     subject, learning_style, description, age_range, price_myr, price_range,
                     amazon_url, shopee_url, lazada_url, popular_url, priority, reason,
                     created_at, updated_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
                """, (
                    child_id,
                    tutoring_result_id,
                    prod['name'],
                    prod.get('type', 'book'),
                    prod.get('category', 'other'),
                    prod.get('subject', 'general'),
                    prod.get('learning_style', 'mixed'),
                    prod.get('keywords', ''),
                    prod.get('age_range', ''),
                    price,
                    price_range,
                    links['amazon'],
                    links['shopee'],
                    links['lazada'],
                    links['popular'],
                    prod.get('priority', 'medium'),
                    prod.get('why', '')
                ))
            except Exception as e:
                # Log error but continue processing
                print(f"Error storing product: {e}")

    return cleaned_html.strip(), products


# --- PRODUCT CLICK TRACKING API ---
@app.route("/api/track-product-click", methods=["POST"])
@login_required
def track_product_click():
    """Track when a user clicks on a product purchase link"""
    try:
        data = request.get_json()
        product_id = data.get("product_id")
        retailer = data.get("retailer")

        if not product_id or not retailer:
            return jsonify({"error": "Missing product_id or retailer"}), 400

        conn = get_db_conn()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO product_clicks
            (product_recommendation_id, parent_id, retailer, clicked_at)
            VALUES (%s, %s, %s, NOW())
        """, (product_id, current_user.id, retailer))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"success": True}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
```

### Modified Tutoring Recommendations Route

```python
@app.route("/dashboard/tutoring")
@login_required
def tutoring_recommendations():
    # ... existing code for fetching child and AI results ...

    elif regen == "1" or not use_cached:
        try:
            prompt = f"""
            You are an expert child education advisor specializing in personalized learning recommendations.

            CHILD PROFILE:
            - Name: {child['name']}
            - Age: {child['age']} years old
            - Grade Level: {child['grade_level'] or 'Not specified'}

            BACKGROUND DATA (for your analysis only - DO NOT repeat these in your output):
            --- Preschool Development Summary ---
            {preschool_result if preschool_result else "No preschool data available."}

            --- Learning Style Analysis ---
            {learning_result if learning_result else "No learning style data available."}

            IMPORTANT: Use the above data to inform your recommendations, but DO NOT include or repeat
            the Preschool Development Summary or Learning Style Analysis in your output.

            Based on your analysis of the child's profile and background data, provide ONLY these 4 sections:

            1. **Potential Weak Areas**: Identify specific skills that need support
            2. **Recommended Focus Areas**: Subjects or domains where tutoring would be most beneficial
            3. **Personalized Activities**: Specific activities aligned with the child's learning style

            4. **RECOMMENDED LEARNING MATERIALS** (IMPORTANT):
               Recommend 3-5 SPECIFIC products (books, learning tools, stationery, toys, workbooks, flashcards, or games) that parents can purchase to support this child's learning.

               Format each product like this (use this EXACT format):
               [PRODUCT_START]
               Name: [Exact product name]
               Type: [book|learning_tool|stationery|toy|workbook|flashcard|game]
               Category: [books|art_craft|math_tools|stationery|educational_toys|digital_apps|other]
               Subject: [mathematics|english|science|social_emotional|physical_development|general]
               Learning Style: [visual|auditory|kinesthetic|reading_writing|mixed]
               Age: [e.g., 3-5 years]
               Price: RM [estimated price, e.g., 25.90]
               Why: [1-2 sentences explaining why this helps the child]
               Keywords: [keywords for searching online, e.g., "phonics workbook kids age 5"]
               Priority: [high|medium|low]
               [PRODUCT_END]

            OUTPUT FORMAT (HTML):

            <h3>1. Potential Weak Areas</h3>
            <ul>
              <li>Specific skill or area that needs support</li>
              <li>Another weak area with brief explanation</li>
            </ul>

            <h3>2. Recommended Focus Areas</h3>
            <ul>
              <li>Subject or domain for tutoring</li>
              <li>Another recommended focus area</li>
            </ul>

            <h3>3. Personalized Activities</h3>
            <ul>
              <li>Activity aligned with learning style</li>
              <li>Another recommended activity</li>
            </ul>

            <h3>4. Recommended Learning Materials</h3>
            <p>Here are specific products to support {child['name']}'s learning:</p>

            [Include ALL product recommendations using the [PRODUCT_START]...[PRODUCT_END] format]

            <p><strong>Parent Action Plan:</strong> [2-3 sentence summary of what parents should focus on first]</p>

            IMPORTANT:
            - DO NOT include Preschool Development Summary
            - DO NOT include Learning Style Analysis
            - Only output the 4 sections listed above
            - Be specific and actionable
            - Avoid generic disclaimers
            """

            model = genai.GenerativeModel("gemini-2.5-flash")
            response = model.generate_content(prompt)
            full_response = response.text.strip()

            # Extract product recommendations
            tutoring_summary, products = extract_products_from_response(full_response, child_id, cursor)

            # ... rest of database save code ...

    # Fetch product recommendations for this child
    cursor.execute("""
        SELECT * FROM product_recommendations
        WHERE child_id = %s
        ORDER BY
            CASE priority
                WHEN 'high' THEN 1
                WHEN 'medium' THEN 2
                WHEN 'low' THEN 3
            END,
            created_at DESC
        LIMIT 10
    """, (child_id,))
    products = cursor.fetchall()

    cursor.close()
    conn.close()

    # ... return with products ...
    return render_template(
        "dashboard.html",
        content_template="dashboard/_tutoring.html",
        selected_child=child,
        tutoring_summary=tutoring_summary,
        last_generated=last_generated,
        use_cached=use_cached,
        products=products,
        active="tutoring",
    )
```

---

## 🎨 FRONTEND CODE

### Main Tutoring Template

**File:** `templates/dashboard/_tutoring.html`

See the system reminder for the complete current state of this file. Key sections:
- Filter tabs (All Products, By Category, By Subject, By Learning Style, By Price)
- Tab content with product display
- JavaScript for product click tracking
- Regeneration functionality

### Product Card Component

**File:** `templates/dashboard/_product_card.html`

```html
<div class="col-md-6 mb-3 product-item">
  <div class="product-card border rounded p-3 h-100">
    <!-- Priority Badge -->
    <div class="d-flex justify-content-between align-items-start mb-2">
      <span class="badge
        {% if product.priority == 'high' %}bg-danger
        {% elif product.priority == 'medium' %}bg-warning text-dark
        {% else %}bg-info text-dark
        {% endif %}">
        {{ product.priority|upper }} PRIORITY
      </span>
      <span class="badge bg-secondary">{{ product.product_type|replace('_', ' ')|title }}</span>
    </div>

    <!-- Product Name -->
    <h6 class="fw-bold mb-2">{{ product.product_name }}</h6>

    <!-- Classification Badges -->
    <div class="mb-2">
      {% if product.category %}
      <span class="badge bg-light text-dark me-1" title="Category">
        <i class="fa fa-tag"></i> {{ product.category|replace('_', ' ')|title }}
      </span>
      {% endif %}
      {% if product.subject %}
      <span class="badge bg-light text-dark me-1" title="Subject">
        <i class="fa fa-book"></i> {{ product.subject|replace('_', ' ')|title }}
      </span>
      {% endif %}
      {% if product.learning_style %}
      <span class="badge bg-light text-dark" title="Learning Style">
        <i class="fa fa-brain"></i> {{ product.learning_style|replace('_', ' ')|title }}
      </span>
      {% endif %}
    </div>

    <!-- Age Range & Price -->
    <div class="mb-2">
      {% if product.age_range %}
      <small class="text-muted"><i class="fa fa-child"></i> Age: {{ product.age_range }}</small>
      {% endif %}
      {% if product.price_myr %}
      <small class="text-success ms-2">
        <i class="fa fa-tag"></i> RM {{ "%.2f"|format(product.price_myr) }}
        {% if product.price_range == 'budget' %}💰
        {% elif product.price_range == 'mid_range' %}💵
        {% elif product.price_range == 'premium' %}💎
        {% endif %}
      </small>
      {% endif %}
    </div>

    <!-- Why This Product -->
    {% if product.reason %}
    <p class="small text-secondary mb-3">
      <strong>Why this helps:</strong> {{ product.reason }}
    </p>
    {% endif %}

    <!-- Purchase Buttons -->
    <div class="btn-group-vertical w-100 purchase-buttons">
      {% if product.shopee_url %}
      <a href="{{ product.shopee_url }}" target="_blank" rel="noopener"
         class="btn btn-sm btn-outline-primary mb-1"
         onclick="trackProductClick({{ product.id }}, 'shopee')">
        <i class="fa fa-shopping-bag"></i> Buy on Shopee
      </a>
      {% endif %}

      {% if product.lazada_url %}
      <a href="{{ product.lazada_url }}" target="_blank" rel="noopener"
         class="btn btn-sm btn-outline-warning mb-1"
         onclick="trackProductClick({{ product.id }}, 'lazada')">
        <i class="fa fa-shopping-cart"></i> Buy on Lazada
      </a>
      {% endif %}

      {% if product.amazon_url %}
      <a href="{{ product.amazon_url }}" target="_blank" rel="noopener"
         class="btn btn-sm btn-outline-secondary mb-1"
         onclick="trackProductClick({{ product.id }}, 'amazon')">
        <i class="fa fa-amazon"></i> Buy on Amazon
      </a>
      {% endif %}

      {% if product.popular_url %}
      <a href="{{ product.popular_url }}" target="_blank" rel="noopener"
         class="btn btn-sm btn-outline-info"
         onclick="trackProductClick({{ product.id }}, 'popular')">
        <i class="fa fa-book"></i> Buy at Popular
      </a>
      {% endif %}
    </div>
  </div>
</div>
```

---

## 🎨 CSS STYLING

**File:** `static/style.css`

See system reminder for complete CSS. Key sections added:
- Product card styling
- Purchase button styles (Shopee, Lazada, Amazon, Popular)
- Product filter tabs
- Classification badges
- Responsive design
- Animations

---

## 🚀 DEPLOYMENT STEPS

### 1. Run Database Migrations

```bash
# Connect to MySQL
mysql -u [username] -p [database_name]

# Run migrations
source /home/user/childfyp6/db/migrations/add_product_recommendations.sql
source /home/user/childfyp6/db/migrations/add_product_classifications.sql

# Verify tables created
SHOW TABLES LIKE 'product%';
DESCRIBE product_recommendations;
DESCRIBE product_clicks;
```

### 2. Verify Code Changes

All files are already in place from git commits:
- ✅ app.py (backend logic)
- ✅ templates/dashboard/_tutoring.html (UI)
- ✅ templates/dashboard/_product_card.html (component)
- ✅ static/style.css (styling)

### 3. Test the Feature

1. Start the application
2. Navigate to Dashboard → Tutoring Recommendations
3. Click "Regenerate" button
4. Verify:
   - Products appear below recommendations
   - Filter tabs work
   - Purchase links open correctly
   - Click tracking works

---

## 📊 ANALYTICS QUERIES

```sql
-- Most clicked products
SELECT pr.product_name, pr.category, COUNT(*) as clicks
FROM product_clicks pc
JOIN product_recommendations pr ON pc.product_recommendation_id = pr.id
GROUP BY pr.id
ORDER BY clicks DESC
LIMIT 10;

-- Popular retailers
SELECT retailer, COUNT(*) as clicks
FROM product_clicks
GROUP BY retailer
ORDER BY clicks DESC;

-- Products by price range
SELECT price_range, COUNT(*) as product_count, AVG(price_myr) as avg_price
FROM product_recommendations
GROUP BY price_range;

-- Click-through rate by category
SELECT
    pr.category,
    COUNT(DISTINCT pr.id) as total_products,
    COUNT(DISTINCT pc.product_recommendation_id) as clicked_products,
    ROUND(COUNT(DISTINCT pc.product_recommendation_id) * 100.0 / COUNT(DISTINCT pr.id), 2) as ctr_percentage
FROM product_recommendations pr
LEFT JOIN product_clicks pc ON pr.id = pc.product_recommendation_id
GROUP BY pr.category
ORDER BY ctr_percentage DESC;
```

---

## ✅ FEATURE CHECKLIST

- [x] Database schema created
- [x] Product extraction from AI response
- [x] Multi-retailer link generation
- [x] Click tracking API
- [x] 4-way classification system
- [x] Filter tabs UI
- [x] Responsive design
- [x] Product card component
- [x] CSS styling
- [x] Price range calculation
- [x] Analytics queries
- [x] Documentation

---

## 🔧 TROUBLESHOOTING

### Products not showing?
```sql
-- Check if products exist
SELECT COUNT(*) FROM product_recommendations WHERE child_id = [CHILD_ID];

-- Check recent AI results
SELECT * FROM ai_results WHERE child_id = [CHILD_ID] AND module = 'tutoring' ORDER BY updated_at DESC LIMIT 1;
```

### Classification not working?
```sql
-- Verify columns exist
SHOW COLUMNS FROM product_recommendations LIKE '%category%';
SHOW COLUMNS FROM product_recommendations LIKE '%subject%';
```

### Links not generated?
- Check `generate_product_links()` function in app.py
- Verify keywords are being extracted from AI response
- Test URL encoding with special characters

---

## 📝 SUMMARY

**Total Files Modified:** 4
**Total Files Created:** 4
**Database Tables Created:** 2
**API Endpoints Added:** 1
**Classification Types:** 4
**Supported Retailers:** 4 (Shopee, Lazada, Amazon, Popular)

**Status:** ✅ **COMPLETE AND READY FOR DEPLOYMENT**

All code is committed to branch: `claude/review-tutoring-recommendation-01MxfCzMKB31mhjkByBHqnHj`
