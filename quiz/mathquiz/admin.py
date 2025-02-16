from django.contrib import admin
from django.urls import reverse, path
from django.utils.html import format_html
from django.shortcuts import get_object_or_404, render
from .models import Category, Question, IncorrectChoice
from django.db import models
from django.forms import Textarea
from django.utils.safestring import mark_safe

# サイト全体のヘッダーとタイトルをカスタマイズ
admin.site.site_header = "問題登録管理"
admin.site.site_title = "問題管理サイト"
admin.site.index_title = "問題登録"

# カテゴリ管理用の管理クラス
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)

# **このクラスを先に定義**
class IncorrectChoiceInline(admin.TabularInline):
    model = IncorrectChoice
    extra = 3
    verbose_name = "不正解"
    verbose_name_plural = "不正解の選択肢"
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})},
    }

    class Media:
        js = [
            'https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js',
        ]

# **QuestionAdmin を後に定義**
class QuestionAdmin(admin.ModelAdmin):
    inlines = [IncorrectChoiceInline]  # ← ここでエラーが出ないようにする

    list_display = ("id", "text", "category", "correct_answer", "explanation_preview", "preview_button")
    list_filter = ("category",)
    search_fields = ("text",)

    formfield_overrides = {
        models.TextField: {"widget": Textarea(attrs={"rows": 3, "cols": 60})},
    }

    def explanation_preview(self, obj):
        if "http" in obj.explanation:
            return mark_safe(f'<a href="{obj.explanation}" target="_blank">プレビュー</a>')
        return obj.explanation
    explanation_preview.short_description = "解説プレビュー"

    def preview_button(self, obj):
        url = reverse("admin:question_preview", args=[obj.pk])
        return format_html('<a class="button" href="{}" target="_blank">編集した問題をプレビュー</a>', url)
    preview_button.short_description = "プレビュー"

    def change_view(self, request, object_id, form_url="", extra_context=None):
        extra_context = extra_context or {}
        preview_url = reverse("admin:question_preview", args=[object_id])

        print(f"DEBUG: change_view() called for question {object_id}")  # デバッグログ
        print(f"DEBUG: preview URL generated: {preview_url}")  # デバッグログ
        
        extra_context["preview_button"] = format_html(
            '<a class="button" href="{}" target="_blank" style="margin-bottom: 10px; display: inline-block;">📄 編集した問題をプレビュー</a>', 
            preview_url
        )
        return super().change_view(request, object_id, form_url, extra_context=extra_context)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('question_preview/<int:question_id>/', self.admin_site.admin_view(self.preview_question), name="question_preview"),
        ]
        return custom_urls + urls

    def preview_question(self, request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        return render(request, "admin/preview.html", {"question": question})

admin.site.register(Question, QuestionAdmin)
