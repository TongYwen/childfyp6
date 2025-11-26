"""
Example Integration: How to use TutoringClassifier in app.py

This shows how to replace the existing tutoring_recommendations()
function with the new classified system.
"""

from tutoring_classifier import TutoringClassifier, format_tutoring_html
import json


def tutoring_recommendations_IMPROVED():
    """
    IMPROVED VERSION of tutoring_recommendations() route
    Uses classification system for structured recommendations
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
        flash("Child not found.", "danger")
        cursor.close()
        conn.close()
        return redirect(url_for("dashboard"))

    # ========== GET DATA FOR CLASSIFICATION ==========

    # 1. Get academic scores with trends
    cursor.execute("""
        SELECT
            subject,
            AVG(score) as avg_score,
            MAX(score) - MIN(score) as score_range,
            CASE
                WHEN MAX(score) - MIN(score) > 15 THEN 'declining'
                ELSE 'stable'
            END as trend
        FROM academic_scores
        WHERE child_id = %s
        GROUP BY subject
    """, (child_id,))
    subject_performance = cursor.fetchall()

    # 2. Get preschool milestone data (with status)
    cursor.execute("""
        SELECT
            domain,
            description,
            date,
            TIMESTAMPDIFF(MONTH, %s, date) as age_months
        FROM preschool_assessments
        WHERE child_id = %s
    """, (child['dob'], child_id))
    milestones = cursor.fetchall()

    # Simple milestone scoring (you'd use more sophisticated logic)
    milestone_scores = []
    for m in milestones:
        # Simplified: mark as delayed if achieved late
        # Real implementation would compare against benchmark_df
        status = 'on-track'  # Default
        milestone_scores.append({
            'domain': m['domain'],
            'description': m['description'],
            'age_months': m['age_months'],
            'status': status
        })

    # 3. Get learning style data
    cursor.execute("""
        SELECT data, result
        FROM ai_results
        WHERE child_id=%s AND module='learning'
        ORDER BY updated_at DESC
        LIMIT 1
    """, (child_id,))
    learning_row = cursor.fetchone()

    learning_style = {
        'primary_style': 'Visual',  # Default
        'vark_scores': {'Visual': 40, 'Auditory': 30, 'Kinesthetic': 20, 'Reading': 10}
    }

    if learning_row and learning_row['data']:
        try:
            learning_data = json.loads(learning_row['data'])
            learning_style = learning_data.get('vark_scores', learning_style)
        except:
            pass

    # ========== CLASSIFY TUTORING NEEDS ==========

    classifier = TutoringClassifier()
    tutoring_plan = classifier.generate_tutoring_plan(
        academic_scores=subject_performance,
        milestone_scores=milestone_scores,
        learning_style=learning_style
    )

    # ========== GENERATE AI ENHANCEMENT (OPTIONAL) ==========
    # The classifier gives structured data, but we can still use AI
    # to add detailed explanations and activities

    if request.args.get('regen') == '1' or not cached:
        try:
            # Create structured prompt for AI
            prompt = f"""
You are a child education expert reviewing CLASSIFIED tutoring recommendations.

CHILD: {child['name']}, Age: {child['age']}, Grade: {child['grade_level']}

CLASSIFIED RECOMMENDATIONS (structured data):
{json.dumps(tutoring_plan['recommendations'], indent=2, default=str)}

LEARNING STYLE: {learning_style['primary_style']}

Your task:
For EACH recommendation above, add:
1. WHY this area needs support (cite specific data)
2. 3-5 SPECIFIC activities parents can do at home (10-15 min each)
3. Signs of progress to look for
4. When to escalate to professional help

Keep the SAME structure as the classified recommendations.
Output as JSON array matching the input structure, adding an "ai_details" field to each.

