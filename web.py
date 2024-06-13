from app.app import init_app

PORT = 8080

if __name__ == '__main__':
    app = init_app()
    app.run(host='0.0.0.0', port=PORT)
