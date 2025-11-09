import streamlit as st
import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import pandas as pd
import base64
from io import BytesIO
import json
import os
from image_analyzer import TeethAnalyzer
from report_generator import ReportGenerator
from database import Database

# Initialize components
if 'analyzer' not in st.session_state:
    st.session_state.analyzer = TeethAnalyzer()
    st.session_state.report_gen = ReportGenerator()
    st.session_state.db = Database()

# Initialize session state
if 'current_screen' not in st.session_state:
    st.session_state.current_screen = 'home'
if 'kid_mode' not in st.session_state:
    st.session_state.kid_mode = False
if 'current_image' not in st.session_state:
    st.session_state.current_image = None
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None
if 'user_rewards' not in st.session_state:
    progress = st.session_state.db.get_user_progress()
    st.session_state.user_rewards = {'stars': progress['stars'], 'coins': progress['coins']}

def main():
    # Configure page
    st.set_page_config(
        page_title="🦷 ToothCheck",
        page_icon="🦷",
        layout="wide"
    )

    # Mode toggle in sidebar
    with st.sidebar:
        st.title("🦷 ToothCheck")
        mode_changed = st.toggle("Kid Mode 🧒", value=st.session_state.kid_mode)
        if mode_changed != st.session_state.kid_mode:
            st.session_state.kid_mode = mode_changed
            st.rerun()
        
        # Navigation
        st.markdown("---")
        if st.button("🏠 Home", use_container_width=True):
            st.session_state.current_screen = 'home'
            st.rerun()
        if st.button("📸 Scan Teeth", use_container_width=True):
            st.session_state.current_screen = 'camera'
            st.rerun()
        if st.button("📈 Progress", use_container_width=True):
            st.session_state.current_screen = 'progress'
            st.rerun()

    # Apply mode-specific styling
    if st.session_state.kid_mode:
        st.markdown("""
        <style>
        .main > div {
            background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 50%, #fecfef 100%);
        }
        </style>
        """, unsafe_allow_html=True)

    # Route to appropriate screen
    if st.session_state.current_screen == 'home':
        show_home_screen()
    elif st.session_state.current_screen == 'camera':
        show_camera_screen()
    elif st.session_state.current_screen == 'quality_check':
        show_quality_check_screen()
    elif st.session_state.current_screen == 'analysis':
        show_analysis_screen()
    elif st.session_state.current_screen == 'results':
        show_results_screen()
    elif st.session_state.current_screen == 'progress':
        show_progress_screen()

def show_home_screen():
    if st.session_state.kid_mode:
        st.markdown("# 🦷✨ Welcome to ToothCheck! ✨🦷")
        st.markdown("### 🌟 Keep your smile sparkling bright! 🌟")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("## 😁🦷😁")
        
        # Kid-friendly buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📸 Scan My Teeth! 🦷", use_container_width=True, type="primary"):
                st.session_state.current_screen = 'camera'
                st.rerun()
        with col2:
            if st.button("📈 My Progress! ⭐", use_container_width=True):
                st.session_state.current_screen = 'progress'
                st.rerun()
        
        # Show rewards
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("⭐ Stars Earned", st.session_state.user_rewards['stars'])
        with col2:
            st.metric("🪙 Coins Collected", st.session_state.user_rewards['coins'])
            
    else:
        st.markdown("# 🦷 ToothCheck - Professional Oral Health Screening")
        st.markdown("### Advanced teeth analysis using computer vision")
        
        # Professional layout
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("""
            **ToothCheck** provides comprehensive oral health analysis by detecting:
            - 🟡 Yellow stains and discoloration
            - 🔴 Possible cavities and dark spots  
            - 🔵 Teeth alignment issues
            
            Get your personalized oral health score with actionable recommendations.
            """)
            
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("📸 Start Scan", use_container_width=True, type="primary"):
                    st.session_state.current_screen = 'camera'
                    st.rerun()
            with col_b:
                if st.button("📈 View Progress", use_container_width=True):
                    st.session_state.current_screen = 'progress'
                    st.rerun()
        
        with col2:
            # Recent stats if available
            recent_scans = st.session_state.db.get_recent_scans(5)
            if recent_scans:
                st.markdown("**Recent Scans**")
                for scan in recent_scans:
                    st.metric(
                        f"Health Score ({scan['date']})", 
                        f"{scan['overall_score']:.0f}/100"
                    )

