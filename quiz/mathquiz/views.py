from django.shortcuts import render, redirect
from .models import Question
import random
import json
from django.utils.html import escape  # HTMLエスケープ用

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
            incorrect_choices = [escape(choice.text) for choice in question.incorrect_choices.all()]
            all_choices = incorrect_choices + [escape(question.correct_answer)]

            if len(all_choices) < 4:
                print(f"問題ID {question.id} の選択肢が不足しています: {all_choices}")

            random.shuffle(all_choices)

            questions_with_choices.append({
                'id': question.id,
                'text': escape(question.text),  # 問題文をエスケープ
                'choices': all_choices,
                'correct_answer': escape(question.correct_answer),  # 正解もエスケープ
                'category': escape(question.category.name) if question.category else '',
                'explanation': escape(question.explanation or '')
            })

        # JSONにエンコードし、ビュー内でサニタイズ済みデータを渡す
        safe_questions_json = json.dumps(questions_with_choices, ensure_ascii=False)

        return render(request, 'mathquiz/quiz.html', {
            'questions_json': safe_questions_json  # エスケープされたJSONデータ
        })

    return redirect('quiz')

# 解答処理ビュー
def submit_quiz_view(request):
    if request.method == 'POST':
        score = 0
        wrong_questions = []
        questions = []

        print("POSTデータ:", request.POST)  # デバッグ用

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
    print("取得したセッションデータ:", request.session.items())  # デバッグ追加
    score = request.session.get('score', 0)
    wrong_question_ids = request.session.get('wrong_questions', [])
    questions_ids = request.session.get('questions', [])

    print(f"Score: {score}")
    print(f"Wrong Question IDs: {wrong_question_ids}")
    print(f"Question IDs: {questions_ids}")

    questions = Question.objects.filter(id__in=questions_ids)
    wrong_questions = Question.objects.filter(id__in=wrong_question_ids)

    wrong_questions_data = [
        {
            'text': escape(question.text),
            'category': escape(question.category.name) if question.category else '不明なカテゴリ',
            'explanation': escape(question.explanation or '解説はありません。')
        }
        for question in wrong_questions
    ]

    total_score = len(questions) * 10
    score_percent = (score / total_score) * 100 if total_score > 0 else 0

    # 励ましメッセージを設定
    encouragement_messages = {
        'high': "素晴らしい！次回もこの調子で頑張りましょう！",
        'medium': "よく頑張りました！復習してさらに高得点を目指しましょう！",
        'low': "少し難しい問題でしたね。復習をしてもう一度挑戦しましょう！"
    }

    if score_percent >= 80:
        encouragement_message = encouragement_messages['high']
    elif score_percent >= 50:
        encouragement_message = encouragement_messages['medium']
    else:
        encouragement_message = encouragement_messages['low']

    # 次の学習トピックを設定
    next_topic = "二次方程式の解法"  # 実際のロジックではデータベースから選択可能

    return render(request, 'mathquiz/result.html', {
        'score': score,
        'total_score': total_score,
        'score_percent': score_percent,
        'correct_answers': score,
        'total_questions': len(questions),
        'wrong_questions': wrong_questions_data,
        'encouragement_message': encouragement_message,
        'next_topic': next_topic
    })
