from django.shortcuts import render, redirect  # 必要なDjangoモジュールをインポート
from .models import Question  # モデルのインポート
import random  # ランダム選択に使用

# 部分一致の許容
def normalize_answer(answer):
    """
    回答の正規化処理を行う補助関数。
    例: スペース除去や小文字化など。
    """
    # 余分なスペースを除去
    answer = answer.strip()
    # 必要に応じて小文字変換などの正規化を追加
    return answer

def is_correct(user_answer, correct_answer):
    """
    ユーザーの回答と正解の比較を行う補助関数。
    """
    # 正規化して比較
    return normalize_answer(user_answer) == normalize_answer(correct_answer)

# トップページ表示ビュー
def home(request):
    """
    トップページを表示するビュー。
    """
    return render(request, 'mathquiz/home.html')  # トップページ用テンプレートを表示

# 問題表示ビュー（GET専用）
def quiz_view(request):
    """
    問題を表示するビュー。
    ランダムに10問を取得してテンプレートに渡します。
    """
    if request.method == 'GET':  # GETリクエストの場合
        questions = list(Question.objects.all())  # データベースからすべての問題を取得
        num_questions = 10  # 出題する問題数
        selected_questions = random.sample(questions, min(num_questions, len(questions)))  # ランダムに10問選択

        # 選択した問題をテンプレートに渡す
        return render(request, 'mathquiz/quiz.html', {'questions': selected_questions})

    # GET以外のリクエストはクイズ画面にリダイレクト
    return redirect('quiz')

# 解答処理ビュー（POST専用）
def submit_quiz_view(request):
    """
    解答を処理するビュー。
    解答を採点し、結果をテンプレートに渡すための処理を行います。
    """
    if request.method == 'POST':  # POSTリクエストのみ処理
        score = 0  # 正解数を初期化
        wrong_questions = []  # 間違えた問題のリスト
        questions = []  # 出題された問題のリスト

        # ユーザーの解答を処理
        for i in range(10):  # 最大10問の解答を処理
            user_answer_str = request.POST.get(f'answer_{i}')  # 回答内容を取得
            question_id = request.POST.get(f'question_id_{i}')  # 問題IDを取得

            # デバッグ: 取得データを出力
            print(f"Debug: Received answer_{i} = {user_answer_str}")
            print(f"Debug: Received question_id_{i} = {question_id}")

            if not question_id:  # 問題IDが存在しない場合スキップ
                continue

            try:
                question_id = int(question_id)  # IDを整数に変換
                question = Question.objects.get(id=question_id)  # データベースから該当問題を取得
                questions.append(question)  # 出題された問題をリストに追加
            except (Question.DoesNotExist, ValueError):  # 問題が見つからない場合またはIDが不正な場合
                continue

            # 回答を判定
            is_correct_flag = False
            if user_answer_str:  # 回答が入力されている場合
                if is_correct(user_answer_str, str(question.correct_answer)):  # 正解と比較
                    score += 1  # 正解数を加算
                    is_correct_flag = True

            # 不正解の場合にリストへ追加
            if not is_correct_flag:
                wrong_questions.append(question.id)  # 問題のIDのみを保存

        # セッションに結果を保存
        request.session['score'] = score  # スコアをセッションに保存
        request.session['wrong_questions'] = wrong_questions  # 間違えた問題のIDを保存
        request.session['questions'] = [q.id for q in questions]  # 出題された問題のIDを保存

        # デバッグ用にセッションデータを確認
        print("Debug: Session Data - Score:", request.session.get('score'))
        print("Debug: Session Data - Wrong Question IDs:", request.session.get('wrong_questions'))
        print("Debug: Session Data - Question IDs:", request.session.get('questions'))

        # 結果画面にリダイレクト
        return redirect('result')

    # POST以外のリクエストはクイズ画面にリダイレクト
    return redirect('quiz')

# 結果表示ビュー
def result_view(request):
    """
    結果画面を表示するビュー。
    セッションに保存されたスコアや間違えた問題をテンプレートに渡します。
    """
    score = request.session.get('score', 0)  # セッションからスコアを取得（デフォルトは0）
    wrong_question_ids = request.session.get('wrong_questions', [])  # セッションから間違えた問題のIDを取得
    questions_ids = request.session.get('questions', [])  # セッションから出題された問題のIDを取得

    # データベースから問題を取得
    questions = Question.objects.filter(id__in=questions_ids)  # 出題された問題
    wrong_questions = Question.objects.filter(id__in=wrong_question_ids)  # 間違えた問題

    # 間違えた問題を辞書形式で処理（解説付き）
    wrong_questions_data = [
        {
            'text': question.text,
            'explanation': question.explanation,  # 解説を含める
            'correct_answer': question.correct_answer  # 正解も含める
        }
        for question in wrong_questions
    ]

    # デバッグ用のログ出力
    print("Debug: Questions =", questions)
    print("Debug: Wrong Questions =", wrong_questions)

    total_score = len(questions) * 10  # 各問題10点満点として総得点を計算
    score_percent = (score / total_score) * 100 if total_score > 0 else 0  # パーセンテージを計算

    # アドバイスの例
    if score_percent == 100:
        advice = "素晴らしい！完全に理解しています！"
    elif score_percent >= 80:
        advice = "よくできました！あと少しで満点です。"
    elif score_percent >= 50:
        advice = "頑張りました！もう少し復習するとさらに良くなります。"
    else:
        advice = "復習が必要です。間違えた問題を確認しましょう。"

    # 結果をテンプレートに渡してレンダリング
    return render(request, 'mathquiz/result.html', {
        'score': score,
        'total_score': total_score,
        'score_percent': score_percent,
        'wrong_questions': wrong_questions_data,  # 修正: 辞書形式で解説を渡す
        'questions': questions,
        'advice': advice
    })
