import cv2
import numpy as np
from PIL import Image
from skimage import filters, morphology, measure
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse
import io

class TeethAnalyzer:
    def __init__(self):
        self.blur_threshold = 100
        self.brightness_min = 50
        self.brightness_max = 200
        
    def check_image_quality(self, img_array):
        """Check image quality for lighting, blur, and framing"""
        
        # Convert to grayscale for analysis
        if len(img_array.shape) == 3:
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        else:
            gray = img_array
            
        # Check lighting
        avg_brightness = np.mean(gray)
        lighting_ok = self.brightness_min < avg_brightness < self.brightness_max
        
        # Check blur using Laplacian variance
        blur_score = cv2.Laplacian(gray, cv2.CV_64F).var()
        blur_ok = blur_score > self.blur_threshold
        
        # Check framing (simplified - check if center region has enough contrast)
        h, w = gray.shape
        center_region = gray[h//4:3*h//4, w//4:3*w//4]
        contrast = np.std(center_region)
        framing_ok = contrast > 20
        
        return {
            'lighting_ok': lighting_ok,
            'blur_ok': blur_ok,
            'framing_ok': framing_ok,
            'brightness': avg_brightness,
            'blur_score': blur_score,
            'contrast': contrast
        }
    
    def classify_severity(self, metric_name, score):
        """
        Classify severity level for each metric
        
        Args:
            metric_name: 'yellowness', 'cavity', or 'alignment'
            score: The metric score
            
        Returns:
            dict with severity level and description
        """
        severity_thresholds = {
            'yellowness': {
                'mild': (0, 15),      # 0-15% staining
                'moderate': (15, 35), # 15-35% staining
                'severe': (35, 100)   # 35%+ staining
            },
            'cavity': {
                'mild': (0, 5),       # 0-5% dark spots
                'moderate': (5, 15),  # 5-15% dark spots
                'severe': (15, 30)    # 15%+ dark spots
            },
            'alignment': {
                # For alignment, score is 0-100, higher is better
                'mild': (70, 100),    # 70-100 is good alignment
                'moderate': (50, 70), # 50-70 needs some work
                'severe': (0, 50)     # 0-50 needs significant work
            }
        }
        
        thresholds = severity_thresholds.get(metric_name, {})
        
        for severity, (min_val, max_val) in thresholds.items():
            if min_val <= score < max_val or (severity == 'severe' and score >= max_val and metric_name != 'alignment'):
                return {
                    'level': severity,
                    'label': severity.capitalize(),
                    'color': self.get_severity_color(severity)
                }
        
        # Default to mild if no match
        return {
            'level': 'mild',
            'label': 'Mild',
            'color': self.get_severity_color('mild')
        }
    
    def get_severity_color(self, severity):
        """Get color code for severity level"""
        colors = {
            'mild': '#27AE60',      # Green
            'moderate': '#F39C12',  # Orange
            'severe': '#E74C3C'     # Red
        }
        return colors.get(severity, '#95A5A6')
    
    def analyze_teeth(self, img_array):
        """Comprehensive teeth analysis with severity classification"""
        
        # Preprocessing
        processed_img = self.preprocess_image(img_array)
        
        # Extract teeth region
        teeth_mask = self.extract_teeth_region(processed_img)
        
        # Perform individual analyses
        yellowness_score = self.detect_yellowness(processed_img, teeth_mask)
        cavity_score = self.detect_cavities(processed_img, teeth_mask)
        alignment_score = self.evaluate_alignment(processed_img, teeth_mask)
        
        # Calculate overall score
        overall_score = self.calculate_overall_score(
            yellowness_score, cavity_score, alignment_score)
        
        # Classify severity for each metric
        yellowness_severity = self.classify_severity('yellowness', yellowness_score)
        cavity_severity = self.classify_severity('cavity', cavity_score)
        alignment_severity = self.classify_severity('alignment', alignment_score)
        
        return {
            'overall_score': overall_score,
            'yellowness_score': yellowness_score,
            'yellowness_severity': yellowness_severity,
            'cavity_score': cavity_score,
            'cavity_severity': cavity_severity,
            'alignment_score': alignment_score,
            'alignment_severity': alignment_severity,
            'teeth_mask': teeth_mask,
            'processed_image': processed_img
        }
    
    def preprocess_image(self, img_array):
        """Preprocess image for analysis"""
        
        # Convert to RGB if needed
        if len(img_array.shape) == 3 and img_array.shape[2] == 3:
            img_rgb = img_array
        else:
            img_rgb = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)
        
        # Apply CLAHE for contrast enhancement
        lab = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2LAB)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        lab[:,:,0] = clahe.apply(lab[:,:,0])
        enhanced = cv2.cvtColor(lab, cv2.COLOR_LAB2RGB)
        
        # Gamma correction for brightness normalization
        gamma = 1.2
        enhanced = np.power(enhanced / 255.0, gamma) * 255.0
        enhanced = enhanced.astype(np.uint8)
        
        return enhanced
    
    def extract_teeth_region(self, img_array):
        """Extract teeth region using improved color-based segmentation"""
        
        # Convert to HSV for better color segmentation
        hsv = cv2.cvtColor(img_array, cv2.COLOR_RGB2HSV)
        
        # Expanded range for teeth color (white/off-white/cream/light yellow)
        lower_teeth = np.array([0, 0, 120])
        upper_teeth = np.array([40, 80, 255])
        
        # Create mask for teeth
        teeth_mask = cv2.inRange(hsv, lower_teeth, upper_teeth)
        
        # Morphological operations to clean up mask
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        teeth_mask = cv2.morphologyEx(teeth_mask, cv2.MORPH_OPEN, kernel)
        teeth_mask = cv2.morphologyEx(teeth_mask, cv2.MORPH_CLOSE, kernel)
        
        # Find largest contour (main teeth region)
        contours, _ = cv2.findContours(teeth_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            # Get the largest contour
            largest_contour = max(contours, key=cv2.contourArea)
            
            # Create refined mask
            refined_mask = np.zeros_like(teeth_mask)
            cv2.fillPoly(refined_mask, [largest_contour], 255)
            
            return refined_mask
        
        return teeth_mask
    
    def detect_yellowness(self, img_array, teeth_mask):
        """Detect yellow staining on teeth with improved color detection"""
        
        # Convert to HSV
        hsv = cv2.cvtColor(img_array, cv2.COLOR_RGB2HSV)
        
        # Convert to LAB color space for better yellow detection
        lab = cv2.cvtColor(img_array, cv2.COLOR_RGB2LAB)
        
        # Define multiple yellow/stain color ranges for better detection
        lower_yellow1 = np.array([18, 40, 100])
        upper_yellow1 = np.array([35, 255, 255])
        
        lower_yellow2 = np.array([10, 20, 120])
        upper_yellow2 = np.array([25, 100, 220])
        
        # Create yellow masks
        yellow_mask1 = cv2.inRange(hsv, lower_yellow1, upper_yellow1)
        yellow_mask2 = cv2.inRange(hsv, lower_yellow2, upper_yellow2)
        
        # Combine masks
        yellow_mask = cv2.bitwise_or(yellow_mask1, yellow_mask2)
        
        # Combine with teeth mask
        yellow_on_teeth = cv2.bitwise_and(yellow_mask, teeth_mask)
        
        # Calculate yellowness percentage
        teeth_pixels = np.sum(teeth_mask > 0)
        yellow_pixels = np.sum(yellow_on_teeth > 0)
        
        if teeth_pixels > 0:
            yellowness_percentage = (yellow_pixels / teeth_pixels) * 100
        else:
            yellowness_percentage = 0
        
        # Apply a scaling factor to make it more realistic
        yellowness_percentage = min(yellowness_percentage * 1.2, 100)
            
        return min(yellowness_percentage, 100)
    
    def detect_cavities(self, img_array, teeth_mask):
        """Detect potential cavities with FIXED algorithm to prevent 100% readings"""
        
        # Convert to grayscale
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        
        # Apply teeth mask
        masked_gray = cv2.bitwise_and(gray, teeth_mask)
        
        # Only process if we have teeth pixels
        teeth_pixels = np.sum(teeth_mask > 0)
        if teeth_pixels == 0:
            return 0
        
        # Calculate average brightness of teeth region
        teeth_region_pixels = gray[teeth_mask > 0]
        avg_brightness = np.mean(teeth_region_pixels)
        
        # Dynamic threshold based on brightness
        # Lower threshold for darker images, higher for brighter
        threshold_value = max(30, int(avg_brightness * 0.6))
        
        # Use binary threshold instead of adaptive for better control
        _, binary = cv2.threshold(masked_gray, threshold_value, 255, cv2.THRESH_BINARY_INV)
        
        # Remove noise with morphological operations
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
        cleaned = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel, iterations=1)
        
        # Find contours of dark spots
        contours, _ = cv2.findContours(cleaned, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Filter contours by size and shape (cavity-like dimensions)
        cavity_contours = []
        min_area = 15
        max_area = 800
        
        for contour in contours:
            area = cv2.contourArea(contour)
            if min_area < area < max_area:
                # Check circularity to filter out non-cavity shapes
                perimeter = cv2.arcLength(contour, True)
                if perimeter > 0:
                    circularity = 4 * np.pi * area / (perimeter * perimeter)
                    if circularity > 0.3:
                        cavity_contours.append(contour)
        
        # Calculate cavity risk percentage
        cavity_pixels = sum([cv2.contourArea(c) for c in cavity_contours])
        
        # Calculate percentage with proper scaling
        cavity_percentage = (cavity_pixels / teeth_pixels) * 100
        
        # Cap at reasonable maximum (cavities shouldn't exceed 30% realistically)
        cavity_percentage = min(cavity_percentage, 30)
            
        return cavity_percentage
    
    def evaluate_alignment(self, img_array, teeth_mask):
        """Evaluate teeth alignment with improved algorithm"""
        
        # Convert to grayscale
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        
        # Apply teeth mask
        masked_gray = cv2.bitwise_and(gray, teeth_mask)
        
        # Find edges of teeth with optimized parameters
        edges = cv2.Canny(masked_gray, 30, 120)
        
        # Find contours
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if not contours:
            return 50
        
        # Get the main teeth contour
        main_contour = max(contours, key=cv2.contourArea)
        
        # Fit an ellipse to the contour to represent ideal alignment
        if len(main_contour) >= 5:
            try:
                ellipse = cv2.fitEllipse(main_contour)
                
                # Calculate alignment based on multiple factors
                hull = cv2.convexHull(main_contour)
                hull_area = cv2.contourArea(hull)
                contour_area = cv2.contourArea(main_contour)
                
                if hull_area > 0:
                    convexity = contour_area / hull_area
                    
                    # Calculate regularity score based on ellipse fit
                    _, (width, height), _ = ellipse
                    aspect_ratio = min(width, height) / max(width, height) if max(width, height) > 0 else 0
                    
                    # Combined score
                    alignment_score = (convexity * 70 + aspect_ratio * 30)
                else:
                    alignment_score = 50
            except:
                alignment_score = 50
        else:
            alignment_score = 50
            
        return min(max(alignment_score, 0), 100)
    
    def calculate_overall_score(self, yellowness, cavity_risk, alignment):
        """Calculate overall oral health score"""
        
        # Weights for different factors
        yellowness_weight = 0.3
        cavity_weight = 0.5
        alignment_weight = 0.2
        
        # Convert scores to positive scale (higher = better)
        whiteness_score = 100 - yellowness
        cavity_health_score = 100 - cavity_risk
        
        # Weighted average
        overall = (
            whiteness_score * yellowness_weight +
            cavity_health_score * cavity_weight +
            alignment * alignment_weight
        )
        
        return min(max(overall, 0), 100)
    
    def create_visual_overlay(self, img_array, analysis_results):
        """Create visual overlay showing detected issues"""
        
        # Create a copy of the original image
        overlay_img = img_array.copy()
        
        # Create figure for matplotlib overlay
        fig, ax = plt.subplots(1, 1, figsize=(10, 8))
        ax.imshow(overlay_img)
        ax.set_title("Smilo Analysis Results", fontsize=16, fontweight='bold')
        
        # Get image dimensions
        height, width = img_array.shape[:2]
        
        # Overlay yellowness (yellow transparent regions)
        if analysis_results['yellowness_score'] > 10:
            # Convert to HSV to find yellow regions
            hsv = cv2.cvtColor(img_array, cv2.COLOR_RGB2HSV)
            lower_yellow = np.array([18, 40, 100])
            upper_yellow = np.array([35, 255, 255])
            yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
            
            # Apply teeth mask
            teeth_mask = analysis_results['teeth_mask']
            yellow_on_teeth = cv2.bitwise_and(yellow_mask, teeth_mask)
            
            # Create yellow overlay
            yellow_overlay = np.zeros_like(overlay_img)
            yellow_overlay[yellow_on_teeth > 0] = [255, 255, 0]
            
            # Blend with original
            alpha = 0.3
            overlay_img = cv2.addWeighted(overlay_img, 1-alpha, yellow_overlay, alpha, 0)
        
        # Overlay cavity indicators (red circles) - FIXED to show actual cavities
        if analysis_results['cavity_score'] > 2:
            # Find dark spots as potential cavities
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
            masked_gray = cv2.bitwise_and(gray, analysis_results['teeth_mask'])
            
            # Get average brightness
            teeth_pixels = gray[analysis_results['teeth_mask'] > 0]
            if len(teeth_pixels) > 0:
                avg_brightness = np.mean(teeth_pixels)
                threshold_value = max(30, int(avg_brightness * 0.6))
                
                # Binary threshold
                _, binary = cv2.threshold(masked_gray, threshold_value, 255, cv2.THRESH_BINARY_INV)
                
                kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
                cleaned = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel, iterations=1)
                
                contours, _ = cv2.findContours(cleaned, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                
                # Draw circles around potential cavities
                for contour in contours:
                    area = cv2.contourArea(contour)
                    if 15 < area < 800:
                        perimeter = cv2.arcLength(contour, True)
                        if perimeter > 0:
                            circularity = 4 * np.pi * area / (perimeter * perimeter)
                            if circularity > 0.3:
                                # Get centroid
                                M = cv2.moments(contour)
                                if M["m00"] != 0:
                                    cx = int(M["m10"] / M["m00"])
                                    cy = int(M["m01"] / M["m00"])
                                    
                                    # Draw circle
                                    circle = Circle((cx, cy), radius=15, fill=False, 
                                                  color='red', linewidth=3, alpha=0.8)
                                    ax.add_patch(circle)
        
        # Overlay alignment indicators (blue outlines)
        if analysis_results['alignment_score'] < 80:
            # Find main teeth contour
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
            masked_gray = cv2.bitwise_and(gray, analysis_results['teeth_mask'])
            edges = cv2.Canny(masked_gray, 30, 120)
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            if contours:
                main_contour = max(contours, key=cv2.contourArea)
                
                # Draw contour outline in blue
                contour_points = main_contour.reshape(-1, 2)
                if len(contour_points) > 0:
                    ax.plot(contour_points[:, 0], contour_points[:, 1], 
                           'b-', linewidth=2, alpha=0.7, label='Alignment Guide')
        
        # Add legend
        legend_elements = []
        if analysis_results['yellowness_score'] > 10:
            legend_elements.append(plt.Line2D([0], [0], color='yellow', lw=4, alpha=0.7, label='Staining'))
        if analysis_results['cavity_score'] > 2:
            legend_elements.append(plt.Line2D([0], [0], marker='o', color='red', lw=0, 
                                            markersize=10, alpha=0.8, label='Potential Cavities'))
        if analysis_results['alignment_score'] < 80:
            legend_elements.append(plt.Line2D([0], [0], color='blue', lw=2, alpha=0.7, label='Alignment Issues'))
        
        if legend_elements:
            ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(1, 1))
        
        # Remove axes
        ax.axis('off')
        
        # Convert matplotlib figure to image
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', dpi=100)
        plt.close(fig)
        buf.seek(0)
        
        # Convert to PIL Image
        pil_image = Image.open(buf)
        
        return pil_image
