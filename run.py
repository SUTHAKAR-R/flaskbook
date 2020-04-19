from app import create_app

app = create_app()

DEBUG = True
PORT = 5000
HOST = '127.0.0.1'

if __name__ == '__main__':
	app.run(HOST, PORT, DEBUG)
