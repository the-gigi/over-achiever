import os
from over_achiever.api import app

if __name__ == "__main__":
    print("If you run locally, browse to http://localhost:5000")
    host = '0.0.0.0'
    port = int(os.environ.get("PORT", 5000))
    app.run(host=host, port=port)
