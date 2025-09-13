"""
Service Facade for Event Registration Information Extraction System
Provides a unified interface for all extraction operations
"""

from typing import Dict, Any, List, Optional, Tuple
from extraction_engine import ComprehensiveExtractionEngine
from template_generation import EventRegistrationTemplateGenerator
from data_model import ExtractionResult

class EventRegistrationExtractionService:
    """Unified service facade for event registration information extraction."""
    
    def __init__(self) -> None:
        """Initialize the service with all required components."""
        self._initializeComponents()
        self._initializeConfiguration()
    
    def _initializeComponents(self) -> None:
        """Initialize core service components."""
        self.extractionEngine = ComprehensiveExtractionEngine()
        self.templateGenerator = EventRegistrationTemplateGenerator()
        
        # Service state
        self.isInitialized = True
        self.lastError = None
    
    def _initializeConfiguration(self) -> None:
        """Initialize service configuration."""
        self.config = {
            'defaultTemplateType': 'standard',
            'enableBatchProcessing': True,
            'maxBatchSize': 100,
            'enableCaching': True,
            'logProcessingMetrics': True
        }
        
        # Cache for processed results (simple in-memory cache)
        self.resultCache = {}
        self.cacheMaxSize = 50
    
    def extractInformation(self, text: str, templateType: str = 'standard') -> Dict[str, Any]:
        """
        Extract information from text and return formatted result.
        
        Args:
            text: Input text containing event registration information
            templateType: Type of output template to generate
            
        Returns:
            Dictionary containing extraction result and formatted output
        """
        try:
            self.lastError = None
            
            # Validate input
            if not self._validateInput(text):
                return self._createErrorResponse("Invalid input text")
            
            # Check cache if enabled
            if self.config['enableCaching']:
                cacheKey = self._generateCacheKey(text, templateType)
                if cacheKey in self.resultCache:
                    return self.resultCache[cacheKey]
            
            # Perform extraction
            extractionResult = self.extractionEngine.extractInformation(text)
            
            # Generate formatted output
            formattedOutput = self.templateGenerator.generateTemplate(extractionResult, templateType)
            
            # Prepare response
            response = {
                'success': extractionResult.isSuccessful(),
                'extractedData': {
                    'participantName': extractionResult.registrationInfo.participantName,
                    'eventName': extractionResult.registrationInfo.eventName,
                    'location': extractionResult.registrationInfo.location,
                    'date': extractionResult.registrationInfo.date
                },
                'formattedOutput': formattedOutput,
                'metadata': {
                    'confidence': extractionResult.registrationInfo.overallConfidence.value,
                    'completionPercentage': extractionResult.registrationInfo.getCompletionPercentage(),
                    'processingTimeMs': extractionResult.processingTimeMs,
                    'extractionMethod': extractionResult.extractionMethod,
                    'entityCount': len(extractionResult.registrationInfo.extractedEntities),
                    'timestamp': extractionResult.registrationInfo.extractionTimestamp.isoformat()
                },
                'warnings': extractionResult.warnings,
                'errors': extractionResult.errorMessages
            }
            
            # Cache result if enabled
            if self.config['enableCaching']:
                self._cacheResult(cacheKey, response)
            
            return response
            
        except Exception as e:
            self.lastError = str(e)
            return self._createErrorResponse(f"Service error: {str(e)}")
    
    def extractBatch(self, texts: List[str], templateType: str = 'standard') -> Dict[str, Any]:
        """
        Extract information from multiple texts in batch.
        
        Args:
            texts: List of input texts
            templateType: Template type for formatting
            
        Returns:
            Dictionary containing batch processing results
        """
        try:
            if not self.config['enableBatchProcessing']:
                return self._createErrorResponse("Batch processing is disabled")
            
            if len(texts) > self.config['maxBatchSize']:
                return self._createErrorResponse(f"Batch size exceeds maximum limit of {self.config['maxBatchSize']}")
            
            results = []
            successful = 0
            totalProcessingTime = 0
            
            for i, text in enumerate(texts):
                try:
                    result = self.extractInformation(text, templateType)
                    results.append({
                        'index': i,
                        'originalText': text,
                        'result': result
                    })
                    
                    if result['success']:
                        successful += 1
                    
                    totalProcessingTime += result['metadata']['processingTimeMs']
                    
                except Exception as e:
                    results.append({
                        'index': i,
                        'originalText': text,
                        'result': self._createErrorResponse(f"Individual extraction failed: {str(e)}")
                    })
            
            # Generate batch summary
            batchSummary = {
                'totalItems': len(texts),
                'successfulItems': successful,
                'successRate': (successful / len(texts)) * 100 if texts else 0,
                'totalProcessingTime': totalProcessingTime,
                'averageProcessingTime': totalProcessingTime / len(texts) if texts else 0
            }
            
            return {
                'success': True,
                'batchSummary': batchSummary,
                'results': results,
                'batchReport': self.templateGenerator.generateBatchReport(
                    [r['result'] for r in results if 'result' in r], templateType
                )
            }
            
        except Exception as e:
            self.lastError = str(e)
            return self._createErrorResponse(f"Batch processing error: {str(e)}")
    
    def getAvailableTemplates(self) -> Dict[str, str]:
        """Get available output template types."""
        return self.templateGenerator.getAvailableTemplates()
    
    def validateTemplate(self, templateFormat: str) -> Tuple[bool, str]:
        """Validate custom template format."""
        return self.templateGenerator.validateTemplate(templateFormat)
    
    def generateCustomOutput(self, text: str, customTemplate: str) -> Dict[str, Any]:
        """Generate output using custom template format."""
        try:
            # First extract information
            extractionResult = self.extractionEngine.extractInformation(text)
            
            # Generate custom output
            customOutput = self.templateGenerator.generateCustomTemplate(extractionResult, customTemplate)
            
            return {
                'success': True,
                'customOutput': customOutput,
                'metadata': {
                    'confidence': extractionResult.registrationInfo.overallConfidence.value,
                    'completionPercentage': extractionResult.registrationInfo.getCompletionPercentage(),
                    'processingTimeMs': extractionResult.processingTimeMs
                }
            }
            
        except Exception as e:
            self.lastError = str(e)
            return self._createErrorResponse(f"Custom template generation error: {str(e)}")
    
    def getServiceStatistics(self) -> Dict[str, Any]:
        """Get comprehensive service statistics."""
        try:
            engineStats = self.extractionEngine.getProcessingStatistics()
            engineMetadata = self.extractionEngine.getEngineMetadata()
            
            return {
                'serviceInfo': {
                    'initialized': self.isInitialized,
                    'lastError': self.lastError,
                    'configuration': dict(self.config)
                },
                'processingStatistics': engineStats,
                'engineMetadata': engineMetadata,
                'cacheStatistics': {
                    'enabled': self.config['enableCaching'],
                    'currentSize': len(self.resultCache),
                    'maxSize': self.cacheMaxSize
                }
            }
            
        except Exception as e:
            return {'error': f"Failed to get statistics: {str(e)}"}
    
    def configureSe(self, configUpdates: Dict[str, Any]) -> bool:
        """Update service configuration."""
        try:
            for key, value in configUpdates.items():
                if key in self.config:
                    self.config[key] = value
                else:
                    return False
            return True
        except Exception:
            return False
    
    def resetService(self) -> bool:
        """Reset service state and clear cache."""
        try:
            self.extractionEngine.resetMetrics()
            self.resultCache.clear()
            self.lastError = None
            return True
        except Exception:
            return False
    
    def exportResults(self, results: List[Dict], exportFormat: str = 'json') -> Optional[str]:
        """Export results to various formats."""
        try:
            if exportFormat.lower() == 'json':
                import json
                return json.dumps(results, indent=2, ensure_ascii=False)
            
            elif exportFormat.lower() == 'csv':
                return self._exportToCsv(results)
            
            elif exportFormat.lower() == 'xml':
                return self._exportToXml(results)
            
            else:
                return None
                
        except Exception:
            return None
    
    def _validateInput(self, text: str) -> bool:
        """Validate input text."""
        if not text or not isinstance(text, str):
            return False
        
        if not text.strip():
            return False
        
        if len(text.strip()) < 10:  # Minimum meaningful text length
            return False
        
        return True
    
    def _generateCacheKey(self, text: str, templateType: str) -> str:
        """Generate cache key for text and template type."""
        import hashlib
        content = f"{text.strip()}{templateType}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def _cacheResult(self, key: str, result: Dict[str, Any]) -> None:
        """Cache processing result."""
        # Simple LRU cache implementation
        if len(self.resultCache) >= self.cacheMaxSize:
            # Remove oldest entry
            oldestKey = next(iter(self.resultCache))
            del self.resultCache[oldestKey]
        
        self.resultCache[key] = result
    
    def _createErrorResponse(self, errorMessage: str) -> Dict[str, Any]:
        """Create standardized error response."""
        return {
            'success': False,
            'error': errorMessage,
            'extractedData': {
                'participantName': None,
                'eventName': None,
                'location': None,
                'date': None
            },
            'formattedOutput': f"Error: {errorMessage}",
            'metadata': {
                'confidence': 'UNKNOWN',
                'completionPercentage': 0.0,
                'processingTimeMs': 0.0,
                'extractionMethod': 'ERROR',
                'entityCount': 0,
                'timestamp': None
            },
            'warnings': [],
            'errors': [errorMessage]
        }
    
    def _exportToCsv(self, results: List[Dict]) -> str:
        """Export results to CSV format."""
        import csv
        import io
        
        output = io.StringIO()
        
        if not results:
            return ""
        
        # Define CSV headers
        headers = [
            'Success', 'Participant Name', 'Event Name', 'Location', 'Date',
            'Confidence', 'Completion %', 'Processing Time (ms)', 'Errors'
        ]
        
        writer = csv.writer(output)
        writer.writerow(headers)
        
        for result in results:
            extracted = result.get('extractedData', {})
            metadata = result.get('metadata', {})
            
            row = [
                result.get('success', False),
                extracted.get('participantName', ''),
                extracted.get('eventName', ''),
                extracted.get('location', ''),
                extracted.get('date', ''),
                metadata.get('confidence', ''),
                metadata.get('completionPercentage', 0),
                metadata.get('processingTimeMs', 0),
                '; '.join(result.get('errors', []))
            ]
            
            writer.writerow(row)
        
        return output.getvalue()
    
    def _exportToXml(self, results: List[Dict]) -> str:
        """Export results to XML format."""
        xml_lines = ['<?xml version="1.0" encoding="UTF-8"?>']
        xml_lines.append('<extractionResults>')
        
        for i, result in enumerate(results):
            xml_lines.append(f'  <result index="{i}">')
            xml_lines.append(f'    <success>{result.get("success", False)}</success>')
            
            extracted = result.get('extractedData', {})
            xml_lines.append('    <extractedData>')
            xml_lines.append(f'      <participantName>{self._escapeXml(extracted.get("participantName", ""))}</participantName>')
            xml_lines.append(f'      <eventName>{self._escapeXml(extracted.get("eventName", ""))}</eventName>')
            xml_lines.append(f'      <location>{self._escapeXml(extracted.get("location", ""))}</location>')
            xml_lines.append(f'      <date>{self._escapeXml(extracted.get("date", ""))}</date>')
            xml_lines.append('    </extractedData>')
            
            metadata = result.get('metadata', {})
            xml_lines.append('    <metadata>')
            xml_lines.append(f'      <confidence>{metadata.get("confidence", "")}</confidence>')
            xml_lines.append(f'      <completionPercentage>{metadata.get("completionPercentage", 0)}</completionPercentage>')
            xml_lines.append(f'      <processingTimeMs>{metadata.get("processingTimeMs", 0)}</processingTimeMs>')
            xml_lines.append('    </metadata>')
            
            xml_lines.append('  </result>')
        
        xml_lines.append('</extractionResults>')
        return '\n'.join(xml_lines)
    
    def _escapeXml(self, text: str) -> str:
        """Escape XML special characters."""
        if not text:
            return ""
        
        return (text.replace('&', '&amp;')
                   .replace('<', '&lt;')
                   .replace('>', '&gt;')
                   .replace('"', '&quot;')
                   .replace("'", '&apos;'))