Example:
[
  {{
    "area": "Math",
    "classification": {{ ... existing ... }},
    "options": [ ... existing ... ],
    "ai_details": {{
      "why_needed": "Your child's math scores show...",
      "activities": [
        "Activity 1: Count colorful objects...",
        "Activity 2: ..."
      ],
      "progress_signs": ["Can count to 10", "Recognizes numbers 1-5"],
      "escalation_trigger": "If no progress in 6-8 weeks..."
    }}
  }},
  ...
]
"""

            model = genai.GenerativeModel("gemini-2.5-flash")
            response = model.generate_content(prompt)

            # Parse AI response
            try:
                ai_enhanced = json.loads(response.text.strip())
                # Merge AI details into recommendations
                for i, rec in enumerate(tutoring_plan['recommendations']):
                    if i < len(ai_enhanced):
                        rec['ai_details'] = ai_enhanced[i].get('ai_details', {})
            except:
                # If AI doesn't return valid JSON, use original recommendations
                pass

            # Save to database
            data_payload = json.dumps(tutoring_plan, default=str)
            tutoring_html = format_tutoring_html(tutoring_plan)

            cursor.execute("""
                INSERT INTO ai_results
                (child_id, module, data, result, created_at, updated_at)
                VALUES (%s, 'tutoring', %s, %s, NOW(), NOW())
                ON DUPLICATE KEY UPDATE
                    data = VALUES(data),
                    result = VALUES(result),
                    updated_at = NOW()
            """, (child_id, data_payload, tutoring_html))

            conn.commit()

        except Exception as e:
            app.logger.error(f"Tutoring classification error: {e}")
            tutoring_html = "<p class='text-danger'>Error generating recommendations</p>"

    else:
        # Use cached
        tutoring_html = format_tutoring_html(tutoring_plan)

    cursor.close()
    conn.close()

    # ========== RENDER WITH CLASSIFICATION DATA ==========

    return render_template(
        "dashboard.html",
        content_template="dashboard/_tutoring_classified.html",
        selected_child=child,
        tutoring_plan=tutoring_plan,  # Structured data
        tutoring_html=tutoring_html,  # Formatted HTML
        active="tutoring",
    )


# ========== CSS FOR CLASSIFIED TUTORING DISPLAY ==========
TUTORING_CSS = """
<style>
.tutoring-plan {
    font-family: Arial, sans-serif;
}

.summary-cards {
    display: flex;
    gap: 15px;
    margin: 20px 0;
}

.summary-cards .card {
    flex: 1;
    padding: 20px;
    border-radius: 8px;
    text-align: center;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.urgency-critical { background: #fee; border-left: 4px solid #c00; }
.urgency-high { background: #ffe; border-left: 4px solid #f90; }
.urgency-moderate { background: #fef; border-left: 4px solid #09f; }

.card-number {
    font-size: 2.5em;
    font-weight: bold;
    margin-bottom: 5px;
}

.urgency-critical .card-number { color: #c00; }
.urgency-high .card-number { color: #f90; }
.urgency-moderate .card-number { color: #09f; }

.recommendation-card {
    background: white;
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.rec-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 15px;
    padding-bottom: 10px;
    border-bottom: 2px solid #eee;
}

.badge {
    padding: 5px 10px;
    border-radius: 4px;
    font-size: 0.85em;
    font-weight: bold;
}

.badge-critical { background: #c00; color: white; }
.badge-high { background: #f90; color: white; }
.badge-moderate { background: #09f; color: white; }
.badge-success { background: #0c0; color: white; }
.badge-info { background: #09f; color: white; }
.badge-warning { background: #f90; color: white; }
.badge-danger { background: #c00; color: white; }

.rec-classification {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 10px;
    margin-bottom: 15px;
    padding: 15px;
    background: #f9f9f9;
    border-radius: 4px;
}

.class-item {
    font-size: 0.9em;
}

.match-note {
    color: #0c0;
    margin-left: 5px;
    font-size: 0.9em;
}

.rec-options {
    margin-top: 15px;
}

.option-card {
    background: #fff;
    border: 1px solid #ddd;
    border-radius: 4px;
    padding: 12px;
    margin-bottom: 10px;
}

.option-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
}

.option-resources {
    margin: 8px 0 0 20px;
    font-size: 0.85em;
    color: #666;
}

.next-steps {
    background: #f0f8ff;
    padding: 20px 20px 20px 40px;
    border-radius: 4px;
    border-left: 4px solid #09f;
}

.next-steps li {
    margin-bottom: 10px;
}
</style>
"""
