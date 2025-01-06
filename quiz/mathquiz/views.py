from django.shortcuts import render, redirect
from .models import Question
import random
from django.http import JsonResponse
import json  # JSONモジュールのインポート

# 回答の正規化
def normalize_answer(answer):
    return answer.strip()

def is_correct(user_answer, correct_answer):
    return normalize_answer(user_answer) == normalize_answer(correct_answer)

# トップページビュー
def home(request):
    return render(request, 'mathquiz/home.html')

# 問題表示ビュー
def quiz_view(request):
    if request.method == 'GET':
        # データベースから全ての問題を取得し、関連する不正解肢も一緒に取得
        questions = list(Question.objects.prefetch_related('incorrect_choices').all())

        # 出題する問題数を指定（例: 10問）
        num_questions = 10
        selected_questions = random.sample(questions, min(num_questions, len(questions)))

        # 4肢択一形式の選択肢を構築
        questions_with_choices = []
        for question in selected_questions:
            # 不正解の選択肢を取得
            incorrect_choices = [choice.text for choice in question.incorrect_choices.all()]
            # 正解を追加
            all_choices = incorrect_choices + [question.correct_answer]
            # 選択肢をランダムに並び替え
            random.shuffle(all_choices)

            # 問題データを構築
            questions_with_choices.append({
                'id': question.id,  # 問題のID
                'text': question.text,  # 問題文
                'choices': all_choices,  # ランダムに並び替えた選択肢
                'correct_answer': question.correct_answer,  # 正解
                'category': question.category.name if question.category else '',  # 単元名（任意）
                'explanation': question.explanation or ''  # 解説（任意）
            })

        # JSON形式で問題データを渡す
        return render(request, 'mathquiz/quiz.html', {
            'questions': json.dumps(questions_with_choices, ensure_ascii=False)  # 日本語対応
        })

    # GET以外のリクエストはリダイレクト
    return redirect('quiz')

# 解答処理ビュー
def submit_quiz_view(request):
    if request.method == 'POST':
        score = 0
        wrong_questions = []
        questions = []

        for i in range(10):
            user_answer = request.POST.get(f'answer_{i}')
            question_id = request.POST.get(f'question_id_{i}')

            if not question_id:
                continue

            try:
                question_id = int(question_id)
                question = Question.objects.get(id=question_id)
                questions.append(question)
            except (Question.DoesNotExist, ValueError):
                continue

            if user_answer and is_correct(user_answer, str(question.correct_answer)):
                score += 1
            else:
                wrong_questions.append(question.id)

        request.session['score'] = score
        request.session['wrong_questions'] = wrong_questions
        request.session['questions'] = [q.id for q in questions]

        return redirect('result')

    return redirect('quiz')

# 結果表示ビュー
def result_view(request):
    score = request.session.get('score', 0)
    wrong_question_ids = request.session.get('wrong_questions', [])
    questions_ids = request.session.get('questions', [])

    questions = Question.objects.filter(id__in=questions_ids)
    wrong_questions = Question.objects.filter(id__in=wrong_question_ids)

    wrong_questions_data = [
        {
            'text': question.text,
            'explanation': question.explanation or '解説はありません。',
            'correct_answer': question.correct_answer
        }
        for question in wrong_questions
    ]

    total_score = len(questions) * 10
    score_percent = (score / total_score) * 100 if total_score > 0 else 0

    if score_percent == 100:
        advice = "素晴らしい！完全に理解しています！"
    elif score_percent >= 80:
        advice = "よくできました！あと少しで満点です。"
    elif score_percent >= 50:
        advice = "頑張りました！もう少し復習するとさらに良くなります。"
    else:
        advice = "復習が必要です。間違えた問題を確認しましょう。"

    return render(request, 'mathquiz/result.html', {
        'score': score,
        'total_score': total_score,
        'score_percent': score_percent,
        'wrong_questions': wrong_questions_data,
        'questions': questions,
        'advice': advice
    })