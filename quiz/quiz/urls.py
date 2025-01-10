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
from mathquiz import views  # 修正済み: mathquiz/views.py をインポート

# プロジェクト全体のURLパターンを定義
urlpatterns = [
    path('admin/', admin.site.urls),  # 管理サイト
    path('', views.home, name='home'),  # ホームページ
    path('quiz/', views.quiz_view, name='quiz'),  # クイズページ
    path('quiz/submit/', views.submit_quiz_view, name='submit_quiz'),  # クイズ送信
    path('results/', views.result_view, name='results'),  # 結果ページ
]

# Debug Toolbar 用の URL パターンを追加
if settings.DEBUG:  # デバッグモードの場合のみ有効
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),  # Debug Toolbar のルートを追加
    ]
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
