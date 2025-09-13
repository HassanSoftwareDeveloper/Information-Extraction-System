"""
Advanced Named Entity Recognition Extractor using Multiple Strategies
"""

import re
from typing import List, Dict, Set, Tuple, Optional, Any
from abstract_extractor import AbstractEntityExtractor
from data_model import ExtractedEntity, EntityType, ExtractionConfidence


class HybridNamedEntityExtractor(AbstractEntityExtractor):
    """Advanced NER extractor combining multiple extraction strategies."""

    def __init__(self) -> None:
        """Initialize the extractor with patterns, knowledge bases and metrics."""
        # Setup core structures
        self._initializePatterns()
        self._initializeKnowledgeBases()
        self._initializeContextualRules()

        # Error and metrics tracking
        self._lastError: Optional[str] = None
        self._extractionCount: int = 0
        self._successfulExtractions: int = 0
        # Supported entity types as uppercase strings for robust matching
        self._supportedEntityTypes: Set[str] = {e.name.upper() for e in EntityType}

        # Optional versioning
        self._version: str = "1.0.0"

    def _initializePatterns(self) -> None:
        """Initialize regex patterns for entity recognition."""
        self.patterns = {
            # Person name patterns (more sophisticated)
            "personNames": [
                re.compile(r"\b[A-Z][a-z]+\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?\b"),
                re.compile(r"\b(?:Mr|Mrs|Ms|Dr|Prof)\.?\s+[A-Z][a-z]+\s+[A-Z][a-z]+\b"),
                re.compile(r"\b[A-Z][a-z]+\s+[A-Z]\.\s+[A-Z][a-z]+\b"),
            ],
            # Event patterns
            "eventPatterns": [
                re.compile(
                    r"\b(?:the\s+)?[A-Z][a-z]*\s+(?:Conference|Summit|Workshop|Meetup|Expo|Convention|Symposium)\b",
                    re.IGNORECASE,
                ),
                re.compile(r"\b[A-Z]+\s+\d{4}\b"),  # e.g., "WWDC 2023"
                re.compile(
                    r"\b\d{4}\s+[A-Z][a-z]+\s+(?:Conference|Summit)\b", re.IGNORECASE
                ),
            ],
            # Location patterns
            "locationPatterns": [
                re.compile(
                    r"\bin\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*),?\s*([A-Z]{2,3})?\b"
                ),
                re.compile(r"\bat\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b"),
                re.compile(
                    r"\b([A-Z][a-z]+),\s*([A-Z][a-z]+)(?:,\s*([A-Z]{2,3}))?\b"
                ),
            ],
            # Date patterns (comprehensive)
            "datePatterns": [
                re.compile(
                    r"\b(?:on\s+)?(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+\d{4}\b",
                    re.IGNORECASE,
                ),
                re.compile(
                    r"\b(?:on\s+)?\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4}\b",
                    re.IGNORECASE,
                ),
                re.compile(r"\b(?:on\s+)?\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b"),
                re.compile(r"\b(?:on\s+)?\d{4}[/-]\d{1,2}[/-]\d{1,2}\b"),
            ],
        }

    def _initializeKnowledgeBases(self) -> None:
        """Initialize knowledge bases for entity recognition."""
        self.commonFirstNames = {
            "john",
            "jane",
            "michael",
            "sarah",
            "david",
            "maria",
            "james",
            "lisa",
            "robert",
            "jennifer",
            "william",
            "elizabeth",
            "richard",
            "patricia",
            "ahmed",
            "fatima",
            "muhammad",
            "aisha",
            "ali",
            "zainab",
            "omar",
            "sara",
        }

        self.commonLastNames = {
            "smith",
            "johnson",
            "brown",
            "taylor",
            "miller",
            "davis",
            "garcia",
            "rodriguez",
            "wilson",
            "martinez",
            "anderson",
            "jackson",
            "white",
            "khan",
            "ahmed",
            "ali",
            "shah",
            "malik",
            "hussain",
            "abbas",
        }

        self.eventTypeIndicators = {
            "conference",
            "summit",
            "workshop",
            "seminar",
            "meetup",
            "expo",
            "convention",
            "symposium",
            "forum",
            "congress",
            "festival",
            "competition",
            "tournament",
            "championship",
            "ceremony",
        }

        self.domainKeywords = {
            "tech",
            "technology",
            "ai",
            "artificial intelligence",
            "ml",
            "machine learning",
            "data science",
            "blockchain",
            "cybersecurity",
            "cloud",
            "mobile",
            "web",
            "software",
            "hardware",
            "iot",
            "robotics",
            "fintech",
            "healthtech",
        }

        self.locationIndicators = {"in", "at", "near", "around", "located in"}

        self.majorCities = {
            "new york",
            "london",
            "tokyo",
            "paris",
            "berlin",
            "sydney",
            "toronto",
            "mumbai",
            "delhi",
            "bangalore",
            "karachi",
            "lahore",
            "islamabad",
            "dubai",
            "singapore",
            "hong kong",
            "san francisco",
            "los angeles",
        }

        self.registrationVerbs = {
            "registered",
            "signed up",
            "enrolled",
            "joined",
            "participated",
            "attended",
            "booked",
            "reserved",
            "confirmed",
            "applied",
            "subscribed",
        }

    def _initializeContextualRules(self) -> None:
        """Initialize contextual rules for better entity recognition."""
        self.contextualRules = {
            "personNameContext": [
                r"\b(?:Mr|Mrs|Ms|Dr|Prof)\.?\s+",
                r"\b(?:registered|signed up|enrolled)\s+(?:for|to)\s+.*?\s+(?:by|participant|attendee)\s+",
                r"\bparticipant\s+(?:name\s*:\s*)?",
                r"\battendee\s+(?:name\s*:\s*)?",
            ],
            "eventNameContext": [
                r"(?:registered|signed up|enrolled)\s+(?:for|to)\s+(?:the\s+)?",
                r"(?:attending|joining)\s+(?:the\s+)?",
                r"(?:event|conference|workshop|summit)\s+(?:name\s*:\s*)?",
            ],
            "locationContext": [
                r"\b(?:in|at|located in|held in|taking place in)\s+",
                r"\b(?:venue|location)\s*:\s*",
                r"\b(?:city|place|destination)\s*:\s*",
            ],
            "dateContext": [
                r"\b(?:on|date|scheduled for|happening on)\s+",
                r"\b(?:date|when)\s*:\s*",
                r"\b(?:starts|begins|commences)\s+(?:on\s+)?",
            ],
        }

    def extractEntities(self, text: str) -> List[ExtractedEntity]:
        """Extract entities using hybrid approach with basic error/metric tracking."""
        self._extractionCount += 1
        if not text or not text.strip():
            return []

        try:
            extractedEntities: List[ExtractedEntity] = []

            # Extract using different strategies
            extractedEntities.extend(self._extractPersonNames(text))
            extractedEntities.extend(self._extractEventNames(text))
            extractedEntities.extend(self._extractLocations(text))
            extractedEntities.extend(self._extractDates(text))

            # Remove duplicates and overlaps
            extractedEntities = self._removeDuplicatesAndOverlaps(extractedEntities)

            # Enhance with contextual information
            extractedEntities = self._enhanceWithContext(extractedEntities, text)

            # Metrics
            self._successfulExtractions += 1
            self._lastError = None
            return extractedEntities

        except Exception as exc:  # capture unexpected errors
            self._lastError = f"Extraction error: {exc}"
            # Optionally, log or raise depending on your app; here we return empty list
            return []

    # --- extraction helper methods (unchanged) ---

    def _extractPersonNames(self, text: str) -> List[ExtractedEntity]:
        """Extract person names using multiple strategies."""
        entities: List[ExtractedEntity] = []

        # Strategy 1: Pattern-based extraction
        for pattern in self.patterns["personNames"]:
            for match in pattern.finditer(text):
                name = match.group().strip()
                if self._validatePersonName(name):
                    confidence = self._calculatePersonNameConfidence(name)
                    entity = ExtractedEntity(
                        entityType=EntityType.PERSON,
                        value=name,
                        confidence=confidence,
                        startPosition=match.start(),
                        endPosition=match.end(),
                        originalText=text[match.start():match.end()],
                    )
                    entities.append(entity)

        # Strategy 2: Contextual extraction
        entities.extend(self._extractPersonNamesFromContext(text))

        return entities

    def _extractEventNames(self, text: str) -> List[ExtractedEntity]:
        """Extract event names using pattern matching and context analysis."""
        entities: List[ExtractedEntity] = []

        for pattern in self.patterns["eventPatterns"]:
            for match in pattern.finditer(text):
                eventName = match.group().strip()
                if self._validateEventName(eventName):
                    confidence = self._calculateEventNameConfidence(eventName, text)
                    entity = ExtractedEntity(
                        entityType=EntityType.EVENT,
                        value=eventName,
                        confidence=confidence,
                        startPosition=match.start(),
                        endPosition=match.end(),
                        originalText=text[match.start():match.end()],
                    )
                    entities.append(entity)

        entities.extend(self._extractEventNamesFromContext(text))

        return entities

    def _extractLocations(self, text: str) -> List[ExtractedEntity]:
        """Extract location information."""
        entities: List[ExtractedEntity] = []

        for pattern in self.patterns["locationPatterns"]:
            for match in pattern.finditer(text):
                # prefer the full match cleaned
                location = self._cleanLocationText(match.group())
                if location and self._validateLocation(location):
                    confidence = self._calculateLocationConfidence(location)
                    entity = ExtractedEntity(
                        entityType=EntityType.LOCATION,
                        value=location,
                        confidence=confidence,
                        startPosition=match.start(),
                        endPosition=match.end(),
                        originalText=text[match.start():match.end()],
                    )
                    entities.append(entity)

        return entities

    def _extractDates(self, text: str) -> List[ExtractedEntity]:
        """Extract date information."""
        entities: List[ExtractedEntity] = []

        for pattern in self.patterns["datePatterns"]:
            for match in pattern.finditer(text):
                dateText = match.group().strip()
                cleanedDate = self._cleanDateText(dateText)
                if cleanedDate and self._validateDate(cleanedDate):
                    confidence = self._calculateDateConfidence(cleanedDate)
                    entity = ExtractedEntity(
                        entityType=EntityType.DATE,
                        value=cleanedDate,
                        confidence=confidence,
                        startPosition=match.start(),
                        endPosition=match.end(),
                        originalText=text[match.start():match.end()],
                    )
                    entities.append(entity)

        return entities

    def _extractPersonNamesFromContext(self, text: str) -> List[ExtractedEntity]:
        """Extract person names using contextual clues."""
        entities: List[ExtractedEntity] = []

        for contextPattern in self.contextualRules["personNameContext"]:
            pattern = contextPattern + r"([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)"
            matches = re.finditer(pattern, text, re.IGNORECASE)

            for match in matches:
                name = match.group(1).strip()
                if self._validatePersonName(name):
                    confidence = ExtractionConfidence.HIGH
                    entity = ExtractedEntity(
                        entityType=EntityType.PERSON,
                        value=name,
                        confidence=confidence,
                        startPosition=match.start(1),
                        endPosition=match.end(1),
                        originalText=name,
                    )
                    entities.append(entity)

        return entities

    def _extractEventNamesFromContext(self, text: str) -> List[ExtractedEntity]:
        """Extract event names using contextual analysis."""
        entities: List[ExtractedEntity] = []

        for verb in self.registrationVerbs:
            pattern = rf"\b{verb}\s+(?:for\s+)?(?:the\s+)?([A-Z][^.!?]*?(?:conference|summit|workshop|meetup|expo|convention|symposium))"
            matches = re.finditer(pattern, text, re.IGNORECASE)

            for match in matches:
                eventName = match.group(1).strip()
                if self._validateEventName(eventName):
                    confidence = ExtractionConfidence.HIGH
                    entity = ExtractedEntity(
                        entityType=EntityType.EVENT,
                        value=eventName,
                        confidence=confidence,
                        startPosition=match.start(1),
                        endPosition=match.end(1),
                        originalText=eventName,
                    )
                    entities.append(entity)

        return entities

    # --- validation and scoring helpers (unchanged) ---

    def _validatePersonName(self, name: str) -> bool:
        if not name or len(name.split()) < 2:
            return False

        words = [word.lower() for word in name.split()]

        hasFirstName = any(word in self.commonFirstNames for word in words)
        hasLastName = any(word in self.commonLastNames for word in words)

        # Allow names that follow capitalized pattern
        hasValidPattern = all(word.isalpha() and word[0].isupper() for word in name.split())

        nonNameWords = {"conference", "summit", "workshop", "meeting", "event", "the", "and", "or"}
        hasNonNameWords = any(word.lower() in nonNameWords for word in name.split())

        return (hasFirstName or hasLastName or hasValidPattern) and not hasNonNameWords

    def _validateEventName(self, eventName: str) -> bool:
        if not eventName or len(eventName.strip()) < 3:
            return False

        eventLower = eventName.lower()

        hasEventIndicator = any(indicator in eventLower for indicator in self.eventTypeIndicators)
        hasDomainKeyword = any(keyword in eventLower for keyword in self.domainKeywords)
        hasYear = bool(re.search(r"\b20\d{2}\b", eventName))

        return hasEventIndicator or hasDomainKeyword or hasYear

    def _validateLocation(self, location: str) -> bool:
        if not location or len(location.strip()) < 2:
            return False

        locationLower = location.lower()

        isKnownCity = locationLower in self.majorCities
        hasLocationPattern = bool(re.search(r"^[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*(?:,\s*[A-Z]{2,})?", location))
        nonLocationWords = {"conference", "summit", "workshop", "meeting", "event", "the", "and", "or"}
        hasNonLocationWords = any(word.lower() in nonLocationWords for word in location.split())

        return (isKnownCity or hasLocationPattern) and not hasNonLocationWords

    def _validateDate(self, date: str) -> bool:
        if not date:
            return False

        datePatterns = [
            r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+\d{4}\b",
            r"\b\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4}\b",
            r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b",
            r"\b\d{4}[/-]\d{1,2}[/-]\d{1,2}\b",
        ]

        return any(re.search(pattern, date, re.IGNORECASE) for pattern in datePatterns)

    def _calculatePersonNameConfidence(self, name: str) -> ExtractionConfidence:
        words = [word.lower() for word in name.split()]
        score = 0

        if any(word in self.commonFirstNames for word in words):
            score += 3
        if any(word in self.commonLastNames for word in words):
            score += 3
        if all(word[0].isupper() and word[1:].islower() for word in name.split()):
            score += 2
        if len(words) == 2:
            score += 2
        elif len(words) > 4:
            score -= 1

        if score >= 5:
            return ExtractionConfidence.HIGH
        elif score >= 3:
            return ExtractionConfidence.MEDIUM
        else:
            return ExtractionConfidence.LOW

    def _calculateEventNameConfidence(self, eventName: str, fullText: str) -> ExtractionConfidence:
        score = 0
        eventLower = eventName.lower()

        if any(indicator in eventLower for indicator in self.eventTypeIndicators):
            score += 4
        if any(keyword in eventLower for keyword in self.domainKeywords):
            score += 3
        if re.search(r"\b20\d{2}\b", eventName):
            score += 2
        if any(verb in fullText.lower() for verb in self.registrationVerbs):
            score += 2
        if eventName and eventName[0].isupper():
            score += 1

        if score >= 6:
            return ExtractionConfidence.HIGH
        elif score >= 3:
            return ExtractionConfidence.MEDIUM
        else:
            return ExtractionConfidence.LOW

    def _calculateLocationConfidence(self, location: str) -> ExtractionConfidence:
        score = 0
        locationLower = location.lower()
        if locationLower in self.majorCities:
            score += 4
        if re.search(r"^[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*(?:,\s*[A-Z]{2,})?", location):
            score += 3
        if 3 <= len(location) <= 30:
            score += 1

        if score >= 4:
            return ExtractionConfidence.HIGH
        elif score >= 2:
            return ExtractionConfidence.MEDIUM
        else:
            return ExtractionConfidence.LOW

    def _calculateDateConfidence(self, date: str) -> ExtractionConfidence:
        if re.search(r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)", date, re.IGNORECASE):
            return ExtractionConfidence.HIGH
        elif re.search(r"\d{4}", date):
            return ExtractionConfidence.MEDIUM
        else:
            return ExtractionConfidence.LOW

    def _cleanLocationText(self, locationText: str) -> str:
        locationText = re.sub(r"^\s*(?:in|at|near)\s+", "", locationText, flags=re.IGNORECASE)
        return locationText.strip()

    def _cleanDateText(self, dateText: str) -> str:
        dateText = re.sub(r"^\s*(?:on|date|scheduled for)\s+", "", dateText, flags=re.IGNORECASE)
        return dateText.strip()

    def _removeDuplicatesAndOverlaps(self, entities: List[ExtractedEntity]) -> List[ExtractedEntity]:
        """Remove duplicate and overlapping entities by keeping the higher-confidence one."""
        if not entities:
            return entities

        entities.sort(key=lambda x: x.startPosition)
        cleaned: List[ExtractedEntity] = []

        for entity in entities:
            hasOverlap = False
            for existingEntity in list(cleaned):
                if (entity.startPosition < existingEntity.endPosition and entity.endPosition > existingEntity.startPosition):
                    # Keep the one with higher confidence (use .value if enum)
                    e_conf = getattr(existingEntity.confidence, "value", existingEntity.confidence)
                    n_conf = getattr(entity.confidence, "value", entity.confidence)
                    if n_conf > e_conf:
                        cleaned.remove(existingEntity)
                        cleaned.append(entity)
                    hasOverlap = True
                    break

            if not hasOverlap:
                cleaned.append(entity)

        return cleaned

    def _enhanceWithContext(self, entities: List[ExtractedEntity], text: str) -> List[ExtractedEntity]:
        for entity in entities:
            contextScore = self._analyzeEntityContext(entity, text)
            if contextScore > 0:
                if entity.confidence == ExtractionConfidence.LOW:
                    entity.confidence = ExtractionConfidence.MEDIUM
                elif entity.confidence == ExtractionConfidence.MEDIUM:
                    entity.confidence = ExtractionConfidence.HIGH
        return entities

    def _analyzeEntityContext(self, entity: ExtractedEntity, text: str) -> int:
        contextWindow = 50
        start = max(0, entity.startPosition - contextWindow)
        end = min(len(text), entity.endPosition + contextWindow)
        context = text[start:end].lower()
        score = 0

        if entity.entityType == EntityType.PERSON:
            personContextKeywords = ["registered", "participant", "attendee", "mr", "mrs", "dr"]
            score += sum(1 for keyword in personContextKeywords if keyword in context)
        elif entity.entityType == EntityType.EVENT:
            eventContextKeywords = ["registered for", "attending", "conference", "summit"]
            score += sum(1 for keyword in eventContextKeywords if keyword in context)
        elif entity.entityType == EntityType.LOCATION:
            locationContextKeywords = ["in", "at", "held in", "located"]
            score += sum(1 for keyword in locationContextKeywords if keyword in context)
        elif entity.entityType == EntityType.DATE:
            dateContextKeywords = ["on", "scheduled", "happening"]
            score += sum(1 for keyword in dateContextKeywords if keyword in context)

        return score

    # --- required abstract method implementations ---

    def getExtractorName(self) -> str:
        """Get the name of this extractor."""
        return "HybridNamedEntityExtractor"

    def getExtractorVersion(self) -> str:
        """Return the extractor version."""
        return getattr(self, "_version", "1.0.0")

    def getSupportedEntityTypes(self) -> List[str]:
        """Get list of supported entity types (as strings)."""
        # Convert the set to a sorted list of strings
        return sorted(list(self._supportedEntityTypes))

    def isEntityTypeSupported(self, entityType: str) -> bool:
        """Check if a given entity type is supported. Accepts enum name or string."""
        if not entityType:
            return False
        # normalize
        normalized = entityType.strip().upper()
        return normalized in self._supportedEntityTypes

    def getPerformanceMetrics(self) -> Dict[str, Any]:
        """Return basic performance metrics for monitoring."""
        success_rate = (self._successfulExtractions / self._extractionCount * 100) if self._extractionCount else 0.0
        return {
            "extractions_run": self._extractionCount,
            "successful_extractions": self._successfulExtractions,
            "success_rate_percent": success_rate,
            "supported_entity_types_count": len(self._supportedEntityTypes),
            "supported_entity_types": self.getSupportedEntityTypes(),  # Added this for completeness
            "version": self.getExtractorVersion(),
        }

    def getLastError(self) -> Optional[str]:
        """Return the last recorded error message, if any."""
        return self._lastError

    def clearErrors(self) -> None:
        """Clear the last error."""
        self._lastError = None