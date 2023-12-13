import os
import urllib.request as request
import zipfile
from DetectAnalytics import logger
from DetectAnalytics.utils.common import get_size
from DetectAnalytics.entity.config_entity import DataIngestionConfig
from pathlib import Path
import gdown
import cv2
import gdown
import numpy as np

class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config


    
    def download_file(self):
        if not os.path.exists(self.config.local_data_file):
            # filename, headers = request.urlretrieve(
            #     url = self.config.source_URL,
            #     filename = self.config.local_data_file
            # )
            # GOOGLE DRIVE DOWNLOAD
            gdown.download(self.config.source_URL, self.config.local_data_file, quiet=False)

            # logger.info(f"{filename} download! with following info: \n{headers}")
        else:
            logger.info(f"File already exists of size: {get_size(Path(self.config.local_data_file))}")  


    
    def extract_zip_file(self):
        """
        zip_file_path: str
        Extracts the zip file into the data directory
        Function returns None
        """
        unzip_path = self.config.unzip_dir
        os.makedirs(unzip_path, exist_ok=True)
        with zipfile.ZipFile(self.config.local_data_file, 'r') as zip_ref:
            zip_ref.extractall(unzip_path)



    def create_dataset(self):
        features = []
        labels = []
        video_files_paths = []

        for class_index, class_name in enumerate(self.config.params_classes_list):
            files_list = os.listdir(os.path.join(self.config.root_dir, class_name))

            for file_name in files_list:
                #get directory of the class
                video_file_path = os.path.join(self.config.root_dir, class_name, file_name)
                #extract the frames of the video file
                frames = self.frames_extraction(video_file_path)
                if len(frames) == self.config.params_sequence:
                    features.append(frames)
                    labels.append(class_index)
                    video_files_paths.append(video_file_path)

        features = np.asarray(features)
        labels = np.asarray(labels)

        np.save("features.npy", features)
        np.save("labels.npy", labels)
        np.save("video_files_paths.npy", video_files_paths)



    def frames_extraction(self, vidpath):
        frames_list = []

        #read vid file
        video_reader = cv2.VideoCapture(vidpath)

        #get total frames in vid
        video_frames_count = int(video_reader.get(cv2.CAP_PROP_FRAME_COUNT))

        #calculate interval for frames to be added
        skip_frames_window = max(int(video_frames_count/self.config.params_sequence), 1)

        for frame_counter in range(self.config.params_sequence):
            video_reader.set(cv2.CAP_PROP_POS_FRAMES, frame_counter * skip_frames_window)

            success, frame = video_reader.read()

            if not success:
                break

            #resize
            resized_frame = cv2.resize(frame, (self.config.params_image_height, self.config.params_image_width))
            normalized_frame = resized_frame / 255

            frames_list.append(normalized_frame)
        
        video_reader.release()

        return frames_list