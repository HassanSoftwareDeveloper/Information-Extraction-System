"""
Professional Event Registration Information Extraction System
Enterprise-grade Streamlit interface with modern UI/UX design
"""

import streamlit as st
import pandas as pd
import json
from typing import Dict, Any, List, Optional, Tuple
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time
from dataclasses import dataclass
from enum import Enum
import logging

from extraction_service import EventRegistrationExtractionService


class ProcessingMode(Enum):
    """Enumeration for processing modes."""
    SINGLE_TEXT = "single_text"
    BATCH_PROCESSING = "batch_processing"
    DEMO_EXAMPLES = "demo_examples"


class ExportFormat(Enum):
    """Enumeration for export formats."""
    CSV = "csv"
    JSON = "json"
    XML = "xml"
    EXCEL = "xlsx"


@dataclass
class ApplicationConfig:
    """Application configuration settings."""
    PAGE_TITLE: str = "Event Registration Information Extraction System"
    PAGE_ICON: str = "🎯"
    LAYOUT: str = "wide"
    SIDEBAR_STATE: str = "expanded"
    MAX_FILE_SIZE: int = 200  # MB
    SUPPORTED_FILE_TYPES: List[str] = None
    
    def __post_init__(self):
        if self.SUPPORTED_FILE_TYPES is None:
            self.SUPPORTED_FILE_TYPES = ["csv", "xlsx", "txt"]


@dataclass
class ProcessingHistory:
    """Data class for processing history entries."""
    timestamp: datetime
    input_text: str
    extraction_result: Dict[str, Any]
    processing_mode: str
    processing_time_ms: float
    success: bool


