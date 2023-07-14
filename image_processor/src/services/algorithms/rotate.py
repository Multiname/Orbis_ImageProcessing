from PIL import Image
from pathlib import Path


class RotateImage:
    def process(self, path, params):
        directions = {
            "clockwise": 90,
            "counterclockwise": -90
        }

        if params["direction"] not in directions:
            return False, "unknown direction"

        try:
            fullPath = Path.cwd() / path
            image = Image.open(fullPath)

            rotated = image.rotate(directions[params["direction"]], expand=True)
            resultFile = fullPath.parent / (
                fullPath.stem + "_rotated" + fullPath.suffix
            )
            rotated.save(resultFile)
        except:
            return False, "processing failed"

        return True, resultFile
