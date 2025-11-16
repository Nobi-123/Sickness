# (c) ՏIᒪᗴᑎT ᘜᕼOՏT ⚡️ # Dont Remove Credit

from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Silent-Ghost'


if __name__ == "__main__":
    app.run()
