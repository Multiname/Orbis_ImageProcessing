from PIL import Image
from pathlib import Path


class ResizeImage:
    def process(self, path, params):
        try:
            fullPath = Path.cwd() / path
            image = Image.open(fullPath)

            width = params["width"]
            height = params["height"]

            resized = image.resize((width, height))
            resultFile = fullPath.parent / (
                fullPath.stem + "_resized" + fullPath.suffix
            )
            resized.save(resultFile)
        except:
            return False, "processing failed"

        return True, resultFile
