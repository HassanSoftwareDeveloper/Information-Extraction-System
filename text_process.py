"""
Advanced Text Preprocessing Service for Information Extraction
"""

import re
import unicodedata
from typing import Any, Dict, List, Tuple, Optional
from abstract_extractor import AbstractTextPreprocessor

class AdvancedTextPreprocessor(AbstractTextPreprocessor):
    """Advanced text preprocessing with multiple normalization techniques."""
    
    def __init__(self) -> None:
        """Initialize preprocessor with patterns and configurations."""
        self._initializePatterns()
        self._initializeReplacementMaps()
        self._initializeConfiguration()
    
    def _initializePatterns(self) -> None:
        """Initialize regex patterns for text processing."""
        self.patterns = {
            'extraWhitespace': re.compile(r'\s+'),
            'specialChars': re.compile(r'[^\w\s\-.,!?;:()\[\]{}"\']'),
            'emailPattern': re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'),
            'phonePattern': re.compile(r'(\+\d{1,3}\s?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}'),
            'datePatterns': [
                re.compile(r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b'),
                re.compile(r'\b\d{4}[/-]\d{1,2}[/-]\d{1,2}\b'),
                re.compile(r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2},? \d{4}\b', re.IGNORECASE),
                re.compile(r'\b\d{1,2} (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{4}\b', re.IGNORECASE)
            ],
            'urlPattern': re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'),
            'sentencePattern': re.compile(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s')
        }
    
    def _initializeReplacementMaps(self) -> None:
        """Initialize replacement maps for text normalization."""
        self.commonReplacements = {
            '&amp;': 'and',
            '&': 'and',
            '@': 'at',
            '#': 'number',
            '%': 'percent',
            '$': 'dollar',
            '€': 'euro',
            '£': 'pound',
            '®': '',
            '©': '',
            '™': ''
        }
        
        self.eventKeywords = [
            'conference', 'summit', 'workshop', 'seminar', 'meetup', 'symposium',
            'expo', 'convention', 'forum', 'congress', 'festival', 'competition',
            'tournament', 'championship', 'ceremony', 'celebration', 'gathering',
            'webinar', 'training', 'lecture', 'session', 'event', 'show'
        ]
        
        self.registrationKeywords = [
            'registered', 'signed up', 'enrolled', 'joined', 'participated',
            'attended', 'booked', 'reserved', 'confirmed', 'applied', 'registered for',
            'signed up for', 'enrolled in', 'joined the', 'participated in'
        ]
    
    def _initializeConfiguration(self) -> None:
        """Initialize preprocessor configuration."""
        self.config = {
            'preserveCaseForEntities': True,
            'normalizeDates': True,
            'normalizeLocations': True,
            'enhanceContext': True,
            'fixCommonErrors': True,
            'removeUrls': True,
            'removeEmails': False,
            'removePhones': False,
            'minTextLength': 10,
            'maxTextLength': 10000
        }
    
    def preprocessText(self, text: str) -> str:
        """
        Main preprocessing pipeline.
        """
        if not text or not isinstance(text, str):
            raise ValueError("Input text must be a non-empty string")
        
        text = text.strip()
        if len(text) < self.config['minTextLength']:
            raise ValueError(f"Text too short (minimum {self.config['minTextLength']} characters required)")
        
        if len(text) > self.config['maxTextLength']:
            raise ValueError(f"Text too long (maximum {self.config['maxTextLength']} characters allowed)")
        
        processed = self.cleanText(text)
        processed = self.normalizeText(processed)
        processed = self._applyAdvancedPreprocessing(processed)
        
        return processed.strip()
    
    def cleanText(self, text: str) -> str:
        """Clean text by removing unwanted characters and formatting."""
        if not text:
            return ""
        
        if self.config['removeUrls']:
            cleaned = self.patterns['urlPattern'].sub('[URL]', text)
        else:
            cleaned = text
        
        if self.config['removeEmails']:
            cleaned = self.patterns['emailPattern'].sub('[EMAIL]', cleaned)
        
        if self.config['removePhones']:
            cleaned = self.patterns['phonePattern'].sub('[PHONE]', cleaned)
        
        cleaned = unicodedata.normalize('NFKD', cleaned)
        
        for original, replacement in self.commonReplacements.items():
            cleaned = cleaned.replace(original, replacement)
        
        cleaned = re.sub(r'([.!?]){2,}', r'\1', cleaned)
        cleaned = re.sub(r'([,:;]){2,}', r'\1', cleaned)
        
        cleaned = self.patterns['extraWhitespace'].sub(' ', cleaned)
        
        return cleaned.strip()
    
    def normalizeText(self, text: str) -> str:
        """Normalize text format for consistent processing."""
        if not text:
            return ""
        
        normalized = text.lower()
        
        if self.config.get('normalizeEventTerms'):
            normalized = self._normalizeEventTerms(normalized)
        
        if self.config['normalizeLocations']:
            normalized = self._normalizeLocationTerms(normalized)
        
        if self.config['normalizeDates']:
            normalized = self._normalizeDateTerms(normalized)
        
        normalized = re.sub(r'\s*([,.!?;:])\s*', r'\1 ', normalized)
        normalized = re.sub(r'\s+', ' ', normalized)
        
        return normalized.strip()
    
    def _normalizeEventTerms(self, text: str) -> str:
        eventReplacements = {
            'tech conference': 'technology conference',
            'ai summit': 'artificial intelligence summit',
            'ml workshop': 'machine learning workshop',
            'dev meetup': 'developer meetup',
            'startup expo': 'startup exposition',
            'data sci': 'data science',
            'web dev': 'web development',
            'ux/ui': 'user experience user interface',
            'iot': 'internet of things'
        }
        
        for variation, standard in eventReplacements.items():
            text = text.replace(variation, standard)
        
        return text
    
    def _normalizeLocationTerms(self, text: str) -> str:
        locationReplacements = {
            'nyc': 'new york city',
            'sf': 'san francisco',
            'la': 'los angeles',
            'uk': 'united kingdom',
            'usa': 'united states',
            'uae': 'united arab emirates',
            'u.s.': 'united states',
            'u.s.a.': 'united states',
            'ny': 'new york',
            'ca': 'california',
            'tx': 'texas',
            'fl': 'florida'
        }
        
        for abbreviation, fullForm in locationReplacements.items():
            text = re.sub(r'\b' + re.escape(abbreviation) + r'\b', fullForm, text, flags=re.IGNORECASE)
        
        return text
    
    def _normalizeDateTerms(self, text: str) -> str:
        monthReplacements = {
            'january': 'jan', 'february': 'feb', 'march': 'mar',
            'april': 'apr', 'may': 'may', 'june': 'jun',
            'july': 'jul', 'august': 'aug', 'september': 'sep',
            'october': 'oct', 'november': 'nov', 'december': 'dec'
        }
        
        for fullMonth, abbrev in monthReplacements.items():
            text = re.sub(r'\b' + fullMonth + r'\b', abbrev, text, flags=re.IGNORECASE)
        
        text = re.sub(r'(\d{1,2})/(\d{1,2})/(\d{4})', r'\1-\2-\3', text)
        text = re.sub(r'(\d{4})/(\d{1,2})/(\d{1,2})', r'\1-\2-\3', text)
        
        return text
    
    def _applyAdvancedPreprocessing(self, text: str) -> str:
        if self.config['enhanceContext']:
            text = self._enhanceKeywordContext(text)
        
        if self.config['fixCommonErrors']:
            text = self._fixCommonErrors(text)
        
        text = self._standardizeFormatting(text)
        
        return text
    
    def _enhanceKeywordContext(self, text: str) -> str:
        for keyword in self.registrationKeywords:
            pattern = r'\b' + re.escape(keyword) + r'\b'
            text = re.sub(pattern, f'[REG_ACTION]{keyword}[/REG_ACTION]', text, flags=re.IGNORECASE)
        
        for keyword in self.eventKeywords:
            pattern = r'\b' + re.escape(keyword) + r'\b'
            text = re.sub(pattern, f'[EVENT_TYPE]{keyword}[/EVENT_TYPE]', text, flags=re.IGNORECASE)
        
        return text
    
    def _fixCommonErrors(self, text: str) -> str:
        commonErrors = {
            r'\bl\b': 'I',
            r'\bO\b': '0',
            r'rneetup': 'meetup',
            r'conferenoe': 'conference',
            r'reglstered': 'registered',
            r'symposlum': 'symposium',
            r'partlclpated': 'participated',
            r'technlcal': 'technical',
            r'lnformatlon': 'information'
        }
        
        for error, correction in commonErrors.items():
            text = re.sub(error, correction, text, flags=re.IGNORECASE)
        
        return text
    
    def _standardizeFormatting(self, text: str) -> str:
        text = re.sub(r'([.!?])\s*([A-Z])', r'\1 \2', text)
        text = re.sub(r'([,:;])\s*', r'\1 ', text)
        
        text = re.sub(r'\s*\(\s*', ' (', text)
        text = re.sub(r'\s*\)\s*', ') ', text)
        
        text = re.sub(r'\s*"\s*', '"', text)
        text = re.sub(r"\s*'\s*", "'", text)
        
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()
    
    def extractStructuralElements(self, text: str) -> Dict[str, List[str]]:
        elements = {
            'emails': self.patterns['emailPattern'].findall(text),
            'phones': self.patterns['phonePattern'].findall(text),
            'dates': [],
            'sentences': self._splitIntoSentences(text),
            'capitalizedWords': re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text),
            'urls': self.patterns['urlPattern'].findall(text)
        }
        
        for pattern in self.patterns['datePatterns']:
            elements['dates'].extend(pattern.findall(text))
        
        return elements
    
    def _splitIntoSentences(self, text: str) -> List[str]:
        sentences = self.patterns['sentencePattern'].split(text)
        return [s.strip() for s in sentences if s.strip()]
    
    def configure(self, configUpdates: Dict[str, Any]) -> bool:
        try:
            for key, value in configUpdates.items():
                if key in self.config:
                    self.config[key] = value
            return True
        except Exception:
            return False
    
    def getConfiguration(self) -> Dict[str, Any]:
        return dict(self.config)
    
    def resetConfiguration(self) -> None:
        self._initializeConfiguration()

    # ---------------- Required abstract methods ---------------- #

    def detectLanguage(self, text: str) -> str:
        """Detect language of the text. Default English."""
        return "en"

    def removeNoise(self, text: str) -> str:
        """Remove unwanted noise characters."""
        return re.sub(r"[^a-zA-Z0-9\s.,!?;:()-]", "", text).strip()

    def tokenizeText(self, text: str) -> List[str]:
        """Tokenize text into words."""
        return text.split()
