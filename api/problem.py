import openai
from flask import Blueprint

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

    return res

"""
UC-12 問題をクライアント側に送信する処理を作る
"""
# @problem.route('/api/problem', methods=['GET'])
# def get_problem():
#   result = jsonify({
#             "status": 0,
#             "message": "success",
#             "scenario": "ある企業の社員が、社外の人間から送信されたメールにより、社内の機密情報が漏えいした。メールは、社員がなりすましメールに騙されたことで開封し、そのメール内には不正なリンクが含まれていた。クリックしたことで、マルウェアが社員のPCに感染し、情報が外部に送信された。",
#             "questions": [
#               { "question_num": 1, "question_txt": "このインシデントにより、何が漏えいしたのか？" },
#               { "question_num": 2, "question_txt": "なぜ社員はなりすましメールを開封してしまったのか？" },
#               { "question_num": 3, "question_txt": "このようなインシデントを防止するために、企業ができることは何か？" },
#               { "question_num": 4, "question_txt": "社員がマルウェアに感染してしまった場合、企業が取るべき対応策は何か？" }
#             ]
#   })  

#   return result