from DetectAnalytics.entity.config_entity import TrainingConfig
import tensorflow as tf
from pathlib import Path
import numpy as np
from sklearn.model_selection import train_test_split

class Training:
    def __init__(self, config: TrainingConfig):
        self.config = config
    
    def get_base_model(self):
        self.model = tf.keras.models.load_model(
            self.config.updated_base_model_path
        )

    def data_generator(self):
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
    def save_model(path: Path, model: tf.keras.Model):
        model.save(path)

    def train(self, callback_list: list):

        self.model.fit(
            x = self.features_train,
            y = self.labels_train,
            epochs = self.config.params_epochs,
            batch_size = self.config.params_batch_size,
            shuffle = True,
            validation_split = 0.2,
            callbacks = callback_list
        )

        self.save_model(
            path=self.config.trained_model_path,
            model=self.model
        )