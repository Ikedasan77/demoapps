from django.shortcuts import render, redirect  # 必要なDjangoモジュールをインポート
from .models import Question  # モデルのインポート
import random  # ランダム選択に使用

# トップページ表示ビュー
def home(request):
    """
    トップページを表示するビュー。
    """
    return render(request, 'mathquiz/home.html')  # `home.html` テンプレートを表示

# 問題表示ビュー（GET専用）
def quiz_view(request):
    """
    問題を表示するビュー。
    GETリクエストの場合にランダムな10問を取得してテンプレートに渡す。
    """
    if request.method == 'GET':  # GETリクエストの場合
        questions = list(Question.objects.all())  # 全ての問題を取得
        num_questions = 10
        selected_questions = random.sample(questions, min(num_questions, len(questions)))  # ランダムに10問選択

        # 選択した問題をテンプレートに渡す
        return render(request, 'mathquiz/quiz.html', {'questions': selected_questions})

    # GET以外のリクエストの場合、問題画面にリダイレクト
    return redirect('quiz')

# 解答処理ビュー（POST専用）
def submit_quiz_view(request):
    """
    解答を処理してスコアを計算し、結果をテンプレートに渡すビュー。
    POSTリクエストを受け取り、回答を採点し、結果画面を表示する。
    """
    if request.method == 'POST':  # POSTリクエストの場合
        score = 0  # 正解数を初期化
        wrong_questions = []  # 間違えた問題のリスト
        questions = []  # 出題された問題のリストを保持

        # 解答の処理
        for i in range(10):
            user_answer_str = request.POST.get(f'answer_{i}')  # 回答の取得
            question_id = request.POST.get(f'question_id_{i}')  # 問題IDの取得

            if not question_id:  # 問題IDが存在しない場合はスキップ
                continue

            try:
                question = Question.objects.get(id=int(question_id))
                questions.append(question)  # 出題された問題をリストに追加
            except (Question.DoesNotExist, ValueError):  # 問題が存在しない場合スキップ
                continue

            # 回答を判定
            if user_answer_str:  # 回答が存在する場合
                try:
                    user_answer = int(user_answer_str)
                    if user_answer == question.correct_answer:  # 正解の場合
                        score += 1
                    else:
                        wrong_questions.append(question)  # 不正解の場合
                except ValueError:
                    wrong_questions.append(question)  # 数値に変換できない場合も不正解扱い
            else:
                wrong_questions.append(question)  # 未回答も不正解扱い

        # 結果画面にレンダリング
        return render(request, 'mathquiz/result.html', {
            'score': score,
            'wrong_questions': wrong_questions,
            'questions': questions
        })

    # POST以外のリクエストの場合、問題画面にリダイレクト
    return redirect('quiz')

# 結果表示ビュー
def result_view(request):
    """
    結果画面用のビュー。
    """
    return render(request, 'mathquiz/result.html')
