from django.shortcuts import render, redirect  # 修正: 正しいインポート
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
        questions = list(Question.objects.prefetch_related('incorrect_choices').all())

        # 出題する問題数
        num_questions = 10
        selected_questions = random.sample(questions, min(num_questions, len(questions)))

        # 4肢択一形式の選択肢
        questions_with_choices = []
        for question in selected_questions:
            incorrect_choices = [choice.text for choice in question.incorrect_choices.all()]
            all_choices = incorrect_choices + [question.correct_answer]

            if len(all_choices) < 4:
                print(f"問題ID {question.id} の選択肢が不足しています: {all_choices}")

            random.shuffle(all_choices)

            questions_with_choices.append({
                'id': question.id,
                'text': question.text,
                'choices': all_choices,
                'correct_answer': question.correct_answer,
                'category': question.category.name if question.category else '',
                'explanation': question.explanation or ''
            })

        return render(request, 'mathquiz/quiz.html', {
            'questions': json.dumps(questions_with_choices, ensure_ascii=False)
        })

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