def show_camera_screen():
    if st.session_state.kid_mode:
        st.markdown("# 📸 Time for a Tooth Photo! 🦷✨")
        st.markdown("### 😊 Show me your beautiful smile! 😊")
    else:
        st.markdown("# 📸 Capture Image for Analysis")
        st.markdown("### Position your mouth within the guide for optimal results")

    # Instructions
    with st.expander("📋 Photo Instructions", expanded=True):
        st.markdown("""
        **For best results:**
        - 💡 Ensure good lighting (natural light preferred)
        - 😁 Open your mouth and show your teeth clearly
        - 📱 Hold camera steady and avoid blur
        - 🎯 Center your mouth within the oval guide
        """)

    # Camera options
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📷 Take Photo**")
        camera_image = st.camera_input("Capture your smile")
        if camera_image:
            st.session_state.current_image = camera_image
            st.success("✅ Photo captured!")
    
    with col2:
        st.markdown("**📁 Upload Photo**")
        uploaded_file = st.file_uploader("Choose image", type=['png', 'jpg', 'jpeg'])
        if uploaded_file:
            st.session_state.current_image = uploaded_file
            st.success("✅ Image uploaded!")

    # Show preview and continue button
    if st.session_state.current_image:
        st.markdown("---")
        st.markdown("**Preview:**")
        
        # Display image with oval overlay guide
        image = Image.open(st.session_state.current_image)
        fig, ax = plt.subplots(1, 1, figsize=(8, 6))
        ax.imshow(image)
        ax.set_title("Image Preview with Guide")
        
        # Draw oval guide
        from matplotlib.patches import Ellipse
        height, width = image.height, image.width
        oval = Ellipse((width/2, height/2), width*0.6, height*0.4, 
                      fill=False, color='lime', linewidth=3, linestyle='--')
        ax.add_patch(oval)
        ax.text(width/2, height*0.1, "Position mouth within green guide", 
                ha='center', color='lime', fontsize=12, weight='bold')
        ax.axis('off')
        
        st.pyplot(fig)
        plt.close()
        
        if st.button("✅ Continue to Analysis", type="primary", use_container_width=True):
            st.session_state.current_screen = 'quality_check'
            st.rerun()

def show_quality_check_screen():
    if st.session_state.kid_mode:
        st.markdown("# 🔍 Checking Your Photo! ✨")
        st.markdown("### Making sure everything looks perfect! 😊")
    else:
        st.markdown("# 🔍 Image Quality Validation")
        st.markdown("### Ensuring optimal conditions for accurate analysis")

    if st.session_state.current_image:
        # Convert to OpenCV format
        image = Image.open(st.session_state.current_image)
        img_array = np.array(image)
        
        # Perform quality checks
        with st.spinner("Checking image quality..."):
            quality_results = st.session_state.analyzer.check_image_quality(img_array)
        
        # Display results
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if quality_results['lighting_ok']:
                st.success("✅ Lighting: Good")
            else:
                st.warning("⚠️ Lighting: Needs improvement")
        
        with col2:
            if quality_results['blur_ok']:
                st.success("✅ Sharpness: Clear")
            else:
                st.warning("⚠️ Sharpness: Too blurry")
        
        with col3:
            if quality_results['framing_ok']:
                st.success("✅ Framing: Well positioned")
            else:
                st.warning("⚠️ Framing: Reposition mouth")

        # Decision based on quality
        all_good = all(quality_results.values())
        
        if all_good:
            if st.session_state.kid_mode:
                st.success("🎉 Perfect! Your photo looks amazing! 🌟")
            else:
                st.success("✅ Image quality validated - proceeding to analysis")
            
            if st.button("🚀 Start Analysis", type="primary", use_container_width=True):
                st.session_state.current_screen = 'analysis'
                st.rerun()
        else:
            if st.session_state.kid_mode:
                st.warning("😊 Oops! Let's try again with better light and a steady hand!")
            else:
                st.warning("⚠️ Image quality issues detected. Please retake photo for better results.")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📸 Retake Photo", type="primary"):
                    st.session_state.current_screen = 'camera'
                    st.session_state.current_image = None
                    st.rerun()
            with col2:
                if st.button("🚀 Analyze Anyway"):
                    st.session_state.current_screen = 'analysis'
                    st.rerun()

