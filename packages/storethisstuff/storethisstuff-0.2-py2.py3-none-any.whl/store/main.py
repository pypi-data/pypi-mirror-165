from flask import Flask


def create_app():
    app = Flask(__name__)
    app.add_url_rule(rule='/store', view_func=hello)
    return app

def hello():
    return 'Hello World'

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app = create_app()
    app.run()
