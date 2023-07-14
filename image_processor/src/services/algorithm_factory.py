from services.algorithms.flip import FlipImage
from services.algorithms.resize import ResizeImage
from services.algorithms.rotate import RotateImage


class AlgorithmFactory:
    def __init__(self):
        self.algorithms = {
            "flip": FlipImage,
            "resize": ResizeImage,
            "rotate": RotateImage,
        }

    def get_algorithm(self, algorithm):
        if algorithm not in self.algorithms:
            return None
        return self.algorithms[algorithm]()
