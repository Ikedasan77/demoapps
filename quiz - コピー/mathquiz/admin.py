from django.contrib import admin  # 管理画面のカスタマイズ用モジュールをインポート
from .models import Category, Question, IncorrectChoice  # CategoryとQuestion、IncorrectChoiceモデルをインポート
from django.db import models
from django.forms import Textarea
from django.utils.safestring import mark_safe

# サイト全体のヘッダーとタイトルをカスタマイズ
admin.site.site_header = "問題登録管理"  # 管理画面の上部に表示されるヘッダー
admin.site.site_title = "問題管理サイト"  # ブラウザタブに表示されるタイトル
admin.site.index_title = "問題登録"  # 管理画面のインデックスページのタイトル

# カテゴリ管理用の管理クラス
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")  # 一覧で表示するフィールド
    search_fields = ("name",)  # カテゴリ名で検索可能にする設定

class IncorrectChoiceInline(admin.TabularInline):
    model = IncorrectChoice
    extra = 3  # デフォルトで3つの空の入力欄を表示
    verbose_name = "不正解"
    verbose_name_plural = "不正解の選択肢"
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})},
    }

    class Media:
        js = [
            'https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js',
        ]

# 問題管理用の管理クラス
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [IncorrectChoiceInline]  # インラインフォームを追加

    # 一覧画面で表示するフィールド
    list_display = ("id", "text", "category", "correct_answer", "explanation_preview")
    list_filter = ("category",)  # カテゴリで絞り込み可能
    search_fields = ("text",)  # 問題文で検索可能

    # フォームのカスタマイズ: テキストエリアのサイズ変更
    formfield_overrides = {
        models.TextField: {"widget": Textarea(attrs={"rows": 3, "cols": 60})},
    }

    # 動画や画像リンクのプレビューを表示
    def explanation_preview(self, obj):
        if "http" in obj.explanation:  # 解説にリンクが含まれる場合のみプレビュー表示
            return mark_safe(f'<a href="{obj.explanation}" target="_blank">プレビュー</a>')
        return obj.explanation
    explanation_preview.short_description = "解説プレビュー"  # プレビュー列のヘッダー名

    # 管理画面のフォームをセクションごとに分割
    fieldsets = (
        (None, {  # 基本情報
            "fields": ("text", "correct_answer", "category")
        }),
        ("詳細情報", {  # その他の詳細情報
            "fields": ("explanation", "algebra_expression", "root_value")
        }),
    )

    # Mediaクラスを追加してJavaScriptを読み込み
    class Media:
        js = [
            'https://cdnjs.cloudflare.com/ajax/libs/mathjax/3.2.2/es5/tex-mml-chtml.js',  # MathJaxライブラリ
            'admin/js/latex_preview.js',  # ローカルのプレビュー用スクリプト
        ]
