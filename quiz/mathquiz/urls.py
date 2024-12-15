from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views  # viewsをインポート

# アプリのURLパターンを定義
urlpatterns = [
    path('', views.home, name='home'),  # トップページ (/) のルートを追加
    path('quiz/', views.quiz_view, name='quiz'),  # 問題画面を表示するURL
    path('quiz/submit/', views.submit_quiz_view, name='submit_quiz'),
    path('result/', views.result_view, name='result'),  # 結果画面を表示するURL
]

# 開発環境でのみ静的ファイルを配信する設定を追加
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
