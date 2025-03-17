"""
URL configuration for quiz project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# 各 views ファイルから必要な関数をインポート（mathquiz.views. を明示）
from mathquiz.views.auth_views import login_view, register_view, logout_view
from mathquiz.views.misc_views import home, preview_question
from mathquiz.views.quiz_views import quiz_view
from mathquiz.views.score_views import result_view

urlpatterns = [
    path('admin/', admin.site.urls),  # 管理サイト
    path('', home, name='home'),  # ホームページ（views.home ではなく、misc_views.py の home を使用）

    # ログイン・新規登録・ログアウト
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),

    # クイズ関連
    path('quiz/<str:category>/', quiz_view, name='quiz'),
    path('results/', result_view, name='results'),

    # 問題プレビュー
    path('preview/<int:question_id>/', preview_question, name='preview_question'),

    # mathquiz アプリ内の URL を include
    path('', include('mathquiz.urls')),
]

# デバッグツールバー（開発時のみ）
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
