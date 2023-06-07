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
                "content": """
Please create only one scenario about an actual security incident. 
The scenario should be between 250 and 300 words in length. The scenario should be directed to high school students and their parents.
Then, please submit a question. The format should be as follows. The format should be as follows, and the output should be readable in Json format. Text should be in Japanese.
-------
{
"scenario": "scenario text",
"questions": [
  { "question_num": 1, "question_txt": "question 1 text" },
  { "question_num": 2, "question_txt": "question 2 text" },
  { "question_num": 3, "question_txt": "question 3 text" },
  { "question_num": 4, "question_txt": "question 4 text" }
]
}
-------
The only content you will output immediately following this is the scenario and the problem statement."""
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
  try:
    res = creScenario()
    json_open = res["choices"][0]["message"]["content"]

    json_load = json.loads(json_open)
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
