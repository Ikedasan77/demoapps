from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "問題種別"
        verbose_name_plural = "問題種別"

    def __str__(self):
        return self.name


class Question(models.Model):
    text = models.TextField(
        verbose_name="問題文",
        help_text="MathJaxを用いた数式を使用できます。"
    )
    correct_answer = models.TextField(
        verbose_name="正答",
        help_text="複数の正答をカンマ区切りで入力できます（例: √2, 1/2, ∞）。"
    )
    explanation = models.TextField(
        verbose_name="解説",
        blank=True,
        help_text="解説を文章、数式、画像リンク、または埋め込み動画として記述できます。"
    )
    algebra_expression = models.TextField(
        verbose_name="数式表現",
        blank=True,
        null=True,  # NULL値を許可
        help_text="問題に関連する数式を記述します（例: Σ, √, lim）。"
    )
    root_value = models.TextField(
        verbose_name="解の値",
        blank=True,
        help_text="複数解がある場合はカンマ区切りで入力します（例: 1, -1, √2）。"
    )
    category = models.ForeignKey(
        Category,
        verbose_name="カテゴリ",
        on_delete=models.CASCADE,
        help_text="この問題が属するカテゴリを選択してください。"
    )

    # 自動コピー機能を追加
    def save(self, *args, **kwargs):
        if not self.algebra_expression:  # 数式表現が空の場合のみ自動コピー
            self.algebra_expression = self.text
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "登録した問題"
        verbose_name_plural = "登録した問題"

    def __str__(self):
        return f"[{self.category.name}] {self.text}"
