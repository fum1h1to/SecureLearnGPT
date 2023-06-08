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
                "content": """You are an information security professional.
Based on the following constraints, expectations and output format, please output a scenario about a security incident and its problem.

# Constraints:
- The length of the scenario must be between 250 and 300 words.
- The output must be readable in Json format according to the "Output Format".
- Output must be in Japanese.

# Expectations:
Please create one scenario about a security incident that might actually happen.
Then submit the question.
The scenario should be directed to high school students and their parents.

# Output format:
{
"scenario": "scenario text",
"questions": [
  { "question_num": 1, "question_txt": "question 1 text" },
  { "question_num": 2, "question_txt": "question 2 text" },
  { "question_num": 3, "question_txt": "question 3 text" },
  { "question_num": 4, "question_txt": "question 4 text" }
]
}
"""
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
    print(json_open)

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
