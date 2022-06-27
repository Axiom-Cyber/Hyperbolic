from PIL import Image
from PIL.ExifTags import TAGS
import hyperbola

@hyperbola.Commander.add_worker("filepath") # This is a worker that takes a filepath and returns a dictionary of the image data.
class ImageMetadata:
    def return_solution(self, filepath):
        try:
            image = Image.open(filepath)
            exifdata = image.getexif()
            info_dict = {
                "Image Size": image.size,
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
                'logs':[{'type':'text', 'msg':f"{key}: {info_dict[key]}"} for key in info_dict],
                'newdata': [{'type':'text', 'data':f"{key}: {info_dict[key]}"} for key in info_dict],
                'end':False
            }
        except:
            return {
                'logs':[{"type": "text", "msg": "Not an image"}],
                'newdata': [],
                'end':False
            }