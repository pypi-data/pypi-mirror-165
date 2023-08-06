from cv2 import cv2, SimpleBlobDetector
import numpy
from utilspy_g4 import add_ext


class MotionDetector:

    def __init__(self, min_area: int = 4000, max_area: int = 150000, noise_size: int = 10, debug: bool = False):
        """
        :param min_area: Min blob size
        :param max_area: Max blob size
        :param noise_size: Max size of noise area
        :param debug: Is debug mod
        """

        self.debug = debug

        self.back_sub = cv2.createBackgroundSubtractorMOG2(history=1, detectShadows=False)

        self.denoise_kernel = numpy.ones((noise_size, noise_size), numpy.uint8)

        self.blob_detector = self._create_blob_detector(min_area, max_area)

    @staticmethod
    def _create_blob_detector(min_area: int, max_area: int) -> SimpleBlobDetector:
        """
        Create and config OpenCV Simple Blob Detector

        :param min_area: Min blob size
        :param max_area: Max blob size
        :rtype: SimpleBlobDetector
        :return: SimpleBlobDetector
        """

        params = cv2.SimpleBlobDetector_Params()

        params.filterByColor = False

        params.minRepeatability = 1
        params.minThreshold = 250
        params.maxThreshold = 255

        # Filter by Area
        params.filterByArea = True
        params.minArea = min_area
        params.maxArea = max_area

        params.filterByCircularity = False
        params.filterByConvexity = False
        params.filterByInertia = False

        return cv2.SimpleBlobDetector_create(params)

    def apply_first_frame(self, first_frame_path: str) -> None:
        """
        :param first_frame_path:
        :rtype: None
        :return: None
        """

        first_frame = cv2.imread(first_frame_path)

        self.back_sub.apply(first_frame)

    def check_motion(self, next_frame_path: str) -> bool:
        """
        :param next_frame_path: Next frame for comparison
        :rtype: bool
        :return: Is motion
        """

        next_frame = cv2.imread(next_frame_path)

        # 1. Delete background

        frame_mask = self.back_sub.apply(next_frame)

        if self.debug:
            cv2.imwrite(add_ext(next_frame_path, 'mask'), frame_mask)

        # 2. Clear noises

        frame_clear = cv2.morphologyEx(frame_mask, cv2.MORPH_OPEN, self.denoise_kernel)

        if self.debug:
            cv2.imwrite(add_ext(next_frame_path, 'clear'), frame_clear)

        # 3. Search blobs

        blobs = self.blob_detector.detect(frame_clear)

        if len(blobs) > 0:
            if self.debug:
                frame_with_blobs = cv2.drawKeypoints(next_frame, blobs, numpy.array([]), (0, 0, 255),
                                                     cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
                frame_mask_with_blobs = cv2.drawKeypoints(frame_clear, blobs, numpy.array([]), (0, 0, 255),
                                                          cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

                cv2.imwrite(add_ext(next_frame_path, 'blobs'), frame_with_blobs)
                cv2.imwrite(add_ext(next_frame_path, 'blobs2'), frame_mask_with_blobs)

            return True

        return False
