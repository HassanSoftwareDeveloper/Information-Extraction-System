"""
Advanced Information Processing Service for Structuring Extracted Entities
"""

from typing import List, Dict, Optional, Set, Tuple
import re
from datetime import datetime
from abstract_extractor import AbstractInformationProcessor
from data_model import (
    ExtractedEntity, EventRegistrationInfo, EntityType, 
    ExtractionConfidence
)

class AdvancedInformationProcessor(AbstractInformationProcessor):
    """Advanced processor for converting extracted entities to structured information."""
    
    def __init__(self) -> None:
        """Initialize the processor with configuration."""
        self._initializeProcessingRules()
        self._initializeValidationRules()
    
    def _initializeProcessingRules(self) -> None:
        """Initialize rules for processing entities."""
        self.entityMappingRules = {
            EntityType.PERSON: self._processPersonEntity,
            EntityType.EVENT: self._processEventEntity,
            EntityType.LOCATION: self._processLocationEntity,
            EntityType.DATE: self._processDateEntity
        }
        
        # Priority rules for handling multiple entities of same type
        self.entityPriorityRules = {
            EntityType.PERSON: self._selectBestPersonEntity,
            EntityType.EVENT: self._selectBestEventEntity,
            EntityType.LOCATION: self._selectBestLocationEntity,
            EntityType.DATE: self._selectBestDateEntity
        }
    
    def _initializeValidationRules(self) -> None:
        """Initialize validation rules for extracted information."""
        self.validationThresholds = {
            'minimumNameLength': 3,
            'maximumNameLength': 100,
            'minimumEventNameLength': 5,
            'maximumEventNameLength': 200,
            'minimumLocationLength': 2,
            'maximumLocationLength': 100
        }
        
        self.invalidPatterns = {
            'personName': [
                r'\b(?:conference|summit|workshop|event|meeting)\b',
                r'\b(?:january|february|march|april|may|june|july|august|september|october|november|december)\b',
                r'\d{4}',  # Years
                r'@'  # Email symbols
            ],
            'eventName': [
                r'^\d+$',  # Only numbers
                r'^[a-z\s]+$'  # Only lowercase (usually not event names)
            ],
            'location': [
                r'\b(?:registered|signed up|enrolled)\b',
                r'^\d+$'  # Only numbers
            ]
        }
    
    def calculateConfidence(self, entities: List[ExtractedEntity]) -> ExtractionConfidence:
        """Calculate confidence score for extracted entities."""
        if not entities:
            return ExtractionConfidence.UNKNOWN
        
        # Calculate average confidence
        confidenceValues = {
            ExtractionConfidence.HIGH: 3,
            ExtractionConfidence.MEDIUM: 2,
            ExtractionConfidence.LOW: 1,
            ExtractionConfidence.UNKNOWN: 0
        }
        
        totalScore = sum(confidenceValues[entity.confidence] for entity in entities)
        averageScore = totalScore / len(entities)
        
        if averageScore >= 2.5:
            return ExtractionConfidence.HIGH
        elif averageScore >= 1.5:
            return ExtractionConfidence.MEDIUM
        elif averageScore > 0:
            return ExtractionConfidence.LOW
        else:
            return ExtractionConfidence.UNKNOWN
    
    def mergeEntities(self, entities: List[ExtractedEntity]) -> List[ExtractedEntity]:
        """Merge overlapping or duplicate entities."""
        if not entities:
            return []
        
        # Group by type and value (case-insensitive)
        grouped = {}
        for entity in entities:
            key = (entity.entityType, entity.value.lower())
            if key not in grouped:
                grouped[key] = []
            grouped[key].append(entity)
        
        # Merge entities with same type and value
        merged = []
        for (entity_type, value_lower), entity_list in grouped.items():
            if len(entity_list) == 1:
                merged.append(entity_list[0])
            else:
                # Select the entity with highest confidence
                best_entity = max(entity_list, key=lambda x: self._confidenceToScore(x.confidence))
                merged.append(best_entity)
        
        return merged
    
    def _confidenceToScore(self, confidence: ExtractionConfidence) -> int:
        """Convert confidence enum to numerical score."""
        return {
            ExtractionConfidence.HIGH: 3,
            ExtractionConfidence.MEDIUM: 2,
            ExtractionConfidence.LOW: 1,
            ExtractionConfidence.UNKNOWN: 0
        }[confidence]
    
    def processExtractedEntities(self, entities: List[ExtractedEntity], originalText: str) -> EventRegistrationInfo:
        """Process extracted entities into structured event registration information."""
        if not entities:
            return EventRegistrationInfo(originalText=originalText)
        
        # Group entities by type
        entitiesByType = self._groupEntitiesByType(entities)
        
        # Process each entity type
        registrationInfo = EventRegistrationInfo(originalText=originalText)
        registrationInfo.extractedEntities = entities
        
        # Process person entities
        if EntityType.PERSON in entitiesByType:
            registrationInfo.participantName = self._processPersonEntities(
                entitiesByType[EntityType.PERSON], originalText
            )
        
        # Process event entities
        if EntityType.EVENT in entitiesByType:
            registrationInfo.eventName = self._processEventEntities(
                entitiesByType[EntityType.EVENT], originalText
            )
        
        # Process location entities
        if EntityType.LOCATION in entitiesByType:
            registrationInfo.location = self._processLocationEntities(
                entitiesByType[EntityType.LOCATION], originalText
            )
        
        # Process date entities
        if EntityType.DATE in entitiesByType:
            registrationInfo.date = self._processDateEntities(
                entitiesByType[EntityType.DATE], originalText
            )
        
        # Calculate overall confidence
        registrationInfo.overallConfidence = self._calculateOverallConfidence(registrationInfo)
        
        # Post-process and enhance
        registrationInfo = self._postProcessInformation(registrationInfo, originalText)
        
        return registrationInfo
    
    def _groupEntitiesByType(self, entities: List[ExtractedEntity]) -> Dict[EntityType, List[ExtractedEntity]]:
        """Group entities by their type."""
        grouped = {}
        for entity in entities:
            if entity.entityType not in grouped:
                grouped[entity.entityType] = []
            grouped[entity.entityType].append(entity)
        return grouped
    
    def _processPersonEntities(self, personEntities: List[ExtractedEntity], originalText: str) -> Optional[str]:
        """Process person entities to extract participant name."""
        if not personEntities:
            return None
        
        # Select the best person entity
        bestEntity = self._selectBestPersonEntity(personEntities)
        
        if bestEntity and self._validatePersonName(bestEntity.value):
            return self._cleanAndFormatPersonName(bestEntity.value)
        
        return None
    
    def _processEventEntities(self, eventEntities: List[ExtractedEntity], originalText: str) -> Optional[str]:
        """Process event entities to extract event name."""
        if not eventEntities:
            return None
        
        # Select the best event entity
        bestEntity = self._selectBestEventEntity(eventEntities)
        
        if bestEntity and self._validateEventName(bestEntity.value):
            return self._cleanAndFormatEventName(bestEntity.value)
        
        return None
    
    def _processLocationEntities(self, locationEntities: List[ExtractedEntity], originalText: str) -> Optional[str]:
        """Process location entities to extract location."""
        if not locationEntities:
            return None
        
        # Select the best location entity
        bestEntity = self._selectBestLocationEntity(locationEntities)
        
        if bestEntity and self._validateLocationName(bestEntity.value):
            return self._cleanAndFormatLocationName(bestEntity.value)
        
        return None
    
    def _processDateEntities(self, dateEntities: List[ExtractedEntity], originalText: str) -> Optional[str]:
        """Process date entities to extract date."""
        if not dateEntities:
            return None
        
        # Select the best date entity
        bestEntity = self._selectBestDateEntity(dateEntities)
        
        if bestEntity and self._validateDateFormat(bestEntity.value):
            return self._cleanAndFormatDate(bestEntity.value)
        
        return None
    
    def _selectBestPersonEntity(self, entities: List[ExtractedEntity]) -> Optional[ExtractedEntity]:
        """Select the best person entity from multiple candidates."""
        if not entities:
            return None
        
        # Score entities
        scoredEntities = []
        for entity in entities:
            score = self._scorePersonEntity(entity)
            scoredEntities.append((entity, score))
        
        # Sort by score (highest first)
        scoredEntities.sort(key=lambda x: x[1], reverse=True)
        
        return scoredEntities[0][0] if scoredEntities else None
    
    def _selectBestEventEntity(self, entities: List[ExtractedEntity]) -> Optional[ExtractedEntity]:
        """Select the best event entity from multiple candidates."""
        if not entities:
            return None
        
        # Score entities based on multiple criteria
        scoredEntities = []
        for entity in entities:
            score = self._scoreEventEntity(entity)
            scoredEntities.append((entity, score))
        
        # Sort by score (highest first)
        scoredEntities.sort(key=lambda x: x[1], reverse=True)
        
        return scoredEntities[0][0] if scoredEntities else None
    
    def _selectBestLocationEntity(self, entities: List[ExtractedEntity]) -> Optional[ExtractedEntity]:
        """Select the best location entity from multiple candidates."""
        if not entities:
            return None
        
        # Score entities based on multiple criteria
        scoredEntities = []
        for entity in entities:
            score = self._scoreLocationEntity(entity)
            scoredEntities.append((entity, score))
        
        # Sort by score (highest first)
        scoredEntities.sort(key=lambda x: x[1], reverse=True)
        
        return scoredEntities[0][0] if scoredEntities else None
    
    def _selectBestDateEntity(self, entities: List[ExtractedEntity]) -> Optional[ExtractedEntity]:
        """Select the best date entity from multiple candidates."""
        if not entities:
            return None
        
        # Score entities based on multiple criteria
        scoredEntities = []
        for entity in entities:
            score = self._scoreDateEntity(entity)
            scoredEntities.append((entity, score))
        
        # Sort by score (highest first)
        scoredEntities.sort(key=lambda x: x[1], reverse=True)
        
        return scoredEntities[0][0] if scoredEntities else None
    
    def _scorePersonEntity(self, entity: ExtractedEntity) -> float:
        """Score a person entity for selection."""
        score = 0.0
        
        # Confidence score
        confidenceScores = {
            ExtractionConfidence.HIGH: 10.0,
            ExtractionConfidence.MEDIUM: 6.0,
            ExtractionConfidence.LOW: 2.0,
            ExtractionConfidence.UNKNOWN: 0.0
        }
        score += confidenceScores.get(entity.confidence, 0.0)
        
        # Name quality score
        words = entity.value.split()
        if len(words) == 2:  # First + Last name
            score += 5.0
        elif len(words) == 3:  # First + Middle + Last
            score += 3.0
        else:
            score -= 1.0  # Penalty for unusual name length
        
        # Capitalization score
        if all(word[0].isupper() and word[1:].islower() for word in words if word):
            score += 3.0
        
        # Length appropriateness
        if 5 <= len(entity.value) <= 50:
            score += 2.0
        
        return score
    
    def _scoreEventEntity(self, entity: ExtractedEntity) -> float:
        """Score an event entity for selection."""
        score = 0.0
        
        # Confidence score
        confidenceScores = {
            ExtractionConfidence.HIGH: 10.0,
            ExtractionConfidence.MEDIUM: 6.0,
            ExtractionConfidence.LOW: 2.0,
            ExtractionConfidence.UNKNOWN: 0.0
        }
        score += confidenceScores.get(entity.confidence, 0.0)
        
        # Event keywords score
        event_keywords = ['conference', 'summit', 'workshop', 'meeting', 'seminar', 'expo', 'forum']
        if any(keyword in entity.value.lower() for keyword in event_keywords):
            score += 5.0
        
        # Length score
        if 10 <= len(entity.value) <= 100:
            score += 3.0
        
        # Capitalization score (events often have proper capitalization)
        words = entity.value.split()
        if words and words[0][0].isupper():
            score += 2.0
        
        return score
    
    def _scoreLocationEntity(self, entity: ExtractedEntity) -> float:
        """Score a location entity for selection."""
        score = 0.0
        
        # Confidence score
        confidenceScores = {
            ExtractionConfidence.HIGH: 10.0,
            ExtractionConfidence.MEDIUM: 6.0,
            ExtractionConfidence.LOW: 2.0,
            ExtractionConfidence.UNKNOWN: 0.0
        }
        score += confidenceScores.get(entity.confidence, 0.0)
        
        # Format score (prefer "City, State" format)
        if ',' in entity.value:
            score += 5.0
        
        # Length score
        if 3 <= len(entity.value) <= 50:
            score += 3.0
        
        # Capitalization score (locations should be properly capitalized)
        words = entity.value.split()
        if all(word[0].isupper() for word in words if word):
            score += 2.0
        
        return score
    
    def _scoreDateEntity(self, entity: ExtractedEntity) -> float:
        """Score a date entity for selection."""
        score = 0.0
        
        # Confidence score
        confidenceScores = {
            ExtractionConfidence.HIGH: 10.0,
            ExtractionConfidence.MEDIUM: 6.0,
            ExtractionConfidence.LOW: 2.0,
            ExtractionConfidence.UNKNOWN: 0.0
        }
        score += confidenceScores.get(entity.confidence, 0.0)
        
        # Completeness score (prefer dates with year)
        if re.search(r'\d{4}', entity.value):
            score += 5.0
        
        # Recent date score (prefer dates in current or next year)
        current_year = datetime.now().year
        if str(current_year) in entity.value or str(current_year + 1) in entity.value:
            score += 3.0
        
        # Format score (prefer standard date formats)
        if re.search(r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})|([A-Za-z]+ \d{1,2},? \d{4})', entity.value):
            score += 2.0
        
        return score
    
    def _validatePersonName(self, name: str) -> bool:
        """Validate person name format and content."""
        if not name or len(name.strip()) < self.validationThresholds['minimumNameLength']:
            return False
        
        if len(name) > self.validationThresholds['maximumNameLength']:
            return False
        
        # Check against invalid patterns
        for pattern in self.invalidPatterns['personName']:
            if re.search(pattern, name, re.IGNORECASE):
                return False
        
        # Must contain only letters, spaces, and basic punctuation
        if not re.match(r'^[A-Za-z\s\.\-\']+$', name):
            return False
        
        # Must have at least one space (first + last name)
        if ' ' not in name.strip():
            return False
        
        return True
    
    def _validateEventName(self, eventName: str) -> bool:
        """Validate event name format and content."""
        if not eventName or len(eventName.strip()) < self.validationThresholds['minimumEventNameLength']:
            return False
        
        if len(eventName) > self.validationThresholds['maximumEventNameLength']:
            return False
        
        # Check against invalid patterns
        for pattern in self.invalidPatterns['eventName']:
            if re.search(pattern, eventName, re.IGNORECASE):
                return False
        
        return True
    
    def _validateLocationName(self, location: str) -> bool:
        """Validate location name format and content."""
        if not location or len(location.strip()) < self.validationThresholds['minimumLocationLength']:
            return False
        
        if len(location) > self.validationThresholds['maximumLocationLength']:
            return False
        
        # Check against invalid patterns
        for pattern in self.invalidPatterns['location']:
            if re.search(pattern, location, re.IGNORECASE):
                return False
        
        return True
    
    def _validateDateFormat(self, date: str) -> bool:
        """Validate date format."""
        if not date or not date.strip():
            return False
        
        # Basic date format validation
        datePatterns = [
            r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+\d{4}\b',
            r'\b\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4}\b',
            r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',
            r'\b\d{4}[/-]\d{1,2}[/-]\d{1,2}\b'
        ]
        
        return any(re.search(pattern, date, re.IGNORECASE) for pattern in datePatterns)
    
    def _cleanAndFormatPersonName(self, name: str) -> str:
        """Clean and format person name."""
        # Remove extra whitespace
        cleaned = ' '.join(name.strip().split())
        
        # Proper case formatting
        words = cleaned.split()
        formatted = []
        for word in words:
            if word.upper() in ['II', 'III', 'IV', 'JR', 'SR']:
                formatted.append(word.upper())
            elif '.' in word:  # Handle initials
                formatted.append(word.upper())
            else:
                formatted.append(word.capitalize())
        
        return ' '.join(formatted)
    
    def _cleanAndFormatLocationName(self, location: str) -> str:
        """Clean and format location name."""
        # Remove extra whitespace
        cleaned = ' '.join(location.strip().split())
        
        # Handle common location formats
        if ',' in cleaned:
            parts = [part.strip() for part in cleaned.split(',')]
            formatted_parts = []
            for part in parts:
                # Capitalize each word in location parts
                words = part.split()
                formatted_words = [word.capitalize() for word in words]
                formatted_parts.append(' '.join(formatted_words))
            return ', '.join(formatted_parts)
        else:
            # Simple capitalization
            words = cleaned.split()
            formatted = [word.capitalize() for word in words]
            return ' '.join(formatted)
    
    def _cleanAndFormatDate(self, date: str) -> str:
        """Clean and format date string."""
        # Remove common prefixes
        cleaned = re.sub(r'^\s*(?:on|date|scheduled for)\s+', '', date, flags=re.IGNORECASE).strip()
        
        # Standardize month names
        monthReplacements = {
            'january': 'January', 'jan': 'January',
            'february': 'February', 'feb': 'February',
            'march': 'March', 'mar': 'March',
            'april': 'April', 'apr': 'April',
            'may': 'May',
            'june': 'June', 'jun': 'June',
            'july': 'July', 'jul': 'July',
            'august': 'August', 'aug': 'August',
            'september': 'September', 'sep': 'September',
            'october': 'October', 'oct': 'October',
            'november': 'November', 'nov': 'November',
            'december': 'December', 'dec': 'December'
        }
        
        for abbrev, fullMonth in monthReplacements.items():
            cleaned = re.sub(r'\b' + abbrev + r'\b', fullMonth, cleaned, flags=re.IGNORECASE)
        
        return cleaned
    
    def _cleanAndFormatEventName(self, eventName: str) -> str:
        """Clean and format event name."""
        # Remove extra whitespace
        cleaned = ' '.join(eventName.strip().split())
        
        # Capitalize appropriately
        words = cleaned.split()
        formatted = []
        for i, word in enumerate(words):
            # Keep certain words lowercase unless they're the first word
            lowercaseWords = {'and', 'or', 'of', 'the', 'in', 'on', 'at', 'for', 'with', 'by'}
            if word.lower() in lowercaseWords and i > 0:
                formatted.append(word.lower())
            else:
                formatted.append(word.capitalize())
        
        return ' '.join(formatted)
    
    def _calculateOverallConfidence(self, info: EventRegistrationInfo) -> ExtractionConfidence:
        """Calculate overall confidence based on extracted information completeness and quality."""
        if not info.extractedEntities:
            return ExtractionConfidence.UNKNOWN
        
        # Count filled fields
        filledFields = sum([
            1 if info.participantName else 0,
            1 if info.eventName else 0,
            1 if info.location else 0,
            1 if info.date else 0
        ])
        
        # Calculate average confidence of entities
        confidenceValues = {
            ExtractionConfidence.HIGH: 3,
            ExtractionConfidence.MEDIUM: 2,
            ExtractionConfidence.LOW: 1,
            ExtractionConfidence.UNKNOWN: 0
        }
        
        totalConfidence = sum(confidenceValues[entity.confidence] for entity in info.extractedEntities)
        averageConfidence = totalConfidence / len(info.extractedEntities) if info.extractedEntities else 0
        
        # Determine overall confidence
        if filledFields == 4 and averageConfidence >= 2.5:
            return ExtractionConfidence.HIGH
        elif filledFields >= 3 and averageConfidence >= 2.0:
            return ExtractionConfidence.HIGH
        elif filledFields >= 2 and averageConfidence >= 1.5:
            return ExtractionConfidence.MEDIUM
        elif filledFields >= 1:
            return ExtractionConfidence.LOW
        else:
            return ExtractionConfidence.UNKNOWN
    
    def _postProcessInformation(self, info: EventRegistrationInfo, originalText: str) -> EventRegistrationInfo:
        """Post-process extracted information for quality enhancement."""
        # Try to extract missing information using fallback methods
        if not info.participantName:
            info.participantName = self._extractNameFallback(originalText)
        
        if not info.eventName:
            info.eventName = self._extractEventFallback(originalText)
        
        if not info.location:
            info.location = self._extractLocationFallback(originalText)
        
        if not info.date:
            info.date = self._extractDateFallback(originalText)
        
        # Recalculate confidence after fallback extraction
        info.overallConfidence = self._calculateOverallConfidence(info)
        
        return info
    
    def _extractNameFallback(self, text: str) -> Optional[str]:
        """Fallback method to extract participant name."""
        # Look for patterns like "Name: John Doe" or "Participant: John Doe"
        patterns = [
            r'(?:name|participant|attendee)\s*:\s*([A-Z][a-z]+\s+[A-Z][a-z]+)',
            r'\b([A-Z][a-z]+\s+[A-Z][a-z]+)\s+(?:registered|signed up|enrolled)',
            r'(?:Mr|Mrs|Ms|Dr)\.?\s+([A-Z][a-z]+\s+[A-Z][a-z]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                name = match.group(1).strip()
                if self._validatePersonName(name):
                    return self._cleanAndFormatPersonName(name)
        
        return None
    
    def _extractEventFallback(self, text: str) -> Optional[str]:
        """Fallback method to extract event name."""
        # Look for quoted event names or specific patterns
        patterns = [
            r'"([^"]*(?:conference|summit|workshop|meetup|expo|convention)[^"]*)"',
            r'(?:event|conference|summit)\s*:\s*([A-Z][^.!?]*?)(?:\.|$)',
            r'(?:attending|joining)\s+(?:the\s+)?([A-Z][^.!?]*?(?:conference|summit|workshop|meetup|expo))'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                eventName = match.group(1).strip()
                if self._validateEventName(eventName):
                    return self._cleanAndFormatEventName(eventName)
        
        return None
    
    def _extractLocationFallback(self, text: str) -> Optional[str]:
        """Fallback method to extract location."""
        # Look for location patterns
        patterns = [
            r'(?:location|venue|city|place)\s*:\s*([A-Z][a-zA-Z\s,]+)',
            r'(?:held|taking place|happening|located)\s+(?:in|at)\s+([A-Z][a-zA-Z\s,]+)',
            r'\b([A-Z][a-z]+,\s*[A-Z][a-z]+)\b'  # City, State pattern
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                location = match.group(1).strip()
                # Remove trailing punctuation
                location = re.sub(r'[.!?]+$', '', location)
                if self._validateLocationName(location):
                    return self._cleanAndFormatLocationName(location)
        
        return None
    
    def _extractDateFallback(self, text: str) -> Optional[str]:
        """Fallback method to extract date."""
        # Look for date patterns with context
        patterns = [
            r'(?:date|when|scheduled|happening)\s*:\s*([A-Za-z0-9\s,/-]+)',
            r'(?:starts|begins|commences)\s+(?:on\s+)?([A-Za-z0-9\s,/-]+)',
            r'\b((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+\d{4})\b'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                date = match.group(1).strip()
                # Remove trailing punctuation
                date = re.sub(r'[.!?]+$', '', date)
                if self._validateDateFormat(date):
                    return self._cleanAndFormatDate(date)
        
        return None
    
    def validateExtractedInfo(self, info: EventRegistrationInfo) -> bool:
        """Validate the completeness and quality of extracted information."""
        if not info:
            return False
        
        # Check if at least some information was extracted
        hasAnyInfo = any([
            info.participantName,
            info.eventName,
            info.location,
            info.date
        ])
        
        if not hasAnyInfo:
            return False
        
        # Validate individual fields if they exist
        validations = []
        
        if info.participantName:
            validations.append(self._validatePersonName(info.participantName))
        
        if info.eventName:
            validations.append(self._validateEventName(info.eventName))
        
        if info.location:
            validations.append(self._validateLocationName(info.location))
        
        if info.date:
            validations.append(self._validateDateFormat(info.date))
        
        # All existing fields must be valid
        return all(validations) if validations else False
    
    def _processPersonEntity(self, entity: ExtractedEntity) -> Optional[str]:
        """Process a single person entity."""
        if self._validatePersonName(entity.value):
            return self._cleanAndFormatPersonName(entity.value)
        return None
    
    def _processEventEntity(self, entity: ExtractedEntity) -> Optional[str]:
        """Process a single event entity."""
        if self._validateEventName(entity.value):
            return self._cleanAndFormatEventName(entity.value)
        return None
    
    def _processLocationEntity(self, entity: ExtractedEntity) -> Optional[str]:
        """Process a single location entity."""
        if self._validateLocationName(entity.value):
            return self._cleanAndFormatLocationName(entity.value)
        return None
    
    def _processDateEntity(self, entity: ExtractedEntity) -> Optional[str]:
        """Process a single date entity."""
        if self._validateDateFormat(entity.value):
            return self._cleanAndFormatDate(entity.value)
        return None