def show_analysis_screen():
    if st.session_state.kid_mode:
        st.markdown("# 🔬 Analyzing Your Smile! ✨")
        st.markdown("### The magic is happening... 🪄")
    else:
        st.markdown("# ⚙️ Processing Image Analysis")
        st.markdown("### Performing comprehensive teeth evaluation")

    if st.session_state.current_image:
        # Progress indicator
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Convert image
        image = Image.open(st.session_state.current_image)
        img_array = np.array(image)
        
        # Analysis steps
        steps = [
            ("Preprocessing image...", 0.2),
            ("Detecting teeth region...", 0.4),
            ("Analyzing yellowness...", 0.6),
            ("Checking for cavities...", 0.8),
            ("Evaluating alignment...", 1.0)
        ]
        
        for step_text, progress in steps:
            status_text.text(step_text)
            progress_bar.progress(progress)
            
            # Simulate processing time
            import time
            time.sleep(0.5)
        
        # Perform actual analysis
        with st.spinner("Finalizing analysis..."):
            results = st.session_state.analyzer.analyze_teeth(img_array)
        
        st.session_state.analysis_results = results
        
        # Success message
        if st.session_state.kid_mode:
            st.success("🎉 Analysis complete! Let's see how your teeth are doing! ⭐")
        else:
            st.success("✅ Analysis completed successfully")
        
        # Auto-redirect to results
        import time
        time.sleep(1)
        st.session_state.current_screen = 'results'
        st.rerun()

def show_results_screen():
    if not st.session_state.analysis_results:
        st.error("No analysis results found. Please scan your teeth first.")
        return

    results = st.session_state.analysis_results
    
    if st.session_state.kid_mode:
        show_kid_results(results)
    else:
        show_adult_results(results)
    
    # Save results to database and update rewards
    st.session_state.db.save_scan_results(results)
    
    # Update rewards in database
    if st.session_state.kid_mode:
        overall_score = results['overall_score']
        if overall_score >= 80:
            stars_earned = 3
            coins_earned = 10
        elif overall_score >= 60:
            stars_earned = 2
            coins_earned = 5
        else:
            stars_earned = 1
            coins_earned = 2
        
        st.session_state.db.update_user_rewards(stars_earned, coins_earned)

def show_kid_results(results):
    st.markdown("# 🎉 Your Tooth Report! 🦷✨")
    
    # Overall score with fun animation
    overall_score = results['overall_score']
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if overall_score >= 80:
            st.markdown("## 😁 Awesome! Great job! 🌟")
        elif overall_score >= 60:
            st.markdown("## 😊 Good work! Let's improve! 💪")
        else:
            st.markdown("## 😷 Time for extra care! 🦷")
    
    # Fun metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🦷 Health Score", f"{overall_score:.0f}/100")
    with col2:
        st.metric("⭐ Stars Earned", st.session_state.user_rewards['stars'])
    with col3:
        st.metric("🪙 Coins Earned", st.session_state.user_rewards['coins'])
    
    # Show analyzed image
    st.markdown("### 🔍 Your Teeth Analysis")
    analyzed_img = st.session_state.analyzer.create_visual_overlay(
        np.array(Image.open(st.session_state.current_image)), results)
    st.image(analyzed_img, caption="Your teeth with colorful markings!", use_container_width=True)
    
    # Kid-friendly tips
    st.markdown("### 💡 Super Tips for You! 🌟")
    tips = generate_kid_tips(results)
    for tip in tips:
        st.markdown(f"• {tip}")
    
    # Action buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🏠 Go Home", use_container_width=True):
            st.session_state.current_screen = 'home'
            st.rerun()
    with col2:
        if st.button("📸 Scan Again", use_container_width=True):
            st.session_state.current_screen = 'camera'
            st.session_state.current_image = None
            st.session_state.analysis_results = None
            st.rerun()

