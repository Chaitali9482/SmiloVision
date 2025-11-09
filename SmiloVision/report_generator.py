from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.platypus.flowables import PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from PIL import Image as PILImage
import io
from datetime import datetime
import numpy as np

class ReportGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
    
    def setup_custom_styles(self):
        """Setup custom styles for the report"""
        
        # Title style with Smilo branding color
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#4A90E2')
        )
        
        # Subtitle style
        self.subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceAfter=20,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#34495E')
        )
        
        # Section header style
        self.section_style = ParagraphStyle(
            'SectionHeader',
            parent=self.styles['Heading3'],
            fontSize=14,
            spaceAfter=10,
            textColor=colors.HexColor('#4A90E2'),
            borderWidth=1,
            borderColor=colors.HexColor('#4A90E2'),
            borderPadding=5
        )
        
        # Body text style
        self.body_style = ParagraphStyle(
            'CustomBody',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=10,
            alignment=TA_JUSTIFY,
            leftIndent=20
        )
        
        # Tips style
        self.tips_style = ParagraphStyle(
            'TipsStyle',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=8,
            leftIndent=30,
            bulletIndent=10,
            textColor=colors.HexColor('#27AE60')
        )
    
    def generate_pdf_report(self, image_file, analysis_results):
        """Generate comprehensive PDF report"""
        
        # Create buffer for PDF
        buffer = io.BytesIO()
        
        # Create document
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )
        
        # Build story (content)
        story = []
        
        # Add header
        story.extend(self.create_header())
        
        # Add summary section
        story.extend(self.create_summary_section(analysis_results))
        
        # Add image analysis
        story.extend(self.create_image_section(image_file, analysis_results))
        
        # Add detailed results
        story.extend(self.create_detailed_results(analysis_results))
        
        # Add recommendations
        story.extend(self.create_recommendations_section(analysis_results))
        
        # Add footer
        story.extend(self.create_footer())
        
        # Build PDF
        doc.build(story)
        
        # Get PDF data
        pdf_data = buffer.getvalue()
        buffer.close()
        
        return pdf_data
    
    def create_header(self):
        """Create report header"""
        story = []
        
        # Title
        title = Paragraph("😊 Smilo Dental Analysis Report", self.title_style)
        story.append(title)
        
        # Date
        date_str = datetime.now().strftime("%B %d, %Y at %I:%M %p")
        date_para = Paragraph(f"Generated on {date_str}", self.subtitle_style)
        story.append(date_para)
        
        story.append(Spacer(1, 20))
        
        return story
    
    def create_summary_section(self, results):
        """Create executive summary section"""
        story = []
        
        # Section header
        header = Paragraph("Executive Summary", self.section_style)
        story.append(header)
        
        # Summary text with proper interpretation
        overall_score = results['overall_score']
        yellowness = results['yellowness_score']
        cavity = results['cavity_score']
        alignment = results['alignment_score']
        
        if overall_score >= 85:
            summary_text = "Excellent oral health! Your teeth show minimal issues and are in great condition. Keep up the outstanding work with your dental care routine."
        elif overall_score >= 70:
            summary_text = "Very good oral health with only minor areas for improvement. Your dental hygiene is working well, continue with regular maintenance."
        elif overall_score >= 55:
            summary_text = "Good oral health with some areas that need attention. Regular dental care and following the recommendations below will help improve your smile."
        else:
            summary_text = "Your oral health needs attention in several areas. Please review the detailed findings and recommendations below, and consider scheduling a dental consultation."
        
        summary = Paragraph(summary_text, self.body_style)
        story.append(summary)
        
        story.append(Spacer(1, 10))
        
        # Scores table
        scores_data = [
            ['Metric', 'Score', 'Status'],
            ['Overall Health', f"{overall_score:.1f}/100", self.get_status_text(overall_score)],
            ['Whiteness Level', f"{100-yellowness:.1f}/100", self.get_status_text(100-yellowness)],
            ['Cavity Health', f"{100-cavity:.1f}/100", self.get_status_text(100-cavity)],
            ['Alignment Score', f"{alignment:.1f}/100", self.get_status_text(alignment)]
        ]
        
        scores_table = Table(scores_data, colWidths=[2*inch, 1.5*inch, 1.5*inch])
        scores_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4A90E2')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(scores_table)
        story.append(Spacer(1, 20))
        
        return story
    
    def create_image_section(self, image_file, results):
        """Create image analysis section"""
        story = []
        
        # Section header
        header = Paragraph("Visual Analysis", self.section_style)
        story.append(header)
        
        # Convert and resize image for PDF
        try:
            # Open original image
            image_file.seek(0)
            pil_image = PILImage.open(image_file)
            
            # Resize for PDF (max width 400px)
            max_width = 400
            if pil_image.width > max_width:
                ratio = max_width / pil_image.width
                new_height = int(pil_image.height * ratio)
                pil_image = pil_image.resize((max_width, new_height), PILImage.LANCZOS)
            
            # Save to buffer
            img_buffer = io.BytesIO()
            pil_image.save(img_buffer, format='PNG')
            img_buffer.seek(0)
            
            # Add to PDF
            img = Image(img_buffer, width=4*inch, height=3*inch)
            story.append(img)
            
        except Exception as e:
            # If image processing fails, add placeholder text
            img_error = Paragraph("Original image could not be processed for PDF inclusion.", 
                                self.body_style)
            story.append(img_error)
        
        story.append(Spacer(1, 10))
        
        # Image analysis description
        analysis_desc = """
        The image has been analyzed using advanced computer vision algorithms to detect:
        <br/><br/>
        - Yellow overlay: Areas of staining or discoloration<br/>
        - Red circles: Potential cavity locations or dark spots<br/>
        - Blue outlines: Alignment irregularities<br/>
        """
        
        desc_para = Paragraph(analysis_desc, self.body_style)
        story.append(desc_para)
        
        story.append(Spacer(1, 20))
        
        return story
    
    def create_detailed_results(self, results):
        """Create detailed results section with accurate interpretations"""
        story = []
        
        # Section header
        header = Paragraph("Detailed Analysis Results", self.section_style)
        story.append(header)
        
        # Yellowness analysis
        yellowness_header = Paragraph("Staining and Discoloration Analysis", 
                                    ParagraphStyle('SubSection', parent=self.body_style, 
                                                 fontSize=12, textColor=colors.HexColor('#F39C12')))
        story.append(yellowness_header)
        
        yellowness_text = f"""
        Staining level detected: {results['yellowness_score']:.1f}%. 
        {self.get_yellowness_interpretation(results['yellowness_score'])}
        """
        story.append(Paragraph(yellowness_text, self.body_style))
        
        story.append(Spacer(1, 10))
        
        # Cavity analysis
        cavity_header = Paragraph("Cavity Risk Assessment", 
                                ParagraphStyle('SubSection', parent=self.body_style, 
                                             fontSize=12, textColor=colors.HexColor('#E74C3C')))
        story.append(cavity_header)
        
        cavity_text = f"""
        Dark spot coverage: {results['cavity_score']:.1f}%. 
        {self.get_cavity_interpretation(results['cavity_score'])}
        """
        story.append(Paragraph(cavity_text, self.body_style))
        
        story.append(Spacer(1, 10))
        
        # Alignment analysis
        alignment_header = Paragraph("Teeth Alignment Evaluation", 
                                   ParagraphStyle('SubSection', parent=self.body_style, 
                                                fontSize=12, textColor=colors.HexColor('#3498DB')))
        story.append(alignment_header)
        
        alignment_text = f"""
        Alignment score: {results['alignment_score']:.1f}/100. 
        {self.get_alignment_interpretation(results['alignment_score'])}
        """
        story.append(Paragraph(alignment_text, self.body_style))
        
        story.append(Spacer(1, 20))
        
        return story
    
    def create_recommendations_section(self, results):
        """Create personalized recommendations section"""
        story = []
        
        # Section header
        header = Paragraph("Personalized Recommendations", self.section_style)
        story.append(header)
        
        # Get recommendations based on results
        recommendations = self.get_detailed_recommendations(results)
        
        for category, tips in recommendations.items():
            # Category header
            cat_header = Paragraph(f"{category}", 
                                 ParagraphStyle('Category', parent=self.body_style, 
                                              fontSize=12, textColor=colors.HexColor('#27AE60')))
            story.append(cat_header)
            
            # Tips
            for tip in tips:
                tip_para = Paragraph(f"  • {tip}", self.tips_style)
                story.append(tip_para)
            
            story.append(Spacer(1, 10))
        
        return story
    
    def create_footer(self):
        """Create report footer"""
        story = []
        
        story.append(Spacer(1, 30))
        
        # Disclaimer
        disclaimer = """
        <b>Important Disclaimer:</b> This analysis is provided by Smilo for informational 
        purposes only and should not replace professional dental care. Please consult with a 
        qualified dentist for comprehensive oral health evaluation and treatment recommendations.
        """
        
        disclaimer_para = Paragraph(disclaimer, 
                                  ParagraphStyle('Disclaimer', parent=self.body_style, 
                                               fontSize=9, textColor=colors.HexColor('#7F8C8D'),
                                               alignment=TA_CENTER))
        story.append(disclaimer_para)
        
        # Footer
        footer_text = f"""
        Generated by Smilo - AI-Powered Smile Analysis<br/>
        Report ID: SM-{datetime.now().strftime('%Y%m%d%H%M%S')}<br/>
        Copyright 2025 Smilo. All rights reserved.
        """
        
        footer_para = Paragraph(footer_text, 
                              ParagraphStyle('Footer', parent=self.body_style, 
                                           fontSize=8, textColor=colors.HexColor('#95A5A6'),
                                           alignment=TA_CENTER))
        story.append(footer_para)
        
        return story
    
    def get_status_text(self, score):
        """Get status text based on score"""
        if score >= 85:
            return "Excellent"
        elif score >= 70:
            return "Very Good"
        elif score >= 55:
            return "Good"
        elif score >= 40:
            return "Fair"
        else:
            return "Needs Attention"
    
    def get_yellowness_interpretation(self, score):
        """Get accurate interpretation for yellowness score"""
        if score <= 5:
            return "Excellent! Minimal to no staining detected. Your teeth appear bright and well-maintained."
        elif score <= 15:
            return "Very good whiteness with only slight staining. Continue your current oral care routine."
        elif score <= 30:
            return "Light to moderate staining present. A whitening toothpaste or routine may be beneficial."
        elif score <= 50:
            return "Moderate staining detected. Consider professional whitening treatment for best results."
        else:
            return "Significant staining present. Professional dental cleaning and whitening treatment recommended."
    
    def get_cavity_interpretation(self, score):
        """Get accurate interpretation for cavity score"""
        if score <= 2:
            return "Excellent! No significant dark spots detected. Maintain your current oral hygiene routine."
        elif score <= 8:
            return "Low cavity risk. A few minor dark areas detected. Monitor and maintain good oral hygiene."
        elif score <= 15:
            return "Moderate dark spot coverage. Schedule a dental checkup to evaluate these areas."
        elif score <= 25:
            return "Notable dark spots detected. Dental examination recommended to assess potential cavities."
        else:
            return "Multiple dark spots identified. Immediate dental consultation strongly advised for evaluation."
    
    def get_alignment_interpretation(self, score):
        """Get accurate interpretation for alignment score"""
        if score >= 85:
            return "Excellent teeth alignment. No significant irregularities detected."
        elif score >= 70:
            return "Very good alignment with minor irregularities that don't require intervention."
        elif score >= 55:
            return "Good alignment with some noticeable irregularities. Monitoring recommended."
        elif score >= 40:
            return "Moderate alignment issues detected. Consider orthodontic consultation."
        else:
            return "Significant alignment concerns identified. Orthodontic evaluation recommended."
    
    def get_detailed_recommendations(self, results):
        """Get detailed recommendations based on actual analysis results"""
        recommendations = {}
        
        # Daily care recommendations
        daily_care = [
            "Brush teeth twice daily for 2 minutes using fluoride toothpaste",
            "Floss daily to remove plaque between teeth",
            "Use an antimicrobial mouthwash to reduce bacteria"
        ]
        
        # Add specific recommendations based on yellowness
        if results['yellowness_score'] > 30:
            daily_care.extend([
                "Use whitening toothpaste specifically designed for stain removal",
                "Limit consumption of coffee, tea, red wine, and dark sodas",
                "Rinse mouth with water immediately after consuming staining foods",
                "Consider an electric toothbrush for more effective cleaning"
            ])
        elif results['yellowness_score'] > 15:
            daily_care.extend([
                "Consider whitening toothpaste for gentle stain removal",
                "Be mindful of staining beverages and use a straw when possible"
            ])
        
        recommendations["Daily Oral Care"] = daily_care
        
        # Professional care
        professional_care = []
        
        if results['cavity_score'] > 15:
            professional_care.extend([
                "Schedule dental examination within 1-2 weeks to evaluate dark spots",
                "Discuss preventive sealants and fluoride treatments",
                "Ask about professional deep cleaning procedures"
            ])
        elif results['cavity_score'] > 8:
            professional_care.extend([
                "Schedule routine dental checkup to monitor dark areas",
                "Discuss fluoride treatment options with your dentist"
            ])
        
        if results['yellowness_score'] > 30:
            professional_care.append("Consult with dentist about professional whitening treatments")
        
        if results['alignment_score'] < 55:
            professional_care.append("Schedule orthodontic consultation for alignment evaluation")
        elif results['alignment_score'] < 70:
            professional_care.append("Discuss alignment concerns with your dentist")
        
        # Add general professional care
        professional_care.extend([
            "Schedule dental cleanings every 6 months",
            "Annual comprehensive dental examination"
        ])
        
        recommendations["Professional Care"] = professional_care
        
        # Lifestyle recommendations
        lifestyle = [
            "Maintain a balanced diet low in sugary snacks and acidic foods",
            "Stay hydrated throughout the day to promote saliva production",
            "Avoid using teeth as tools (opening packages, biting nails, etc.)",
            "Replace toothbrush every 3-4 months or when bristles fray"
        ]
        
        if results['cavity_score'] > 10:
            lifestyle.extend([
                "Reduce frequency of sugary snacks between meals",
                "Choose sugar-free gum with xylitol after meals"
            ])
        
        recommendations["Lifestyle Adjustments"] = lifestyle
        
        return recommendations
