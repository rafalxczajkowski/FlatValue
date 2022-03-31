from flask import Flask
from flatvalue import create_html

app = Flask('app')

@app.route('/')
def func():
  return create_html()

app.run(host='0.0.0.0', port=8080)