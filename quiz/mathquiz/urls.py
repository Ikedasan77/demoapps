from django.urls import path
from . import views

# アプリのURLパターンを定義
urlpatterns = [
    path('', views.quiz_view, name='quiz'),  # ルートURLでquiz_viewを表示
]
