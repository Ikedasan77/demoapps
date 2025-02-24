from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Category, Question
import random
import json
from django.utils.html import escape


def home(request):
    return render(request, 'mathquiz/home.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect("category_selection")
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("category_selection")
        else:
            messages.error(request, "ユーザーIDまたはパスワードが間違っています")
    return render(request, "mathquiz/login.html")


def register_view(request):
    if request.user.is_authenticated:
        return redirect("category_selection")
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
            return redirect("category_selection")
    return render(request, "mathquiz/register.html")


def logout_view(request):
    logout(request)
    return redirect("login")


def category_selection_view(request):
    if not request.user.is_authenticated:
        return redirect("login")
    categories = Category.objects.all()
    return render(request, "mathquiz/category_selection.html", {"categories": categories})


# ★ 修正済みの quiz_view ★
# URLパスで渡されたカテゴリーをそのまま利用するので、GETパラメータで上書きしません。
def quiz_view(request, category):
    if not request.user.is_authenticated:
        return redirect("login")

    # URLパスで渡された category をそのまま使用
    print(f"選択されたカテゴリー: {category}")

    if not category:
        print("カテゴリーが指定されていません。リダイレクトします。")
        return redirect("category_selection")

    if category == "全分野":
        questions = list(Question.objects.all())
    else:
        questions = list(Question.objects.filter(category__name=category))

    print(f"取得した問題数: {len(questions)}")

    if not questions:
        print(f"警告: '{category}' の問題が見つかりません。カテゴリ選択画面にリダイレクトします。")
        messages.warning(request, f"'{category}' の問題がありません。")
        return redirect("category_selection")

    num_questions = 10
    selected_questions = random.sample(questions, min(num_questions, len(questions)))

    questions_with_choices = []
    for question in selected_questions:
        incorrect_choices = [escape(choice.text) for choice in question.incorrect_choices.all()]
        correct_choices = [escape(answer.text) for answer in question.correct_answers.all()]

        all_choices = incorrect_choices + correct_choices
        random.shuffle(all_choices)

        questions_with_choices.append({
            "id": question.id,
            "text": escape(question.text),
            "choices": all_choices,
            "correct_answer": correct_choices[0] if correct_choices else "",
            "category": category,
            "explanation": escape(question.explanation or ""),
        })

    print(f"生成された問題データ: {json.dumps(questions_with_choices, ensure_ascii=False, indent=2)}")
    safe_questions_json = json.dumps(questions_with_choices, ensure_ascii=False)

    return render(request, "mathquiz/quiz.html", {
        "questions_json": safe_questions_json,
        "selected_category": category
    })


def submit_quiz_view(request):
    if request.method == "POST":
        score = 0
        wrong_questions = []
        questions = []
        for i in range(10):
            user_answer = request.POST.get(f"answer_{i}")
            question_id = request.POST.get(f"question_id_{i}")
            if not question_id:
                continue
            try:
                question = Question.objects.get(id=int(question_id))
                questions.append(question)
            except (Question.DoesNotExist, ValueError):
                continue
            correct_answers = [answer.text.strip() for answer in question.correct_answers.all()]
            if user_answer and user_answer.strip() in correct_answers:
                score += 1
            else:
                wrong_questions.append(question.id)
        total_questions = len(questions)
        request.session["score"] = score
        request.session["wrong_questions"] = wrong_questions
        request.session["questions"] = [q.id for q in questions]
        request.session["total_questions"] = total_questions
        return redirect("results")
    return redirect("quiz")


def result_view(request):
    score = request.session.get("score", 0)
    wrong_question_ids = request.session.get("wrong_questions", [])
    questions_ids = request.session.get("questions", [])
    total_questions = request.session.get("total_questions", 10)
    correct_answers = score
    wrong_answers = total_questions - correct_answers
    score_percent = (score / total_questions) * 100 if total_questions > 0 else 0
    encouragement_messages = {
        "high": "素晴らしい！次回もこの調子で頑張りましょう！",
        "medium": "よく頑張りました！復習してさらに高得点を目指しましょう！",
        "low": "少し難しい問題でしたね。復習をしてもう一度挑戦しましょう！"
    }
    if score_percent >= 80:
        encouragement_message = encouragement_messages["high"]
    elif score_percent >= 50:
        encouragement_message = encouragement_messages["medium"]
    else:
        encouragement_message = encouragement_messages["low"]
    return render(request, "mathquiz/dashboard.html", {
        "score": score,
        "total_questions": total_questions,
        "score_percent": score_percent,
        "correct_answers": correct_answers,
        "wrong_answers": wrong_answers,
        "encouragement_message": encouragement_message
    })


def preview_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    return render(request, "mathquiz/preview.html", {"question": question})