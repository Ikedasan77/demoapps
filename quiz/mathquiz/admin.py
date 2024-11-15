from django.contrib import admin
from .models import Category, Question  # CategoryとQuestionモデルをインポート

# Categoryモデルを管理画面に登録
admin.site.register(Category)

# Questionモデルの管理設定
class QuestionAdmin(admin.ModelAdmin):
    # 管理画面で表示するフィールドリスト
    list_display = ('text', 'category', 'correct_answer')
    # 問題をカテゴリで絞り込み可能にする
    list_filter = ('category',)
    # 問題文で検索できるようにする
    search_fields = ('text',)

# Questionモデルをカスタム設定で管理画面に登録
admin.site.register(Question, QuestionAdmin)
