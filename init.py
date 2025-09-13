# src/__init__.py
"""
Event Registration Information Extraction System
Main package initialization
"""

__version__ = "1.0.0"
__author__ = "Event Extraction System Team"
__description__ = "Advanced NLP-powered event registration information extraction system"

# Import main components for easy access
from extraction_service import EventRegistrationExtractionService
from frontend import StreamlitEventExtractionInterface

__all__ = [
    'EventRegistrationExtractionService',
    'StreamlitEventExtractionInterface'
]

# src/models/__init__.py
"""
Data models and structures for the extraction system
"""

from data_model import (  # Changed from data_model to data_models
    EventRegistrationInfo,
    ExtractedEntity,
    ExtractionResult,
    ExtractionConfidence,
    EntityType,
    ProcessingMetrics
)

__all__ = [
    'EventRegistrationInfo',
    'ExtractedEntity', 
    'ExtractionResult',
    'ExtractionConfidence',
    'EntityType',
    'ProcessingMetrics'
]

# src/preprocessing/__init__.py
"""
Text preprocessing and normalization components
"""

from .text_process import AdvancedTextPreprocessor  # Changed from text_preprocessor

__all__ = ['AdvancedTextPreprocessor']

# src/extraction/__init__.py
"""
Named Entity Recognition and extraction components
"""

from .Name_Entity_Recogniztion import HybridNamedEntityExtractor  # Changed from ner_extractor

__all__ = ['HybridNamedEntityExtractor']

# src/processing/__init__.py
"""
Information processing and validation components
"""

from .info_processing import AdvancedInformationProcessor  # Changed from information_processor

__all__ = ['AdvancedInformationProcessor']

# src/output/__init__.py
"""
Template generation and output formatting components
"""

from .template_generation import EventRegistrationTemplateGenerator  # Changed from template_generator

__all__ = ['EventRegistrationTemplateGenerator']

# src/services/__init__.py
"""
Service layer and facade components
"""

from .extraction_service import EventRegistrationExtractionService

__all__ = ['EventRegistrationExtractionService']

# src/ui/__init__.py
"""
User interface components
"""

from .frontend import StreamlitEventExtractionInterface  # Changed from streamlit_interface

__all__ = ['StreamlitEventExtractionInterface']

# src/core/__init__.py
"""
Core extraction engine and abstract interfaces
"""

from .extraction_engine import ComprehensiveExtractionEngine
from .abstract_extractor import (
    AbstractEntityExtractor,
    AbstractInformationProcessor,
    AbstractExtractionEngine,
    AbstractTextPreprocessor,
    AbstractPostProcessor,
    AbstractValidationService
)

__all__ = [
    'ComprehensiveExtractionEngine',
    'AbstractEntityExtractor',
    'AbstractInformationProcessor', 
    'AbstractExtractionEngine',
    'AbstractTextPreprocessor',
    'AbstractPostProcessor',
    'AbstractValidationService'
]