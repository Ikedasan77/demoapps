from django.contrib import admin
from django.utils.safestring import mark_safe
from django.urls import reverse, path  # ✅ reverse と path をインポート
from django.utils.html import format_html
from django.shortcuts import render, get_object_or_404  # ✅ プレビュー用ビューで必要
from .models import Category, Question, CorrectAnswer, IncorrectChoice


class CorrectAnswerInline(admin.TabularInline):
    """問題に紐づく正解の選択肢をインライン編集できるようにする"""
    model = CorrectAnswer
    extra = 1  # ✅ 新規追加用に1行表示


class IncorrectChoiceInline(admin.TabularInline):
    """問題に紐づく不正解の選択肢をインライン編集できるようにする"""
    model = IncorrectChoice
    extra = 3  # ✅ 新規追加用に3行表示


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """カテゴリ管理"""
    list_display = ('id', 'name')  # ✅ IDとカテゴリ名を一覧に表示
    search_fields = ('name',)  # ✅ カテゴリ名で検索可能に


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """問題管理"""
    list_display = ('id', 'text', 'category', 'get_correct_answers', 'preview_link')  # ✅ preview_link はメソッドとして定義
    search_fields = ('text', 'category__name')
    list_filter = ('category',)
    inlines = [CorrectAnswerInline, IncorrectChoiceInline]

    def get_correct_answers(self, obj):
        """管理画面で正解の選択肢を表示"""
        return ", ".join([answer.text for answer in obj.correct_answers.all()])
    get_correct_answers.short_description = "正解の選択肢"

    def preview_link(self, obj):
        """管理画面にプレビューボタンを追加"""
        try:
            url = reverse('preview_question', args=[obj.id])  # ✅ URLを正しく取得
            return format_html('<a href="{}" target="_blank">プレビュー</a>', url)
        except:
            return "プレビュー不可"  # ✅ URLが存在しない場合の処理
    preview_link.short_description = "プレビュー"  # ✅ 表示名を設定
    preview_link.allow_tags = True  # ✅ HTMLのレンダリングを許可


# ✅ プレビュー用のビューを追加
def preview_question(request, question_id):
    """管理画面からプレビュー画面を表示するビュー"""
    question = get_object_or_404(Question, id=question_id)
    return render(request, 'mathquiz/question_preview.html', {'question': question})


# ✅ Djangoの管理画面のカスタマイズ
admin.site.site_header = "計算アプリ管理画面"
admin.site.site_title = "計算アプリ"
admin.site.index_title = "管理メニュー"


# ✅ Djangoの管理画面にカスタムURLを追加
class CustomAdminSite(admin.AdminSite):
    """カスタム管理サイトのURL設定"""
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('question/<int:question_id>/preview/', preview_question, name='admin_preview_question'),  # ✅ URLパターンを修正
        ]
        return custom_urls + urls


# ✅ カスタム管理画面を適用
admin.site = CustomAdminSite()
admin.site.register(Category, CategoryAdmin)
admin.site.register(Question, QuestionAdmin)
