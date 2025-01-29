from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views  # viewsをインポート

# アプリのURLパターンを定義
urlpatterns = [
    path('', views.home, name='home'),  # トップページ (/) のルート

    # **認証関連のURL**
    path('login/', views.login_view, name='login'),  # ログインページ
    path('register/', views.register_view, name='register'),  # 新規登録ページ
    path('logout/', views.logout_view, name='logout'),  # ログアウト処理

    # **クイズ関連のURL**
    path('quiz/', views.quiz_view, name='quiz'),  # 問題画面を表示
    path('quiz/submit/', views.submit_quiz_view, name='submit_quiz'),  # クイズの解答を処理
    path('result/', views.result_view, name='result'),  # 結果画面を表示

    # **Django Debug Toolbar（開発用）**
    path('__debug__/', include('debug_toolbar.urls')),
]

# **開発環境での静的ファイルの配信**
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
