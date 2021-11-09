import time
from concurrent.futures import ThreadPoolExecutor

import numpy as np
import tensorflow as tf
import tornado.gen
from tornado.concurrent import is_future


ID_BOBBER = 1
ID_SPLASH = 2
ID_FISHING = 3
FISHING_TIME_SECONDS = 22


class FishingStatuses:
    NONE = 0
    LOOKING_FOR_FISHING_PERK = 1
    LOOKING_FOR_BOBBER = 2
    WAITING_FOR_SPLASH = 3
    LOOTING = 4


class Bober(object):
    def __init__(self, io_loop, screen_controller, mice_controller,
                 keyboard_controller, accuracy=0.6):
        self.io_loop = io_loop
        self.screen_controller = screen_controller
        self.mice_controller = mice_controller
        self.keyboard_controller = keyboard_controller
        self.model = tf.saved_model.load('./')
        self.executor = ThreadPoolExecutor(max_workers=10)
        self.is_working = False
        self.worker = None
        self.on_start_callback = lambda x: x
        self.accuracy = accuracy

    def add_on_start_callback(self, f):
        self.on_start_callback = f

    @staticmethod
    def convert_box_to_xy(screen_width, screen_height, box):
        ymin, xmin, ymax, xmax = box
        return [ymin * screen_height,
                xmin * screen_width,
                ymax * screen_height,
                xmax * screen_width]

    def blocking_detect(self, image):
        input_tensor = tf.convert_to_tensor(image)
        input_tensor = input_tensor[tf.newaxis, ...]
        detections = self.model(input_tensor)
        num_detections = int(detections.pop('num_detections'))
        detections = {key: value[0, :num_detections].numpy()
                      for key, value in detections.items()}
        detections['num_detections'] = num_detections
        detections['detection_classes'] = detections[
            'detection_classes'
        ].astype(np.int64)
        detection_scores = np.where(detections['detection_scores']
                                    >= self.accuracy)[0]
        result = np.take(detections['detection_classes'], detection_scores)
        detection_boxes = np.squeeze(detections['detection_boxes'])

        bobber_objects = []
        splashes_objects = []
        fishing_objects = []

        for index in detection_scores:
            idx = result[index]
            image_width, image_height = image.size
            coordinates = self.convert_box_to_xy(image_width, image_height,
                                                 detection_boxes[index])
            if idx == ID_BOBBER:
                bobber_objects.append(coordinates)

            if idx == ID_SPLASH:
                splashes_objects.append(coordinates)

            if idx == ID_FISHING:
                fishing_objects.append(coordinates)

        # TODO(s1z): Remove duplicates in coordinates for all objects.
        #            Tensorflow can return several boxes of the same object.
        return bobber_objects, splashes_objects, fishing_objects

    @tornado.gen.coroutine
    def detect(self, image):
        # Tensorflow is blocking but we are executing this is in async.
        result = yield self.executor.submit(self.blocking_detect, image)
        raise tornado.gen.Return(result)

    @tornado.gen.coroutine
    def click_fishing_perk(self, coordinates):
        # TODO(s1z): IMPL ME
        pass

    def click_on_splash(self, coordinates):
        # TODO(s1z): IMPL ME
        pass

    @tornado.gen.coroutine
    def run(self):
        # TODO(s1z): Add cancel feature.
        status = FishingStatuses.NONE

        start_time = 0
        elapsed_time = 0
        while self.is_working:
            image = yield self.screen_controller.get_image()
            bobbers, splashes, fishing_perks = yield self.detect(image)

            if status in [FishingStatuses.NONE,
                          FishingStatuses.LOOKING_FOR_FISHING_PERK]:
                # ready to start fishing
                status = FishingStatuses.LOOKING_FOR_FISHING_PERK
                clicked = yield self.click_fishing_perk(fishing_perks)
                if clicked:
                    # start fishing
                    start_time = time.time()
                    status = FishingStatuses.LOOKING_FOR_BOBBER
            elif status == FishingStatuses.LOOKING_FOR_BOBBER:
                if len(bobbers) > 0:
                    status = FishingStatuses.WAITING_FOR_SPLASH
            elif status == FishingStatuses.WAITING_FOR_SPLASH:
                clicked = yield self.click_on_splash(splashes)
                if clicked:
                    status = FishingStatuses.LOOKING_FOR_FISHING_PERK

            elapsed_time = time.time() - start_time
            if elapsed_time >= FISHING_TIME_SECONDS:
                status = FishingStatuses.LOOKING_FOR_FISHING_PERK

            yield tornado.gen.sleep(0.1)

    @tornado.gen.coroutine
    def start(self):
        self.is_working = True
        self.worker = self.run()
        self.io_loop.add_future(self.worker, self.on_start_callback)

    @tornado.gen.coroutine
    def stop(self):
        self.is_working = False
        if is_future(self.worker):
            yield self.worker
