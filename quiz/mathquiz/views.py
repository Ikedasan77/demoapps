from django.shortcuts import render, redirect
from .models import Question
import random
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

    # メッセージのリストを定義
    if score_percent == 100:
        advice_list = [
            "素晴らしい！完全に理解しています！",
            "満点おめでとうございます！これからもこの調子で頑張ってください！",
            "すごい！全問正解です！次のチャレンジも期待しています！"
        ]
    elif score_percent >= 80:
        advice_list = [
            "よくできました！あと少しで満点です。",
            "素晴らしい成果です！次回は満点を目指しましょう。",
            "とても良い結果です！引き続き頑張りましょう！"
        ]
    elif score_percent >= 50:
        advice_list = [
            "頑張りました！もう少し復習するとさらに良くなります。",
            "良いスタートです！間違えた問題を復習して次回に備えましょう。",
            "半分以上正解しました！次はもっと良い結果を目指しましょう！"
        ]
    else:
        advice_list = [
            "復習が必要です。間違えた問題を確認しましょう。",
            "少し難しい問題でしたね。復習してもう一度挑戦しましょう！",
            "結果に落ち込まず、復習を重ねて次回頑張りましょう！"
        ]

    # ランダムに励ましメッセージを選択
    advice = random.choice(advice_list)

    return render(request, 'mathquiz/result.html', {
        'score': score,
        'total_score': total_score,
        'score_percent': score_percent,
        'wrong_questions': wrong_questions_data,
        'questions': questions,
        'advice': advice
    })
