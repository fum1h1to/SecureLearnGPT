from flask import Blueprint, request, jsonify
import openai
import json
import os

answer = Blueprint('answer', __name__)

# OpenAI APIキーを設定する
openai.api_key = ""

"""
UC-13 ChatGPTから回答に対する解答と解説を取得する処理を作る
"""
# 解答と解説を取得する関数を定義する
def get_answer_and_explanation(scenario, questions, answers):
    # OpenAIに問い合わせを送信する
    command = """この会話では，必ず次のフォーマット(Json形式)で値を出力してください．
    値が不十分と判断しても，以下のフォーマットは必ず守ってください．これ以外の文字列を絶対に出力しないでください．
{
    "commentary": [
    { "commentary_num": 1, "commentart_txt": "{1番目の解説文}" },
    { "commentary_num": 2, "commentary_txt": "{2番目の解説文}" },
    { "commentary_num": 3, "commentary_txt": "{3番目の解説文}" },
    { "commentary_num": 4, "commentary_txt": "{4番目の解説文}" }
    ]
}"""

    prompt = f"""\
なお，解答には，それぞれの問題に対する解説と私の解答に対する講評を含めて，それぞれ200文字以上250以下程度で出力してください．
事前に提示したフォーマットには絶対に従ってください．それ以外の文字列は不要です．

<シナリオ>
{scenario}

<問題>
1.{questions[0]}
2.{questions[1]}
3.{questions[2]}
4.{questions[3]}

<私の回答>
1.{answers[0]}
2.{answers[1]}
3.{answers[2]}
4.{answers[3]}
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
    # リクエストからデータを取得する
    try:
        res_json = request.get_json()
        
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
                answer = "分かりません．"
            if len(answer) > 100:
                return jsonify({
                    "status": 1,
                    "message": "解答はそれぞれ100文字以内で行ってください．"
                })
            
            answers.append(answer)
    except:
        return jsonify({
            "status": 1,
            "message": "jsonの形式が正しくありません．",
        })
    
    gpt_responce = get_answer_and_explanation(scenario, questions, answers)
    gpt_responce_json = gpt_responce["choices"][0]["message"]["content"]

    # print(gpt_responce_json)
    try:
        commentarys_json = json.loads(gpt_responce_json)
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
