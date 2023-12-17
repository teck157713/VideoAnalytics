from DetectAnalytics import logger
from DetectAnalytics.pipeline.stage_01_data_ingestion import DataIngestionTrainingPipeline
from DetectAnalytics.pipeline.stage_02_preparing_model import PrepareModelTrainingPipeline

STAGE_NAME = "Data Ingestion Stage"
try:
    logger.info(f">>> stage {STAGE_NAME} started <<<")
    data_ingestion = DataIngestionTrainingPipeline()
    data_ingestion.main()
    logger.info(f">>> stage {STAGE_NAME} completed <<<\n\nx==========xx")
except Exception as e:
    logger.exception(e)
    raise e
    

STAGE_NAME = "Prepare Model"
try:
    logger.info(f">>> stage {STAGE_NAME} started <<<")
    data_ingestion = PrepareModelTrainingPipeline()
    data_ingestion.main()
    logger.info(f">>> stage {STAGE_NAME} completed <<<\n\nx==========xx")
except Exception as e:
    logger.exception(e)
    raise e