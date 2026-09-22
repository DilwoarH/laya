from flask import Flask, jsonify, request
from laya import Router

app = Flask(__name__)

agent = None


def get_agent():
    global agent

    if agent is None:
        agent = Router()
        try:
            agent.preload(["typed-decisions"])
        except Exception as exc:
            agent = None
            raise RuntimeError(
                "The typed-decisions model is not available. "
                "Check your internet access or the local Hugging Face cache."
            ) from exc

    return agent


@app.post("/predict")
def predict():
    try:
        model = get_agent()
    except Exception as exc:
        return jsonify({"error": str(exc), "status": "model_unavailable"}), 503

    payload = request.get_json(force=True)
    state = payload["state"]
    questions = payload["questions"]
    result = model.predict(state, questions, model="typed-decisions")
    return jsonify(result)


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)