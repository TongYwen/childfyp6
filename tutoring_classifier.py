"""
Tutoring Recommendation Classification System
Classifies tutoring needs into structured, actionable categories
"""

import json
from typing import Dict, List, Any


class TutoringClassifier:
    """Classifies tutoring recommendations across multiple dimensions"""

    def __init__(self):
        self.classifications = {
            'support_type': {
                'academic': 'Subject-based learning support',
                'developmental': 'Milestone & developmental domain support',
                'behavioral': 'Social-emotional and behavioral guidance',
                'enrichment': 'Advanced learning for gifted children'
            },
            'urgency': {
                'critical': 'Immediate intervention needed',
                'high': 'Significant gap requiring attention',
                'moderate': 'Some support beneficial',
                'low': 'Preventive/maintenance support'
            },
            'format': {
                'one_on_one': 'Individual tutoring session',
                'small_group': 'Group of 2-4 children',
                'online': 'Virtual/remote tutoring',
                'hybrid': 'Combination of online and in-person',
                'self_paced': 'Parent-guided with materials'
            },
            'cost': {
                'free': 'No cost (parent-led, free resources)',
                'low': 'RM 0-50 per month',
                'medium': 'RM 51-150 per month',
                'high': 'RM 151+ per month'
            },
            'time_commitment': {
                'minimal': '1x per week, 20-30 min',
                'moderate': '2x per week, 30-45 min',
                'intensive': '3-4x per week, 45-60 min',
                'daily': 'Daily practice, 15-20 min'
            },
            'duration': {
                'short_term': '4-8 weeks (skill-specific)',
                'medium_term': '3-6 months (subject mastery)',
                'long_term': '6+ months (comprehensive support)',
                'ongoing': 'Continuous support'
            },
            'provider': {
                'professional': 'Licensed tutor/therapist',
                'teacher': 'Qualified educator',
                'peer': 'Older student/peer tutor',
                'parent_led': 'Parent guides with structured program',
                'community': 'Library/community center program',
                'digital': 'App/online platform'
            }
        }

    def classify_from_academic_scores(self, subject_performance: List[Dict]) -> List[Dict]:
        """Classify tutoring needs based on academic performance"""
        recommendations = []

        for subject in subject_performance:
            avg_score = subject.get('avg_score', 0)
            trend = subject.get('trend', 'stable')
            subject_name = subject.get('subject', 'Unknown')

            # Determine urgency based on score and trend
            if avg_score < 40:
                urgency = 'critical'
            elif avg_score < 55:
                urgency = 'high'
            elif avg_score < 70:
                urgency = 'moderate'
            else:
                urgency = 'low'

            # Adjust urgency based on trend
            if trend == 'declining' and urgency in ['moderate', 'low']:
                urgency = 'high' if urgency == 'moderate' else 'moderate'

            # Only recommend if urgency is moderate or higher
            if urgency in ['critical', 'high', 'moderate']:
                rec = self._create_recommendation(
                    area=subject_name,
                    support_type='academic',
                    urgency=urgency,
                    score=avg_score,
                    trend=trend
                )
                recommendations.append(rec)

        return recommendations

    def classify_from_preschool_data(self, milestone_scores: List[Dict]) -> List[Dict]:
        """Classify tutoring needs based on developmental milestones"""
        recommendations = []

        # Group by domain
        domains = {}
        for milestone in milestone_scores:
            domain = milestone.get('domain', 'Unknown')
            status = milestone.get('status', 'on-track')

            if domain not in domains:
                domains[domain] = {'total': 0, 'delayed': 0, 'advanced': 0}

            domains[domain]['total'] += 1
            if status == 'delayed':
                domains[domain]['delayed'] += 1
            elif status == 'advanced':
                domains[domain]['advanced'] += 1

        # Create recommendations for delayed domains
        for domain, stats in domains.items():
            if stats['delayed'] > 0:
                delay_percentage = (stats['delayed'] / stats['total']) * 100

                if delay_percentage >= 50:
                    urgency = 'critical'
                elif delay_percentage >= 30:
                    urgency = 'high'
                else:
                    urgency = 'moderate'

                rec = self._create_recommendation(
                    area=f"{domain} Development",
                    support_type='developmental',
                    urgency=urgency,
                    delay_count=stats['delayed'],
                    total_milestones=stats['total']
                )
                recommendations.append(rec)

        return recommendations

    def classify_from_learning_style(self, learning_style_data: Dict) -> Dict:
        """Determine optimal tutoring format based on learning style"""
        primary_style = learning_style_data.get('primary_style', 'Mixed')

        format_recommendations = {
            'Visual': {
                'preferred': ['one_on_one', 'online'],
                'reason': 'Visual learners benefit from screen-based tutoring with diagrams'
            },
            'Auditory': {
                'preferred': ['one_on_one', 'small_group'],
                'reason': 'Auditory learners need verbal interaction and discussion'
            },
            'Kinesthetic': {
                'preferred': ['one_on_one', 'hybrid'],
                'reason': 'Kinesthetic learners need hands-on, in-person activities'
            },
            'Reading': {
                'preferred': ['self_paced', 'online'],
                'reason': 'Reading/writing learners can succeed with structured materials'
            },
            'Mixed': {
                'preferred': ['hybrid', 'one_on_one'],
                'reason': 'Mixed learners benefit from multi-modal approaches'
            }
        }

        return format_recommendations.get(primary_style, format_recommendations['Mixed'])

    def _create_recommendation(self, area: str, support_type: str,
                               urgency: str, **kwargs) -> Dict:
        """Create a classified tutoring recommendation"""

        # Determine format based on support type
        format_mapping = {
            'academic': 'one_on_one',
            'developmental': 'hybrid',
            'behavioral': 'small_group',
            'enrichment': 'online'
        }

        # Determine time commitment based on urgency
        time_mapping = {
            'critical': 'intensive',
            'high': 'moderate',
            'moderate': 'moderate',
            'low': 'minimal'
        }

        # Determine duration based on urgency and type
        duration_mapping = {
            ('critical', 'academic'): 'long_term',
            ('critical', 'developmental'): 'ongoing',
            ('high', 'academic'): 'medium_term',
            ('high', 'developmental'): 'long_term',
            ('moderate', 'academic'): 'short_term',
            ('moderate', 'developmental'): 'medium_term',
            ('low', 'academic'): 'short_term',
            ('low', 'developmental'): 'short_term'
        }

        recommendation = {
            'area': area,
            'classification': {
                'support_type': support_type,
                'urgency': urgency,
                'format': format_mapping.get(support_type, 'one_on_one'),
                'time_commitment': time_mapping.get(urgency, 'moderate'),
                'duration': duration_mapping.get((urgency, support_type), 'medium_term'),
                'cost': 'free',  # Default to free, can be adjusted
                'provider': 'parent_led'  # Default to parent-led
            },
            'descriptions': {
                'support_type': self.classifications['support_type'][support_type],
                'urgency': self.classifications['urgency'][urgency],
                'format': self.classifications['format'][format_mapping.get(support_type, 'one_on_one')],
                'time_commitment': self.classifications['time_commitment'][time_mapping.get(urgency, 'moderate')],
                'duration': self.classifications['duration'][duration_mapping.get((urgency, support_type), 'medium_term')]
            },
            'options': self._generate_options(support_type, urgency, area),
            'metadata': kwargs
        }

        return recommendation

    def _generate_options(self, support_type: str, urgency: str, area: str) -> List[Dict]:
        """Generate tutoring options for each recommendation"""
        options = []

        # Free option (always include)
        options.append({
            'name': 'Parent-Led Support',
            'provider': 'parent_led',
            'cost': 'free',
            'format': 'self_paced',
            'description': f'Structured activities and resources for parents to work with child on {area}',
            'resources': [
                'Printable worksheets',
                'YouTube tutorial videos',
                'Khan Academy Kids (free app)',
                'Step-by-step parent guide'
            ]
        })

        # Digital option
        if support_type == 'academic':
            options.append({
                'name': 'Educational Apps',
                'provider': 'digital',
                'cost': 'low',
                'format': 'online',
                'description': f'Interactive apps focused on {area} skills',
                'resources': [
                    'ABCmouse (RM 30/month)',
                    'Homer Learning (RM 25/month)',
                    'Starfall (RM 35/year)'
                ]
            })

        # Community option
        options.append({
            'name': 'Community Programs',
            'provider': 'community',
            'cost': 'free',
            'format': 'small_group',
            'description': f'Free or low-cost programs at libraries and community centers',
            'resources': [
                'National Library reading programs',
                'Community center learning groups',
                'School extra help sessions'
            ]
        })

        # Professional option (for high/critical urgency)
        if urgency in ['critical', 'high']:
            options.append({
                'name': 'Professional Tutoring',
                'provider': 'professional',
                'cost': 'high' if urgency == 'critical' else 'medium',
                'format': 'one_on_one',
                'description': f'Licensed tutor specialized in {area}',
                'resources': [
                    'Private tuition centers',
                    'Online tutoring platforms (e.g., Superprof MY)',
                    'Early intervention specialists (for developmental)'
                ]
            })

        return options

    def generate_tutoring_plan(self, academic_scores: List[Dict],
                               milestone_scores: List[Dict],
                               learning_style: Dict) -> Dict:
        """Generate complete classified tutoring plan"""

        # Classify all needs
        academic_recs = self.classify_from_academic_scores(academic_scores)
        developmental_recs = self.classify_from_preschool_data(milestone_scores)
        format_prefs = self.classify_from_learning_style(learning_style)

        # Combine and prioritize
        all_recommendations = academic_recs + developmental_recs
        all_recommendations.sort(key=lambda x: {
            'critical': 0, 'high': 1, 'moderate': 2, 'low': 3
        }[x['classification']['urgency']])

        # Apply learning style preferences to format
        for rec in all_recommendations:
            if rec['classification']['format'] in format_prefs['preferred']:
                rec['classification']['format_note'] = '✓ Matches learning style'
            else:
                rec['classification']['format_suggestion'] = format_prefs['preferred'][0]

        return {
            'recommendations': all_recommendations,
            'summary': {
                'total_areas': len(all_recommendations),
                'critical': len([r for r in all_recommendations if r['classification']['urgency'] == 'critical']),
                'high': len([r for r in all_recommendations if r['classification']['urgency'] == 'high']),
                'moderate': len([r for r in all_recommendations if r['classification']['urgency'] == 'moderate']),
                'by_type': {
                    'academic': len([r for r in all_recommendations if r['classification']['support_type'] == 'academic']),
                    'developmental': len([r for r in all_recommendations if r['classification']['support_type'] == 'developmental'])
                }
            },
            'learning_style_guidance': format_prefs,
            'next_steps': self._generate_next_steps(all_recommendations)
        }

    def _generate_next_steps(self, recommendations: List[Dict]) -> List[str]:
        """Generate prioritized action steps"""
        steps = []

        if not recommendations:
            return ['Continue monitoring child\'s progress', 'Schedule regular check-ins']

        # Step 1: Address critical issues
        critical = [r for r in recommendations if r['classification']['urgency'] == 'critical']
        if critical:
            steps.append(f"🚨 URGENT: Seek professional assessment for {', '.join([r['area'] for r in critical])}")

        # Step 2: Start with highest priority
        if recommendations:
            top_rec = recommendations[0]
            steps.append(f"Start with {top_rec['area']} - Begin with free parent-led activities this week")

        # Step 3: Schedule regular practice
        steps.append(f"Set up consistent schedule: {recommendations[0]['descriptions']['time_commitment']}")

        # Step 4: Monitor progress
        steps.append("Track progress weekly and adjust approach as needed")

        # Step 5: Expand support
        if len(recommendations) > 1:
            steps.append(f"After 2-4 weeks, add support for {recommendations[1]['area']}")

        return steps


