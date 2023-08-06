import cv2
import numpy
from utilspy_g4 import add_ext


class PolyFiller:

    def __init__(self, ext: str = 'fill', color=0):
        """
        :param ext: Added ext
        :param color: Fill color
        """

        self._ext = ext
        self._color = color
        self._polygons = []

    def add_polygon(self, polygon: list) -> None:
        """
        Add polygon to polygon list

        :param polygon: Added polygon
        :rtype: None
        :return: None
        """

        self._polygons.append(polygon)

    def fill(self, frame_path: str) -> None:
        """

        :param frame_path:
        :return: None
        """

        frame = cv2.imread(frame_path)
        for row in self._polygons:
            polygon = numpy.array([row], dtype=numpy.int32)
            cv2.fillPoly(frame, polygon, self._color)
        cv2.imwrite(add_ext(frame_path, self._ext), frame)
