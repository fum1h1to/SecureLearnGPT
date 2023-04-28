from flask import Blueprint

answer = Blueprint('answer', __name__)

"""
UC-13 ChatGPTから回答に対する解答と解説を取得する処理を作る
"""
import openai
import re

# OpenAI APIキーを設定する
openai.api_key = "YOUR_API_KEY"

# 解答と解説を取得する関数を定義する
def get_answer_and_explanation(question, context):
    # OpenAIに問い合わせを送信する
    response = openai.Completion.create(
        engine="davinci",
        prompt=f"Q: {question}\nC: {context}\nA:",
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    # 解答を抽出する
    answer = response.choices[0].text.strip()

    # 解説を抽出する
    explanation = re.search(r"E: (.+)", response.choices[0].text).group(1)

    # 解答と解説を返す
    return answer, explanation

"""
UC-14 解答と解説をクライアント側に送信する
"""