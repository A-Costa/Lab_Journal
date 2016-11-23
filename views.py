from Lab_Journal import app

@app.route('/')
def index():
    return 'Hello World'
