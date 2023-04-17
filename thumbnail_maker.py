import logging
import os
import time
from PIL import Image
from urllib.parse import urlparse
from urllib.request import urlretrieve

logging.basicConfig(filename='logfile.log', level=logging.DEBUG)


class ThumbnailMakerService:
    def __init__(self, home_dir='.'):
        self.home_dir = home_dir
        self.input_dir = self.home_dir + os.path.sep + 'incoming'
        self.output_dir = self.home_dir + os.path.sep + 'outgoing'

    def download_images(self, img_url_list):
        if not img_url_list:
            raise ValueError('Sth is no yes')

        os.makedirs(self.input_dir, exist_ok=True)

        logging.info("Beginning image download")

        start = time.perf_counter()

        for url in img_url_list:
            img_filename = urlparse(url.path)
            urlretrieve(url, self.input_dir + os.path.sep + str(img_filename))

        stop = time.perf_counter()

        logging.info(f'Downloaded {len(img_url_list)} images in {stop - start} seconds.')

    def perform_resizing(self):
        if not os.listdir(self.input_dir):
            raise ValueError('No images in this directory.')

        os.makedirs(self.output_dir, exist_ok=True)

        logging.info("Beginning resizing images.")

        target_sizes = [32, 64, 200]
        num_images = len(os.listdir(self.input_dir))

        start = time.perf_counter()

        for filename in os.listdir(self.input_dir):
            original_image = Image.open(self.input_dir + os.path.sep + filename)
            for base_width in target_sizes:
                width_percentage = base_width / original_image.size[0]
                height = int(original_image[1] * width_percentage)
                img = original_image.resize((base_width, height), Image.Resampling.LANCZOS)
                name, dot, extension = filename.partition('.')
                new_filename = name + "_" + str(base_width) + dot + extension
                img.save(self.output_dir + os.path.sep + new_filename)

            os.remove(self.input_dir + os.path.sep + filename)

        stop = time.perf_counter()

        logging.info(f'Created {3* num_images} thumbnails in {stop - start} seconds.')

    def make_thumbnails(self, img_url_list):

        logging.info('START make_thumbnails.')

        start = time.perf_counter()

        self.download_images(img_url_list)
        self.perform_resizing()

        stop = time.perf_counter()

        logging.info(f'Ended make thumbnails in {stop - start} second.')
