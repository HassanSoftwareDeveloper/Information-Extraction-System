"""
Main Information Extraction Engine
Orchestrates the complete extraction pipeline
"""

import time
from typing import Dict, Any, List, Optional
from abstract_extractor import AbstractExtractionEngine
from text_process import AdvancedTextPreprocessor
from Name_Entity_Recogniztion import HybridNamedEntityExtractor
from info_processing import AdvancedInformationProcessor
from data_model import ExtractionResult, ProcessingMetrics, EventRegistrationInfo
from logging_config import get_logger  # pyright: ignore[reportMissingImports]


class ComprehensiveExtractionEngine(AbstractExtractionEngine):
    """Main extraction engine that orchestrates the complete pipeline."""

    def __init__(self, config: Optional[Dict[str, bool]] = None) -> None:
        """Initialize the extraction engine with all components.

        Args:
            config: Optional pipeline configuration dictionary
        """
        self.logger = get_logger(__name__)
        self._initializeComponents()
        self._initializeMetrics()

        if config:
            self.configurePipeline(config)

    def _initializeComponents(self) -> None:
        """Initialize all processing components."""
        self.textPreprocessor = AdvancedTextPreprocessor()
        self.entityExtractor = HybridNamedEntityExtractor()
        self.informationProcessor = AdvancedInformationProcessor()

        # Pipeline configuration with defaults
        self.pipelineConfig = {
            "enablePreprocessing": True,
            "enableAdvancedNER": True,
            "enablePostProcessing": True,
            "enableFallbackExtraction": True,
            "enableValidation": True,
            "enableHeuristics": True,
            "enableTemporalAnalysis": True,
        }

    def _initializeMetrics(self) -> None:
        """Initialize processing metrics."""
        self.metrics = ProcessingMetrics()
        self.processingHistory = []

    # -------------------------------------------------------------------------
    # Required abstract method implementations (FIX)
    # -------------------------------------------------------------------------
    def batchExtractInformation(
        self, texts: List[str], context: Optional[Dict[str, Any]] = None
    ) -> List[ExtractionResult]:
        """Extract information from a batch of texts."""
        results = []
        for text in texts:
            results.append(self.extractInformation(text, context))
        return results

    def getEngineVersion(self) -> str:
        """Return engine version string."""
        return "1.0.0"

    def getSupportedLanguages(self) -> List[str]:
        """Return list of supported languages."""
        # Example: English only for now
        return ["en"]

    def isLanguageSupported(self, language: str) -> bool:
        """Check if a language is supported."""
        return language.lower() in self.getSupportedLanguages()

    # -------------------------------------------------------------------------

    def extractInformation(
        self, text: str, context: Optional[Dict[str, Any]] = None
    ) -> ExtractionResult:
        """Extract complete information from text using the full pipeline."""
        startTime = time.time()

        try:
            # Validate input
            if not text or not text.strip():
                return self._createErrorResult("Input text cannot be empty", startTime)

            self.logger.info(f"Starting extraction process for text: {text[:100]}...")

            # Step 1: Text Preprocessing
            preprocessedText = self._preprocessText(text)

            # Step 2: Entity Extraction
            extractedEntities = self._extractEntities(preprocessedText)

            # Step 3: Information Processing
            registrationInfo = self._processInformation(extractedEntities, text, context)

            # Step 4: Validation and Post-processing
            result = self._finalizeResult(registrationInfo, startTime)

            # Update metrics
            self._updateMetrics(result)

            self.logger.info(
                f"Extraction completed in {result.processingTimeMs:.2f}ms with "
                f"{result.registrationInfo.getCompletionPercentage():.1f}% completion"
            )

            return result

        except Exception as e:
            self.logger.error(f"Extraction failed: {str(e)}", exc_info=True)
            return self._createErrorResult(f"Extraction failed: {str(e)}", startTime)

    def _preprocessText(self, text: str) -> str:
        """Preprocess text for extraction."""
        if not self.pipelineConfig["enablePreprocessing"]:
            return text

        try:
            preprocessed = self.textPreprocessor.preprocessText(text)
            self.logger.debug(
                f"Text preprocessing completed. Original length: {len(text)}, "
                f"Processed length: {len(preprocessed)}"
            )
            return preprocessed
        except Exception as e:
            self.logger.warning(f"Preprocessing failed, using original text: {str(e)}")
            return text

    def _extractEntities(self, text: str) -> List:
        """Extract entities from preprocessed text."""
        try:
            entities = self.entityExtractor.extractEntities(text)
            self.logger.debug(f"Extracted {len(entities)} entities from text")
            return entities if entities else []
        except Exception as e:
            self.logger.warning(f"Entity extraction failed: {str(e)}")
            return []

    def _processInformation(
        self, entities: List, originalText: str, context: Optional[Dict[str, Any]] = None
    ):
        """Process extracted entities into structured information."""
        try:
            return self.informationProcessor.processExtractedEntities(
                entities, originalText
            )
        except Exception as e:
            self.logger.warning(f"Information processing failed: {str(e)}")
            return EventRegistrationInfo(originalText=originalText)

    def _finalizeResult(
        self, registrationInfo: EventRegistrationInfo, startTime: float
    ) -> ExtractionResult:
        """Finalize extraction result with validation and metrics."""
        processingTime = (time.time() - startTime) * 1000

        isValid = True
        if self.pipelineConfig["enableValidation"]:
            isValid = self.informationProcessor.validateExtractedInfo(registrationInfo)

        result = ExtractionResult(
            registrationInfo=registrationInfo,
            processingTimeMs=processingTime,
            extractionMethod=self._getExtractionMethodDescription(),
        )

        completion_percentage = registrationInfo.getCompletionPercentage()
        if completion_percentage < 80.0:
            result.warnings.append(
                f"Extraction incomplete: {completion_percentage:.1f}% complete"
            )

        # Remove the validation errors call since the method doesn't exist
        if not isValid:
            result.warnings.append("Some extracted information may not be accurate")

        return result

    def _createErrorResult(
        self, errorMessage: str, startTime: float
    ) -> ExtractionResult:
        """Create error result when extraction fails."""
        processingTime = (time.time() - startTime) * 1000

        return ExtractionResult(
            registrationInfo=EventRegistrationInfo(),
            processingTimeMs=processingTime,
            extractionMethod=self._getExtractionMethodDescription(),
            errorMessages=[errorMessage],
            warnings=["Extraction process encountered errors"],
        )

    def _getExtractionMethodDescription(self) -> str:
        """Get description of extraction method used."""
        methods = []

        if self.pipelineConfig["enablePreprocessing"]:
            methods.append("Advanced Text Preprocessing")

        if self.pipelineConfig["enableAdvancedNER"]:
            methods.append("Hybrid Named Entity Recognition")

        if self.pipelineConfig["enableHeuristics"]:
            methods.append("Rule-based Heuristics")

        if self.pipelineConfig["enableTemporalAnalysis"]:
            methods.append("Temporal Analysis")

        if self.pipelineConfig["enablePostProcessing"]:
            methods.append("Information Processing & Validation")

        if self.pipelineConfig["enableFallbackExtraction"]:
            methods.append("Fallback Pattern Matching")

        return " → ".join(methods)

    def _updateMetrics(self, result: ExtractionResult) -> None:
        """Update processing metrics with new result."""
        self.metrics.updateMetrics(result)

        # Handle confidence correctly
        confidence_value = "UNKNOWN"
        if hasattr(result.registrationInfo, "overallConfidence") and result.registrationInfo.overallConfidence:
            confidence_value = result.registrationInfo.overallConfidence.value

        self.processingHistory.append(
            {
                "timestamp": time.time(),
                "processingTime": result.processingTimeMs,
                "completionPercentage": result.registrationInfo.getCompletionPercentage(),
                "confidence": confidence_value,
                "successful": result.isSuccessful(),
                "entitiesExtracted": len(result.registrationInfo.extractedEntities)
                if hasattr(result.registrationInfo, "extractedEntities") and result.registrationInfo.extractedEntities
                else 0,
            }
        )

        if len(self.processingHistory) > 100:
            self.processingHistory = self.processingHistory[-100:]

    def getEngineMetadata(self) -> Dict[str, Any]:
        """Get engine metadata and capabilities."""
        successful = self.metrics.successfulExtractions
        total = max(1, self.metrics.totalProcessed)

        # FIX: Handle confidenceDistribution properly - ensure it's always a dict
        confidence_dist = {}
        if hasattr(self.metrics, 'confidenceDistribution'):
            if isinstance(self.metrics.confidenceDistribution, dict):
                confidence_dist = dict(self.metrics.confidenceDistribution)
            elif isinstance(self.metrics.confidenceDistribution, list):
                # Convert list to dict if needed
                confidence_dist = {f"item_{i}": item for i, item in enumerate(self.metrics.confidenceDistribution)}
            else:
                confidence_dist = {}

        return {
            "engineName": "ComprehensiveExtractionEngine",
            "version": self.getEngineVersion(),
            "capabilities": {
                "supportedEntityTypes": self._getSupportedEntityTypes(),
                "preprocessingEnabled": self.pipelineConfig["enablePreprocessing"],
                "advancedNEREnabled": self.pipelineConfig["enableAdvancedNER"],
                "postProcessingEnabled": self.pipelineConfig["enablePostProcessing"],
                "fallbackExtractionEnabled": self.pipelineConfig[
                    "enableFallbackExtraction"
                ],
                "validationEnabled": self.pipelineConfig["enableValidation"],
                "heuristicsEnabled": self.pipelineConfig["enableHeuristics"],
                "temporalAnalysisEnabled": self.pipelineConfig[
                    "enableTemporalAnalysis"
                ],
            },
            "components": {
                "textPreprocessor": self.textPreprocessor.__class__.__name__,
                "entityExtractor": self._getExtractorName(),
                "informationProcessor": self.informationProcessor.__class__.__name__,
            },
            "metrics": {
                "totalProcessed": self.metrics.totalProcessed,
                "successRate": (successful / total) * 100,
                "averageProcessingTime": self.metrics.averageProcessingTimeMs,
                "averageCompletionRate": self.metrics.averageCompletionPercentage,
                "confidenceDistribution": confidence_dist,
                "recentPerformance": self.getProcessingStatistics(),
            },
        }

    def _getSupportedEntityTypes(self) -> List[str]:
        """Get supported entity types safely."""
        try:
            if hasattr(self.entityExtractor, 'getSupportedEntityTypes'):
                return self.entityExtractor.getSupportedEntityTypes()
            else:
                # Return default entity types
                return ["PERSON", "EVENT", "LOCATION", "DATE", "ORGANIZATION"]
        except Exception:
            return ["PERSON", "EVENT", "LOCATION", "DATE", "ORGANIZATION"]

    def _getExtractorName(self) -> str:
        """Get extractor name safely."""
        try:
            if hasattr(self.entityExtractor, 'getExtractorName'):
                return self.entityExtractor.getExtractorName()
            else:
                return self.entityExtractor.__class__.__name__
        except Exception:
            return "HybridNamedEntityExtractor"

    def getProcessingStatistics(self) -> Dict[str, Any]:
        """Get detailed processing statistics."""
        if not self.processingHistory:
            return {
                "totalProcessed": 0,
                "recentProcessingTimes": [],
                "recentCompletionRates": [],
                "recentSuccessRate": 0,
                "averageProcessingTime": 0,
                "averageCompletionRate": 0,
                "minProcessingTime": 0,
                "maxProcessingTime": 0,
            }

        recent = (
            self.processingHistory[-10:]
            if len(self.processingHistory) >= 10
            else self.processingHistory
        )

        processing_times = [record["processingTime"] for record in recent]
        completion_rates = [record["completionPercentage"] for record in recent]
        successful_records = [record for record in recent if record["successful"]]

        return {
            "totalProcessed": len(self.processingHistory),
            "recentProcessingTimes": processing_times,
            "recentCompletionRates": completion_rates,
            "recentSuccessRate": len(successful_records) / len(recent) * 100
            if recent
            else 0,
            "averageProcessingTime": sum(processing_times) / len(processing_times)
            if processing_times
            else 0,
            "averageCompletionRate": sum(completion_rates) / len(completion_rates)
            if completion_rates
            else 0,
            "minProcessingTime": min(processing_times) if processing_times else 0,
            "maxProcessingTime": max(processing_times) if processing_times else 0,
        }

    def configurePipeline(self, config: Dict[str, bool]) -> None:
        """Configure pipeline components."""
        for key, value in config.items():
            if key in self.pipelineConfig:
                self.pipelineConfig[key] = value
                self.logger.info(f"Pipeline configuration updated: {key} = {value}")

    def resetMetrics(self) -> None:
        """Reset processing metrics."""
        self.metrics = ProcessingMetrics()
        self.processingHistory = []
        self.logger.info("Processing metrics reset")

    def processMultipleTexts(self, texts: List[str]) -> List[ExtractionResult]:
        """Process multiple texts efficiently."""
        results = []
        self.logger.info(f"Processing batch of {len(texts)} texts")

        for i, text in enumerate(texts):
            result = self.extractInformation(text)
            results.append(result)

            if len(texts) > 10 and (i + 1) % 10 == 0:
                self.logger.info(f"Processed {i + 1}/{len(texts)} texts")

        return results

    def getBenchmarkReport(self) -> Dict[str, Any]:
        """Generate benchmark report for engine performance."""
        stats = self.getProcessingStatistics()
        metadata = self.getEngineMetadata()

        return {
            "engineInfo": {
                "name": metadata["engineName"],
                "version": metadata["version"],
                "components": metadata["components"],
            },
            "performance": {
                "totalProcessed": stats.get("totalProcessed", 0),
                "successRate": metadata["metrics"]["successRate"],
                "averageProcessingTime": stats.get("averageProcessingTime", 0),
                "averageCompletionRate": stats.get("averageCompletionRate", 0),
                "minProcessingTime": stats.get("minProcessingTime", 0),
                "maxProcessingTime": stats.get("maxProcessingTime", 0),
            },
            "quality": {
                "confidenceDistribution": metadata["metrics"]["confidenceDistribution"],
                "recentSuccessRate": stats.get("recentSuccessRate", 0),
                "recentCompletionRates": stats.get("recentCompletionRates", []),
            },
            "configuration": self.pipelineConfig,
            "timestamp": time.time(),
        }

    def getPerformanceInsights(self) -> Dict[str, Any]:
        """Get performance insights and recommendations."""
        stats = self.getProcessingStatistics()
        metadata = self.getEngineMetadata()

        insights = {
            "performanceScore": 0,
            "bottlenecks": [],
            "recommendations": [],
            "configurationReview": [],
        }

        success_rate = metadata["metrics"]["successRate"]
        avg_processing_time = stats.get("averageProcessingTime", 0)
        avg_completion = stats.get("averageCompletionRate", 0)

        time_score = max(0, 100 - (avg_processing_time / 1000))
        success_score = success_rate
        completion_score = avg_completion

        performance_score = (
            (time_score * 0.3) + (success_score * 0.4) + (completion_score * 0.3)
        )
        insights["performanceScore"] = performance_score

        if avg_processing_time > 500:
            insights["bottlenecks"].append("Processing time is high")
            insights["recommendations"].append(
                "Consider disabling some pipeline components for faster processing"
            )

        if success_rate < 80:
            insights["bottlenecks"].append("Low success rate")
            insights["recommendations"].append(
                "Review extraction patterns and consider adding more fallback mechanisms"
            )

        if avg_completion < 70:
            insights["bottlenecks"].append("Low information completion rate")
            insights["recommendations"].append(
                "Enhance entity recognition patterns and add more contextual analysis"
            )

        if not self.pipelineConfig["enableFallbackExtraction"]:
            insights["configurationReview"].append(
                "Fallback extraction is disabled - this may reduce success rate"
            )

        if not self.pipelineConfig["enableValidation"]:
            insights["configurationReview"].append(
                "Validation is disabled - extracted data quality may be lower"
            )

        return insights