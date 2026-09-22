from flask import Flask, jsonify, request
from laya import Router

app = Flask(__name__)

# Loaded once at process startup so requests never pay the checkpoint-load cost.
agent = Router()
agent.preload(["typed-decisions"])


@app.post("/predict")
def predict():
    payload = request.get_json(force=True)
    state = payload["state"]
    questions = payload["questions"]
    result = agent.predict(state, questions, model="typed-decisions")
    return jsonify(result)


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)