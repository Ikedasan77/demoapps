# クイズ関連の処理
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.html import escape
from django.http import JsonResponse  # ← インポート追加
import random
import json
import logging
from mathquiz.models import Question, Category  # 修正済み

logger = logging.getLogger(__name__)

# ✅ トップページを表示する関数 (home)
def home(request):
    """トップページを表示"""
    return render(request, 'mathquiz/home.html')  # 必ず 'mathquiz/home.html' というテンプレートを作成してください

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

    questions = list(Question.objects.filter(category__name=category)) if category != "全分野" else list(Question.objects.all())

    logger.info(f"取得した問題数: {len(questions)}")

    if not questions:
        messages.warning(request, f"'{category}' の問題がありません。")
        return redirect("category_selection")

    selected_questions = random.sample(questions, min(10, len(questions)))

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


# ✅ 追加: クイズの解答を処理するビュー関数 (submit_quiz_view)
@login_required(login_url="login")
def submit_quiz_view(request):
    """クイズの解答を処理"""
    if request.method == "POST":
        # フロントエンドから送信されたJSONデータを取得
        submitted_data = json.loads(request.body)

        # 必要なデータを取り出す
        user_answers = submitted_data.get("user_answers", {})
        category = request.session.get("selected_category", "全分野")
        
        # 正答数をカウント
        correct_count = 0
        total_count = len(user_answers)
        
        for question_id, user_answer in user_answers.items():
            try:
                question = Question.objects.get(id=question_id)
                correct_answers = [answer.text for answer in question.correct_answers.all()]

                if user_answer in correct_answers:
                    correct_count += 1
            except Question.DoesNotExist:
                logger.warning(f"問題が存在しません: {question_id}")

        # 成績を保存するなどの処理を追加可能

        # 結果をフロントエンドに返す
        response_data = {
            "correct_count": correct_count,
            "total_count": total_count,
            "score": (correct_count / total_count) * 100 if total_count > 0 else 0,
        }

        return JsonResponse(response_data)

    # POST 以外のリクエストは許可しない
    return JsonResponse({"error": "POSTリクエストのみ許可されています。"}, status=400)

# ✅ カテゴリー選択画面を表示するビュー関数 (これが必要です)
def category_selection(request):
    """カテゴリー選択画面を表示するビュー"""
    return render(request, 'mathquiz/category_selection.html')