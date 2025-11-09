"""
Comprehensive Dental Health Tips Library
Organized by metric type and severity level
"""

class DentalTipsLibrary:
    def __init__(self):
        self.tips = {
            'yellowness': {
                'mild': {
                    'description': 'Minimal staining detected - excellent oral hygiene!',
                    'tips': [
                        "Continue your current brushing routine - it's working well",
                        "Maintain regular dental cleanings every 6 months",
                        "Rinse mouth with water after consuming staining foods",
                        "Consider using a straw when drinking coffee, tea, or wine",
                        "Keep up the great work maintaining your bright smile"
                    ],
                    'prevention': [
                        "Brush teeth twice daily for 2 minutes each time",
                        "Use fluoride toothpaste to strengthen enamel",
                        "Stay hydrated by drinking plenty of water throughout the day"
                    ]
                },
                'moderate': {
                    'description': 'Moderate staining detected - time to enhance your routine',
                    'tips': [
                        "Use whitening toothpaste daily to reduce surface stains",
                        "Brush immediately or rinse after consuming dark beverages",
                        "Increase water intake and reduce consumption of staining drinks",
                        "Consider professional cleaning to remove stubborn stains",
                        "Eat crunchy fruits and vegetables that naturally clean teeth",
                        "Try oil pulling with coconut oil for 10-15 minutes daily"
                    ],
                    'prevention': [
                        "Limit coffee, tea, red wine, and dark sodas",
                        "Avoid tobacco products which cause severe staining",
                        "Use an electric toothbrush for more effective cleaning",
                        "Schedule a professional cleaning within the next month"
                    ]
                },
                'severe': {
                    'description': 'Significant staining detected - professional intervention recommended',
                    'tips': [
                        "Schedule professional teeth whitening consultation immediately",
                        "Consider in-office whitening treatments for fast results",
                        "Eliminate or significantly reduce coffee, tea, and red wine",
                        "Use prescription-strength whitening products under dental supervision",
                        "Get professional deep cleaning to remove tartar buildup",
                        "Ask dentist about porcelain veneers for severe cases"
                    ],
                    'prevention': [
                        "Quit smoking or tobacco use - major cause of severe staining",
                        "Brush and floss after every meal if possible",
                        "Use whitening strips or trays as directed by dentist",
                        "Schedule follow-up appointments every 3-4 months",
                        "Avoid dark-colored foods and beverages for 48 hours after whitening"
                    ]
                }
            },
            'cavity': {
                'mild': {
                    'description': 'Low cavity risk detected - maintain your excellent habits',
                    'tips': [
                        "Continue current oral hygiene routine - it's effective",
                        "Maintain regular dental checkups every 6 months",
                        "Keep up daily flossing to prevent future cavities",
                        "Use fluoride toothpaste to strengthen tooth enamel",
                        "Your cavity prevention is working well"
                    ],
                    'prevention': [
                        "Limit sugary snacks and drinks between meals",
                        "Chew sugar-free gum after meals to increase saliva",
                        "Drink tap water with fluoride to strengthen teeth",
                        "Seal molars if recommended by your dentist"
                    ]
                },
                'moderate': {
                    'description': 'Moderate cavity risk - increase preventive measures',
                    'tips': [
                        "Schedule dental examination within 2-4 weeks",
                        "Increase flossing frequency to at least once daily",
                        "Use fluoride mouthwash daily after brushing",
                        "Focus on brushing back molars where cavities often form",
                        "Consider dental sealants to protect vulnerable teeth",
                        "Ask dentist about prescription fluoride toothpaste"
                    ],
                    'prevention': [
                        "Reduce sugar intake significantly, especially between meals",
                        "Never go to bed without brushing teeth thoroughly",
                        "Replace toothbrush every 3 months or when bristles fray",
                        "Avoid constant snacking which exposes teeth to acids",
                        "Consider using an antimicrobial mouthwash"
                    ]
                },
                'severe': {
                    'description': 'High cavity risk - immediate dental attention required',
                    'tips': [
                        "Schedule emergency dental appointment within 1 week",
                        "Get professional cavity assessment and treatment plan",
                        "May require fillings, crowns, or other restorative work",
                        "Use prescription-strength fluoride treatments",
                        "Consider silver diamine fluoride to arrest decay",
                        "Discuss antibacterial rinses with your dentist"
                    ],
                    'prevention': [
                        "Eliminate sugary foods and drinks from diet entirely",
                        "Brush after every meal and snack without exception",
                        "Floss daily and use interdental brushes",
                        "Apply fluoride varnish at dental office quarterly",
                        "Get dental sealants on all vulnerable teeth",
                        "Consider saliva testing to identify bacterial levels"
                    ]
                }
            },
            'alignment': {
                'mild': {
                    'description': 'Excellent alignment - minimal irregularities detected',
                    'tips': [
                        "Your teeth alignment is in great shape",
                        "Maintain good oral posture and avoid teeth grinding",
                        "Continue regular dental checkups to monitor alignment",
                        "If you had braces previously, wear retainers as prescribed",
                        "Good alignment helps prevent future dental issues"
                    ],
                    'prevention': [
                        "Wear night guard if you grind teeth during sleep",
                        "Avoid biting hard objects like ice or pens",
                        "Maintain good jaw posture throughout the day",
                        "Address any TMJ issues with your dentist"
                    ]
                },
                'moderate': {
                    'description': 'Moderate alignment concerns - monitoring recommended',
                    'tips': [
                        "Schedule orthodontic consultation for evaluation",
                        "Minor misalignment can often be corrected with clear aligners",
                        "Consider Invisalign or similar removable aligners",
                        "Address alignment issues early to prevent worsening",
                        "Improved alignment can enhance both function and appearance",
                        "Ask about short-term orthodontic options (6-12 months)"
                    ],
                    'prevention': [
                        "Stop harmful habits like thumb-sucking or tongue thrusting",
                        "Wear retainers if previously prescribed",
                        "Address teeth grinding which can shift alignment",
                        "Get regular checkups to monitor any changes",
                        "Consider night guards to prevent grinding-related shifts"
                    ]
                },
                'severe': {
                    'description': 'Significant alignment issues - orthodontic treatment recommended',
                    'tips': [
                        "Schedule comprehensive orthodontic evaluation immediately",
                        "Likely need braces, aligners, or other orthodontic appliances",
                        "Severe misalignment can affect chewing, speech, and jaw health",
                        "Early intervention prevents more complex problems later",
                        "Discuss traditional braces vs. clear aligner options",
                        "May require combination of orthodontics and oral surgery"
                    ],
                    'prevention': [
                        "Commit to full orthodontic treatment plan as prescribed",
                        "Wear all appliances and retainers exactly as directed",
                        "Attend all scheduled orthodontic appointments",
                        "Maintain excellent oral hygiene during treatment",
                        "Avoid hard, sticky foods that can damage braces",
                        "Consider jaw exercises recommended by orthodontist"
                    ]
                }
            },
            'general': {
                'daily_routine': [
                    "Brush teeth twice daily for 2 minutes each time",
                    "Floss at least once daily, preferably before bedtime",
                    "Use fluoride toothpaste to strengthen enamel",
                    "Replace toothbrush every 3-4 months",
                    "Drink plenty of water throughout the day"
                ],
                'diet': [
                    "Limit sugary and acidic foods and beverages",
                    "Eat calcium-rich foods like dairy, leafy greens",
                    "Consume crunchy fruits and vegetables (apples, carrots, celery)",
                    "Choose water over sugary or acidic drinks",
                    "Wait 30 minutes after eating acidic foods before brushing"
                ],
                'professional_care': [
                    "Schedule dental checkups and cleanings every 6 months",
                    "Get annual dental X-rays to detect hidden issues",
                    "Discuss any concerns or changes with your dentist",
                    "Follow through with recommended treatments promptly",
                    "Ask about fluoride treatments and dental sealants"
                ],
                'lifestyle': [
                    "Quit smoking and tobacco use - major oral health risk",
                    "Limit alcohol consumption which can damage teeth and gums",
                    "Wear mouthguard during sports to prevent injuries",
                    "Manage stress to reduce teeth grinding and jaw clenching",
                    "Stay hydrated to maintain healthy saliva production"
                ]
            }
        }
    
    def get_tips_by_severity(self, metric_type, severity_level):
        """
        Get tips for a specific metric and severity level
        
        Args:
            metric_type: 'yellowness', 'cavity', or 'alignment'
            severity_level: 'mild', 'moderate', or 'severe'
            
        Returns:
            dict with description, tips, and prevention advice
        """
        if metric_type in self.tips and severity_level in self.tips[metric_type]:
            return self.tips[metric_type][severity_level]
        return None
    
    def get_comprehensive_tips(self, results):
        """
        Generate comprehensive tips based on analysis results with severity levels
        
        Args:
            results: Analysis results dict with severity information
            
        Returns:
            dict with categorized tips
        """
        comprehensive_tips = {
            'priority_actions': [],
            'daily_routine': [],
            'prevention': [],
            'professional_care': []
        }
        
        # Add severity-based tips for each metric
        metrics = [
            ('yellowness', 'yellowness_severity'),
            ('cavity', 'cavity_severity'),
            ('alignment', 'alignment_severity')
        ]
        
        for metric_name, severity_key in metrics:
            if severity_key in results:
                severity = results[severity_key]['level']
                tips_data = self.get_tips_by_severity(metric_name, severity)
                
                if tips_data:
                    # Add priority actions for moderate/severe cases
                    if severity in ['moderate', 'severe']:
                        comprehensive_tips['priority_actions'].extend(tips_data['tips'][:3])
                    
                    # Add prevention tips
                    if 'prevention' in tips_data:
                        comprehensive_tips['prevention'].extend(tips_data['prevention'])
        
        # Add general tips
        comprehensive_tips['daily_routine'] = self.tips['general']['daily_routine']
        comprehensive_tips['professional_care'] = self.tips['general']['professional_care']
        
        # Remove duplicates while preserving order
        for category in comprehensive_tips:
            comprehensive_tips[category] = list(dict.fromkeys(comprehensive_tips[category]))
        
        return comprehensive_tips
    
    def get_kid_friendly_tips(self, results):
        """
        Generate kid-friendly tips based on severity levels
        
        Args:
            results: Analysis results with severity information
            
        Returns:
            list of kid-friendly tips
        """
        kid_tips = []
        
        # Yellowness tips
        if 'yellowness_severity' in results:
            severity = results['yellowness_severity']['level']
            if severity == 'severe':
                kid_tips.extend([
                    "🦷 Your teeth need extra brushing! Brush super well after every meal! ✨",
                    "🥛 Drink lots of water instead of juice or soda! 💧",
                    "🍎 Eat crunchy apples and carrots to clean your teeth naturally! 🥕"
                ])
            elif severity == 'moderate':
                kid_tips.extend([
                    "🦷 Brush a little longer to make your teeth whiter! ✨",
                    "💧 Rinse your mouth with water after eating treats!",
                    "🌟 Ask a grown-up about special toothpaste for whiter teeth!"
                ])
            else:
                kid_tips.append("🌟 Your teeth are super white! Keep brushing! ⭐")
        
        # Cavity tips
        if 'cavity_severity' in results:
            severity = results['cavity_severity']['level']
            if severity == 'severe':
                kid_tips.extend([
                    "🦷 Time to visit the dentist! They'll help fix any problems! 👨‍⚕️",
                    "🍬 Stay away from candy and sugary treats! 🚫",
                    "🪥 Brush your back teeth really well - that's where sugar hides!"
                ])
            elif severity == 'moderate':
                kid_tips.extend([
                    "🪥 Make sure to brush all your teeth, especially in the back!",
                    "🍎 Choose healthy snacks like fruit instead of candy! 🥕"
                ])
            else:
                kid_tips.append("🎉 Amazing! No cavities detected! Keep it up! 🌟")
        
        # Alignment tips
        if 'alignment_severity' in results:
            severity = results['alignment_severity']['level']
            if severity == 'severe':
                kid_tips.extend([
                    "😁 Your dentist might help straighten your smile!",
                    "💪 Stand up straight and keep good posture!"
                ])
            elif severity == 'moderate':
                kid_tips.append("😊 Your teeth are looking good! Keep smiling! ⭐")
            else:
                kid_tips.append("🦷 Your teeth are lined up perfectly! Great job! ✨")
        
        # Always add general tips
        kid_tips.extend([
            "⏰ Remember: Brush for 2 whole minutes, twice a day!",
            "🪥 Make brushing fun - sing a song while you brush! 🎵"
        ])
        
        return kid_tips
