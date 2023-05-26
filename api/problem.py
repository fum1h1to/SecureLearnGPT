import openai
import json
from flask import Blueprint, jsonify

problem = Blueprint('problem', __name__)

openai.api_key = ""

"""
UC-11 ChatGPTから問題を取得する処理を作る
"""
def creScenario():
    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": """実際にセキュリティ的なインシデントについてシナリオだけを一つ作ってください。シナリオは250文字以上300文字以下程度の分量とします。その後、問題を出題してください。なお、フォーマットは以下とします。またJson形式で読み取れるような形で出力してください。

-------
{
"scenario": "シナリオの内容",
"questions": [
  { "question_num": 1, "question_txt": "1番目の問題文" },
  { "question_num": 2, "question_txt": "2番目の問題文" },
  { "question_num": 3, "question_txt": "3番目の問題文" },
  { "question_num": 4, "question_txt": "4番目の問題文" }
]
}
-------

あなたが、この直後出力する内容は、シナリオと問題文のみです。"""
            },
            {
                "role": "user",
                "content": ""
            },
        ],
    )

    return res["choices"][0]["message"]["content"]

"""
UC-12 問題をクライアント側に送信する処理を作る
"""
@problem.route('/api/problem', methods=['GET'])
def get_problem():
  try:
    json_open = creScenario()
    json_load = json.load(json_open)
    s = json_load['scenario']
    q1 = json_load['questions'][0]['question_txt']
    q2 = json_load['questions'][1]['question_txt']
    q3 = json_load['questions'][2]['question_txt']
    q4 = json_load['questions'][3]['question_txt']
    result = jsonify({
              "status": 0,
              "message": "success",
              "scenario": s,
              "questions": [
                { "question_num": 1, "question_txt": q1 },
                { "question_num": 2, "question_txt": q2 },
                { "question_num": 3, "question_txt": q3 },
                { "question_num": 4, "question_txt": q4 }
              ]
    })  
  except:
    result = jsonify({
      "status": 1,
      "message": "エラーが発生しました。再度お試しください。"
    })

  return result