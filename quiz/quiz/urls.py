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
from mathquiz import views  # mathquiz/views.py をインポート

urlpatterns = [
    path('admin/', admin.site.urls),  # 管理サイト
    path('', views.home, name='home'),  # ホームページ

    # ログイン・新規登録・ログアウト
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    # 問題選択画面
    path('category_selection/', views.category_selection_view, name='category_selection'),

    # クイズ関連：カテゴリー情報は必ずURLパスで受け取る
    path('quiz/submit/', views.submit_quiz_view, name='submit_quiz'),
    path('quiz/<str:category>/', views.quiz_view, name='quiz'),

    path('results/', views.result_view, name='results'),

    # プレビュー用のURL
    path('preview/<int:question_id>/', views.preview_question, name='preview_question'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)