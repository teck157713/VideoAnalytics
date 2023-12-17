from DetectAnalytics import logger
from DetectAnalytics.pipeline.stage_01_data_ingestion import DataIngestionTrainingPipeline
from DetectAnalytics.pipeline.stage_02_preparing_model import PrepareModelTrainingPipeline
from DetectAnalytics.pipeline.stage_03_training import ModelTrainingPipeline
from DetectAnalytics.pipeline.stage_04_evaluation import EvaluationPipeline

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
    prepare_base_model = PrepareModelTrainingPipeline()
    prepare_base_model.main()
    logger.info(f">>> stage {STAGE_NAME} completed <<<\n\nx==========xx")
except Exception as e:
    logger.exception(e)
    raise e


STAGE_NAME = "Training"
try:
    logger.info(f">>> stage {STAGE_NAME} started <<<")
    model_trainer = ModelTrainingPipeline()
    model_trainer.main()
    logger.info(f">>> stage {STAGE_NAME} completed <<<\n\nx==========xx")
except Exception as e:
    logger.exception(e)
    raise e


STAGE_NAME = "Evaluation Stage"
try:
    logger.info(f">>> stage {STAGE_NAME} started <<<")
    model_evalution = EvaluationPipeline()
    model_evalution.main()
    logger.info(f">>> stage {STAGE_NAME} completed <<<\n\nx==========xx")
except Exception as e:
    logger.exception(e)
    raise e