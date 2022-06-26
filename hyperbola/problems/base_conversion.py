import base64
import hyperbola
import re

@hyperbola.Commander.add_worker("text")
class BaseDecoder:
    async def return_solution(self, text: str):
        b2 = []
        for result in re.findall(r'[01]+', text):
            try: b2.append(chr(int(result,2)))
            except: pass
        b16 = []
        for result in re.findall(r"[0-9A-F]+", text):
            try: b16.append(base64.b16decode(result.encode()).decode())
            except: pass
        
        b32 = []
        for result in re.findall(r"[0-9A-V]+", text):
            try: b32.append(base64.b32decode(result.encode()).decode())
            except: pass

        b64 = []
        for result in re.findall(r"[0-9A-Za-z]+", text):
            try: b64.append(base64.b64decode(result.encode()).decode())
            except: pass
        
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

        return {"logs": [{"type": "text", "msg": i} for i in b16+b32+b64], "newdata": [{"type": "text", "data": i} for i in b16+b32+b64], "end": False}
