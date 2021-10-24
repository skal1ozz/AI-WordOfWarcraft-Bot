from concurrent.futures import ThreadPoolExecutor

import tensorflow as tf
import tornado.gen


class Bober(object):
    def __init__(self, io_loop):
        self.model = tf.saved_model.load('./')
        self.executor = ThreadPoolExecutor(max_workers=10)
        self.is_working = False
        self.io_loop = io_loop

    def blocking_detect(self, image):
        input_tensor = tf.convert_to_tensor(image)
        input_tensor = input_tensor[tf.newaxis, ...]
        detections = self.model(input_tensor)
        return detections

    @tornado.gen.coroutine
    def detect(self, image):
        result = yield self.executor.submit(self.blocking_detect, image)
        raise tornado.gen.Return(result)

    @tornado.gen.coroutine
    def run(self):
        pass

    @tornado.gen.coroutine
    def start(self):
        self.is_working = True

    @tornado.gen.coroutine
    def stop(self):
        self.is_working = False
