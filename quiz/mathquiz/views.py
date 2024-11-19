from django.shortcuts import render, redirect
from .models import Question
import random

# 10問の問題を表示し、結果を処理するビュー
def quiz_view(request):
    if request.method == 'POST':  # POSTリクエスト（解答送信後）の場合
        score = 0  # 正解数の初期化
        wrong_questions = []  # 間違えた問題のリスト
        questions = []  # 全ての出題された問題を保持するリスト

        for i in range(10):
            user_answer_str = request.POST.get(f'answer_{i}')
            question_id = request.POST.get(f'question_id_{i}')
            if question_id is None:
                continue  # 問題IDが取得できない場合はスキップ
            question_id = int(question_id)
            question = Question.objects.get(id=question_id)  # 問題をデータベースから取得
            questions.append(question)  # 出題された問題をリストに追加

            if user_answer_str is None or user_answer_str == '':
                # 空欄の回答はNoneとして扱い、間違えとしてカウント
                wrong_questions.append(question)
                continue

            try:
                user_answer = int(user_answer_str)  # ユーザーの解答を整数に変換
                if user_answer == question.correct_answer:  # 正解かどうかを判定
                    score += 1
                else:
                    wrong_questions.append(question)  # 間違えた場合、リストに追加
            except ValueError:
                # 数値に変換できない回答も間違えとしてカウント
                wrong_questions.append(question)

        incorrect_count = 10 - score  # 不正解数を計算

        return render(request, 'mathquiz/result.html', {
            'score': score,  # 正解数をテンプレートに渡す
            'questions': questions,  # 出題された全ての問題をテンプレートに渡す
            'wrong_questions': wrong_questions,
            'advice': get_advice(score)  # アドバイスもテンプレートに渡す
        })

    else:  # GETリクエスト（クイズ開始時）の場合
        questions = list(Question.objects.all())  # すべての問題を取得
        selected_questions = random.sample(questions, 10)  # ランダムに10問選択
        return render(request, 'mathquiz/quiz.html', {'questions': selected_questions})  # クイズページを表示

# 正解数に応じたアドバイスを返す関数
def get_advice(score):
    if score == 10:
        return "素晴らしい！この調子で少し難しい問題にも挑戦してみてくださいね。"
    elif score >= 7:
        return "よくできました！間違えた問題についてはなぜ間違えたか解説を読んで確認してみてください。"
    elif score >= 4:
        return "頑張りましたね！分数やる以上の計算など同じ間違いを繰り返しているようなら、その部分だけでも基本に立ち返りましょう。"
    else:
        return "１度教科書を読み返したり、学校や塾の先生に解き方を教えてもらったらここに戻ってきて問題解いてみてください。必ず前回よりできるようになっているはずです、。"
