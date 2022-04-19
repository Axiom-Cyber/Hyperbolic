'''
flag 'flag\{\w{4,50}\}'
binary [01]{8,}
hex [0-9A-Fa-f]{2,}
'''

import subprocess
import re

# result = subprocess.run(['python3', '--version'], capture_output=True, encoding='UTF-8')