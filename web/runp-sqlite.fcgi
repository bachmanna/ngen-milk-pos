from flipflop import WSGIServer
from web import app

if __name__ == '__main__':
    WSGIServer(app).run()