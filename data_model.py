"""
Data Models for Event Registration Information Extraction System
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum

class ExtractionConfidence(Enum):
    """Confidence levels for extracted information."""
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    UNKNOWN = "UNKNOWN"

class EntityType(Enum):
    """Types of entities that can be extracted."""
    PERSON = "PERSON"
    EVENT = "EVENT"
    LOCATION = "LOCATION"
    DATE = "DATE"
    ORGANIZATION = "ORGANIZATION"

@dataclass
class ExtractedEntity:
    """Represents a single extracted entity with metadata."""
    entityType: EntityType
    value: str
    confidence: ExtractionConfidence
    startPosition: int
    endPosition: int
    originalText: str
    
    def __post_init__(self) -> None:
        """Validate entity data after initialization."""
        if not isinstance(self.entityType, EntityType):
            raise ValueError("Invalid entity type")
        if not self.value or not self.value.strip():
            raise ValueError("Entity value cannot be empty")
        if self.startPosition < 0 or self.endPosition < self.startPosition:
            raise ValueError("Invalid position values")
        if not isinstance(self.confidence, ExtractionConfidence):
            raise ValueError("Invalid confidence level")
    
    def toDict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "entityType": self.entityType.value,
            "value": self.value,
            "confidence": self.confidence.value,
            "startPosition": self.startPosition,
            "endPosition": self.endPosition,
            "originalText": self.originalText
        }

@dataclass
class EventRegistrationInfo:
    """Structured event registration information."""
    participantName: Optional[str] = None
    eventName: Optional[str] = None
    location: Optional[str] = None
    date: Optional[str] = None
    extractedEntities: List[ExtractedEntity] = field(default_factory=list)
    extractionTimestamp: datetime = field(default_factory=datetime.now)
    originalText: str = ""
    overallConfidence: ExtractionConfidence = ExtractionConfidence.UNKNOWN
    
    def __post_init__(self) -> None:
        """Validate registration info after initialization."""
        if self.participantName and not isinstance(self.participantName, str):
            raise ValueError("participantName must be a string")
        if self.eventName and not isinstance(self.eventName, str):
            raise ValueError("eventName must be a string")
        if self.location and not isinstance(self.location, str):
            raise ValueError("location must be a string")
        if self.date and not isinstance(self.date, str):
            raise ValueError("date must be a string")
        if not isinstance(self.overallConfidence, ExtractionConfidence):
            raise ValueError("Invalid overall confidence level")
    
    def isComplete(self) -> bool:
        """Check if all required fields are extracted."""
        return all([
            self.participantName and self.participantName.strip(),
            self.eventName and self.eventName.strip(),
            self.location and self.location.strip(),
            self.date and self.date.strip()
        ])
    
    def getCompletionPercentage(self) -> float:
        """Calculate completion percentage of extracted information."""
        fields = [self.participantName, self.eventName, self.location, self.date]
        completed = sum(1 for field in fields if field and field.strip())
        return (completed / len(fields)) * 100.0 if fields else 0.0
    
    def getMissingFields(self) -> List[str]:
        """Get list of missing required fields."""
        missing = []
        if not self.participantName or not self.participantName.strip():
            missing.append("participantName")
        if not self.eventName or not self.eventName.strip():
            missing.append("eventName")
        if not self.location or not self.location.strip():
            missing.append("location")
        if not self.date or not self.date.strip():
            missing.append("date")
        return missing
    
    def getConfidenceScore(self) -> float:
        """Calculate numeric confidence score based on confidence level."""
        confidence_scores = {
            ExtractionConfidence.HIGH: 1.0,
            ExtractionConfidence.MEDIUM: 0.7,
            ExtractionConfidence.LOW: 0.4,
            ExtractionConfidence.UNKNOWN: 0.1
        }
        return confidence_scores.get(self.overallConfidence, 0.1)
    
    def toDict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "participantName": self.participantName,
            "eventName": self.eventName,
            "location": self.location,
            "date": self.date,
            "extractedEntities": [entity.toDict() for entity in self.extractedEntities],
            "extractionTimestamp": self.extractionTimestamp.isoformat(),
            "originalText": self.originalText,
            "overallConfidence": self.overallConfidence.value,
            "completionPercentage": self.getCompletionPercentage(),
            "missingFields": self.getMissingFields(),
            "confidenceScore": self.getConfidenceScore(),
            "isComplete": self.isComplete()
        }
    
    def toTemplateFormat(self) -> str:
        """Convert to the expected template format."""
        return f"""Event Registration Confirmation

