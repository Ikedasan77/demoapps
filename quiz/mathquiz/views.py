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

            # 問題をデータベースから取得
            try:
                question = Question.objects.get(id=int(question_id))
            except (Question.DoesNotExist, ValueError):
                continue  # 問題が見つからない、またはIDが無効な場合はスキップ

            questions.append(question)  # 出題された問題をリストに追加

            # 空欄の回答はNoneとして扱い、間違えとしてカウント
            if not user_answer_str:
                wrong_questions.append(question)
                continue

            # ユーザーの解答を整数に変換して正解判定
            try:
                user_answer = int(user_answer_str)
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
        # すべての問題を取得
        questions = list(Question.objects.all())
        num_questions = 10  # 表示する問題数
        sample_size = min(num_questions, len(questions))  # サンプル数を制限

        # ランダムに選択した問題をテンプレートに渡す
        selected_questions = random.sample(questions, sample_size)

        return render(request, 'mathquiz/quiz.html', {'questions': selected_questions})

# 正解数に応じたアドバイスを返す関数
def get_advice(score):
    if score == 10:
        return "素晴らしい！この調子で少し難しい問題にも挑戦してみてくださいね。"
    elif score >= 7:
        return "よくできました！間違えた問題についてはなぜ間違えたか解説を読んで確認してみてください。"
    elif score >= 4:
        return "頑張りましたね！同じ間違いを繰り返しているようなら、基本に立ち返って復習しましょう。"
    else:
        return "教科書を読み返したり、学校や塾の先生に解き方を教えてもらい、もう一度挑戦してください。必ず前回よりできるようになっているはずです。"
