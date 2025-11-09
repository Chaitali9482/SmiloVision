# Smilo - Dental Health Analysis Application

## Overview

Smilo is a Streamlit-based web application that performs automated dental health analysis using computer vision. The application allows users to upload teeth images and receive comprehensive analysis reports covering aspects like tooth staining, cavity detection (dark spots), and alignment scoring. It features a dual-mode interface (standard and kid-friendly) with a gamification system that rewards users with stars and coins for regular dental health monitoring.

## Recent Changes (v2.0)

### Branding Update
- Rebranded from "ToothCheck" to "Smilo" throughout application
- Updated color scheme to use #4A90E2 (blue) as primary brand color
- Modernized UI with improved visual hierarchy and styling

### Critical Bug Fixes
- **FIXED: Cavity Detection Algorithm** - Previously showing 100% for all scans
  - Implemented proper brightness-based thresholding
  - Added circularity filtering to identify actual cavity-like shapes
  - Limited maximum cavity percentage to realistic 30% cap
  - Now provides accurate percentage readings (typically 0-15% for healthy teeth)

### Analysis Improvements
- **Yellowness Detection**: Improved HSV color range calibration with multi-tone stain detection
- **Whiteness Scoring**: Enhanced with proper contrast normalization and lighting compensation
- **Alignment Evaluation**: Refined using improved edge detection and symmetry analysis
- **Overall Scoring**: Better weighted combination of all metrics

### Report Enhancements
- More accurate personalized reviews based on actual detected metrics
- Proper interpretation thresholds for each health aspect
- Evidence-based recommendations scaled to severity
- PDF reports now branded as "Smilo" with updated styling

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture

**Framework Choice: Streamlit**
- **Rationale**: Streamlit provides rapid prototyping for data-driven applications with minimal frontend code
- **Pros**: Fast development, built-in state management, easy data visualization integration
- **Cons**: Limited customization compared to traditional web frameworks, server-side rendering only

**State Management**
- Uses Streamlit's native session state for maintaining application state across reruns
- Key state variables: `current_screen`, `kid_mode`, `current_image`, `analysis_results`, `user_rewards`
- Component instances (analyzer, report generator, database) are cached in session state for performance

**UI Patterns**
- Sidebar navigation for mode switching and main controls
- Wide layout configuration for better image display
- Dual-mode interface: standard mode for adults, kid mode with simplified language and gamification elements
- Modern card-based design with shadows and rounded corners

### Backend Architecture

**Modular Component Design**
- **TeethAnalyzer**: Handles all image processing and analysis logic using OpenCV and scikit-image
- **ReportGenerator**: Creates PDF reports using ReportLab with custom styling
- **Database**: Manages data persistence and retrieval operations
- **Rationale**: Separation of concerns allows independent testing and maintenance of each module

**Image Processing Pipeline**
- Quality checks (lighting, blur, framing) before analysis
- Multi-metric analysis system: staining detection, cavity scoring, alignment assessment
- Uses computer vision techniques: Laplacian variance for blur detection, adaptive/binary thresholding, contrast analysis
- **Chosen approach**: OpenCV + scikit-image combination provides robust image processing capabilities

**Analysis Scoring System**
- Individual scores for yellowness (0-100%), cavities (0-30%), and alignment (0-100)
- Overall composite score calculation with weighted formula
- Quality thresholds: blur_threshold: 100, brightness range: 50-200

**Key Algorithm Improvements**
1. **Cavity Detection Fix**:
   - Dynamic brightness-based thresholding instead of fixed adaptive threshold
   - Circularity filtering (> 0.3) to identify round cavity-like shapes
   - Size constraints: 15-800 pixels to filter noise and large shadows
   - Realistic percentage cap at 30% maximum

2. **Yellowness Detection**:
   - Dual HSV range detection for different stain tones
   - LAB color space support for better color accuracy
   - Expanded detection range: H[10-35], S[20-255], V[100-255]

3. **Alignment Evaluation**:
   - Improved Canny edge detection parameters (30, 120)
   - Combined convexity and aspect ratio scoring
   - Ellipse fitting for ideal alignment comparison

### Data Storage

**Database: SQLite**
- **Rationale**: Lightweight, serverless, requires no configuration - ideal for single-user desktop/web application
- **Schema Design**:
  - `scans`: Stores historical scan data with scores and analysis metadata
  - `user_progress`: Tracks gamification metrics (stars, coins, total scans)
  - `reminders`: Manages scheduled dental care reminders
- **Data Serialization**: JSON format for complex analysis_data storage within SQLite
- **Database file**: `smilo.db` (changed from toothcheck.db)

**Session State vs Persistent Storage**
- Transient data (current image, active analysis) stored in Streamlit session state
- Historical data and user progress persisted to SQLite
- **Trade-off**: Session state provides fast access but requires database sync for persistence

### Report Generation

**PDF Generation: ReportLab**
- Custom styled reports with Smilo branding (#4A90E2 theme color)
- Headers, tables, and embedded images
- Predefined styles for consistency (CustomTitle, CustomSubtitle, SectionHeader)
- Support for multiple page sizes (Letter, A4)
- Accurate interpretations based on actual analysis metrics

### Gamification System

**Reward Mechanism**
- Stars and coins awarded for scan completions
- Progress tracking with last_scan_date to encourage regular use
- Integration with database for persistent reward state
- **Purpose**: Increase user engagement, particularly effective in kid mode

## External Dependencies

### Core Python Libraries

**Computer Vision & Image Processing**
- `opencv-python (cv2)`: Primary image processing, quality checks, blur detection
- `scikit-image`: Advanced morphological operations, filtering, measurements
- `Pillow (PIL)`: Image format conversions and basic manipulations
- `numpy`: Array operations and numerical computations for image data

**Visualization**
- `matplotlib`: Static plot generation for analysis visualizations
- `plotly`: Interactive charts (express and graph_objects) for progress tracking
- `streamlit`: Web application framework and UI components

**Report Generation**
- `reportlab`: PDF creation with custom styling and layouts

**Data Management**
- `pandas`: Data manipulation for historical scan data and progress tracking
- `sqlite3`: Built-in Python library for database operations

**Utilities**
- `datetime`: Timestamp management for scans and reminders
- `json`: Serialization of complex analysis data
- `base64`: Image encoding for data transfer
- `io.BytesIO`: In-memory file operations

### Database

**SQLite (Local File-Based)**
- Database file: `smilo.db`
- No external database server required
- Suitable for single-user deployment
- Migration path available if multi-user support needed (could migrate to PostgreSQL)

### File System Dependencies

**Local Storage**
- Temporary image storage during analysis
- PDF report output location
- Database file persistence
- No cloud storage integration in current implementation

## Testing

To test the application with the included sample image:
1. Run the application
2. Navigate to "Scan Smile"
3. Upload `test_image.png`
4. Verify that cavity detection shows realistic percentages (not 100%)
5. Check that all metrics display accurately in results
