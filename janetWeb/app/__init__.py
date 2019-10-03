from flask import Flask

app = Flask(__name__)
app.config.update(dict(
    SECRET_KEY="key1",
    WTF_CSRF_SECRET_KEY="key2"
))
#TODO manera mmas limpia de hacer esto
janet_host = "0.0.0.0"
janet_port = 8080

from app import views, janet_access
