"""
Template Generation Service for Event Registration Confirmations
"""

from typing import Dict, Any, Optional, List, Tuple, Union
from datetime import datetime
from data_model import EventRegistrationInfo, ExtractionResult, ExtractionConfidence
import json

class EventRegistrationTemplateGenerator:
    """Generates formatted templates for event registration confirmations."""
    
    def __init__(self) -> None:
        """Initialize template generator with configurations."""
        self._initializeTemplates()
        self._initializeFormatters()
    
    def _initializeTemplates(self) -> None:
        """Initialize template formats."""
        self.templates = {
            'standard': {
                'title': 'Event Registration Confirmation',
                'format': """Event Registration Confirmation

Participant Name: {participantName}
Event: {eventName}
Location: {location}
Date: {date}

Status: {status}
Extraction Confidence: {confidence}
Completion: {completionPercentage}%

Generated on: {timestamp}"""
            },
            
            'detailed': {
                'title': 'Detailed Event Registration Report',
                'format': """========================================
DETAILED EVENT REGISTRATION REPORT
========================================

PARTICIPANT INFORMATION:
  Name: {participantName}
  
EVENT DETAILS:
  Event Name: {eventName}
  Location: {location}
  Date: {date}
  
EXTRACTION SUMMARY:
  Overall Confidence: {confidence}
  Completion Rate: {completionPercentage}%
  Extraction Method: {extractionMethod}
  Processing Time: {processingTime} ms
  Status: {status}
  
QUALITY METRICS:
  Entities Extracted: {entityCount}
  High Confidence Fields: {highConfidenceCount}
  Validation Status: {validationStatus}
  
{additionalInfo}

Generated: {timestamp}
========================================"""
            },
            
            'compact': {
                'title': 'Registration Summary',
                'format': """{participantName} → {eventName}
📍 {location} | 📅 {date}
✅ {status} ({confidence})"""
            },
            
            'json': {
                'title': 'JSON Format',
                'format': 'json'
            },
            
            'xml': {
                'title': 'XML Format',
                'format': """<?xml version="1.0" encoding="UTF-8"?>
<eventRegistration>
    <participant>
        <name>{participantName}</name>
    </participant>
    <event>
        <name>{eventName}</name>
        <location>{location}</location>
        <date>{date}</date>
    </event>
    <extraction>
        <confidence>{confidence}</confidence>
        <completionPercentage>{completionPercentage}</completionPercentage>
        <status>{status}</status>
        <timestamp>{timestamp}</timestamp>
    </extraction>
</eventRegistration>"""
            },
            
            'html': {
                'title': 'HTML Format',
                'format': """<!DOCTYPE html>
<html>
<head>
    <title>Event Registration Confirmation</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .header {{ background-color: #f0f8ff; padding: 15px; border-radius: 5px; }}
        .info-grid {{ display: grid; grid-template-columns: 1fr 2fr; gap: 10px; margin: 15px 0; }}
        .label {{ font-weight: bold; color: #333; }}
        .value {{ color: #666; }}
        .status {{ padding: 5px 10px; border-radius: 3px; color: white; }}
        .complete {{ background-color: #28a745; }}
        .partial {{ background-color: #ffc107; color: black; }}
        .incomplete {{ background-color: #dc3545; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Event Registration Confirmation</h1>
        <p>Generated on {timestamp}</p>
    </div>
    
    <div class="info-grid">
        <div class="label">Participant Name:</div>
        <div class="value">{participantName}</div>
        
        <div class="label">Event:</div>
        <div class="value">{eventName}</div>
        
        <div class="label">Location:</div>
        <div class="value">{location}</div>
        
        <div class="label">Date:</div>
        <div class="value">{date}</div>
        
        <div class="label">Status:</div>
        <div class="value">
            <span class="status {statusClass}">{status}</span>
        </div>
        
        <div class="label">Confidence:</div>
        <div class="value">{confidence}</div>
        
        <div class="label">Completion:</div>
        <div class="value">{completionPercentage}%</div>
    </div>
    
    {warningsSection}
    {extractionDetails}
</body>
</html>"""
            },
            
            'email': {
                'title': 'Email Template',
                'format': """Subject: Event Registration Confirmation: {eventName}

Dear {participantName},

Thank you for registering for the following event:

Event: {eventName}
Date: {date}
Location: {location}

Your registration has been {statusLower}. Please keep this confirmation for your records.

If you have any questions, please contact us at events@example.com.

Best regards,
Event Management Team

---
Confidence Level: {confidence}
Generated on: {timestamp}"""
            },
            
            'markdown': {
                'title': 'Markdown Format',
                'format': """# Event Registration Confirmation

## Participant Information
- **Name**: {participantName}

## Event Details
- **Event**: {eventName}
- **Location**: {location}
- **Date**: {date}

## Extraction Summary
- **Status**: {status}
- **Confidence**: {confidence}
- **Completion**: {completionPercentage}%
- **Processing Time**: {processingTime} ms

## Quality Metrics
- **Entities Extracted**: {entityCount}
- **High Confidence Fields**: {highConfidenceCount}

{additionalInfo}

*Generated on {timestamp}*"""
            }
        }
    
    def _initializeFormatters(self) -> None:
        """Initialize value formatters."""
        self.formatters = {
            'participantName': self._formatParticipantName,
            'eventName': self._formatEventName,
            'location': self._formatLocation,
            'date': self._formatDate,
            'status': self._formatStatus,
            'confidence': self._formatConfidence,
            'timestamp': self._formatTimestamp
        }
    
    def generateTemplate(self, result: ExtractionResult, templateType: str = 'standard') -> str:
        """Generate formatted template from extraction result.
        
        Args:
            result: ExtractionResult containing registration information
            templateType: Type of template to generate
            
        Returns:
            Formatted template string
        """
        if templateType not in self.templates:
            raise ValueError(f"Unknown template type: {templateType}. Available types: {list(self.templates.keys())}")
        
        template = self.templates[templateType]
        
        if templateType == 'json':
            return self._generateJsonTemplate(result)
        
        # Prepare template variables
        templateVars = self._prepareTemplateVariables(result)
        
        # Special handling for HTML template
        if templateType == 'html':
            return self._generateHtmlTemplate(result, templateVars)
        elif templateType == 'email':
            return self._generateEmailTemplate(result, templateVars)
        else:
            return template['format'].format(**templateVars)
    
    def generateAllTemplates(self, result: ExtractionResult) -> Dict[str, str]:
        """Generate all available template formats.
        
        Args:
            result: ExtractionResult containing registration information
            
        Returns:
            Dictionary with all template formats
        """
        return {
            template_type: self.generateTemplate(result, template_type)
            for template_type in self.templates.keys()
        }
    
    def generateBatchReport(self, results: List[Dict[str, Any]], templateType: str = 'detailed') -> str:
        """Generate batch processing report.
        
        Args:
            results: List of extraction results
            templateType: Template type for individual entries
            
        Returns:
            Batch report string
        """
        if not results:
            return "No results to report."
        
        report_lines = [
            "=" * 60,
            "BATCH PROCESSING REPORT",
            "=" * 60,
            f"Total Items Processed: {len(results)}",
            f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}",
            "",
            "SUMMARY:",
        ]
        
        successful = sum(1 for r in results if r.get('success', False))
        report_lines.extend([
            f"  Successful Extractions: {successful}/{len(results)}",
            f"  Success Rate: {(successful/len(results)*100):.1f}%",
            "",
            "INDIVIDUAL RESULTS:",
            "-" * 30
        ])
        
        for i, result in enumerate(results[:10], 1):  # Show first 10 results
            extracted = result.get('extractedData', {})
            metadata = result.get('metadata', {})
            
            report_lines.extend([
                f"{i}. {extracted.get('participantName', 'N/A')} → {extracted.get('eventName', 'N/A')}",
                f"   Status: {result.get('success', False)}, Confidence: {metadata.get('confidence', 'UNKNOWN')}",
                f"   Completion: {metadata.get('completionPercentage', 0):.1f}%",
                ""
            ])
        
        if len(results) > 10:
            report_lines.append(f"... and {len(results) - 10} more results")
        
        return "\n".join(report_lines)
    
    def _prepareTemplateVariables(self, result: ExtractionResult) -> Dict[str, str]:
        """Prepare variables for template formatting.
        
        Args:
            result: ExtractionResult to extract variables from
            
        Returns:
            Dictionary of formatted template variables
        """
        info = result.registrationInfo
        
        # Count high confidence entities safely
        high_confidence_count = 0
        if hasattr(info, 'extractedEntities') and info.extractedEntities:
            for entity in info.extractedEntities:
                if hasattr(entity, 'confidence') and entity.confidence == ExtractionConfidence.HIGH:
                    high_confidence_count += 1
        
        return {
            'participantName': self._formatParticipantName(info.participantName),
            'eventName': self._formatEventName(info.eventName),
            'location': self._formatLocation(info.location),
            'date': self._formatDate(info.date),
            'status': self._formatStatus(info),
            'statusLower': self._formatStatus(info).lower(),
            'confidence': self._formatConfidence(info.overallConfidence.value if hasattr(info, 'overallConfidence') else 'UNKNOWN'),
            'completionPercentage': f"{info.getCompletionPercentage():.1f}",
            'extractionMethod': result.extractionMethod,
            'processingTime': f"{result.processingTimeMs:.2f}",
            'entityCount': str(len(info.extractedEntities) if hasattr(info, 'extractedEntities') and info.extractedEntities else 0),
            'highConfidenceCount': str(high_confidence_count),
            'validationStatus': 'PASSED' if result.isSuccessful() else 'FAILED',
            'timestamp': self._formatTimestamp(info.extractionTimestamp if hasattr(info, 'extractionTimestamp') else datetime.now()),
            'additionalInfo': self._generateAdditionalInfo(result),
            'statusClass': self._getStatusClass(info)
        }
    
    def _formatParticipantName(self, name: Optional[str]) -> str:
        """Format participant name for display.
        
        Args:
            name: Participant name or None
            
        Returns:
            Formatted participant name
        """
        return name if name else '[Name Not Extracted]'
    
    def _formatEventName(self, eventName: Optional[str]) -> str:
        """Format event name for display.
        
        Args:
            eventName: Event name or None
            
        Returns:
            Formatted event name
        """
        return eventName if eventName else '[Event Name Not Extracted]'
    
    def _formatLocation(self, location: Optional[str]) -> str:
        """Format location for display.
        
        Args:
            location: Location or None
            
        Returns:
            Formatted location
        """
        return location if location else '[Location Not Extracted]'
    
    def _formatDate(self, date: Optional[str]) -> str:
        """Format date for display.
        
        Args:
            date: Date string or None
            
        Returns:
            Formatted date
        """
        return date if date else '[Date Not Extracted]'
    
    def _formatStatus(self, info: EventRegistrationInfo) -> str:
        """Format extraction status.
        
        Args:
            info: EventRegistrationInfo object
            
        Returns:
            Formatted status string
        """
        completion = info.getCompletionPercentage()
        if completion >= 90:
            return 'COMPLETE'
        elif completion >= 70:
            return 'MOSTLY COMPLETE'
        elif completion >= 50:
            return 'PARTIALLY COMPLETE'
        elif completion > 0:
            return 'INCOMPLETE'
        else:
            return 'EXTRACTION FAILED'
    
    def _getStatusClass(self, info: EventRegistrationInfo) -> str:
        """Get CSS class for status.
        
        Args:
            info: EventRegistrationInfo object
            
        Returns:
            CSS class name
        """
        completion = info.getCompletionPercentage()
        if completion >= 90:
            return 'complete'
        elif completion >= 70:
            return 'partial'
        elif completion >= 50:
            return 'partial'
        else:
            return 'incomplete'
    
    def _formatConfidence(self, confidence: str) -> str:
        """Format confidence level for display.
        
        Args:
            confidence: Confidence level string
            
        Returns:
            Formatted confidence string
        """
        return str(confidence).upper()
    
    def _formatTimestamp(self, timestamp: datetime) -> str:
        """Format timestamp for display.
        
        Args:
            timestamp: Datetime object
            
        Returns:
            Formatted timestamp string
        """
        return timestamp.strftime('%Y-%m-%d %H:%M:%S UTC')
    
    def _generateAdditionalInfo(self, result: ExtractionResult) -> str:
        """Generate additional information section.
        
        Args:
            result: ExtractionResult object
            
        Returns:
            Additional information string
        """
        info = []
        
        if hasattr(result, 'warnings') and result.warnings:
            info.append("WARNINGS:")
            for warning in result.warnings:
                info.append(f"  ⚠ {warning}")
            info.append("")
        
        if hasattr(result, 'errorMessages') and result.errorMessages:
            info.append("ERRORS:")
            for error in result.errorMessages:
                info.append(f"  ❌ {error}")
            info.append("")
        
        if not info:
            info.append("No additional information or warnings.")
        
        return "\n".join(info)
    
    def _generateJsonTemplate(self, result: ExtractionResult) -> str:
        """Generate JSON template.
        
        Args:
            result: ExtractionResult object
            
        Returns:
            JSON string
        """
        info = result.registrationInfo
        
        # Count high confidence entities safely
        high_confidence_count = 0
        if hasattr(info, 'extractedEntities') and info.extractedEntities:
            for entity in info.extractedEntities:
                if hasattr(entity, 'confidence') and entity.confidence == ExtractionConfidence.HIGH:
                    high_confidence_count += 1
        
        data = {
            'participant': {
                'name': info.participantName
            },
            'event': {
                'name': info.eventName,
                'location': info.location,
                'date': info.date
            },
            'extraction': {
                'confidence': info.overallConfidence.value if hasattr(info, 'overallConfidence') else 'UNKNOWN',
                'completionPercentage': info.getCompletionPercentage(),
                'status': self._formatStatus(info),
                'method': result.extractionMethod,
                'processingTimeMs': result.processingTimeMs,
                'timestamp': (info.extractionTimestamp if hasattr(info, 'extractionTimestamp') else datetime.now()).isoformat(),
                'entitiesExtracted': len(info.extractedEntities) if hasattr(info, 'extractedEntities') and info.extractedEntities else 0,
                'highConfidenceEntities': high_confidence_count
            },
            'quality': {
                'warnings': result.warnings if hasattr(result, 'warnings') else [],
                'errors': result.errorMessages if hasattr(result, 'errorMessages') else [],
                'isSuccessful': result.isSuccessful() if hasattr(result, 'isSuccessful') else False
            }
        }
        
        return json.dumps(data, indent=2, ensure_ascii=False, default=str)
    
    def _generateHtmlTemplate(self, result: ExtractionResult, templateVars: Dict[str, str]) -> str:
        """Generate HTML template with enhanced formatting.
        
        Args:
            result: ExtractionResult object
            templateVars: Template variables
            
        Returns:
            HTML string
        """
        # Generate warnings section if any
        warnings_section = ""
        if hasattr(result, 'warnings') and result.warnings:
            warnings_html = "".join(f"<li>⚠ {warning}</li>" for warning in result.warnings)
            warnings_section = f"""
            <div class="warnings">
                <h3>Warnings</h3>
                <ul>{warnings_html}</ul>
            </div>"""
        
        # Generate extraction details section
        extraction_details = f"""
        <div class="extraction-details">
            <h3>Extraction Details</h3>
            <p><strong>Method:</strong> {result.extractionMethod}</p>
            <p><strong>Processing Time:</strong> {result.processingTimeMs:.2f} ms</p>
            <p><strong>Entities Extracted:</strong> {len(result.registrationInfo.extractedEntities) if hasattr(result.registrationInfo, 'extractedEntities') and result.registrationInfo.extractedEntities else 0}</p>
        </div>"""
        
        # Add sections to template variables
        templateVars['warningsSection'] = warnings_section
        templateVars['extractionDetails'] = extraction_details
        
        return self.templates['html']['format'].format(**templateVars)
    
    def _generateEmailTemplate(self, result: ExtractionResult, templateVars: Dict[str, str]) -> str:
        """Generate email template with proper formatting.
        
        Args:
            result: ExtractionResult object
            templateVars: Template variables
            
        Returns:
            Email template string
        """
        # Add custom formatting for email
        templateVars['statusLower'] = templateVars['status'].lower()
        return self.templates['email']['format'].format(**templateVars)
    
    def getAvailableTemplates(self) -> Dict[str, str]:
        """Get list of available templates with descriptions.
        
        Returns:
            Dictionary of template information
        """
        return {
            template_type: template_info['title']
            for template_type, template_info in self.templates.items()
        }
    
    def validateTemplate(self, templateFormat: str) -> Tuple[bool, str]:
        """Validate template format.
        
        Args:
            templateFormat: Template format to validate
            
        Returns:
            Tuple of (is_valid, message)
        """
        if not templateFormat or not templateFormat.strip():
            return False, "Template format cannot be empty"
        
        if templateFormat not in self.templates:
            return False, f"Unknown template format. Available: {list(self.templates.keys())}"
        
        return True, "Template format is valid"
    
    def generateCustomTemplate(self, result: ExtractionResult, customTemplate: str) -> str:
        """Generate output using custom template format.
        
        Args:
            result: ExtractionResult object
            customTemplate: Custom template string
            
        Returns:
            Formatted custom template
        """
        try:
            templateVars = self._prepareTemplateVariables(result)
            return customTemplate.format(**templateVars)
        except KeyError as e:
            return f"Error: Template variable {e} not found"
        except Exception as e:
            return f"Error generating custom template: {str(e)}"
    
    def validateTemplateOutput(self, template_output: str, template_type: str) -> bool:
        """Validate that template output is properly formatted.
        
        Args:
            template_output: Generated template output
            template_type: Type of template
            
        Returns:
            True if valid, False otherwise
        """
        if not template_output or not template_output.strip():
            return False
        
        if template_type == 'json':
            try:
                json.loads(template_output)
                return True
            except json.JSONDecodeError:
                return False
        
        # Basic validation for other template types
        required_fields = ['participantName', 'eventName', 'date']
        for field in required_fields:
            if field not in template_output:
                return False
        
        return True
    
    def getTemplatePreview(self, template_type: str, sample_data: Optional[Dict[str, Any]] = None) -> str:
        """Get a preview of a template with sample data.
        
        Args:
            template_type: Type of template to preview
            sample_data: Optional sample data to use
            
        Returns:
            Preview template string
        """
        if sample_data is None:
            sample_data = {
                'participantName': 'John Doe',
                'eventName': 'Tech Conference 2024',
                'location': 'San Francisco Convention Center',
                'date': '2024-03-15',
                'confidence': 'HIGH',
                'completionPercentage': 85.5,
                'extractionMethod': 'Hybrid NER → Information Processing',
                'processingTime': 245.67,
                'entityCount': 12,
                'highConfidenceCount': 8,
                'validationStatus': 'PASSED',
                'timestamp': datetime.now()
            }
        
        # Create mock ExtractionResult for preview
        class MockExtractionResult:
            def __init__(self, data):
                class MockRegistrationInfo:
                    def __init__(self, data):
                        self.participantName = data['participantName']
                        self.eventName = data['eventName']
                        self.location = data['location']
                        self.date = data['date']
                        self.overallConfidence = type('Confidence', (), {'value': data['confidence']})()
                        self.extractedEntities = [type('Entity', (), {'confidence': ExtractionConfidence.HIGH})()] * data['entityCount']
                        self.extractionTimestamp = data['timestamp']
                    
                    def getCompletionPercentage(self):
                        return data['completionPercentage']
                
                self.registrationInfo = MockRegistrationInfo(data)
                self.extractionMethod = data['extractionMethod']
                self.processingTimeMs = data['processingTime']
                self.warnings = []
                self.errorMessages = []
            
            def isSuccessful(self):
                return True
        
        mock_result = MockExtractionResult(sample_data)
        
        return self.generateTemplate(mock_result, template_type)