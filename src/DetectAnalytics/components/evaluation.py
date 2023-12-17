import tensorflow as tf
from pathlib import Path
from DetectAnalytics.entity.config_entity import EvaluationConfig
from DetectAnalytics.utils.common import save_json
from urllib.parse import urlparse
import numpy as np
from sklearn.model_selection import train_test_split

class Evaluation:
    def __init__(self, config: EvaluationConfig):
        self.config = config

    
    def _valid_generator_sample(self):

        datagenerator_kwargs = dict(
            rescale = 1./255,
            validation_split=0.30
        )

        dataflow_kwargs = dict(
            target_size=self.config.params_image_size[:-1],
            batch_size=self.config.params_batch_size,
            interpolation="bilinear"
        )

        valid_datagenerator = tf.keras.preprocessing.image.ImageDataGenerator(
            **datagenerator_kwargs
        )

        self.valid_generator = valid_datagenerator.flow_from_directory(
            directory=self.config.training_data,
            subset="validation",
            shuffle=False,
            **dataflow_kwargs
        )

    def _valid_generator(self):

        features = np.load("features.npy")
        labels = np.load("labels.npy")
        video_files_paths = np.load("video_files_paths.npy")

        encoded_labels = tf.keras.utils.to_categorical(labels)

        self.features_train, self.features_test, self.labels_train, self.labels_test = train_test_split(
            features, 
            encoded_labels, 
            test_size = 0.1, 
            shuffle = True, 
            random_state = 42
        )

    
    @staticmethod
    def load_model(path: Path) -> tf.keras.Model:
        return tf.keras.models.load_model(path)
    

    def evaluation(self):
        self.model = self.load_model(self.config.path_of_model)
        self._valid_generator()
        self.score = self.model.evaluate(self.features_test, self.labels_test)

    
    def save_score(self):
        scores = {"loss": self.score[0], "accuracy": self.score[1]}
        save_json(path=Path("scores.json"), data=scores)