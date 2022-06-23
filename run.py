from flaskapp import socketio, app
# from hyperbola import defaults
if __name__ == '__main__':
    socketio.run(app, debug=True)