from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
  return "success ssl"

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000, ssl_context=("ssl/server.crt", "ssl/server.key"), threaded=True, debug=True)