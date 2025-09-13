"""
Abstract Base Classes for Information Extraction
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
from data_model import (
    ExtractedEntity,
    EventRegistrationInfo,
    ExtractionResult,
    ExtractionConfidence,
)


class AbstractEntityExtractor(ABC):
    """Abstract base class for entity extractors."""

    @abstractmethod
    def extractEntities(self, text: str) -> List[ExtractedEntity]:
        """Extract entities from text."""
        pass

    @abstractmethod
    def getExtractorName(self) -> str:
        """Get name of the extractor."""
        pass

    @abstractmethod
    def getExtractorVersion(self) -> str:
        """Get version of the extractor."""
        pass

    @abstractmethod
    def getSupportedEntityTypes(self) -> List[str]:
        """Get list of supported entity types."""
        pass

    @abstractmethod
    def isEntityTypeSupported(self, entityType: str) -> bool:
        """Check if entity type is supported."""
        pass

    @abstractmethod
    def getPerformanceMetrics(self) -> Dict[str, Any]:
        """Get performance metrics for the extractor."""
        pass

    @abstractmethod
    def getLastError(self) -> Optional[str]:
        """Get last error message if any."""
        pass

    @abstractmethod
    def clearErrors(self) -> None:
        """Clear any stored error messages."""
        pass


class AbstractInformationProcessor(ABC):
    """Abstract base class for information processing."""

    @abstractmethod
    def processExtractedEntities(
        self, entities: List[ExtractedEntity], originalText: str
    ) -> EventRegistrationInfo:
        """Process extracted entities into structured information."""
        pass

    @abstractmethod
    def validateExtractedInfo(
        self, info: EventRegistrationInfo
    ) -> Tuple[bool, List[str]]:
        """Validate extracted information and return validation results with messages."""
        pass

    @abstractmethod
    def calculateConfidence(self, info: EventRegistrationInfo) -> ExtractionConfidence:
        """Calculate confidence level for extracted information."""
        pass

    @abstractmethod
    def mergeEntities(
        self, primaryEntities: List[ExtractedEntity], secondaryEntities: List[ExtractedEntity]
    ) -> List[ExtractedEntity]:
        """Merge entities from multiple sources."""
        pass


class AbstractExtractionEngine(ABC):
    """Abstract base class for complete extraction engine."""

    @abstractmethod
    def extractInformation(self, text: str) -> ExtractionResult:
        """Extract complete information from text."""
        pass

    @abstractmethod
    def batchExtractInformation(self, texts: List[str]) -> List[ExtractionResult]:
        """Extract information from multiple texts."""
        pass

    @abstractmethod
    def getEngineMetadata(self) -> Dict[str, Any]:
        """Get engine metadata and capabilities."""
        pass

    @abstractmethod
    def getEngineVersion(self) -> str:
        """Get version of the extraction engine."""
        pass

    @abstractmethod
    def getSupportedLanguages(self) -> List[str]:
        """Get list of supported languages."""
        pass

    @abstractmethod
    def isLanguageSupported(self, language: str) -> bool:
        """Check if language is supported."""
        pass


class AbstractTextPreprocessor(ABC):
    """Abstract base class for text preprocessing."""

    @abstractmethod
    def preprocessText(self, text: str) -> str:
        """Preprocess raw text for extraction."""
        pass

    @abstractmethod
    def normalizeText(self, text: str) -> str:
        """Normalize text format."""
        pass

    @abstractmethod
    def cleanText(self, text: str) -> str:
        """Clean text by removing unwanted characters."""
        pass

    @abstractmethod
    def tokenizeText(self, text: str) -> List[str]:
        """Tokenize text into words or phrases."""
        pass

    @abstractmethod
    def detectLanguage(self, text: str) -> str:
        """Detect language of the text."""
        pass

    @abstractmethod
    def removeNoise(self, text: str) -> str:
        """Remove noise and irrelevant content from text."""
        pass


class AbstractPostProcessor(ABC):
    """Abstract base class for post-processing extracted information."""

    @abstractmethod
    def postProcessInformation(self, info: EventRegistrationInfo) -> EventRegistrationInfo:
        """Post-process extracted information."""
        pass

    @abstractmethod
    def enhanceInformation(self, info: EventRegistrationInfo) -> EventRegistrationInfo:
        """Enhance extracted information with additional processing."""
        pass

    @abstractmethod
    def resolveConflicts(self, info: EventRegistrationInfo) -> EventRegistrationInfo:
        """Resolve conflicts in extracted information."""
        pass

    @abstractmethod
    def fillMissingInformation(self, info: EventRegistrationInfo) -> EventRegistrationInfo:
        """Attempt to fill missing information using context."""
        pass

    @abstractmethod
    def standardizeFormat(self, info: EventRegistrationInfo) -> EventRegistrationInfo:
        """Standardize formats of extracted information."""
        pass


class AbstractValidationService(ABC):
    """Abstract base class for validation services."""

    @abstractmethod
    def validateParticipantName(self, name: str) -> Tuple[bool, Optional[str]]:
        """Validate participant name and return result with optional message."""
        pass

    @abstractmethod
    def validateEventName(self, eventName: str) -> Tuple[bool, Optional[str]]:
        """Validate event name and return result with optional message."""
        pass

    @abstractmethod
    def validateLocation(self, location: str) -> Tuple[bool, Optional[str]]:
        """Validate location and return result with optional message."""
        pass

    @abstractmethod
    def validateDate(self, date: str) -> Tuple[bool, Optional[str]]:
        """Validate date format and return result with optional message."""
        pass

    @abstractmethod
    def validateAll(self, info: EventRegistrationInfo) -> Dict[str, Tuple[bool, Optional[str]]]:
        """Validate all fields and return comprehensive results."""
        pass

    @abstractmethod
    def getValidationRules(self) -> Dict[str, Any]:
        """Get validation rules and criteria."""
        pass


class AbstractMetricsCollector(ABC):
    """Abstract base class for metrics collection."""

    @abstractmethod
    def recordExtraction(self, result: ExtractionResult) -> None:
        """Record extraction result metrics."""
        pass

    @abstractmethod
    def getSummaryMetrics(self) -> Dict[str, Any]:
        """Get summary metrics."""
        pass

    @abstractmethod
    def resetMetrics(self) -> None:
        """Reset all metrics."""
        pass


class AbstractConfigurationManager(ABC):
    """Abstract base class for configuration management."""

    @abstractmethod
    def loadConfiguration(self, configPath: str) -> bool:
        """Load configuration from file."""
        pass

    @abstractmethod
    def saveConfiguration(self, configPath: str) -> bool:
        """Save configuration to file."""
        pass

    @abstractmethod
    def getConfiguration(self) -> Dict[str, Any]:
        """Get current configuration."""
        pass

    @abstractmethod
    def updateConfiguration(self, updates: Dict[str, Any]) -> bool:
        """Update configuration with new values."""
        pass
