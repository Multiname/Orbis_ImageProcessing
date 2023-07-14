from PIL import Image
from pathlib import Path


class FlipImage:
    def process(self, path, params):
        orientations = {
            "horizontal": Image.FLIP_LEFT_RIGHT,
            "vertical": Image.FLIP_TOP_BOTTOM,
        }

        if params["orientation"] not in orientations:
            return False, "unknown orientation"

        try:
            fullPath = Path.cwd() / path
            image = Image.open(fullPath)

            flipped = image.transpose(orientations[params["orientation"]])
            resultFile = fullPath.parent / (
                fullPath.stem + "_flipped" + fullPath.suffix
            )
            flipped.save(resultFile)
        except:
            return False, "processing failed"

        return True, resultFile
