from django.contrib import admin
from django.urls import reverse, path
from django.utils.html import format_html
from django.shortcuts import get_object_or_404, render
from .models import Category, Question, IncorrectChoice
from django.db import models
from django.forms import Textarea
from django.utils.safestring import mark_safe
import json

# サイト全体のヘッダーとタイトルをカスタマイズ
admin.site.site_header = "問題登録管理"
admin.site.site_title = "問題管理サイト"
admin.site.index_title = "問題登録"

# **不正解選択肢のインライン設定**
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

# **問題管理用の管理クラス**
class QuestionAdmin(admin.ModelAdmin):
    inlines = [IncorrectChoiceInline]  # インラインフォーム追加

    list_display = ("id", "text", "category", "correct_answer", "explanation_preview", "preview_button")
    list_filter = ("category",)
    search_fields = ("text",)

    formfield_overrides = {
        models.TextField: {"widget": Textarea(attrs={"rows": 3, "cols": 60})},
    }

    # **解説のプレビュー**
    def explanation_preview(self, obj):
        if "http" in obj.explanation:
            return mark_safe(f'<a href="{obj.explanation}" target="_blank">プレビュー</a>')
        return obj.explanation
    explanation_preview.short_description = "解説プレビュー"

    # **一覧画面のプレビューボタン**
    def preview_button(self, obj):
        url = reverse("admin:mathquiz_question_preview", args=[obj.pk])  # 修正: `admin:` を追加
        return format_html('<a class="button" href="{}" target="_blank">編集した問題をプレビュー</a>', url)
    preview_button.short_description = "プレビュー"

    # **編集画面のプレビューボタンを「保存して編集を続ける」の右側に配置**
    def change_view(self, request, object_id, form_url="", extra_context=None):
        extra_context = extra_context or {}
        preview_url = reverse("admin:mathquiz_question_preview", args=[object_id])  # 修正: `admin:` を追加

        # **デバッグログ**
        print(f"DEBUG: change_view() called for question {object_id}")  
        print(f"DEBUG: preview URL generated: {preview_url}")  

        # **プレビューボタンを管理画面のボタンと統一**
        extra_context["preview_button"] = format_html(
            '<a class="button preview-button" href="{}" target="_blank" style="background-color: #5b80b2; color: white; padding: 8px 16px; border-radius: 4px;">'
            '📄 編集した問題をプレビュー</a>',
            preview_url
        )

        return super().change_view(request, object_id, form_url, extra_context=extra_context)

    # **カスタムURLを追加**
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('question_preview/<int:question_id>/', self.admin_site.admin_view(self.preview_question), name="mathquiz_question_preview"),  # 修正: URL名変更
        ]
        return custom_urls + urls  # 既存のURLと統合

    # **プレビュー画面のビュー関数**
    def preview_question(self, request, question_id):
        question = get_object_or_404(Question, pk=question_id)  # 指定したIDの問題を取得
        
        # 選択肢のリストを作成
        choices = [question.correct_answer] + list(IncorrectChoice.objects.filter(question=question).values_list("text", flat=True))
        
        # シャッフルする (ランダム化したい場合)
        import random
        random.shuffle(choices)

        # JSON形式に変換
        question_data = {
            "text": question.text,
            "choices": choices,
            "correct_answer": question.correct_answer,
            "explanation": question.explanation,
            "id": question.id,
        }
        
        # テンプレートへデータを渡す
        return render(request, "admin/preview.html", {
            "question_json": json.dumps(question_data),
        })

# `QuestionAdmin` を Django に登録
admin.site.register(Question, QuestionAdmin)
