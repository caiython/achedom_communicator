from app import create_app, utils
from config import HOST, PORT
import threading

t = threading.Thread(target=utils.update_data)
app = create_app()

if __name__ == "__main__":
    t.start()
    app.run(HOST, PORT)