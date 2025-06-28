from app import app

@app.route('/')
def index():
    return "Hello, Task Management App!"
