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
from dental_tips_library import DentalTipsLibrary

# Initialize components
if 'analyzer' not in st.session_state:
    st.session_state.analyzer = TeethAnalyzer()
    st.session_state.report_gen = ReportGenerator()
    st.session_state.db = Database()
    st.session_state.tips_library = DentalTipsLibrary()

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
        page_title="😊 Smilo - Smile Analysis",
        page_icon="😊",
        layout="wide"
    )

    # Custom CSS for better UI
    st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        border-radius: 10px;
        font-weight: 600;
    }
    .stMetric {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    h1 {
        color: #4A90E2;
    }
    h2, h3 {
        color: #2C3E50;
    }
    </style>
    """, unsafe_allow_html=True)

    # Mode toggle in sidebar
    with st.sidebar:
        st.title("😊 Smilo")
        st.markdown("### Your Smile Companion")
        mode_changed = st.toggle("Kid Mode 🧒", value=st.session_state.kid_mode)
        if mode_changed != st.session_state.kid_mode:
            st.session_state.kid_mode = mode_changed
            st.rerun()
        
        # Navigation
        st.markdown("---")
        if st.button("🏠 Home", use_container_width=True):
            st.session_state.current_screen = 'home'
            st.rerun()
        if st.button("📸 Scan Smile", use_container_width=True):
            st.session_state.current_screen = 'camera'
            st.rerun()
        if st.button("📈 Progress", use_container_width=True):
            st.session_state.current_screen = 'progress'
            st.rerun()
        if st.button("🔄 Compare Scans", use_container_width=True):
            st.session_state.current_screen = 'compare'
            st.rerun()
        
        # Footer
        st.markdown("---")
        st.markdown("**Version 2.0**")
        st.markdown("*Powered by AI*")

    # Apply mode-specific styling
    if st.session_state.kid_mode:
        st.markdown("""
        <style>
        .main {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
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
    elif st.session_state.current_screen == 'compare':
        show_comparison_screen()

def show_home_screen():
    if st.session_state.kid_mode:
        st.markdown("# 😊✨ Welcome to Smilo! ✨😊")
        st.markdown("### 🌟 Keep your smile bright and healthy! 🌟")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("## 😁🦷😁")
        
        # Kid-friendly buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📸 Scan My Smile! 😊", use_container_width=True, type="primary"):
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
        st.markdown("# 😊 Smilo - Professional Smile Analysis")
        st.markdown("### Advanced dental health screening using AI-powered computer vision")
        
        # Professional layout
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("""
            **Smilo** provides comprehensive oral health analysis by detecting:
            - 🟡 Staining and discoloration levels
            - 🔴 Potential cavities and dark spots  
            - 🔵 Teeth alignment quality
            
            Get your personalized smile score with evidence-based recommendations.
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
                        f"Score ({scan['date']})", 
                        f"{scan['overall_score']:.0f}/100"
                    )

def show_camera_screen():
    if st.session_state.kid_mode:
        st.markdown("# 📸 Time for a Smile Photo! 😊✨")
        st.markdown("### 😁 Show me your amazing smile! 😁")
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
        all_good = all([quality_results['lighting_ok'], quality_results['blur_ok'], quality_results['framing_ok']])
        
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
        st.markdown("# ⚙️ Processing Smile Analysis")
        st.markdown("### Performing comprehensive dental evaluation")

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
            ("Analyzing staining...", 0.6),
            ("Checking for dark spots...", 0.8),
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
            st.success("🎉 Analysis complete! Let's see how your smile is doing! ⭐")
        else:
            st.success("✅ Analysis completed successfully")
        
        # Auto-redirect to results
        import time
        time.sleep(1)
        st.session_state.current_screen = 'results'
        st.rerun()

def show_results_screen():
    if not st.session_state.analysis_results:
        st.error("No analysis results found. Please scan your smile first.")
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
    st.markdown("# 🎉 Your Smile Report! 😊✨")
    
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
        st.metric("🦷 Smile Score", f"{overall_score:.0f}/100")
    with col2:
        st.metric("⭐ Stars Earned", st.session_state.user_rewards['stars'])
    with col3:
        st.metric("🪙 Coins Earned", st.session_state.user_rewards['coins'])
    
    # Show analyzed image
    st.markdown("### 🔍 Your Smile Analysis")
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
    st.markdown("# 📊 Comprehensive Smile Analysis")
    
    # Overall score
    overall_score = results['overall_score']
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Overall Health Score", f"{overall_score:.0f}/100")
    with col2:
        whiteness_score = 100 - results['yellowness_score']
        st.metric("Whiteness Level", f"{whiteness_score:.0f}/100")
        if 'yellowness_severity' in results:
            severity = results['yellowness_severity']
            st.markdown(f"<span style='background-color: {severity['color']}; color: white; padding: 4px 12px; border-radius: 12px; font-size: 0.75em; font-weight: bold;'>{severity['label']}</span>", unsafe_allow_html=True)
    with col3:
        cavity_health = 100 - results['cavity_score']
        st.metric("Dark Spot Health", f"{cavity_health:.0f}/100")
        if 'cavity_severity' in results:
            severity = results['cavity_severity']
            st.markdown(f"<span style='background-color: {severity['color']}; color: white; padding: 4px 12px; border-radius: 12px; font-size: 0.75em; font-weight: bold;'>{severity['label']}</span>", unsafe_allow_html=True)
    with col4:
        st.metric("Alignment Score", f"{results['alignment_score']:.0f}/100")
        if 'alignment_severity' in results:
            severity = results['alignment_severity']
            st.markdown(f"<span style='background-color: {severity['color']}; color: white; padding: 4px 12px; border-radius: 12px; font-size: 0.75em; font-weight: bold;'>{severity['label']}</span>", unsafe_allow_html=True)
    
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
        - 🔴 Red circles: Potential dark spots/cavities
        - 🔵 Blue outlines: Alignment irregularities
        """)
    
    with col2:
        # Score breakdown chart
        st.markdown("### 📈 Score Breakdown")
        
        categories = ['Whiteness', 'Dark Spot\nHealth', 'Alignment']
        scores = [
            100 - results['yellowness_score'],
            100 - results['cavity_score'],
            results['alignment_score']
        ]
        
        fig = go.Figure(data=go.Bar(x=categories, y=scores, 
                                   marker_color=['#FFD700', '#FF6B6B', '#4A90E2']))
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
                file_name=f"smilo_report_{datetime.now().strftime('%Y%m%d')}.pdf",
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
                     title="How Your Smile Health is Improving! 😊✨",
                     color_discrete_sequence=['#667eea'])
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
                         color_discrete_sequence=['#4A90E2'])
            fig.update_layout(yaxis_range=[0, 100])
            st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            # Multi-metric chart
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df['date'], y=100-df['yellowness_score'], 
                                   name='Whiteness', line_color='gold'))
            fig.add_trace(go.Scatter(x=df['date'], y=100-df['cavity_score'], 
                                   name='Dark Spot Health', line_color='lightcoral'))
            fig.add_trace(go.Scatter(x=df['date'], y=df['alignment_score'], 
                                   name='Alignment', line_color='lightblue'))
            fig.update_layout(title="Detailed Health Metrics", yaxis_range=[0, 100])
            st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            # Scan history table
            st.markdown("**Recent Scan History**")
            display_scans = scans[-10:] if len(scans) > 10 else scans
            display_scans.reverse()
            
            for scan in display_scans:
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

