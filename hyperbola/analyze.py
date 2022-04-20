'''
flag 'flag\{\w{4,50}\}'
binary [01]{8,}
hex [0-9A-Fa-f]{2,}
url http\w+
'''

from contextlib import AsyncExitStack
import subprocess
import re
import magic

# result = subprocess.run(['python3', '--version'], capture_output=True, encoding='UTF-8')
# patoolib.extract_archive("archive.zip", outdir="temp")


class Inspector:
    def __init__(self, worker: object, title, points, description, category, tags, attached_files):
        self.worker = worker
        self.title = title
        self.points = points
        self.description = description
        self.category = category
        self.tags = tags
        self.attached_files = attached_files

    def sort_file(self):
        self.filetype = magic.from_file(self.path)
    
    def extract_decompress_file(self):
        pass