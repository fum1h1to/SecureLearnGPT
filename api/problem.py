from flask import Blueprint, request, jsonify
import openai
import json
import os
from dotenv import load_dotenv

# load envファイル
load_dotenv()

problem = Blueprint('problem', __name__)

openai.api_key = os.environ['OPENAI_APIKEY']

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

  return res


"""
UC-12 問題をクライアント側に送信する処理を作る
"""
@problem.route('/api/problem', methods=['GET'])
def get_problem():
  res = creScenario()
  res_json = json.loads(res["choices"][0]["message"]["content"])
  
  # print(res_json)
  try:
    result = jsonify({
      "status": 0,
      "message": "success",
      "scenario": res_json['scenario'],
      "questions": [
        { "question_num": 1, "question_txt": res_json['questions'][0]['question_txt'] },
        { "question_num": 2, "question_txt": res_json['questions'][1]['question_txt'] },
        { "question_num": 3, "question_txt": res_json['questions'][2]['question_txt'] },
        { "question_num": 4, "question_txt": res_json['questions'][3]['question_txt'] }
      ]
    })
  except:
    result = jsonify({
      "status": 1,
      "message": "OpenAIが正しいフォーマットで解答してくれませんでした。再度お試しください。"
    })  

  return result