# E-commerce Product Recommendations Feature

## Overview

The tutoring recommendation system now includes **direct purchase links** for recommended learning materials. Parents can buy books, learning tools, stationery, toys, workbooks, flashcards, and games directly from popular Malaysian e-commerce platforms.

## Features

### 1. AI-Powered Product Recommendations
- The AI analyzes each child's learning profile and recommends **specific products**
- Products are tailored to:
  - Child's age and grade level
  - Learning style (Visual, Auditory, Kinesthetic, etc.)
  - Identified weak areas from assessments
  - Budget considerations (price estimates in RM)

### 2. Multi-Retailer Support
Each product includes purchase links to:
- **Shopee Malaysia** - Popular online marketplace
- **Lazada Malaysia** - Leading e-commerce platform
- **Amazon** - International products
- **Popular Bookstore** - Local educational retailer

### 3. Priority-Based Recommendations
Products are categorized by urgency:
- 🔴 **HIGH PRIORITY** - Immediate support needed
- 🟡 **MEDIUM PRIORITY** - Important for development
- 🔵 **LOW PRIORITY** - Optional enrichment

### 4. Product Details
Each recommendation includes:
- Product name and type
- Age appropriateness
- Estimated price (RM)
- Explanation of how it helps the child
- Direct purchase links to multiple retailers

### 5. Analytics & Tracking
- Tracks which products parents click on
- Records retailer preferences
- Helps improve future recommendations

## Database Schema

### New Tables

#### `product_recommendations`
Stores recommended products for each child:
```sql
- id (Primary Key)
- child_id (Foreign Key → children)
- tutoring_result_id (Foreign Key → ai_results)
- product_name
- product_type (book, learning_tool, stationery, toy, etc.)
- description
- age_range
- price_myr
- amazon_url, shopee_url, lazada_url, popular_url
- priority (high, medium, low)
- reason (why this product helps)
- created_at, updated_at
```

#### `product_clicks`
Tracks user engagement with product links:
```sql
- id (Primary Key)
- product_recommendation_id (Foreign Key)
- parent_id (Foreign Key → users)
- retailer (shopee, lazada, amazon, popular)
- clicked_at (timestamp)
```

## Technical Implementation

### Backend (app.py)

#### New Functions

1. **`generate_product_links(keywords, product_type)`**
   - Generates search URLs for e-commerce platforms
   - Takes product keywords and creates optimized search queries
   - Returns dictionary with links to all retailers

2. **`extract_products_from_response(full_response, child_id, cursor)`**
   - Parses AI response to extract product recommendations
   - Uses regex to find [PRODUCT_START]...[PRODUCT_END] blocks
   - Stores products in database
   - Returns cleaned HTML and product list

#### Modified Functions

1. **`tutoring_recommendations()`**
   - Enhanced AI prompt to request specific products
   - Includes child's age and grade in context
   - Fetches product recommendations from database
   - Passes products to template

#### New API Endpoint

**`POST /api/track-product-click`**
- Records when users click purchase links
- Parameters: `product_id`, `retailer`
- Used for analytics

### Frontend (_tutoring.html)

#### New UI Components

1. **Product Cards Section**
   - Displays recommended products in a grid
   - Shows priority badges (color-coded)
   - Lists product details and pricing
   - Includes purchase buttons for each retailer

2. **Purchase Buttons**
   - Color-coded by retailer
   - Opens product search in new tab
   - Tracks clicks via JavaScript

3. **Product Display Features**
   - Responsive grid (2 columns on desktop, 1 on mobile)
   - Animated card appearance (fade-in effect)
   - Hover effects for better UX
   - Priority-based sorting

### Styling (style.css)

New CSS classes for:
- `.product-card` - Main product container
- `.purchase-buttons` - Button group styling
- Retailer-specific button colors (Shopee orange, Lazada blue, etc.)
- Responsive design breakpoints
- Fade-in animations

## AI Prompt Structure

The AI is instructed to recommend products using this format:

```
[PRODUCT_START]
Name: [Exact product name]
Type: [book|learning_tool|stationery|toy|workbook|flashcard|game]
Age: [e.g., 3-5 years]
Price: RM [estimated price]
Why: [Explanation of how this helps]
Keywords: [Search terms for e-commerce sites]
Priority: [high|medium|low]
[PRODUCT_END]
```

