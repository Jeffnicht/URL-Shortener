from app import create_app
from dotenv import load_dotenv
import os

load_dotenv()
hostAdr = os.getenv("hostAdr", "127.0.0.1")
flaskPort = int(os.getenv("flaskPort", 5000))
flaskDebug = os.getenv("flaskDebug", "False").lower() in ("true", "1", "yes")

app = create_app()

if __name__ == "__main__":
    app.run(host=hostAdr, port=flaskPort, debug=flaskDebug)


