from django.contrib import admin
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.utils.html import format_html
from .models import Category, Question, CorrectAnswer, IncorrectChoice


class CorrectAnswerInline(admin.TabularInline):
    """問題に紐づく正解の選択肢をインライン編集できるようにする"""
    model = CorrectAnswer
    extra = 1  # 新規追加用に1行表示


class IncorrectChoiceInline(admin.TabularInline):
    """問題に紐づく不正解の選択肢をインライン編集できるようにする"""
    model = IncorrectChoice
    extra = 3  # 新規追加用に3行表示


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """カテゴリ管理"""
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """問題管理"""
    list_display = ('id', 'text', 'category', 'get_correct_answers', 'preview_link')  # ✅ 正解とプレビューリンクを追加
    search_fields = ('text', 'category__name')
    list_filter = ('category',)
    inlines = [CorrectAnswerInline, IncorrectChoiceInline]  # ✅ 正解・不正解をインライン編集可能に

    def get_correct_answers(self, obj):
        """管理画面で正解の選択肢を表示"""
        return ", ".join([answer.text for answer in obj.correct_answers.all()])
    get_correct_answers.short_description = "正解の選択肢"

    def preview_link(self, obj):
        """プレビューボタンを追加"""
        url = reverse('preview_question', args=[obj.id])  # ✅ プレビュー用のURLを生成
        return format_html('<a href="{}" target="_blank">プレビュー</a>', url)
    preview_link.short_description = "プレビュー"


# ✅ プレビュー用のビューを追加するためのURLパターン
from django.urls import path
from django.shortcuts import render, get_object_or_404

def preview_question(request, question_id):
    """管理画面からプレビュー画面を表示するビュー"""
    question = get_object_or_404(Question, id=question_id)
    return render(request, 'mathquiz/question_preview.html', {'question': question})


# ✅ Djangoの管理画面のURLをカスタマイズ
admin.site.site_header = "計算アプリ管理画面"
admin.site.site_title = "計算アプリ"
admin.site.index_title = "管理メニュー"


# ✅ DjangoのURL設定をカスタマイズ
def get_admin_urls(urls):
    def get_urls():
        custom_urls = [
            path('question/<int:question_id>/preview/', preview_question, name='preview_question'),  # プレビュー用URL
        ]
        return custom_urls + urls
    return get_urls

admin.site.get_urls = get_admin_urls(admin.site.get_urls())
