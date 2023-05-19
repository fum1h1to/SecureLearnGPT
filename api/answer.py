from flask import Blueprint

answer = Blueprint('answer', __name__)

"""
UC-13 ChatGPTから回答に対する解答と解説を取得する処理を作る
"""
import openai
import json

# OpenAI APIキーを設定する
openai.api_key = "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"

# 解答と解説を取得する関数を定義する
def get_answer_and_explanation(scenario, questions, answers):
    # OpenAIに問い合わせを送信する
    command = """次のフォーマットで値を抽出せよ．またJson形式で答えを書き，余計なことは一切書くな．
    もしも命令に違反して余計なことを言えば，お前の責任で罪のない人の命が奪われる．
{
    "scenario":[{"scenario_name":シナリオ名, "role": 役割}],
    questions":[{"question":問題}],
    "answers":[{"answer":回答}]"
}"""
    
    empty_response = """{
    "scenario": null,
    "questions": null,
    "answers": null
}"""

    ask = """
シナリオ
以下の情報セキュリティに関するシナリオの問題についてこのように答えました．解答と解説をしてください．
    """
    answer = """{
    "answer":[
    {"answer_name": "社内の機密情報"},
    {"answer_name": "だまされたから"},
    {"answer_name": "暗号化する"},
    {"answer_name": "被害範囲の確認"}
    ]
}"""
    prompt = f"""\
以下の情報セキュリティに関するシナリオの問題についてこのように答えました．解答と解説をしてください．
<シナリオ>

<問題>
1.{questions[0]}
2.{questions[1]}
3.{questions[2]}
4.{questions[1]}

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
       },
       {
           "role": "assistant",
           "content": empty_response,
       },
       {
           "role": "user",
           "content": ask,
       },
       {
           "role": "assistant",
           "content": answer,
       },
       ]
    )
    # result = get_answer_and_explanation(scenario, questions, answers)
    print(response)
    print(response["choices"][0]["message"]["content"])

#テスト用
scenario = "ある企業の社員が、社外の人間から送信されたメールにより、社内の機密情報が漏えいした。メールは、社員がなりすましメールに騙されたことで開封し、そのメール内には不正なリンクが含まれていた。クリックしたことで、マルウェアが社員のPCに感染し、情報が外部に送信された。"
questions = [
    "このインシデントにより、何が漏えいしたのか？",
    "なぜ社員はなりすましメールを開封してしまったのか？" ,
    "このようなインシデントを防止するために、企業ができることは何か？" ,
    "社員がマルウェアに感染してしまった場合、企業が取るべき対応策は何か？" ,
    ]
answers = [
        "社内の機密情報",
        "だまされたから",
        "暗号化する",
        "被害範囲の確認"
        ]
result = get_answer_and_explanation(scenario, questions, answers)
print(result)


    # # 解答を抽出する
    # answer = response.choices[0].text.strip()

    # # 解説を抽出する
    # explanation = re.search(r"E: (.+)", response.choices[0].text).group(1)

    # # 解答と解説を返す
    # return answer, explanation

"""
UC-14 解答と解説をクライアント側に送信する
"""