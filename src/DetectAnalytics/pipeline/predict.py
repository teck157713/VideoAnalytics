import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from DetectAnalytics.constants import PARAMS_FILE_PATH
from DetectAnalytics.utils.common import read_yaml
import os
import cv2

class PredictionPipeline:
    params_filepath = PARAMS_FILE_PATH
    params = read_yaml(params_filepath)
    filename = ''
    def __init__(self, filename):
        self.filename = filename

    def predict(self):
        
        # load model
        model = load_model(os.path.join("artifacts","training", "model.h5"))

        imagename = self.filename
        test_image = image.load_img(imagename, target_size = (224,224))
        test_image = image.img_to_array(test_image)
        test_image = np.expand_dims(test_image, axis = 0)
        result = np.argmax(model.predict(test_image), axis=1)
        print(result)

        if result[0] == 1:
            prediction = 'Healthy'
            return [{ "image" : prediction}]
        else:
            prediction = 'Coccidiosis'
            return [{ "image" : prediction}]
        
    def predictvid(self, vid):
        model = load_model(os.path.join("artifacts","training", "model.h5"))
        print(f"vid = {vid}")
        
        video_reader = cv2.VideoCapture(vid)
        original_width = int(video_reader.get(cv2.CAP_PROP_FRAME_WIDTH))
        original_height = int(video_reader.get(cv2.CAP_PROP_FRAME_HEIGHT))

        frames_list = []
        predicted_class_name = ''

        video_frames_count = int(video_reader.get(cv2.CAP_PROP_FRAME_COUNT))
        print(f"video_frames_count = {video_frames_count}")
        print(f"seq = {self.params.SEQUENCE}")
        skip_frames_window = max(int(video_frames_count/self.params.SEQUENCE), 1)

        for frame_counter in range(self.params.SEQUENCE):
            video_reader.set(cv2.CAP_PROP_POS_FRAMES, frame_counter * skip_frames_window)

            success, frame = video_reader.read()

            if not success:
                break

            resized_frame = cv2.resize(frame, (self.params.IMAGE_HEIGHT, self.params.IMAGE_WIDTH))
        
            # Normalize the resized frame.
            normalized_frame = resized_frame / 255
        
            # Appending the pre-processed frame into the frames list
            frames_list.append(normalized_frame)
 
        # Pa    ssing the  pre-processed frames to the model and get the predicted probabilities.
        predicted_labels_probabilities = model.predict(np.expand_dims(frames_list, axis = 0))[0]
 
        # Get the index of class with highest probability.
        predicted_label = np.argmax(predicted_labels_probabilities)
 
        # Get the class name using the retrieved index.
        predicted_class_name = self.params.CLASSES_LIST[predicted_label]
    
        # Display the predicted class along with the prediction confidence.
        print(f'Predicted: {predicted_class_name}\nConfidence: {predicted_labels_probabilities[predicted_label]}')
        