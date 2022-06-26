from PIL import Image
from PIL.ExifTags import TAGS
import hyperbola

@hyperbola.Commander.add_worker("filepath") # This is a worker that takes a filepath and returns a dictionary of the image data.
class ImageMetadata:
    def return_solution(filepath):
        image = Image.open(filepath)
        exifdata = image.getexif()
        info_dict = { #
            "Filename": image.filename,
            "Image Size": image.size,
            "Image Height": image.height,
            "Image Width": image.width,
            "Image Format": image.format,
            "Image Mode": image.mode,
            "Image is Animated": getattr(image, "is_animated", False),
            "Frames in Image": getattr(image, "n_frames", 1)
        }

        for tag_id in exifdata:
            tag = TAGS.get(tag_id, tag_id)
            data = exifdata.get(tag_id)
            info_dict[tag] = data
        
        return {
            'logs':[],
            'newdata': [{'type':'text', 'data':f"{key}: {info_dict[key]}"} for key in info_dict],
            'end':False
       }