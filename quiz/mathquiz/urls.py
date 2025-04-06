from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# 各 views モジュールから必要なビュー関数をインポートする
from mathquiz.views.quiz_views import home, quiz_view, submit_quiz_view, category_selection  # ← category_selection を追加
from mathquiz.views.score_views import score_history_view, result_view
from mathquiz.views.auth_views import login_view, register_view, logout_view
from mathquiz.views.misc_views import preview_question

# アプリのURLパターンを定義
urlpatterns = [
    path('', home, name='home'),  # トップページ (/) のルート
    path("preview/<int:question_id>/", preview_question, name="preview_question"),  # プレビュー機能
    path('score_history/', score_history_view, name='score_history'),  # 成績履歴のルート

    # **認証関連のURL**
    path('login/', login_view, name='login'),  # ログインページ
    path('register/', register_view, name='register'),  # 新規登録ページ
    path('logout/', logout_view, name='logout'),  # ログアウト処理

    # **クイズ関連のURL**
    path('quiz/', quiz_view, name='quiz'),  # 問題画面を表示
    path('quiz/submit/', submit_quiz_view, name='submit_quiz'),  # クイズの解答を処理
    path('result/', result_view, name='result'),  # 結果画面を表示
    path('category_selection/', category_selection, name='category_selection'),  # ✅ 追加: カテゴリー選択の URL

    # **Django Debug Toolbar（開発用）**
    path('__debug__/', include('debug_toolbar.urls')),
]

# **開発環境での静的ファイルの配信**
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