def show_adult_results(results):
    st.markdown("# 📊 Comprehensive Oral Health Analysis")
    
    # Overall score
    overall_score = results['overall_score']
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Overall Health Score", f"{overall_score:.0f}/100")
    with col2:
        st.metric("Whiteness Level", f"{100-results['yellowness_score']:.0f}/100")
    with col3:
        st.metric("Cavity Health", f"{100-results['cavity_score']:.0f}/100")
    with col4:
        st.metric("Alignment Score", f"{results['alignment_score']:.0f}/100")
    
    # Visual analysis
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 🔍 Visual Analysis")
        analyzed_img = st.session_state.analyzer.create_visual_overlay(
            np.array(Image.open(st.session_state.current_image)), results)
        st.image(analyzed_img, caption="Detected issues marked with overlays", use_container_width=True)
        
        # Legend
        st.markdown("""
        **Legend:**
        - 🟡 Yellow overlay: Staining detected
        - 🔴 Red circles: Potential cavities
        - 🔵 Blue outlines: Alignment issues
        """)
    
    with col2:
        # Score breakdown chart
        st.markdown("### 📈 Score Breakdown")
        
        categories = ['Whiteness', 'Cavity Health', 'Alignment']
        scores = [
            100 - results['yellowness_score'],
            100 - results['cavity_score'],
            results['alignment_score']
        ]
        
        fig = go.Figure(data=go.Bar(x=categories, y=scores, 
                                   marker_color=['gold', 'lightcoral', 'lightblue']))
        fig.update_layout(title="Health Metrics", yaxis_range=[0, 100], height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    # Personalized recommendations
    st.markdown("### 💡 Personalized Recommendations")
    tips = generate_adult_tips(results)
    for i, tip in enumerate(tips, 1):
        st.markdown(f"{i}. {tip}")
    
    # Action buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📄 Generate PDF Report", use_container_width=True):
            with st.spinner("Generating PDF report..."):
                pdf_data = st.session_state.report_gen.generate_pdf_report(
                    st.session_state.current_image, results)
            st.download_button(
                label="⬇️ Download PDF",
                data=pdf_data,
                file_name=f"toothcheck_report_{datetime.now().strftime('%Y%m%d')}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
    with col2:
        if st.button("🏠 Home", use_container_width=True):
            st.session_state.current_screen = 'home'
            st.rerun()
    with col3:
        if st.button("📸 New Scan", use_container_width=True):
            st.session_state.current_screen = 'camera'
            st.session_state.current_image = None
            st.session_state.analysis_results = None
            st.rerun()

def show_progress_screen():
    if st.session_state.kid_mode:
        st.markdown("# 📈 My Progress Journey! ⭐")
        st.markdown("### Look how awesome you're doing! 🌟")
    else:
        st.markdown("# 📈 Progress Tracker")
        st.markdown("### Historical analysis and trends")

    # Get historical data
    scans = st.session_state.db.get_all_scans()
    
    if not scans:
        if st.session_state.kid_mode:
            st.info("🎯 No scans yet! Take your first photo to start your journey! 🚀")
        else:
            st.info("📊 No historical data available. Complete your first scan to track progress.")
        return
    
    # Convert to DataFrame for easier plotting
    df = pd.DataFrame(scans)
    df['date'] = pd.to_datetime(df['date'])
    
    if st.session_state.kid_mode:
        # Kid-friendly progress view
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("🦷 Total Scans", len(scans))
            st.metric("⭐ Total Stars", st.session_state.user_rewards['stars'])
        
        with col2:
            latest_score = df['overall_score'].iloc[-1] if len(df) > 0 else 0
            st.metric("🏆 Latest Score", f"{latest_score:.0f}/100")
            st.metric("🪙 Total Coins", st.session_state.user_rewards['coins'])
        
        # Simple progress chart
        st.markdown("### 📊 Your Progress Chart! 🌈")
        fig = px.line(df, x='date', y='overall_score', 
                     title="How Your Teeth Health is Improving! 🦷✨",
                     color_discrete_sequence=['#FF6B6B'])
        fig.update_layout(
            xaxis_title="Date 📅",
            yaxis_title="Health Score 🏆",
            yaxis_range=[0, 100]
        )
        st.plotly_chart(fig, use_container_width=True)
        
    else:
        # Professional progress view
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Scans", len(scans))
        with col2:
            avg_score = df['overall_score'].mean()
            st.metric("Average Score", f"{avg_score:.1f}/100")
        with col3:
            if len(df) >= 2:
                improvement = df['overall_score'].iloc[-1] - df['overall_score'].iloc[-2]
                st.metric("Score Change", f"{improvement:+.1f}", delta=f"{improvement:.1f}")
            else:
                st.metric("Score Change", "N/A")
        with col4:
            latest_score = df['overall_score'].iloc[-1] if len(df) > 0 else 0
            st.metric("Latest Score", f"{latest_score:.1f}/100")
        
        # Detailed charts
        tab1, tab2, tab3 = st.tabs(["📊 Overall Trends", "🔍 Detailed Metrics", "📅 Scan History"])
        
        with tab1:
            # Overall score trend
            fig = px.line(df, x='date', y='overall_score', 
                         title="Overall Health Score Trend",
                         color_discrete_sequence=['#2E86C1'])
            fig.update_layout(yaxis_range=[0, 100])
            st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            # Multi-metric chart
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df['date'], y=100-df['yellowness_score'], 
                                   name='Whiteness', line_color='gold'))
            fig.add_trace(go.Scatter(x=df['date'], y=100-df['cavity_score'], 
                                   name='Cavity Health', line_color='lightcoral'))
            fig.add_trace(go.Scatter(x=df['date'], y=df['alignment_score'], 
                                   name='Alignment', line_color='lightblue'))
            fig.update_layout(title="Detailed Health Metrics", yaxis_range=[0, 100])
            st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            # Scan history table
            st.markdown("**Recent Scan History**")
            for scan in scans[-10:]:
                col1, col2, col3 = st.columns([2, 1, 1])
                with col1:
                    st.text(scan['date'])
                with col2:
                    st.text(f"Score: {scan['overall_score']:.0f}/100")
                with col3:
                    if scan['overall_score'] >= 80:
                        st.text("✅ Excellent")
                    elif scan['overall_score'] >= 60:
                        st.text("⚠️ Good")
                    else:
                        st.text("❌ Needs Care")

