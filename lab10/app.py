from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'This is a flask api behind an nginx proxy'

if __name__ == '__main__':
    app.run(debug=False, port=5000)
