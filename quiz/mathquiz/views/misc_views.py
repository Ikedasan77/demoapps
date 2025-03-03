# その他の補助機能
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Question

@login_required(login_url="login")
def preview_question(request, question_id):
    """問題のプレビューを表示"""
    question = get_object_or_404(Question, id=question_id)
    return render(request, "mathquiz/preview.html", {"question": question})
