from flask import Blueprint, request, jsonify
import openai
import json
import os
from dotenv import load_dotenv

# load envファイル
load_dotenv()

answer = Blueprint('answer', __name__)

openai.api_key = os.environ['OPENAI_APIKEY']

"""
UC-13 ChatGPTから回答に対する解答と解説を取得する処理を作る
"""
def get_answer_and_explanation(scenario, questions, answers):
  '''OpenAIに利用者の回答に対する解答と解説を問い合わせる

  Parameters
  ----------
  scenario : str
      シナリオ
  questions: list
      質問のリスト
  answers: list
      回答のリスト

  Returns
  -------
  answer : chatGPTのレスポンスとして得たJsonデータを返す

  '''
  # OpenAIに問い合わせを送信する
  command = """You are an information security specialist.
Please output your feedback on my answer based on the following constraints and expectations, input statement, and output format.

# Constraints:
- Feedback should be between 250 and 300 characters each.
- The output must be readable in Json format according to the "Output Format".
- Refer to the input text for "Scenario," "Question," and "My Answer".
- There is one scenario and four questions and answers each.
- Output must be in Japanese.

# Expectations:
My response to the "Question" for the security incident scenario.
You output feedback on "My Answer".
In the feedback, please indicate that it is correct if correct, and include advice and explanations that would improve the answer. If incorrect, please explain why and include advice and explanations on how to get closer to the correct answer.
The feedback should also be directed to high school students and their parents.

# Output format:
{
  "commentary": [
  { "commentary_num": 1, "commentary_txt": "commentary 1 text" },
  { "commentary_num": 3, "commentary_txt": "commentary 2 text" },
  { "commentary_num": 2, "commentary_txt": "commentary 3 text" },
  { "commentary_num": 4, "commentary_txt": "commentary 4 text" }
  ]
}
"""

  prompt = f"""\
# Input text:
<Scenario>
{scenario}

<question and my answer>.
Question 1:{questions[0]}, My Answer 1:{answers[0]}
Question 2:{questions[1]}, My Answer 2:{answers[1]}
Question 3:{questions[2]}, My Answer 3:{answers[2]}
Question 4:{questions[3]}, My Answer 4:{answers[3]}
\
"""
  prompt.format(scenario=scenario, questions=questions, answers=answers)

  response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
          {
          "role": "system",
          "content": command,
      },
      {
          "role": "user",
          "content": prompt
      }
      ]
  )

  return response


"""
UC-14 解答と解説をクライアント側に送信する
"""
@answer.route('/api/answer', methods=['POST'])
def g_answer():
  try:
    res_json = request.json
    
    scenario = res_json['scenario']

    questions_json = res_json['questions']
    questions = []
    for i in range(len(questions_json)):
      questions.append(questions_json[i]['question_txt'])

    answers_json = res_json['answers']
    answers = []
    for i in range(len(answers_json)):
      answer = answers_json[i]['answer_txt']
      if answer == "":
        answer = "分かりません。"
      if len(answer) > 100:
        return jsonify({
          "status": 1,
          "message": "解答はそれぞれ100文字以内で行ってください。",
        })
      
      answers.append(answer)
  except:
    return jsonify({
      "status": 1,
      "message": "jsonの形式が正しくありません。",
    })
  
  gpt_response = get_answer_and_explanation(scenario, questions, answers)
  gpt_response_json = gpt_response["choices"][0]["message"]["content"]
  print(gpt_response_json)

  # print(gpt_response_json)
  try:
    commentarys_json = json.loads(gpt_response_json)
    result = jsonify({
      "status": 0,
      "message": "success",
      "commentarys": [
        { "commentary_num": 1, "commentary_txt": commentarys_json['commentary'][0]['commentary_txt'] },
        { "commentary_num": 2, "commentary_txt": commentarys_json['commentary'][1]['commentary_txt'] },
        { "commentary_num": 3, "commentary_txt": commentarys_json['commentary'][2]['commentary_txt'] },
        { "commentary_num": 4, "commentary_txt": commentarys_json['commentary'][3]['commentary_txt'] }
      ]
    })  
  except:
    result = jsonify({
      "status": 1,
      "message": "OpenAIが正しいフォーマットで解答してくれませんでした。再度お試しください。",
    })
  
  return result