def format_tutoring_html(tutoring_plan: Dict) -> str:
    """Format classified tutoring plan as HTML"""

    html = f"""
    <div class="tutoring-plan">
        <h3>📊 Tutoring Needs Summary</h3>
        <div class="summary-cards">
            <div class="card urgency-critical">
                <div class="card-number">{tutoring_plan['summary']['critical']}</div>
                <div class="card-label">Critical Priority</div>
            </div>
            <div class="card urgency-high">
                <div class="card-number">{tutoring_plan['summary']['high']}</div>
                <div class="card-label">High Priority</div>
            </div>
            <div class="card urgency-moderate">
                <div class="card-number">{tutoring_plan['summary']['moderate']}</div>
                <div class="card-label">Moderate Priority</div>
            </div>
        </div>

        <h3>🎯 Recommended Support Areas</h3>
        <div class="recommendations-list">
    """

    for i, rec in enumerate(tutoring_plan['recommendations'], 1):
        urgency_class = f"urgency-{rec['classification']['urgency']}"

        html += f"""
        <div class="recommendation-card {urgency_class}">
            <div class="rec-header">
                <h4>{i}. {rec['area']}</h4>
                <span class="badge badge-{rec['classification']['urgency']}">
                    {rec['classification']['urgency'].upper()}
                </span>
            </div>

            <div class="rec-classification">
                <div class="class-item">
                    <strong>Type:</strong> {rec['descriptions']['support_type']}
                </div>
                <div class="class-item">
                    <strong>Format:</strong> {rec['descriptions']['format']}
                    {f"<span class='match-note'>{rec['classification'].get('format_note', '')}</span>" if rec['classification'].get('format_note') else ''}
                </div>
                <div class="class-item">
                    <strong>Time:</strong> {rec['descriptions']['time_commitment']}
                </div>
                <div class="class-item">
                    <strong>Duration:</strong> {rec['descriptions']['duration']}
                </div>
            </div>

            <div class="rec-options">
                <h5>Tutoring Options:</h5>
        """

        for option in rec['options']:
            cost_badge = {'free': 'success', 'low': 'info', 'medium': 'warning', 'high': 'danger'}
            html += f"""
                <div class="option-card">
                    <div class="option-header">
                        <strong>{option['name']}</strong>
                        <span class="badge badge-{cost_badge.get(option['cost'], 'secondary')}">
                            {option['cost'].upper()}
                        </span>
                    </div>
                    <p>{option['description']}</p>
                    <ul class="option-resources">
                        {''.join([f'<li>{r}</li>' for r in option['resources']])}
                    </ul>
                </div>
            """

        html += """
            </div>
        </div>
        """

    html += f"""
        </div>

        <h3>📝 Next Steps</h3>
        <ol class="next-steps">
            {''.join([f'<li>{step}</li>' for step in tutoring_plan['next_steps']])}
        </ol>

        <h3>💡 Learning Style Note</h3>
        <p>{tutoring_plan['learning_style_guidance']['reason']}</p>
        <p><strong>Recommended formats:</strong> {', '.join(tutoring_plan['learning_style_guidance']['preferred'])}</p>
    </div>
    """

    return html