def generate_kid_tips(results):
    tips = []
    
    if results['yellowness_score'] > 20:
        tips.append("🦷 Try brushing your teeth extra well tonight! ✨")
        tips.append("🥛 Drink more water and less sugary drinks! 💧")
    else:
        tips.append("🌟 Your teeth are nice and white! Keep it up!")
    
    if results['cavity_score'] > 15:
        tips.append("🍎 Eat healthy snacks like apples and carrots! 🥕")
        tips.append("😷 Ask a grown-up to schedule a dentist visit! 👩‍⚕️")
    else:
        tips.append("🎉 Great job keeping cavities away!")
    
    if results['alignment_score'] < 70:
        tips.append("😁 Keep smiling and practice good posture! 💪")
    else:
        tips.append("🦷 Your teeth alignment looks great!")
    
    tips.append("⏰ Remember to brush twice a day for 2 minutes!")
    
    return tips

def generate_adult_tips(results):
    tips = []
    
    if results['yellowness_score'] > 30:
        tips.append("Consider professional teeth whitening treatment")
        tips.append("Reduce consumption of coffee, tea, and red wine")
        tips.append("Use whitening toothpaste as part of daily routine")
    elif results['yellowness_score'] > 15:
        tips.append("Monitor staining and consider whitening toothpaste")
        tips.append("Rinse mouth with water after consuming staining foods")
    else:
        tips.append("Excellent whiteness! Maintain current oral hygiene routine")
    
    if results['cavity_score'] > 20:
        tips.append("Schedule immediate dental examination for dark spots")
        tips.append("Increase flossing frequency to daily")
        tips.append("Consider fluoride treatments with your dentist")
    elif results['cavity_score'] > 10:
        tips.append("Monitor dark spots and maintain regular dental checkups")
        tips.append("Ensure thorough brushing twice daily")
    else:
        tips.append("Low cavity risk detected - keep up good oral hygiene")
    
    if results['alignment_score'] < 60:
        tips.append("Consult an orthodontist for alignment evaluation")
        tips.append("Consider orthodontic treatment options")
    elif results['alignment_score'] < 80:
        tips.append("Minor alignment irregularities detected - monitor progress")
    else:
        tips.append("Excellent teeth alignment")
    
    tips.append("Schedule dental cleanings every 6 months")
    tips.append("Replace toothbrush every 3-4 months")
    
    return tips

if __name__ == "__main__":
    main()
