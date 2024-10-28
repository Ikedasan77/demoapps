from django.contrib import admin
from .models import Question

# Questionモデルを管理画面に登録
admin.site.register(Question)
