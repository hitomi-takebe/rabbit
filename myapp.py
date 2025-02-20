from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from langchain.chat_models import ChatOpenAI
import os


app = Flask(__name__)
CORS(app)  # CORSの設定（フロントエンドと通信するため）

# OpenAI APIキー
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
llm = ChatOpenAI(model_name="gpt-4", openai_api_key=OPENAI_API_KEY)


@app.route("/")
def index():
    return render_template('index.html')

# チャット用のAPIエンドポイント
@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        user_message = data.get("message", "")

        if not user_message:
            return jsonify({"error": "Message cannot be empty"}), 400

        # OpenAI に問い合わせ
        response = llm.invoke(user_message)

        # response は AIMessage オブジェクト → content を取得
        return jsonify({"response": response.content})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)