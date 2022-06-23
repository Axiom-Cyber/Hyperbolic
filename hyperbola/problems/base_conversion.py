# John - we need to talk about some fixes. We can discuss them in class tommorow. This is commented out for testing purposes now.
# import base64
# import hyperbola
# import re

# @hyperbola.Commander.add_worker("text")
# class BaseDecoder:
#     async def return_solution(self, text: str):
#         b16 = base64.b16decode(text.encode()).decode()
#         b32 = base64.b32decode(text.encode()).decode()
#         b64 = base64.b64decode(text.encode()).decode()

#         return {"logs": [], "newdata": [{"type": "text", "data": i} for i in [b16,32,64]], "end": False}

# @hyperbola.Commander.add_worker("text")
# class BaseEncoder:
#     async def return_solution(self, text):
#         b16 = base64.b16encode(text.encode()).decode()
#         b32 = base64.b32encode(text.encode()).decode()
#         b64 = base64.b64encode(text.encode()).decode()

#         return {"logs": [], "newdata": [{"type": "text", "data": i} for i in [b16, b32, b64]], "end": False}
