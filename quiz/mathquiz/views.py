from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Question
import random
import json
from django.utils.html import escape  # HTMLエスケープ用
from collections import Counter  # 🔴 分野の統計を取るために追加


# 回答の正規化（空白を削除して比較しやすくする）
def normalize_answer(answer):
    return answer.strip()


# 解答が正しいか判定する関数
def is_correct(user_answer, correct_answer):
    return normalize_answer(user_answer) == normalize_answer(correct_answer)


# トップページビュー（ホーム）
def home(request):
    return render(request, 'mathquiz/home.html')


# **ログインビュー**
def login_view(request):
    if request.user.is_authenticated:
        return redirect("/quiz/")

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("/quiz/")
        else:
            messages.error(request, "ユーザーIDまたはパスワードが間違っています")

    return render(request, "mathquiz/login.html")


# **新規登録ビュー**
def register_view(request):
    if request.user.is_authenticated:
        return redirect("/quiz/")

    if request.method == "POST":
        email = request.POST["email"]
        username = request.POST["username"]
        password = request.POST["password"]

        if User.objects.filter(username=username).exists():
            messages.error(request, "このユーザーIDは既に使用されています")
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            login(request, user)
            return redirect("/quiz/")

    return render(request, "mathquiz/register.html")


# **ログアウトビュー**
def logout_view(request):
    logout(request)
    return redirect("/login/")


# **問題表示ビュー**
def quiz_view(request):
    if not request.user.is_authenticated:
        return redirect("/login/")

    if request.method == 'GET':
        questions = list(Question.objects.prefetch_related('incorrect_choices').all())

        num_questions = 10
        selected_questions = random.sample(questions, min(num_questions, len(questions)))

        questions_with_choices = []
        for question in selected_questions:
            incorrect_choices = [escape(choice.text) for choice in question.incorrect_choices.all()]
            all_choices = incorrect_choices + [escape(question.correct_answer)]
            random.shuffle(all_choices)

            questions_with_choices.append({
                'id': question.id,
                'text': escape(question.text),
                'choices': all_choices,
                'correct_answer': escape(question.correct_answer),
                'category': escape(question.category.name) if question.category else '',
                'explanation': escape(question.explanation or '')
            })

        safe_questions_json = json.dumps(questions_with_choices, ensure_ascii=False)

        return render(request, 'mathquiz/quiz.html', {
            'questions_json': safe_questions_json
        })

    return redirect('quiz')


# **解答処理ビュー**
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

        return redirect('results')    # 'results' に修正

    return redirect('quiz')


# **結果表示ビュー**
def result_view(request):
    score = request.session.get('score', 0)
    wrong_question_ids = request.session.get('wrong_questions', [])
    questions_ids = request.session.get('questions', [])

    questions = Question.objects.filter(id__in=questions_ids)
    wrong_questions = Question.objects.filter(id__in=wrong_question_ids)

    total_questions = len(questions)  # 出題された問題数
    correct_answers = score  # 正解数
    wrong_answers = total_questions - correct_answers  # 不正解数

    total_score = 10  # 100点満点基準
    score_percent = (score / total_score) * 100 if total_score > 0 else 0

    # 励ましメッセージ
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

    next_topic = "二次方程式の解法"

    return render(request, 'mathquiz/result.html', {
        'score': score,
        'total_score': total_score,
        'score_percent': score_percent,
        'correct_answers': correct_answers,  # 修正
        'wrong_answers': wrong_answers,  # 追加
        'total_questions': total_questions,
        'encouragement_message': encouragement_message,
        'next_topic': next_topic
    })