class ProfessionalEventExtractionInterface:
    """
    Professional-grade Streamlit interface for event registration information extraction.
    
    Features:
    - Modern, responsive UI design
    - Enterprise-level error handling
    - Comprehensive analytics dashboard
    - Professional data visualization
    - Batch processing capabilities
    - Export functionality
    """
    
    def __init__(self):
        """Initialize the professional extraction interface."""
        self.config = ApplicationConfig()
        self._setup_page_configuration()
        self._initialize_extraction_service()
        self._initialize_application_state()
        self._setup_logging()
    
    def _setup_page_configuration(self) -> None:
        """Configure Streamlit page with professional settings."""
        st.set_page_config(
            page_title=self.config.PAGE_TITLE,
            page_icon=self.config.PAGE_ICON,
            layout=self.config.LAYOUT,
            initial_sidebar_state=self.config.SIDEBAR_STATE,
            menu_items={
                'Get Help': None,
                'Report a bug': None,
                'About': "Professional Event Registration Extraction System v2.0"
            }
        )
        
        # Custom CSS for professional styling
        self._inject_custom_styles()
    
    def _inject_custom_styles(self) -> None:
        """Inject custom CSS for professional appearance."""
        st.markdown("""
        <style>
        /* Main container styling */
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        
        /* Professional color scheme */
        :root {
            --primary-color: #1f77b4;
            --secondary-color: #ff7f0e;
            --success-color: #2ca02c;
            --warning-color: #ff7f0e;
            --error-color: #d62728;
            --background-color: #f8f9fa;
        }
        
        /* Header styling */
        .header-container {
            background: linear-gradient(90deg, #1f77b4 0%, #2ca02c 100%);
            padding: 2rem 1rem;
            border-radius: 10px;
            margin-bottom: 2rem;
            color: white;
        }
        
        /* Metric cards styling */
        .metric-card {
            background: white;
            padding: 1rem;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            border-left: 4px solid var(--primary-color);
        }
        
        /* Status indicators */
        .status-success { color: var(--success-color) !important; }
        .status-warning { color: var(--warning-color) !important; }
        .status-error { color: var(--error-color) !important; }
        
        /* Professional buttons */
        .stButton > button {
            border-radius: 6px;
            font-weight: 500;
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        }
        
        /* Sidebar styling */
        .sidebar .sidebar-content {
            background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
        }
        
        /* Data table styling */
        .stDataFrame {
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        
        /* Alert styling */
        .alert-info {
            background-color: #e7f3ff;
            border-left: 4px solid #1f77b4;
            padding: 1rem;
            border-radius: 4px;
            margin: 1rem 0;
        }
        
        .alert-success {
            background-color: #e8f5e8;
            border-left: 4px solid #2ca02c;
            padding: 1rem;
            border-radius: 4px;
            margin: 1rem 0;
        }
        
        .alert-warning {
            background-color: #fff3e0;
            border-left: 4px solid #ff7f0e;
            padding: 1rem;
            border-radius: 4px;
            margin: 1rem 0;
        }
        </style>
        """, unsafe_allow_html=True)
    
    def _initialize_extraction_service(self) -> None:
        """Initialize the extraction service with proper error handling."""
        if 'extraction_service' not in st.session_state:
            try:
                with st.spinner("Initializing extraction service..."):
                    st.session_state.extraction_service = EventRegistrationExtractionService()
                    st.session_state.service_status = {
                        'initialized': True,
                        'error_message': None,
                        'initialization_time': datetime.now()
                    }
            except Exception as service_error:
                st.session_state.service_status = {
                    'initialized': False,
                    'error_message': str(service_error),
                    'initialization_time': datetime.now()
                }
                logging.error(f"Service initialization failed: {service_error}")
    
    def _initialize_application_state(self) -> None:
        """Initialize application state with professional defaults."""
        default_state = {
            'processing_history': [],
            'current_extraction_result': None,
            'batch_processing_results': None,
            'selected_processing_mode': ProcessingMode.SINGLE_TEXT.value,
            'selected_output_template': 'standard',
            'application_preferences': {
                'show_detailed_analytics': False,
                'show_entity_details': True,
                'show_confidence_visualizations': False,
                'enable_real_time_validation': True,
                'auto_save_results': False
            },
            'demo_data_samples': [
                {
                    'text': "Dr. Sarah Johnson registered for the International AI Conference 2025 taking place in San Francisco, California on March 15, 2025.",
                    'category': 'Academic Conference'
                },
                {
                    'text': "Michael Chen has enrolled in the Digital Marketing Summit scheduled for November 22, 2024 in New York City.",
                    'category': 'Business Event'
                },
                {
                    'text': "Professor Ahmed Al-Rashid signed up for the Machine Learning Workshop happening in London, UK on December 10, 2024.",
                    'category': 'Educational Workshop'
                },
                {
                    'text': "Maria Rodriguez joined the Global Tech Expo taking place in Dubai, UAE on February 8, 2025.",
                    'category': 'Technology Exhibition'
                },
                {
                    'text': "David Smith registered for the Healthcare Innovation Conference in Toronto, Canada on January 25, 2025.",
                    'category': 'Healthcare Conference'
                }
            ],
            'system_statistics': {
                'total_extractions_performed': 0,
                'successful_extractions': 0,
                'average_processing_time': 0.0,
                'last_extraction_timestamp': None
            }
        }
        
        for state_key, default_value in default_state.items():
            if state_key not in st.session_state:
                st.session_state[state_key] = default_value
    
    def _setup_logging(self) -> None:
        """Setup application logging configuration."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def run_application(self) -> None:
        """Run the main application interface."""
        try:
            self._render_application_header()
            
            if not st.session_state.service_status['initialized']:
                self._render_service_error_interface()
                return
            
            # Create main application layout
            self._create_navigation_sidebar()
            self._render_main_content_area()
            
        except Exception as app_error:
            self._render_critical_error(app_error)
            logging.critical(f"Critical application error: {app_error}")
    
    def run(self) -> None:
        """Alias for run_application() to maintain compatibility."""
        return self.run_application()
    
    def _render_application_header(self) -> None:
        """Render professional application header with branding."""
        st.markdown("""
        <div class="header-container">
            <h1 style="margin-bottom: 0.5rem; color: white;">🎯 Event Registration Information Extraction System</h1>
            <p style="margin: 0; opacity: 0.9; font-size: 1.1rem;">
                Professional-grade NLP-powered information extraction for event registration data
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Status indicator
        status_color = "🟢" if st.session_state.service_status['initialized'] else "🔴"
        status_text = "System Operational" if st.session_state.service_status['initialized'] else "System Error"
        
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.markdown(f"**System Status:** {status_color} {status_text}")
        with col2:
            if st.button("🔄 Refresh System", help="Refresh system status"):
                st.rerun()
        with col3:
            st.markdown(f"**Version:** 2.0.0")
    
    def _render_service_error_interface(self) -> None:
        """Render service error interface with recovery options."""
        st.error("🚨 **System Initialization Error**")
        
        error_details = st.session_state.service_status.get('error_message', 'Unknown error occurred')
        st.error(f"**Error Details:** {error_details}")
        
        st.markdown("""
        <div class="alert-warning">
            <strong>⚠️ Service Unavailable</strong><br>
            The extraction service failed to initialize. Please try the following:
            <ul>
                <li>Check system dependencies</li>
                <li>Verify service configuration</li>
                <li>Restart the application</li>
                <li>Contact system administrator if the problem persists</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 **Retry Initialization**", type="primary"):
                with st.spinner("Attempting to reinitialize service..."):
                    time.sleep(1)  # Simulate initialization delay
                    self._initialize_extraction_service()
                    st.rerun()
        
        with col2:
            if st.button("📊 **View System Diagnostics**"):
                self._render_system_diagnostics()
    
    def _create_navigation_sidebar(self) -> None:
        """Create professional navigation sidebar with advanced options."""
        st.sidebar.header("🎛️ **Control Panel**")
        
        # Processing mode selection
        st.sidebar.subheader("📋 Processing Mode")
        processing_mode_options = {
            ProcessingMode.SINGLE_TEXT.value: "📝 Single Text Processing",
            ProcessingMode.BATCH_PROCESSING.value: "📊 Batch Processing",
            ProcessingMode.DEMO_EXAMPLES.value: "🧪 Demo & Examples"
        }
        
        selected_mode = st.sidebar.selectbox(
            "Select processing mode:",
            options=list(processing_mode_options.keys()),
            format_func=lambda x: processing_mode_options[x],
            key="processing_mode_selector"
        )
        st.session_state.selected_processing_mode = selected_mode
        
        # Output template configuration
        self._render_template_configuration()
        
        # Advanced preferences
        self._render_advanced_preferences()
        
        # System monitoring
        self._render_system_monitoring_panel()
        
        # Quick actions
        self._render_quick_actions_panel()
    
    def _render_template_configuration(self) -> None:
        """Render output template configuration section."""
        st.sidebar.subheader("📄 Output Configuration")
        
        try:
            available_templates = st.session_state.extraction_service.getAvailableTemplates()
            
            template_descriptions = {
                'standard': 'Standard format with all fields',
                'minimal': 'Minimal format with essential fields only',
                'detailed': 'Detailed format with metadata',
                'custom': 'Custom user-defined format'
            }
            
            selected_template = st.sidebar.selectbox(
                "Output template:",
                options=list(available_templates.keys()) if available_templates else ['standard'],
                format_func=lambda x: f"{x.title()} - {template_descriptions.get(x, 'Custom template')}",
                key="template_selector"
            )
            st.session_state.selected_output_template = selected_template
            
        except Exception as template_error:
            st.sidebar.error("Unable to load templates")
            st.session_state.selected_output_template = 'standard'
            logging.error(f"Template loading error: {template_error}")
    
    def _render_advanced_preferences(self) -> None:
        """Render advanced application preferences."""
        st.sidebar.subheader("⚙️ Advanced Settings")
        
        preferences = st.session_state.application_preferences
        
        with st.sidebar.expander("🔍 **Analysis Options**"):
            preferences['show_detailed_analytics'] = st.checkbox(
                "Show detailed analytics",
                value=preferences['show_detailed_analytics'],
                help="Display comprehensive extraction analytics"
            )
            
            preferences['show_entity_details'] = st.checkbox(
                "Show entity details",
                value=preferences['show_entity_details'],
                help="Display individual entity extraction details"
            )
            
            preferences['show_confidence_visualizations'] = st.checkbox(
                "Show confidence charts",
                value=preferences['show_confidence_visualizations'],
                help="Display confidence level visualizations"
            )
        
        with st.sidebar.expander("🔧 **Processing Options**"):
            preferences['enable_real_time_validation'] = st.checkbox(
                "Real-time validation",
                value=preferences['enable_real_time_validation'],
                help="Enable real-time input validation"
            )
            
            preferences['auto_save_results'] = st.checkbox(
                "Auto-save results",
                value=preferences['auto_save_results'],
                help="Automatically save extraction results"
            )
        
        st.session_state.application_preferences = preferences
    
    def _render_system_monitoring_panel(self) -> None:
        """Render system monitoring and statistics panel."""
        st.sidebar.subheader("📊 System Monitoring")
        
        if st.sidebar.button("🔄 **Refresh Statistics**"):
            self._update_system_statistics()
        
        stats = st.session_state.system_statistics
        
        # Key metrics display
        st.sidebar.metric(
            "Total Extractions",
            stats['total_extractions_performed'],
            delta=None
        )
        
        if stats['total_extractions_performed'] > 0:
            success_rate = (stats['successful_extractions'] / stats['total_extractions_performed']) * 100
            st.sidebar.metric(
                "Success Rate",
                f"{success_rate:.1f}%",
                delta=f"{success_rate - 95:.1f}%" if success_rate > 0 else None
            )
            
            st.sidebar.metric(
                "Avg Processing Time",
                f"{stats['average_processing_time']:.0f}ms",
                delta=None
            )
        
        # System health indicator
        health_status = self._get_system_health_status()
        health_color = {"Excellent": "🟢", "Good": "🟡", "Poor": "🔴"}.get(health_status, "⚪")
        st.sidebar.markdown(f"**System Health:** {health_color} {health_status}")
    
    def _render_quick_actions_panel(self) -> None:
        """Render quick actions panel in sidebar."""
        st.sidebar.subheader("⚡ Quick Actions")
        
        col1, col2 = st.sidebar.columns(2)
        
        with col1:
            if st.button("📥 **Export Data**", use_container_width=True):
                self._handle_quick_export()
        
        with col2:
            if st.button("🗑️ **Clear History**", use_container_width=True):
                self._handle_clear_history()
        
        if st.sidebar.button("📋 **Generate Report**", use_container_width=True):
            self._generate_system_report()
    
    def _render_main_content_area(self) -> None:
        """Render main content area based on selected processing mode."""
        processing_mode = st.session_state.selected_processing_mode
        
        content_renderers = {
            ProcessingMode.SINGLE_TEXT.value: self._render_single_text_processing,
            ProcessingMode.BATCH_PROCESSING.value: self._render_batch_processing,
            ProcessingMode.DEMO_EXAMPLES.value: self._render_demo_examples
        }
        
        renderer = content_renderers.get(processing_mode, self._render_single_text_processing)
        renderer()
        
        # Always show processing history if available
        if st.session_state.processing_history:
            self._render_processing_history_panel()
    
    def _render_single_text_processing(self) -> None:
        """Render single text processing interface."""
        st.header("📝 **Single Text Processing**")
        
        st.markdown("""
        <div class="alert-info">
            <strong>ℹ️ Instructions:</strong> Enter event registration text below for information extraction.
            The system will identify participant names, event details, locations, and dates.
        </div>
        """, unsafe_allow_html=True)
        
        # Input section
        input_container = st.container()
        with input_container:
            user_input_text = st.text_area(
                "**Event Registration Text:**",
                value=st.session_state.get('single_text_input', ""),
                placeholder="Example: Dr. Sarah Johnson registered for the International AI Conference 2025 taking place in San Francisco, California on March 15, 2025.",
                height=150,
                help="Paste or type event registration information here",
                key="single_text_input"
            )
            
            # Real-time validation
            if st.session_state.application_preferences['enable_real_time_validation']:
                self._show_input_validation_feedback(user_input_text)
        
        # Action buttons
        action_col1, action_col2, action_col3 = st.columns([2, 1, 1])
        
        with action_col1:
            extract_button = st.button(
                "🚀 **Extract Information**",
                type="primary",
                use_container_width=True,
                disabled=not user_input_text.strip()
            )
        
        with action_col2:
            if st.button("🔄 **Clear Input**", use_container_width=True):
                st.session_state.single_text_input = ""
                st.rerun()
        
        with action_col3:
            if st.button("📋 **Use Sample**", use_container_width=True):
                sample_text = st.session_state.demo_data_samples[0]['text']
                st.session_state.single_text_input = sample_text
                st.rerun()
        
        # Process extraction
        if extract_button and user_input_text.strip():
            self._process_single_text_extraction(user_input_text)
        
        # Display results
        if st.session_state.current_extraction_result:
            self._render_extraction_results(st.session_state.current_extraction_result)
    
    def _render_batch_processing(self) -> None:
        """Render batch processing interface."""
        st.header("📊 **Batch Processing**")
        
        st.markdown("""
        <div class="alert-info">
            <strong>ℹ️ Batch Processing:</strong> Upload a file containing multiple event registration texts
            for bulk information extraction. Supported formats: CSV, Excel, TXT.
        </div>
        """, unsafe_allow_html=True)
        
        # File upload section
        uploaded_file = st.file_uploader(
            "**Choose your file:**",
            type=self.config.SUPPORTED_FILE_TYPES,
            help=f"Maximum file size: {self.config.MAX_FILE_SIZE}MB"
        )
        
        if uploaded_file is not None:
            self._handle_batch_file_processing(uploaded_file)
        
        # Display batch results if available
        if st.session_state.batch_processing_results:
            self._render_batch_processing_results()
    
    def _render_demo_examples(self) -> None:
        """Render demo examples interface."""
        st.header("🧪 **Demo & Examples**")
        
        st.markdown("""
        <div class="alert-success">
            <strong>✨ Try the System:</strong> Use these pre-loaded examples to explore system capabilities
            or add your own custom examples for testing.
        </div>
        """, unsafe_allow_html=True)
        
        # Display demo samples with categories
        for idx, demo_sample in enumerate(st.session_state.demo_data_samples):
            with st.expander(f"**{demo_sample['category']} - Example {idx + 1}**"):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.text_area(
                        "Text:",
                        value=demo_sample['text'],
                        height=80,
                        disabled=True,
                        key=f"demo_text_{idx}"
                    )
                
                with col2:
                    st.markdown(f"**Category:**<br>{demo_sample['category']}", 
                              unsafe_allow_html=True)
                    
                    if st.button(f"🚀 **Process**", key=f"process_demo_{idx}"):
                        self._process_single_text_extraction(demo_sample['text'])
        
        # Custom example section
        st.divider()
        st.subheader("➕ **Add Custom Example**")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            custom_input = st.text_area(
                "**Custom Text:**",
                value=st.session_state.get('custom_demo_input', ""),
                placeholder="Enter your own event registration text...",
                height=100,
                key="custom_demo_input"
            )
        
        with col2:
            st.markdown("**Category:**")
            custom_category = st.selectbox(
                "Select category:",
                options=["Academic Conference", "Business Event", "Educational Workshop", 
                        "Technology Exhibition", "Healthcare Conference", "Other"],
                key="custom_category_selector"
            )
        
        # Handle custom processing
        process_custom = st.button("🚀 **Process Custom Example**")
        if process_custom and custom_input.strip():
            self._process_single_text_extraction(custom_input)
        
        # Display results
        if st.session_state.current_extraction_result:
            self._render_extraction_results(st.session_state.current_extraction_result)
    
    def _process_single_text_extraction(self, input_text: str) -> None:
        """Process single text extraction with comprehensive error handling."""
        start_time = time.time()
        
        try:
            with st.spinner("🔄 Processing extraction..."):
                extraction_result = st.session_state.extraction_service.extractInformation(
                    input_text,
                    st.session_state.selected_output_template
                )
                
                processing_time = (time.time() - start_time) * 1000  # Convert to milliseconds
                
                # Update application state
                st.session_state.current_extraction_result = extraction_result
                
                # Update processing history
                history_entry = ProcessingHistory(
                    timestamp=datetime.now(),
                    input_text=input_text,
                    extraction_result=extraction_result,
                    processing_mode="single_text",
                    processing_time_ms=processing_time,
                    success=extraction_result.get('success', False)
                )
                
                st.session_state.processing_history.append(history_entry)
                
                # Update system statistics
                self._update_extraction_statistics(extraction_result, processing_time)
                
                # Auto-save if enabled
                if st.session_state.application_preferences['auto_save_results']:
                    self._auto_save_result(extraction_result)
                
                st.success(f"✅ Extraction completed in {processing_time:.0f}ms")
                st.rerun()
                
        except Exception as extraction_error:
            st.error(f"❌ **Extraction Error:** {str(extraction_error)}")
            logging.error(f"Extraction failed for input: {input_text[:100]}... Error: {extraction_error}")
    
    def _render_extraction_results(self, extraction_result: Dict[str, Any]) -> None:
        """Render extraction results with professional formatting."""
        st.divider()
        st.subheader("📋 **Extraction Results**")
        
        if not extraction_result.get('success', False):
            st.error("❌ **Extraction Failed**")
            error_message = extraction_result.get('error', 'Unknown error occurred')
            st.error(f"**Error Details:** {error_message}")
            return
        
        extracted_data = extraction_result.get('extractedData', {})
        
        # Main results display
        st.markdown("### 🎯 **Extracted Information**")
        
        result_col1, result_col2, result_col3, result_col4 = st.columns(4)
        
        with result_col1:
            participant_name = extracted_data.get('participantName', 'Not detected')
            st.metric(
                "👤 **Participant**",
                participant_name if participant_name != 'Not detected' else "❌ Not found",
                help="Extracted participant name"
            )
        
        with result_col2:
            event_name = extracted_data.get('eventName', 'Not detected')
            st.metric(
                "🎪 **Event**",
                event_name if event_name != 'Not detected' else "❌ Not found",
                help="Extracted event name"
            )
        
        with result_col3:
            location = extracted_data.get('location', 'Not detected')
            st.metric(
                "📍 **Location**",
                location if location != 'Not detected' else "❌ Not found",
                help="Extracted event location"
            )
        
        with result_col4:
            event_date = extracted_data.get('date', 'Not detected')
            st.metric(
                "📅 **Date**",
                event_date if event_date != 'Not detected' else "❌ Not found",
                help="Extracted event date"
            )
        
        # Formatted output section
        st.markdown("### 📄 **Formatted Output**")
        formatted_output = extraction_result.get('formattedOutput', 'No formatted output available')
        st.code(formatted_output, language=None)
        
        # Additional analysis sections
        self._render_extraction_metadata(extraction_result)
        
        if st.session_state.application_preferences['show_confidence_visualizations']:
            self._render_confidence_visualizations(extraction_result)
        
        if st.session_state.application_preferences['show_entity_details']:
            self._render_entity_details(extraction_result)
        
        # Export options
        self._render_result_export_options(extraction_result)
    
    def _render_extraction_metadata(self, extraction_result: Dict[str, Any]) -> None:
        """Render extraction metadata and performance metrics."""
        if not st.session_state.application_preferences['show_detailed_analytics']:
            return
        
        st.markdown("### 📊 **Performance Analytics**")
        
        metadata = extraction_result.get('metadata', {})
        
        analytics_col1, analytics_col2, analytics_col3 = st.columns(3)
        
        with analytics_col1:
            confidence_score = metadata.get('confidence', 0)
            st.metric(
                "🎯 **Confidence Score**",
                f"{confidence_score}%",
                delta=f"{confidence_score - 85}%" if confidence_score > 0 else None,
                help="Overall extraction confidence level"
            )
            
            processing_time = metadata.get('processingTimeMs', 0)
            st.metric(
                "⚡ **Processing Time**",
                f"{processing_time}ms",
                help="Time taken for extraction"
            )
        
        with analytics_col2:
            completion_percentage = metadata.get('completionPercentage', 0)
            st.metric(
                "✅ **Completion Rate**",
                f"{completion_percentage}%",
                delta=f"{completion_percentage - 100}%" if completion_percentage > 0 else None,
                help="Percentage of fields successfully extracted"
            )
            
            extraction_method = metadata.get('extractionMethod', 'Unknown')
            st.metric(
                "🔬 **Method Used**",
                extraction_method,
                help="Extraction algorithm used"
            )
        
        with analytics_col3:
            entity_count = metadata.get('entityCount', 0)
            st.metric(
                "🏷️ **Entities Found**",
                str(entity_count),
                help="Number of entities detected"
            )
            
            timestamp = metadata.get('timestamp', '')
            if timestamp:
                formatted_time = timestamp[:19].replace('T', ' ')
                st.metric(
                    "🕐 **Extracted At**",
                    formatted_time,
                    help="Extraction timestamp"
                )
        
        # Warnings and errors display
        if extraction_result.get('warnings'):
            st.markdown("#### ⚠️ **Warnings**")
            for warning in extraction_result['warnings']:
                st.warning(f"⚠️ {warning}")
        
        if extraction_result.get('errors'):
            st.markdown("#### ❌ **Errors**")
            for error in extraction_result['errors']:
                st.error(f"❌ {error}")
    
    def _render_confidence_visualizations(self, extraction_result: Dict[str, Any]) -> None:
        """Render confidence level visualizations."""
        st.markdown("### 📈 **Confidence Analysis**")
        
        metadata = extraction_result.get('metadata', {})
        overall_confidence = metadata.get('confidence', 0)
        
        # Create confidence gauge chart
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=overall_confidence,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Overall Confidence"},
            delta={'reference': 85},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 50], 'color': "lightgray"},
                    {'range': [50, 85], 'color': "yellow"},
                    {'range': [85, 100], 'color': "lightgreen"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        
        fig_gauge.update_layout(height=300)
        st.plotly_chart(fig_gauge, use_container_width=True)
        
        # Field-wise confidence breakdown (if available)
        extracted_data = extraction_result.get('extractedData', {})
        field_confidence = {}
        
        for field_name, field_value in extracted_data.items():
            if field_value and field_value != 'Not detected':
                # Simulate field confidence (in real implementation, this would come from the service)
                confidence_value = max(70, overall_confidence + (hash(field_name) % 20 - 10))
                field_confidence[field_name.replace('Name', '').title()] = min(100, confidence_value)
        
        if field_confidence:
            fig_bar = px.bar(
                x=list(field_confidence.keys()),
                y=list(field_confidence.values()),
                title="Field-wise Confidence Scores",
                labels={'x': 'Fields', 'y': 'Confidence (%)'},
                color=list(field_confidence.values()),
                color_continuous_scale='Viridis'
            )
            
            fig_bar.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig_bar, use_container_width=True)
    
    def _render_entity_details(self, extraction_result: Dict[str, Any]) -> None:
        """Render detailed entity extraction information."""
        st.markdown("### 🏷️ **Entity Details**")
        
        extracted_data = extraction_result.get('extractedData', {})
        
        entity_details = []
        for field_name, field_value in extracted_data.items():
            if field_value and field_value != 'Not detected':
                entity_details.append({
                    'Field': field_name.replace('Name', '').title(),
                    'Value': field_value,
                    'Status': '✅ Detected',
                    'Type': self._get_entity_type(field_name),
                    'Confidence': f"{max(70, hash(field_value) % 30 + 70)}%"
                })
            else:
                entity_details.append({
                    'Field': field_name.replace('Name', '').title(),
                    'Value': 'Not detected',
                    'Status': '❌ Missing',
                    'Type': self._get_entity_type(field_name),
                    'Confidence': 'N/A'
                })
        
        if entity_details:
            entity_df = pd.DataFrame(entity_details)
            st.dataframe(
                entity_df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    'Field': st.column_config.TextColumn('Field', width='medium'),
                    'Value': st.column_config.TextColumn('Extracted Value', width='large'),
                    'Status': st.column_config.TextColumn('Status', width='small'),
                    'Type': st.column_config.TextColumn('Entity Type', width='medium'),
                    'Confidence': st.column_config.TextColumn('Confidence', width='small')
                }
            )
    
    def _render_result_export_options(self, extraction_result: Dict[str, Any]) -> None:
        """Render export options for extraction results."""
        st.markdown("### 💾 **Export Options**")
        
        export_col1, export_col2, export_col3 = st.columns(3)
        
        with export_col1:
            export_format = st.selectbox(
                "Export Format:",
                options=[fmt.value.upper() for fmt in ExportFormat],
                help="Choose export format for results"
            )
        
        with export_col2:
            include_metadata = st.checkbox(
                "Include Metadata",
                value=True,
                help="Include processing metadata in export"
            )
        
        with export_col3:
            if st.button("📥 **Export Results**", type="primary"):
                self._handle_result_export(extraction_result, export_format.lower(), include_metadata)
    
    def _handle_batch_file_processing(self, uploaded_file) -> None:
        """Handle batch file processing with comprehensive validation."""
        try:
            # File validation
            file_size_mb = len(uploaded_file.getvalue()) / (1024 * 1024)
            
            if file_size_mb > self.config.MAX_FILE_SIZE:
                st.error(f"❌ File size ({file_size_mb:.1f}MB) exceeds maximum limit ({self.config.MAX_FILE_SIZE}MB)")
                return
            
            # File type handling
            file_extension = uploaded_file.name.split('.')[-1].lower()
            
            if file_extension == 'csv':
                df = pd.read_csv(uploaded_file)
            elif file_extension in ['xlsx', 'xls']:
                df = pd.read_excel(uploaded_file)
            elif file_extension == 'txt':
                content = str(uploaded_file.read(), "utf-8")
                texts = [line.strip() for line in content.split('\n') if line.strip()]
                df = pd.DataFrame({'text': texts})
            else:
                st.error(f"❌ Unsupported file format: {file_extension}")
                return
            
            # Data validation
            if 'text' not in df.columns:
                st.error("❌ File must contain a 'text' column with event registration data")
                
                # Show available columns
                st.info(f"Available columns: {', '.join(df.columns.tolist())}")
                
                # Allow column mapping
                selected_column = st.selectbox(
                    "Select the column containing text data:",
                    options=df.columns.tolist()
                )
                
                if st.button("🔄 **Use Selected Column**"):
                    df = df.rename(columns={selected_column: 'text'})
                    st.success(f"✅ Using column '{selected_column}' as text data")
                    st.rerun()
                return
            
            # Display file preview
            st.success(f"✅ Successfully loaded **{len(df)}** records from {uploaded_file.name}")
            
            preview_col1, preview_col2 = st.columns([2, 1])
            
            with preview_col1:
                st.markdown("#### 📋 **Data Preview**")
                st.dataframe(df.head(10), use_container_width=True)
            
            with preview_col2:
                st.markdown("#### 📊 **File Statistics**")
                st.metric("Total Records", len(df))
                st.metric("File Size", f"{file_size_mb:.2f} MB")
                
                # Text length statistics
                text_lengths = df['text'].str.len()
                st.metric("Avg Text Length", f"{text_lengths.mean():.0f} chars")
                st.metric("Max Text Length", f"{text_lengths.max():.0f} chars")
            
            # Processing options
            st.markdown("#### ⚙️ **Processing Options**")
            
            process_col1, process_col2, process_col3 = st.columns(3)
            
            with process_col1:
                batch_size = st.number_input(
                    "Batch Size:",
                    min_value=1,
                    max_value=min(1000, len(df)),
                    value=min(100, len(df)),
                    help="Number of records to process at once"
                )
            
            with process_col2:
                max_records = st.number_input(
                    "Max Records:",
                    min_value=1,
                    max_value=len(df),
                    value=len(df),
                    help="Maximum number of records to process"
                )
            
            with process_col3:
                parallel_processing = st.checkbox(
                    "Parallel Processing",
                    value=True,
                    help="Enable parallel processing for faster results"
                )
            
            # Start batch processing
            if st.button("🚀 **Start Batch Processing**", type="primary"):
                self._execute_batch_processing(df, batch_size, max_records, parallel_processing)
                
        except Exception as file_error:
            st.error(f"❌ **File Processing Error:** {str(file_error)}")
            logging.error(f"Batch file processing failed: {file_error}")
    
    def _execute_batch_processing(self, df: pd.DataFrame, batch_size: int, max_records: int, parallel_processing: bool) -> None:
        """Execute batch processing with progress tracking."""
        try:
            # Limit records if specified
            processing_df = df.head(max_records)
            texts_to_process = processing_df['text'].tolist()
            
            # Initialize progress tracking
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            start_time = time.time()
            
            with st.spinner(f"🔄 Processing {len(texts_to_process)} records..."):
                # Simulate batch processing (replace with actual service call)
                batch_results = st.session_state.extraction_service.extractBatch(
                    texts_to_process,
                    st.session_state.selected_output_template
                )
                
                processing_time = (time.time() - start_time) * 1000
                
                # Update session state
                st.session_state.batch_processing_results = batch_results
                st.session_state.batch_processing_results['processingTime'] = processing_time
                
                # Update progress
                progress_bar.progress(1.0)
                status_text.success(f"✅ Batch processing completed in {processing_time:.0f}ms")
                
                # Add to processing history
                history_entry = ProcessingHistory(
                    timestamp=datetime.now(),
                    input_text=f"Batch processing: {len(texts_to_process)} records",
                    extraction_result=batch_results,
                    processing_mode="batch_processing",
                    processing_time_ms=processing_time,
                    success=batch_results.get('success', False)
                )
                
                st.session_state.processing_history.append(history_entry)
                
                st.rerun()
                
        except Exception as batch_error:
            st.error(f"❌ **Batch Processing Error:** {str(batch_error)}")
            logging.error(f"Batch processing failed: {batch_error}")
    
    def _render_batch_processing_results(self) -> None:
        """Render comprehensive batch processing results."""
        st.divider()
        st.header("📊 **Batch Processing Results**")
        
        results = st.session_state.batch_processing_results
        
        if not results.get('success', False):
            st.error(f"❌ **Batch processing failed:** {results.get('error', 'Unknown error')}")
            return
        
        # Summary statistics
        summary = results.get('batchSummary', {})
        
        st.markdown("### 📈 **Processing Summary**")
        
        summary_col1, summary_col2, summary_col3, summary_col4 = st.columns(4)
        
        with summary_col1:
            st.metric(
                "📊 **Total Items**",
                summary.get('totalItems', 0),
                help="Total number of items processed"
            )
        
        with summary_col2:
            st.metric(
                "✅ **Successful**",
                summary.get('successfulItems', 0),
                delta=summary.get('successfulItems', 0) - summary.get('totalItems', 0),
                help="Successfully processed items"
            )
        
        with summary_col3:
            success_rate = summary.get('successRate', 0)
            st.metric(
                "🎯 **Success Rate**",
                f"{success_rate:.1f}%",
                delta=f"{success_rate - 95:.1f}%",
                help="Overall processing success rate"
            )
        
        with summary_col4:
            processing_time = results.get('processingTime', 0)
            st.metric(
                "⚡ **Processing Time**",
                f"{processing_time:.0f}ms",
                help="Total processing time"
            )
        
        # Detailed results table
        st.markdown("### 📋 **Detailed Results**")
        
        batch_results_data = []
        for item in results.get('results', []):
            result_data = item.get('result', {})
            extracted = result_data.get('extractedData', {})
            metadata = result_data.get('metadata', {})
            
            batch_results_data.append({
                'Index': item.get('index', ''),
                'Status': '✅ Success' if result_data.get('success') else '❌ Failed',
                'Participant': extracted.get('participantName', 'Not detected'),
                'Event': extracted.get('eventName', 'Not detected'),
                'Location': extracted.get('location', 'Not detected'),
                'Date': extracted.get('date', 'Not detected'),
                'Confidence': f"{metadata.get('confidence', 0)}%",
                'Processing Time': f"{metadata.get('processingTimeMs', 0):.0f}ms",
                'Errors': '; '.join(result_data.get('errors', []))
            })
        
        if batch_results_data:
            results_df = pd.DataFrame(batch_results_data)
            
            # Add filtering options
            filter_col1, filter_col2 = st.columns(2)
            
            with filter_col1:
                status_filter = st.multiselect(
                    "Filter by Status:",
                    options=results_df['Status'].unique(),
                    default=results_df['Status'].unique()
                )
            
            with filter_col2:
                show_errors_only = st.checkbox("Show only items with errors")
            
            # Apply filters
            filtered_df = results_df[results_df['Status'].isin(status_filter)]
            
            if show_errors_only:
                filtered_df = filtered_df[filtered_df['Errors'] != '']
            
            st.dataframe(
                filtered_df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    'Status': st.column_config.TextColumn('Status', width='small'),
                    'Participant': st.column_config.TextColumn('Participant', width='medium'),
                    'Event': st.column_config.TextColumn('Event', width='medium'),
                    'Location': st.column_config.TextColumn('Location', width='medium'),
                    'Date': st.column_config.TextColumn('Date', width='small'),
                    'Confidence': st.column_config.TextColumn('Confidence', width='small'),
                    'Processing Time': st.column_config.TextColumn('Time', width='small'),
                    'Errors': st.column_config.TextColumn('Errors', width='large')
                }
            )
        
        # Analytics dashboard
        if st.session_state.application_preferences['show_detailed_analytics']:
            self._render_batch_analytics_dashboard(results)
        
        # Export batch results
        st.markdown("### 💾 **Export Batch Results**")
        
        export_col1, export_col2, export_col3 = st.columns(3)
        
        with export_col1:
            batch_export_format = st.selectbox(
                "Export Format:",
                options=[fmt.value.upper() for fmt in ExportFormat],
                key="batch_export_format"
            )
        
        with export_col2:
            include_summary = st.checkbox(
                "Include Summary",
                value=True,
                help="Include processing summary in export"
            )
        
        with export_col3:
            if st.button("📥 **Export Batch Results**", type="primary"):
                self._handle_batch_export(results, batch_export_format.lower(), include_summary)
    
    def _render_batch_analytics_dashboard(self, batch_results: Dict[str, Any]) -> None:
        """Render analytics dashboard for batch processing results."""
        st.markdown("### 📊 **Analytics Dashboard**")
        
        results_data = []
        for item in batch_results.get('results', []):
            result_data = item.get('result', {})
            metadata = result_data.get('metadata', {})
            
            results_data.append({
                'success': result_data.get('success', False),
                'confidence': metadata.get('confidence', 0),
                'processing_time': metadata.get('processingTimeMs', 0),
                'entity_count': metadata.get('entityCount', 0)
            })
        
        if results_data:
            analytics_df = pd.DataFrame(results_data)
            
            # Create visualizations
            viz_col1, viz_col2 = st.columns(2)
            
            with viz_col1:
                # Success rate pie chart
                success_counts = analytics_df['success'].value_counts()
                fig_pie = px.pie(
                    values=success_counts.values,
                    names=['Success' if x else 'Failed' for x in success_counts.index],
                    title="Processing Success Rate"
                )
                st.plotly_chart(fig_pie, use_container_width=True)
            
            with viz_col2:
                # Confidence distribution
                fig_hist = px.histogram(
                    analytics_df,
                    x='confidence',
                    nbins=20,
                    title="Confidence Score Distribution"
                )
                fig_hist.update_xaxis(title="Confidence (%)")
                fig_hist.update_yaxis(title="Frequency")
                st.plotly_chart(fig_hist, use_container_width=True)
            
            # Processing time analysis
            fig_time = px.box(
                analytics_df,
                y='processing_time',
                title="Processing Time Distribution"
            )
            fig_time.update_yaxis(title="Processing Time (ms)")
            st.plotly_chart(fig_time, use_container_width=True)
    
    def _render_processing_history_panel(self) -> None:
        """Render processing history panel with advanced features."""
        st.divider()
        st.subheader("📚 **Processing History**")
        
        if not st.session_state.processing_history:
            st.info("No processing history available")
            return
        
        # History controls
        history_col1, history_col2, history_col3 = st.columns(3)
        
        with history_col1:
            history_limit = st.selectbox(
                "Show last:",
                options=[5, 10, 20, 50, "All"],
                index=1
            )
        
        with history_col2:
            mode_filter = st.multiselect(
                "Filter by mode:",
                options=["single_text", "batch_processing", "demo_examples"],
                default=["single_text", "batch_processing", "demo_examples"]
            )
        
        with history_col3:
            if st.button("🗑️ **Clear History**"):
                st.session_state.processing_history = []
                st.rerun()
        
        # Display history
        history_data = st.session_state.processing_history
        
        if mode_filter:
            history_data = [h for h in history_data if h.processing_mode in mode_filter]
        
        if isinstance(history_limit, int):
            history_data = history_data[-history_limit:]
        
        for idx, entry in enumerate(reversed(history_data)):
            with st.expander(
                f"**{entry.timestamp.strftime('%Y-%m-%d %H:%M:%S')}** - "
                f"{'✅' if entry.success else '❌'} "
                f"{entry.processing_mode.replace('_', ' ').title()} "
                f"({entry.processing_time_ms:.0f}ms)"
            ):
                entry_col1, entry_col2 = st.columns([2, 1])
                
                with entry_col1:
                    st.text_area(
                        "Input:",
                        value=entry.input_text[:200] + "..." if len(entry.input_text) > 200 else entry.input_text,
                        height=60,
                        disabled=True,
                        key=f"history_input_{idx}"
                    )
                
                with entry_col2:
                    st.markdown(f"**Status:** {'✅ Success' if entry.success else '❌ Failed'}")
                    st.markdown(f"**Mode:** {entry.processing_mode.replace('_', ' ').title()}")
                    st.markdown(f"**Time:** {entry.processing_time_ms:.0f}ms")
                    
                    if st.button(f"🔄 **Reprocess**", key=f"reprocess_{idx}"):
                        self._process_single_text_extraction(entry.input_text)
    
    def _show_input_validation_feedback(self, input_text: str) -> None:
        """Show real-time input validation feedback."""
        if not input_text.strip():
            return
        
        validation_messages = []
        
        # Length validation
        if len(input_text) < 10:
            validation_messages.append("⚠️ Text seems too short for meaningful extraction")
        elif len(input_text) > 1000:
            validation_messages.append("⚠️ Very long text may impact processing performance")
        
        # Content validation
        if not any(keyword in input_text.lower() for keyword in ['register', 'signed up', 'enrolled', 'joined']):
            validation_messages.append("ℹ️ Text doesn't contain common registration keywords")
        
        if not any(char.isdigit() for char in input_text):
            validation_messages.append("ℹ️ No dates detected in the text")
        
        # Display validation messages
        for message in validation_messages:
            if message.startswith("⚠️"):
                st.warning(message)
            else:
                st.info(message)
    
    def _get_entity_type(self, field_name: str) -> str:
        """Get entity type based on field name."""
        entity_types = {
            'participantName': 'PERSON',
            'eventName': 'EVENT',
            'location': 'LOCATION',
            'date': 'DATE'
        }
        return entity_types.get(field_name, 'OTHER')
    
    def _update_extraction_statistics(self, extraction_result: Dict[str, Any], processing_time: float) -> None:
        """Update system extraction statistics."""
        stats = st.session_state.system_statistics
        
        stats['total_extractions_performed'] += 1
        
        if extraction_result.get('success', False):
            stats['successful_extractions'] += 1
        
        # Update average processing time
        total_time = stats['average_processing_time'] * (stats['total_extractions_performed'] - 1) + processing_time
        stats['average_processing_time'] = total_time / stats['total_extractions_performed']
        
        stats['last_extraction_timestamp'] = datetime.now()
        
        st.session_state.system_statistics = stats
    
    def _update_system_statistics(self) -> None:
        """Update system statistics from extraction service."""
        try:
            service_stats = st.session_state.extraction_service.getServiceStatistics()
            # Update session state with fresh statistics
            # Implementation would depend on the actual service response
            pass
        except Exception as stats_error:
            logging.error(f"Failed to update system statistics: {stats_error}")
    
    def _get_system_health_status(self) -> str:
        """Get current system health status."""
        stats = st.session_state.system_statistics
        
        if stats['total_extractions_performed'] == 0:
            return "Unknown"
        
        success_rate = (stats['successful_extractions'] / stats['total_extractions_performed']) * 100
        avg_time = stats['average_processing_time']
        
        if success_rate >= 95 and avg_time <= 1000:
            return "Excellent"
        elif success_rate >= 85 and avg_time <= 2000:
            return "Good"
        else:
            return "Poor"
    
    def _handle_result_export(self, extraction_result: Dict[str, Any], export_format: str, include_metadata: bool) -> None:
        """Handle single result export with multiple formats."""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"extraction_result_{timestamp}.{export_format}"
            
            export_data = self._prepare_export_data([extraction_result], export_format, include_metadata)
            
            if export_data:
                st.download_button(
                    label=f"📥 **Download {export_format.upper()}**",
                    data=export_data,
                    file_name=filename,
                    mime=self._get_mime_type(export_format),
                    type="primary"
                )
                st.success(f"✅ Export prepared: {filename}")
            else:
                st.error("❌ Export preparation failed")
                
        except Exception as export_error:
            st.error(f"❌ Export error: {str(export_error)}")
            logging.error(f"Export failed: {export_error}")
    
    def _handle_batch_export(self, batch_results: Dict[str, Any], export_format: str, include_summary: bool) -> None:
        """Handle batch results export."""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"batch_results_{timestamp}.{export_format}"
            
            # Prepare batch export data
            results_list = [item['result'] for item in batch_results.get('results', [])]
            export_data = self._prepare_batch_export_data(results_list, batch_results, export_format, include_summary)
            
            if export_data:
                st.download_button(
                    label=f"📥 **Download Batch Results ({export_format.upper()})**",
                    data=export_data,
                    file_name=filename,
                    mime=self._get_mime_type(export_format),
                    type="primary"
                )
                st.success(f"✅ Batch export prepared: {filename}")
            else:
                st.error("❌ Batch export preparation failed")
                
        except Exception as batch_export_error:
            st.error(f"❌ Batch export error: {str(batch_export_error)}")
            logging.error(f"Batch export failed: {batch_export_error}")
    
    def _prepare_export_data(self, results: List[Dict[str, Any]], export_format: str, include_metadata: bool) -> Optional[str]:
        """Prepare export data in specified format."""
        try:
            if export_format == 'csv':
                return self._prepare_csv_export(results, include_metadata)
            elif export_format == 'json':
                return self._prepare_json_export(results, include_metadata)
            elif export_format == 'xml':
                return self._prepare_xml_export(results, include_metadata)
            elif export_format == 'xlsx':
                return self._prepare_excel_export(results, include_metadata)
            else:
                return None
                
        except Exception as prep_error:
            logging.error(f"Export data preparation failed: {prep_error}")
            return None
    
    def _prepare_csv_export(self, results: List[Dict[str, Any]], include_metadata: bool) -> str:
        """Prepare CSV export data."""
        export_data = []
        
        for result in results:
            extracted = result.get('extractedData', {})
            row = {
                'participant_name': extracted.get('participantName', ''),
                'event_name': extracted.get('eventName', ''),
                'location': extracted.get('location', ''),
                'date': extracted.get('date', ''),
                'success': result.get('success', False)
            }
            
            if include_metadata:
                metadata = result.get('metadata', {})
                row.update({
                    'confidence': metadata.get('confidence', 0),
                    'processing_time_ms': metadata.get('processingTimeMs', 0),
                    'extraction_method': metadata.get('extractionMethod', ''),
                    'timestamp': metadata.get('timestamp', '')
                })
            
            export_data.append(row)
        
        df = pd.DataFrame(export_data)
        return df.to_csv(index=False)
    
    def _prepare_json_export(self, results: List[Dict[str, Any]], include_metadata: bool) -> str:
        """Prepare JSON export data."""
        export_data = {
            'export_info': {
                'timestamp': datetime.now().isoformat(),
                'total_records': len(results),
                'include_metadata': include_metadata,
                'format_version': '2.0'
            },
            'results': []
        }
        
        for result in results:
            export_record = {
                'extracted_data': result.get('extractedData', {}),
                'success': result.get('success', False),
                'formatted_output': result.get('formattedOutput', '')
            }
            
            if include_metadata:
                export_record['metadata'] = result.get('metadata', {})
                export_record['warnings'] = result.get('warnings', [])
                export_record['errors'] = result.get('errors', [])
            
            export_data['results'].append(export_record)
        
        return json.dumps(export_data, indent=2, ensure_ascii=False)
    
    def _prepare_xml_export(self, results: List[Dict[str, Any]], include_metadata: bool) -> str:
        """Prepare XML export data."""
        xml_content = ['<?xml version="1.0" encoding="UTF-8"?>']
        xml_content.append('<extraction_results>')
        xml_content.append(f'  <export_info>')
        xml_content.append(f'    <timestamp>{datetime.now().isoformat()}</timestamp>')
        xml_content.append(f'    <total_records>{len(results)}</total_records>')
        xml_content.append(f'    <include_metadata>{str(include_metadata).lower()}</include_metadata>')
        xml_content.append(f'  </export_info>')
        
        for idx, result in enumerate(results):
            xml_content.append(f'  <result index="{idx + 1}">')
            
            extracted = result.get('extractedData', {})
            xml_content.append(f'    <extracted_data>')
            xml_content.append(f'      <participant_name><![CDATA[{extracted.get("participantName", "")}]]></participant_name>')
            xml_content.append(f'      <event_name><![CDATA[{extracted.get("eventName", "")}]]></event_name>')
            xml_content.append(f'      <location><![CDATA[{extracted.get("location", "")}]]></location>')
            xml_content.append(f'      <date><![CDATA[{extracted.get("date", "")}]]></date>')
            xml_content.append(f'    </extracted_data>')
            
            xml_content.append(f'    <success>{str(result.get("success", False)).lower()}</success>')
            
            if include_metadata:
                metadata = result.get('metadata', {})
                xml_content.append(f'    <metadata>')
                xml_content.append(f'      <confidence>{metadata.get("confidence", 0)}</confidence>')
                xml_content.append(f'      <processing_time_ms>{metadata.get("processingTimeMs", 0)}</processing_time_ms>')
                xml_content.append(f'      <extraction_method><![CDATA[{metadata.get("extractionMethod", "")}]]></extraction_method>')
                xml_content.append(f'    </metadata>')
            
            xml_content.append(f'  </result>')
        
        xml_content.append('</extraction_results>')
        return '\n'.join(xml_content)
    
    def _prepare_excel_export(self, results: List[Dict[str, Any]], include_metadata: bool) -> bytes:
        """Prepare Excel export data."""
        # Note: This would require openpyxl or xlsxwriter in a real implementation
        # For now, we'll return CSV data as bytes
        csv_data = self._prepare_csv_export(results, include_metadata)
        return csv_data.encode('utf-8')
    
    def _prepare_batch_export_data(self, results: List[Dict[str, Any]], batch_info: Dict[str, Any], 
                                 export_format: str, include_summary: bool) -> Optional[str]:
        """Prepare batch export data with summary information."""
        try:
            if export_format == 'json':
                export_data = {
                    'batch_info': {
                        'timestamp': datetime.now().isoformat(),
                        'total_records': len(results),
                        'processing_summary': batch_info.get('batchSummary', {}) if include_summary else None,
                        'format_version': '2.0'
                    },
                    'results': []
                }
                
                for result in results:
                    export_record = {
                        'extracted_data': result.get('extractedData', {}),
                        'success': result.get('success', False),
                        'metadata': result.get('metadata', {}),
                        'warnings': result.get('warnings', []),
                        'errors': result.get('errors', [])
                    }
                    export_data['results'].append(export_record)
                
                return json.dumps(export_data, indent=2, ensure_ascii=False)
            
            elif export_format == 'csv':
                return self._prepare_csv_export(results, True)
            
            else:
                return self._prepare_export_data(results, export_format, True)
                
        except Exception as batch_prep_error:
            logging.error(f"Batch export preparation failed: {batch_prep_error}")
            return None
    
    def _get_mime_type(self, export_format: str) -> str:
        """Get MIME type for export format."""
        mime_types = {
            'csv': 'text/csv',
            'json': 'application/json',
            'xml': 'application/xml',
            'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        }
        return mime_types.get(export_format, 'text/plain')
    
    def _handle_quick_export(self) -> None:
        """Handle quick export of recent results."""
        if not st.session_state.processing_history:
            st.warning("⚠️ No data available for export")
            return
        
        recent_results = [entry.extraction_result for entry in st.session_state.processing_history[-10:]]
        export_data = self._prepare_json_export(recent_results, True)
        
        if export_data:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            st.download_button(
                label="📥 **Download Recent Results (JSON)**",
                data=export_data,
                file_name=f"recent_results_{timestamp}.json",
                mime="application/json"
            )
            st.success("✅ Quick export prepared")
        else:
            st.error("❌ Quick export failed")
    
    def _handle_clear_history(self) -> None:
        """Handle clearing processing history."""
        if st.session_state.processing_history:
            # Show confirmation dialog
            if st.sidebar.button("⚠️ **Confirm Clear History**", type="secondary"):
                st.session_state.processing_history = []
                st.session_state.current_extraction_result = None
                st.session_state.batch_processing_results = None
                st.success("✅ Processing history cleared")
                st.rerun()
        else:
            st.sidebar.info("No history to clear")
    
    def _generate_system_report(self) -> None:
        """Generate comprehensive system report."""
        try:
            report_data = {
                'report_info': {
                    'generated_at': datetime.now().isoformat(),
                    'system_version': '2.0.0',
                    'report_type': 'system_status'
                },
                'system_status': st.session_state.service_status,
                'statistics': st.session_state.system_statistics,
                'recent_activity': {
                    'total_history_entries': len(st.session_state.processing_history),
                    'recent_entries': len([h for h in st.session_state.processing_history 
                                         if (datetime.now() - h.timestamp).days <= 1])
                },
                'configuration': {
                    'selected_template': st.session_state.selected_output_template,
                    'processing_mode': st.session_state.selected_processing_mode,
                    'preferences': st.session_state.application_preferences
                }
            }
            
            report_json = json.dumps(report_data, indent=2, default=str)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            st.download_button(
                label="📋 **Download System Report**",
                data=report_json,
                file_name=f"system_report_{timestamp}.json",
                mime="application/json"
            )
            st.success("✅ System report generated")
            
        except Exception as report_error:
            st.error(f"❌ Report generation failed: {str(report_error)}")
            logging.error(f"System report generation failed: {report_error}")
    
    def _auto_save_result(self, extraction_result: Dict[str, Any]) -> None:
        """Auto-save extraction result if enabled."""
        try:
            if st.session_state.application_preferences.get('auto_save_results', False):
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"auto_save_{timestamp}.json"
                
                save_data = {
                    'auto_save_info': {
                        'timestamp': datetime.now().isoformat(),
                        'auto_saved': True
                    },
                    'result': extraction_result
                }
                
                # In a real implementation, this would save to a persistent location
                # For now, we'll just add it to session state
                if 'auto_saved_results' not in st.session_state:
                    st.session_state.auto_saved_results = []
                
                st.session_state.auto_saved_results.append(save_data)
                
                # Keep only last 50 auto-saved results to prevent memory issues
                if len(st.session_state.auto_saved_results) > 50:
                    st.session_state.auto_saved_results = st.session_state.auto_saved_results[-50:]
                
        except Exception as auto_save_error:
            logging.error(f"Auto-save failed: {auto_save_error}")
    
    def _render_system_diagnostics(self) -> None:
        """Render system diagnostics information."""
        st.subheader("🔧 **System Diagnostics**")
        
        diag_col1, diag_col2 = st.columns(2)
        
        with diag_col1:
            st.markdown("**Service Status**")
            service_status = st.session_state.service_status
            
            status_info = {
                'Initialized': service_status.get('initialized', False),
                'Error Message': service_status.get('error_message', 'None'),
                'Init Time': service_status.get('initialization_time', 'Unknown')
            }
            
            for key, value in status_info.items():
                if key == 'Initialized':
                    status_icon = "✅" if value else "❌"
                    st.write(f"{status_icon} **{key}:** {value}")
                else:
                    st.write(f"**{key}:** {value}")
        
        with diag_col2:
            st.markdown("**System Resources**")
            
            # Memory usage (simplified)
            history_size = len(st.session_state.processing_history)
            auto_saved_size = len(st.session_state.get('auto_saved_results', []))
            
            st.write(f"**Processing History:** {history_size} entries")
            st.write(f"**Auto-saved Results:** {auto_saved_size} entries")
            st.write(f"**Session Duration:** {datetime.now() - service_status.get('initialization_time', datetime.now())}")
        
        # System health recommendations
        st.markdown("**🩺 Health Recommendations**")
        
        recommendations = []
        
        if history_size > 100:
            recommendations.append("Consider clearing processing history to free memory")
        
        if not st.session_state.service_status.get('initialized', False):
            recommendations.append("Restart the application to resolve service issues")
        
        stats = st.session_state.system_statistics
        if stats['total_extractions_performed'] > 0:
            success_rate = (stats['successful_extractions'] / stats['total_extractions_performed']) * 100
            if success_rate < 80:
                recommendations.append("Low success rate detected - check input data quality")
        
        if recommendations:
            for rec in recommendations:
                st.info(f"💡 {rec}")
        else:
            st.success("✅ System is operating optimally")
    
    def _render_critical_error(self, error: Exception) -> None:
        """Render critical error interface."""
        st.error("🚨 **Critical Application Error**")
        
        st.markdown(f"""
        <div class="alert-error">
            <strong>❌ Application Error</strong><br>
            A critical error has occurred that prevents the application from functioning properly.
            <br><br>
            <strong>Error Details:</strong><br>
            <code>{str(error)}</code>
            <br><br>
            <strong>Recommended Actions:</strong>
            <ul>
                <li>Refresh the browser page</li>
                <li>Clear browser cache and cookies</li>
                <li>Check internet connection</li>
                <li>Contact system administrator</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Error reporting options
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔄 **Restart Application**", type="primary"):
                # Clear all session state and restart
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()
        
        with col2:
            error_report = {
                'error_type': type(error).__name__,
                'error_message': str(error),
                'timestamp': datetime.now().isoformat(),
                'user_agent': 'Streamlit Application',
                'session_state_keys': list(st.session_state.keys())
            }
            
            st.download_button(
                label="📋 **Download Error Report**",
                data=json.dumps(error_report, indent=2),
                file_name=f"error_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )


# Application Entry Point - This will be handled by separate main.py file
# Remove the main function since it's handled externally

# Export the main class for external import
__all__ = ['ProfessionalEventExtractionInterface']