The system extracts this information and generates purchase links automatically.

## User Flow

1. **Parent views tutoring recommendations**
   - AI analyzes child's learning profile
   - Generates personalized recommendations
   - Extracts product suggestions

2. **Products are displayed**
   - Shown below tutoring recommendations
   - Sorted by priority (high → low)
   - Each product has multiple purchase options

3. **Parent clicks purchase link**
   - Opens retailer's search page in new tab
   - Click is tracked in database
   - Parent can compare prices across platforms

4. **Analytics**
   - System tracks which products are popular
   - Records which retailers parents prefer
   - Data can improve future recommendations

## Example Product Recommendation

### For a 5-year-old Kinesthetic Learner with Math Difficulties:

**HIGH PRIORITY**
- **Magnetic Number Tiles Set**
  - Type: Learning Tool
  - Age: 4-6 years
  - Price: RM 35.90
  - Why: Hands-on manipulation of numbers helps kinesthetic learners grasp math concepts through physical interaction
  - Purchase: [Shopee] [Lazada] [Amazon] [Popular]

**MEDIUM PRIORITY**
- **"My First Math Workbook" Activity Book**
  - Type: Workbook
  - Age: 5-7 years
  - Price: RM 19.90
  - Why: Interactive exercises with tracing and coloring engage tactile learning while building number recognition
  - Purchase: [Shopee] [Lazada] [Amazon] [Popular]

## Future Enhancements

### Potential Improvements:

1. **Affiliate Integration**
   - Add affiliate IDs to links
   - Generate commission on purchases
   - Track conversion rates

2. **Price Comparison**
   - Fetch real-time prices from APIs
   - Show lowest price across platforms
   - Alert parents to sales/discounts

3. **Wishlist Feature**
   - Let parents save products for later
   - Share wishlist with family/friends
   - Get notifications for price drops

4. **Purchase History**
   - Track which products parents bought
   - Request reviews/feedback
   - Improve recommendations based on purchases

5. **Local Store Integration**
   - Partner with physical bookstores
   - Show in-store availability
   - Support local businesses

6. **Product Images**
   - Fetch product images from retailer APIs
   - Display visual previews
   - Improve engagement

7. **Budget Planner**
   - Set monthly education budget
   - Prioritize purchases within budget
   - Track spending over time

## Migration Instructions

### To enable this feature:

1. **Run database migration:**
   ```bash
   mysql -u [username] -p [database_name] < db/migrations/add_product_recommendations.sql
   ```

2. **No code changes required** - feature is ready to use!

3. **Test the feature:**
   - Generate new tutoring recommendations
   - Verify products appear below recommendations
   - Click purchase links to test tracking

## Troubleshooting

### Products not showing?
- Ensure database migration ran successfully
- Check if AI generated products in [PRODUCT_START]...[PRODUCT_END] format
- Verify child has learning/preschool assessments completed

### Links not working?
- Check internet connection
- Verify retailer URLs are properly encoded
- Test if retailer websites are accessible

### Tracking not working?
- Check browser console for JavaScript errors
- Verify `/api/track-product-click` endpoint is accessible
- Ensure `product_clicks` table exists

## Analytics Queries

### Most clicked products:
```sql
SELECT pr.product_name, COUNT(*) as click_count
FROM product_clicks pc
JOIN product_recommendations pr ON pc.product_recommendation_id = pr.id
GROUP BY pr.id
ORDER BY click_count DESC
LIMIT 10;
```

### Most popular retailers:
```sql
SELECT retailer, COUNT(*) as clicks
FROM product_clicks
GROUP BY retailer
ORDER BY clicks DESC;
```

### Conversion by priority:
```sql
SELECT pr.priority, COUNT(DISTINCT pc.parent_id) as unique_users
FROM product_recommendations pr
LEFT JOIN product_clicks pc ON pr.id = pc.product_recommendation_id
GROUP BY pr.priority;
```

## Support

For questions or issues with this feature:
- Check this documentation
- Review console logs for errors
- Contact development team

---

**Version:** 1.0
**Last Updated:** 2025-11-28
**Author:** Child Growth Insights Development Team
