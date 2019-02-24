import os
from over_achiever.api import app

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    print(f'If you run locally, browse to http://localhost:{port}/login')
    host = '0.0.0.0'
    app.run(host=host, port=port)
