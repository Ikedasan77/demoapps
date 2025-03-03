# 成績関連の処理
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserScore

@login_required(login_url="login")
def score_history_view(request):
    """成績履歴ページを表示"""
    user_scores = UserScore.objects.filter(user=request.user).order_by('-created_at')

    if not user_scores.exists():
        messages.info(request, "まだ成績履歴がありません。クイズを受けてみましょう！")

    return render(request, "mathquiz/score_history.html", {"user_scores": user_scores})
