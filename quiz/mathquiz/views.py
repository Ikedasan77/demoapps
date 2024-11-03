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
                user_answer = None  # 空欄をNoneとして扱う
            else:
                user_answer = int(user_answer_str)  # ユーザーの解答を取得
            
            if user_answer is not None and user_answer == question.correct_answer:  # 正解かどうかを判定
                score += 1
            else:
                wrong_questions.append(question)  # 間違えた場合、または空欄の場合、リストに追加
        
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
        return "素晴らしい！この調子でレベルアップした問題にもチャレンジだ！"
    elif score >= 7:
        return "よくできました！間違えた問題はその原因を確認してくださいね。"
    elif score >= 4:
        return "頑張りましたね！分数や累乗の計算など同じような問題で間違えていませんか？間違えた問題は必ず復讐です。"
    else:
        return "もう一度学習しなおすいいチャンスと考えてくださいね。テキストや塾の先生から解き方を学びましょう。次回問題を解くときは今回より成績上がるはず！"
