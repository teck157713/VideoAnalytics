import os
import urllib.request as request
from zipfile import ZipFile
import tensorflow as tf
from pathlib import Path
from DetectAnalytics.entity.config_entity import PrepareModelConfig

class PrepareBaseModel:
    def __init__(self, config: PrepareModelConfig):
        self.config = config


    
    def get_base_model(self):

        self.model = tf.keras.applications.mobilenet_v2.MobileNetV2(
            include_top=self.config.params_include_top,
            weights=self.config.params_weights
        )

        self.model.trainable = True
        for layer in self.model.layers[:-40]:
            layer.trainable=False
            
        self.save_model(path=self.config.base_model_path, model=self.model)


    
    @staticmethod
    def _prepare_full_model(model, classes, freeze_all, freeze_till, learning_rate, image_size):

        sequential = tf.keras.models.Sequential()
        sequential.add(tf.keras.layers.Input(shape = (image_size)))
        sequential.add(tf.keras.layers.TimeDistributed(model))
        sequential.add(tf.keras.layers.Dropout(0.25))
        sequential.add(tf.keras.layers.TimeDistributed(tf.keras.layers.Flatten()))
        lstm_fw = tf.keras.layers.LSTM(units=32)
        lstm_bw = tf.keras.layers.LSTM(units=32, go_backwards=True)
        sequential.add(tf.keras.layers.Bidirectional(lstm_fw, backward_layer = lstm_bw))
        sequential.add(tf.keras.layers.Dropout(0.25))
        sequential.add(tf.keras.layers.Dense(256, activation='relu'))
        sequential.add(tf.keras.layers.Dropout(0.25))
        sequential.add(tf.keras.layers.Dense(128, activation='relu'))
        sequential.add(tf.keras.layers.Dropout(0.25))
        sequential.add(tf.keras.layers.Dense(64, activation='relu'))
        sequential.add(tf.keras.layers.Dropout(0.25))
        sequential.add(tf.keras.layers.Dense(32, activation='relu'))
        sequential.add(tf.keras.layers.Dropout(0.25))

        sequential.add(tf.keras.layers.Dense(classes, activation='softmax'))

        sequential.compile(
            optimizer=tf.keras.optimizers.SGD(learning_rate=learning_rate),
            loss=tf.keras.losses.CategoricalCrossentropy(),
            metrics=["accuracy"]
        )

        sequential.summary()
        return sequential
    

    def update_base_model(self):
        self.full_model = self._prepare_full_model(
            model=self.model,
            classes=self.config.params_classes,
            freeze_all=True,
            freeze_till=None,
            learning_rate=self.config.params_learning_rate,
            image_size=self.config.params_image_size
        )

        self.save_model(path=self.config.updated_base_model_path, model=self.full_model)

    
    @staticmethod
    def save_model(path: Path, model: tf.keras.Model):
        model.save(path)

    