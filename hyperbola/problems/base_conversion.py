import base64
import hyperbola

@hyperbola.Commander.add_worker("text")
class BaseDecoder:
    def return_solution(text: str):
        b16 = base64.b16decode(text.encode()).decode()
        b32 = base64.b32decode(text.encode()).decode()
        b64 = base64.b64decode(text.encode()).decode()

        out = f"base16: {b16}; base32: {b32}; base64: {b64}"

        return {"logs": [], "newdata": [{"type": "text", "data": out}], "end": False}

@hyperbola.Commander.add_worker("text")
class BaseEncoder:
    def return_solution(text: str):
        b16 = base64.b16encode(text.encode()).decode()
        b32 = base64.b32encode(text.encode()).decode()
        b64 = base64.b64encode(text.encode()).decode()

        out = f"base16: {b16}; base32: {b32}; base64: {b64}"

        return {"logs": [], "newdata": [{"type": "text", "data": out}], "end": False}