Participant Name: {self.participantName or 'N/A'}
Event: {self.eventName or 'N/A'}
Location: {self.location or 'N/A'}
Date: {self.date or 'N/A'}"""

@dataclass
class ExtractionResult:
    """Complete result of information extraction process."""
    registrationInfo: EventRegistrationInfo
    processingTimeMs: float
    extractionMethod: str
    errorMessages: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    
    def __post_init__(self) -> None:
        """Validate extraction result after initialization."""
        if not isinstance(self.registrationInfo, EventRegistrationInfo):
            raise ValueError("registrationInfo must be an EventRegistrationInfo instance")
        if self.processingTimeMs < 0:
            raise ValueError("processingTimeMs cannot be negative")
        if not self.extractionMethod or not isinstance(self.extractionMethod, str):
            raise ValueError("extractionMethod must be a non-empty string")
    
    def isSuccessful(self) -> bool:
        """Check if extraction was successful."""
        return len(self.errorMessages) == 0 and self.registrationInfo.getCompletionPercentage() > 0
    
    def hasHighConfidence(self) -> bool:
        """Check if extraction has high confidence."""
        return self.registrationInfo.overallConfidence == ExtractionConfidence.HIGH
    
    def toDict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "registrationInfo": self.registrationInfo.toDict(),
            "processingTimeMs": self.processingTimeMs,
            "extractionMethod": self.extractionMethod,
            "errorMessages": self.errorMessages,
            "warnings": self.warnings,
            "isSuccessful": self.isSuccessful(),
            "hasHighConfidence": self.hasHighConfidence()
        }

@dataclass
class ProcessingMetrics:
    """Metrics for monitoring extraction performance."""
    totalProcessed: int = 0
    successfulExtractions: int = 0
    averageProcessingTimeMs: float = 0.0
    averageCompletionPercentage: float = 0.0
    confidenceDistribution: Dict[str, int] = field(default_factory=dict)
    
    def updateMetrics(self, result: ExtractionResult) -> None:
        """Update metrics with new extraction result."""
        self.totalProcessed += 1
        if result.isSuccessful():
            self.successfulExtractions += 1
        
        # Update average processing time
        self.averageProcessingTimeMs = (
            (self.averageProcessingTimeMs * (self.totalProcessed - 1) + result.processingTimeMs)
            / self.totalProcessed
        )
        
        # Update average completion percentage
        completion = result.registrationInfo.getCompletionPercentage()
        self.averageCompletionPercentage = (
            (self.averageCompletionPercentage * (self.totalProcessed - 1) + completion)
            / self.totalProcessed
        )
        
        # Update confidence distribution
        confidence = result.registrationInfo.overallConfidence.value
        self.confidenceDistribution[confidence] = self.confidenceDistribution.get(confidence, 0) + 1
    
    def getSuccessRate(self) -> float:
        """Calculate success rate percentage."""
        if self.totalProcessed == 0:
            return 0.0
        return (self.successfulExtractions / self.totalProcessed) * 100.0
    
    def toDict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "totalProcessed": self.totalProcessed,
            "successfulExtractions": self.successfulExtractions,
            "successRate": self.getSuccessRate(),
            "averageProcessingTimeMs": self.averageProcessingTimeMs,
            "averageCompletionPercentage": self.averageCompletionPercentage,
            "confidenceDistribution": self.confidenceDistribution
        }

@dataclass
class ExtractionRequest:
    """Request object for extraction processing."""
    text: str
    requireHighConfidence: bool = False
    timeoutMs: int = 5000
    
    def __post_init__(self) -> None:
        """Validate extraction request."""
        if not self.text or not self.text.strip():
            raise ValueError("Text cannot be empty")
        if self.timeoutMs <= 0:
            raise ValueError("Timeout must be positive")
    
    def toDict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "text": self.text,
            "requireHighConfidence": self.requireHighConfidence,
            "timeoutMs": self.timeoutMs
        }

@dataclass
class ExtractionResponse:
    """Response object for extraction processing."""
    result: ExtractionResult
    request: ExtractionRequest
    timestamp: datetime = field(default_factory=datetime.now)
    
    def toDict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "result": self.result.toDict(),
            "request": self.request.toDict(),
            "timestamp": self.timestamp.isoformat()
        }