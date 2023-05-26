from flask import Flask, render_template

from api.problem import problem
from api.answer import answer

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

app.register_blueprint(problem)
app.register_blueprint(answer)


if __name__ == "__main__":
  app.run(port=8080, debug=True)