import base64
import hyperbola
import re

@hyperbola.Commander.add_worker("text")
class BaseDecoder:
    def return_solution(self, text: str):
        #try to decode in each base, but if it fails, return an empty list
        try: b2 = [chr(int(i,2)) for i in re.findall(r'[01]+')]
        except: b2 = []
        try: b16 = [base64.b16decode(i.encode()).decode() for i in re.findall(r'[0-9A-F]+')]
        except: b16 = []
        try: b32 = [base64.b32decode(i.encode()).decode() for i in re.findall(r'[0-9A-V]+')]
        except: b32 = []
        try: b64 = [base64.b64decode(i.encode()).decode() for i in re.findall(r'[0-9A-Za-z]+')]
        except: b64 = []
        
        return {"logs": [], "newdata": [{"type": "number", "data": i} for i in b2+b16+b32+b64], "end": False}

@hyperbola.Commander.add_worker("number")
class ToString:
    def return_solution(self, data):
        return {"logs": [], "newdata": [{"type": "number", "data": data.decode()}], "end": False}

@hyperbola.Commander.add_worker("text")
class BaseEncoder:
    def return_solution(self, text):
        b16 = [base64.b16encode(i.encode()).decode() for i in re.findall(r'[0-9A-F]+')]
        b32 = [base64.b32encode(i.encode()).decode() for i in re.findall(r'[0-9A-V]+')]
        b64 = [base64.b64encode(i.encode()).decode() for i in re.findall(r'[0-9A-Za-z]+')]

        return {"logs": [], "newdata": [{"type": "text", "data": i} for i in b16+b32+b64], "end": False}
