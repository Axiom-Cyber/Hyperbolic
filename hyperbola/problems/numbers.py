import hyperbola
import re

# @hyperbola.Commander.add_worker('text')
# class Hexadecimal:
#     async def return_solution(self, data):
#         matches = re.findall(r'[0-9A-Fa-f]+', data)
#         return {'logs':[], 'newdata':
#           [{'type':'text', 'data':''.join([chr(int(i[j:j+2],16)) for j in range(0, len(i), 2) if j<len(i)-1])} for i in matches],
#           'end':False
#         }
# @hyperbola.Commander.add_worker('text')
# class Binary:
#     async def return_solution(self, data):
#         matches = re.findall(r'[01]+', data)
        
#         return {'logs':[], 'newdata':
#           [{'type':'text', 'data':''.join([chr(int(i[j:j+8],16)) for j in range(0, len(i), 8) if j<len(i)-7])} for i in matches], 
#           'end':False
#         }
#@hyperbola.Commander.add_worker('text')
# class B64:
#     def return_solution(self, data):
#         newdata = []
#         for i in re.findall(r'[A-Za-z0-9+/]+', data):
#             stri = []
#             for j in range(len(i)):
#                 num = bin(int(i[j:j+8],64))[2:]
#                 stri.append(chr(int(num[:8], 2))+chr(int(num[8:], 2)))
#             newdata.append(''.join(stri))
#         return {'logs':[], 'newdata':[{'type':'text', 'data':i} for i in newdata], 'end':False}
