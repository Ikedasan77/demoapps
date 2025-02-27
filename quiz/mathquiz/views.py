from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Category, Question, UserScore  # ✅ UserScore を追加
import random
import json
from django.utils.html import escape
from django.contrib.auth.decorators import login_required  # ✅ ログイン必須のデコレーターを追加
import logging

# ✅ ログ設定
logger = logging.getLogger(__name__)

def home(request):
    """ホーム画面を表示"""
    return render(request, 'mathquiz/home.html')

def login_view(request):
    """ログイン処理"""
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
    """新規ユーザー登録"""
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
    """ログアウト処理"""
    logout(request)
    return redirect("login")

def category_selection_view(request):
    """カテゴリ選択画面を表示"""
    if not request.user.is_authenticated:
        return redirect("login")
    
    categories = Category.objects.all()
    return render(request, "mathquiz/category_selection.html", {"categories": categories})

@login_required(login_url="login")
def quiz_view(request, category):
    """クイズ画面を表示"""
    if not request.user.is_authenticated:
        return redirect("login")

    logger.info(f"選択されたカテゴリー: {category}")

    if not category:
        messages.warning(request, "カテゴリーが指定されていません")
        return redirect("category_selection")

    request.session["selected_category"] = category or "全分野"

    # ✅ カテゴリーに応じた問題を取得
    questions = list(Question.objects.filter(category__name=category)) if category != "全分野" else list(Question.objects.all())

    logger.info(f"取得した問題数: {len(questions)}")

    if not questions:
        messages.warning(request, f"'{category}' の問題がありません。")
        return redirect("category_selection")

    selected_questions = random.sample(questions, min(10, len(questions)))

    # ✅ 問題と選択肢を格納
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

    safe_questions_json = json.dumps(questions_with_choices, ensure_ascii=False)

    return render(request, "mathquiz/quiz.html", {
        "questions_json": safe_questions_json,
        "selected_category": category
    })

@login_required(login_url="login")
def submit_quiz_view(request):
    """クイズの解答を処理し、成績を保存"""
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

        # ✅ スコアをデータベースに保存
        if request.user.is_authenticated:
            category_name = request.session.get("selected_category", "全分野")
            category = Category.objects.filter(name=category_name).first()
            UserScore.objects.create(user=request.user, category=category, score=score, total_questions=total_questions)

        request.session["score"] = score
        request.session["wrong_questions"] = wrong_questions
        request.session["questions"] = [q.id for q in questions]
        request.session["total_questions"] = total_questions
        return redirect("result")
    
    return redirect("quiz")

@login_required(login_url="login")
def score_history_view(request):
    """成績履歴ページを表示"""
    user_scores = UserScore.objects.filter(user=request.user).order_by('-created_at')

    if not user_scores.exists():
        messages.info(request, "まだ成績履歴がありません。クイズを受けてみましょう！")
    
    return render(request, "mathquiz/score_history.html", {"user_scores": user_scores})

@login_required(login_url="login")
def preview_question(request, question_id):
    """問題のプレビューを表示"""
    question = get_object_or_404(Question, id=question_id)
    return render(request, "mathquiz/preview.html", {"question": question})


@login_required(login_url="login")  # ✅ ログイン必須
def result_view(request):
    """クイズ結果ページを表示"""
    score = request.session.get("score", 0)
    total_questions = request.session.get("total_questions", 10)
    correct_answers = score
    wrong_answers = total_questions - correct_answers
    score_percent = (score / total_questions) * 100 if total_questions > 0 else 0

    encouragement_messages = {
        "high": "素晴らしい！次回もこの調子で頑張りましょう！",
        "medium": "よく頑張りました！復習してさらに高得点を目指しましょう！",
        "low": "少し難しい問題でしたね。復習をしてもう一度挑戦しましょう！"
    }

    encouragement_message = encouragement_messages["high"] if score_percent >= 80 else (
        encouragement_messages["medium"] if score_percent >= 50 else encouragement_messages["low"])

    # ✅ `selected_category` の取得を修正（空文字やNoneを防ぐ）
    selected_category = request.session.get("selected_category") or "全分野"

    return render(request, "mathquiz/dashboard.html", {
        "score": score,
        "total_questions": total_questions,
        "score_percent": score_percent,
        "correct_answers": correct_answers,
        "wrong_answers": wrong_answers,
        "encouragement_message": encouragement_message,
        "selected_category": selected_category,  # ✅ カテゴリを追加
    })