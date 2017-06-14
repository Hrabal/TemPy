from flask import Flask
from templates.tempy_helloworld import page
app = Flask(__name__)


@app.route('/')
def main_handler():
    page.body.inject({'message': 'hello_world'})
    return page.render()

if __name__ == '__main__':
    app.run(port=8888, debug=False)
