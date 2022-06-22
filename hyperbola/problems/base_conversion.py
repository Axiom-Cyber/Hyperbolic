import re
import base64

#@hyperbola.Commander.add_worker("text")
class BaseEncoder:
    def return_solution(text: str): # string formatted "[base][e/d] [text]" e=encode d=decode
        switch_vals = {
            "16": {
                "e": base64.b16encode,
                "d": base64.b16decode
            },
            "32": {
                "e": base64.b32encode,
                "d": base64.b32decode
            },
            "64": {
                "e": base64.b64encode,
                "d": base64.b64decode
            }
        }
        return switch_vals[text[0:2]][text[2]](text[4:]).decode()