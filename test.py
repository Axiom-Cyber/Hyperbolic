from hyperbola.connection import Worker

w = Worker('https://demo.ctfd.io', 'user', 'password')
print(w)
print(repr(w))
w.close()