def show_comparison_screen():
    """Screen to compare two historical scans side by side"""
    st.markdown("# 🔄 Compare Your Scans")
    st.markdown("### Track your progress by comparing two scans")
    
    # Get all scans
    scans = st.session_state.db.get_all_scans()
    
    if len(scans) < 2:
        st.info("📊 You need at least 2 scans to compare. Take more scans to track your progress!")
        if st.button("📸 Take a Scan", use_container_width=True):
            st.session_state.current_screen = 'camera'
            st.rerun()
        return
    
    # Create scan selection dropdowns
    col1, col2 = st.columns(2)
    
    # Prepare scan options with dates and scores
    scan_options = [f"{scan['date']} (Score: {scan['overall_score']:.0f})" for scan in scans]
    
    with col1:
        st.markdown("### 📊 First Scan")
        scan1_idx = st.selectbox("Select first scan", range(len(scans)), 
                                 format_func=lambda x: scan_options[x],
                                 key="scan1_select")
        scan1 = scans[scan1_idx]
    
    with col2:
        st.markdown("### 📊 Second Scan")
        # Default to latest scan if available
        default_idx = len(scans) - 1 if scan1_idx != len(scans) - 1 else len(scans) - 2
        scan2_idx = st.selectbox("Select second scan", range(len(scans)), 
                                 format_func=lambda x: scan_options[x],
                                 index=default_idx,
                                 key="scan2_select")
        scan2 = scans[scan2_idx]
    
    if scan1_idx == scan2_idx:
        st.warning("⚠️ Please select two different scans to compare")
        return
    
    st.markdown("---")
    
    # Display comparison
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"### 📅 {scan1['date']}")
        st.metric("Overall Score", f"{scan1['overall_score']:.0f}/100")
        
        # Individual metrics
        st.markdown("**Detailed Metrics:**")
        st.metric("Whiteness", f"{100-scan1['yellowness_score']:.0f}/100")
        st.metric("Dark Spot Health", f"{100-scan1['cavity_score']:.0f}/100")
        st.metric("Alignment", f"{scan1['alignment_score']:.0f}/100")
    
    with col2:
        st.markdown(f"### 📅 {scan2['date']}")
        
        # Calculate deltas
        overall_delta = scan2['overall_score'] - scan1['overall_score']
        whiteness_delta = (100-scan2['yellowness_score']) - (100-scan1['yellowness_score'])
        cavity_delta = (100-scan2['cavity_score']) - (100-scan1['cavity_score'])
        alignment_delta = scan2['alignment_score'] - scan1['alignment_score']
        
        st.metric("Overall Score", f"{scan2['overall_score']:.0f}/100", 
                 f"{overall_delta:+.1f}", delta_color="normal")
        
        # Individual metrics with deltas
        st.markdown("**Detailed Metrics:**")
        st.metric("Whiteness", f"{100-scan2['yellowness_score']:.0f}/100",
                 f"{whiteness_delta:+.1f}", delta_color="normal")
        st.metric("Dark Spot Health", f"{100-scan2['cavity_score']:.0f}/100",
                 f"{cavity_delta:+.1f}", delta_color="normal")
        st.metric("Alignment", f"{scan2['alignment_score']:.0f}/100",
                 f"{alignment_delta:+.1f}", delta_color="normal")
    
    # Visual comparison charts
    st.markdown("---")
    st.markdown("### 📊 Visual Comparison")
    
    # Create comparison chart
    metrics = ['Overall\nScore', 'Whiteness', 'Dark Spot\nHealth', 'Alignment']
    scan1_values = [
        scan1['overall_score'],
        100 - scan1['yellowness_score'],
        100 - scan1['cavity_score'],
        scan1['alignment_score']
    ]
    scan2_values = [
        scan2['overall_score'],
        100 - scan2['yellowness_score'],
        100 - scan2['cavity_score'],
        scan2['alignment_score']
    ]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        name=f'Scan 1: {scan1["date"][:10]}',
        x=metrics,
        y=scan1_values,
        marker_color='#95A5A6'
    ))
    fig.add_trace(go.Bar(
        name=f'Scan 2: {scan2["date"][:10]}',
        x=metrics,
        y=scan2_values,
        marker_color='#4A90E2'
    ))
    
    fig.update_layout(
        title="Side-by-Side Comparison",
        yaxis_title="Score (0-100)",
        yaxis_range=[0, 100],
        barmode='group',
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Improvement analysis
    st.markdown("---")
    st.markdown("### 💡 Progress Analysis")
    
    improvements = []
    declines = []
    
    if overall_delta > 0:
        improvements.append(f"✅ Overall score improved by {overall_delta:.1f} points")
    elif overall_delta < 0:
        declines.append(f"⚠️ Overall score decreased by {abs(overall_delta):.1f} points")
    
    if whiteness_delta > 0:
        improvements.append(f"✅ Whiteness improved by {whiteness_delta:.1f} points")
    elif whiteness_delta < 0:
        declines.append(f"⚠️ Whiteness decreased by {abs(whiteness_delta):.1f} points")
    
    if cavity_delta > 0:
        improvements.append(f"✅ Dark spot health improved by {cavity_delta:.1f} points")
    elif cavity_delta < 0:
        declines.append(f"⚠️ Dark spot health decreased by {abs(cavity_delta):.1f} points")
    
    if alignment_delta > 0:
        improvements.append(f"✅ Alignment improved by {alignment_delta:.1f} points")
    elif alignment_delta < 0:
        declines.append(f"⚠️ Alignment decreased by {abs(alignment_delta):.1f} points")
    
    if improvements:
        st.markdown("**Improvements:**")
        for improvement in improvements:
            st.markdown(improvement)
    
    if declines:
        st.markdown("**Areas Needing Attention:**")
        for decline in declines:
            st.markdown(decline)
    
    if not improvements and not declines:
        st.info("📊 Scores remain stable between these two scans")
    
    # Action buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🏠 Home", use_container_width=True):
            st.session_state.current_screen = 'home'
            st.rerun()
    with col2:
        if st.button("📸 New Scan", use_container_width=True):
            st.session_state.current_screen = 'camera'
            st.rerun()

def generate_kid_tips(results):
    """Generate kid-friendly tips using severity-based library"""
    return st.session_state.tips_library.get_kid_friendly_tips(results)

def generate_adult_tips(results):
    """Generate adult tips using severity-based comprehensive library"""
    comprehensive_tips = st.session_state.tips_library.get_comprehensive_tips(results)
    
    # Combine priority actions and prevention tips
    tips = []
    
    # Add priority actions first
    if comprehensive_tips['priority_actions']:
        tips.extend(comprehensive_tips['priority_actions'][:5])  # Top 5 priority items
    
    # Add key prevention tips
    if comprehensive_tips['prevention']:
        tips.extend(comprehensive_tips['prevention'][:3])  # Top 3 prevention items
    
    # Add professional care reminder
    if comprehensive_tips['professional_care']:
        tips.append(comprehensive_tips['professional_care'][0])  # First professional care item
    
    return tips

if __name__ == "__main__":
    main()
