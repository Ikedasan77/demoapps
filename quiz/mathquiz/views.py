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
            user_answer = int(request.POST.get(f'answer_{i}'))  # ユーザーの解答を取得
            question_id = int(request.POST.get(f'question_id_{i}'))  # 問題のIDを取得
            question = Question.objects.get(id=question_id)  # 問題をデータベースから取得
            questions.append(question)  # 出題された問題をリストに追加
            if user_answer == question.correct_answer:  # 正解かどうかを判定
                score += 1
            else:
                wrong_questions.append(question)  # 間違えた場合、リストに追加
        
        incorrect_count = 10 - score  # 不正解数を計算

        return render(request, 'mathquiz/result.html', {
            'score': score,  # 正解数をテンプレートに渡す
            'questions': questions,  # 出題された全ての問題をテンプレートに渡す
            'wrong_questions': wrong_questions,
            'advice': get_advice(score)  # アドバイスもテンプレートに渡す  # 間違えた問題をテンプレートに渡す
        })

    else:  # GETリクエスト（クイズ開始時）の場合
        questions = list(Question.objects.all())  # すべての問題を取得
        selected_questions = random.sample(questions, 10)  # ランダムに10問選択
        return render(request, 'mathquiz/quiz.html', {'questions': selected_questions})  # クイズページを表示

# 正解数に応じたアドバイスを返す関数
def get_advice(score):
    if score == 10:
        return "素晴らしい！この調子で少し難しめの問題にもチャレンジしてみてください！"
    elif score >= 7:
        return "よくできました！間違えた問題については解説を読んでみて間違いの原因を確認してくださいね。"
    elif score >= 4:
        return "惜しい間違いが多いようですよ。たし算と引き算の計算、掛け算と割り算の計算の違いを理解しましょう。"
    else:
        return "計算のルールがまだ覚えられていないようです。解説を読んですぐ問題を解いてみてください。必ず先ほどよりはできるようになっていますよ！"