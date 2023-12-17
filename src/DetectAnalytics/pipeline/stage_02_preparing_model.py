from DetectAnalytics.config.configuration import ConfigurationManager
from DetectAnalytics.components.preparing_model import PrepareBaseModel
from DetectAnalytics import logger

STAGE_NAME = "Prepare Model"

class PrepareModelTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        config = ConfigurationManager()
        prepare_base_model_config = config.get_prepare_base_model_config()
        prepare_base_model = PrepareBaseModel(config=prepare_base_model_config)
        prepare_base_model.get_base_model()
        prepare_base_model.update_base_model()

if __name__ == '__main__':
    try:
        logger.info(f">>> stage {STAGE_NAME} started <<<")
        obj = PrepareModelTrainingPipeline()
        obj.main()
        logger.info(f">>> stage {STAGE_NAME} completed <<<\n\nx==========xx")
    except Exception as e:
        logger.exception(e)
        raise e