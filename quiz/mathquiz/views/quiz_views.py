# クイズ関連の処理
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.html import escape
import random
import json
import logging
from .models import Question, Category

logger = logging.getLogger(__name__)

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
