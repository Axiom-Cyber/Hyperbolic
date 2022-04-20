from hyperbola.connection import Worker

w = Worker('https://demo.ctfd.io', 'user', 'password')
print(w)
w.close()