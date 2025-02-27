from django.db import models
from django.contrib.auth.models import User

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
        on_delete=models.SET_NULL,  # ✅ カテゴリ削除時にNULLを設定
        null=True,
        blank=True,
        help_text="この問題が属するカテゴリを選択してください。"
    )

    def save(self, *args, **kwargs):
        if not self.algebra_expression and self.text:  # ✅ text が None の場合のチェック
            self.algebra_expression = self.text
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "登録した問題"
        verbose_name_plural = "登録した問題"

    def __str__(self):
        category_name = self.category.name if self.category else "未分類"
        return f"[{category_name}] {self.text}"

class CorrectAnswer(models.Model):  # ✅ 正解の選択肢を独立したモデルに変更
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="correct_answers",
        verbose_name="正答"
    )
    text = models.TextField(
        verbose_name="正解の選択肢",
        help_text="この選択肢を登録してください。"
    )

    class Meta:
        verbose_name = "正解の選択肢"
        verbose_name_plural = "正解の選択肢"

    def __str__(self):
        return f"正解: {self.text} (問題: {self.question.text})"

class IncorrectChoice(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="incorrect_choices",
        verbose_name="問題"
    )
    text = models.TextField(
        verbose_name="不正解の選択肢",
        help_text="この選択肢を登録してください。"
    )

    class Meta:
        verbose_name = "不正解の選択肢"
        verbose_name_plural = "不正解の選択肢"

    def __str__(self):
        return f"不正解選択肢: {self.text} (問題: {self.question.text})"

class UserScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # ユーザー情報
    category = models.ForeignKey("Category", on_delete=models.SET_NULL, null=True, blank=True)  # カテゴリー
    score = models.IntegerField()  # スコア
    total_questions = models.IntegerField()  # 総問題数
    created_at = models.DateTimeField(auto_now_add=True)  # 成績記録日時

    def __str__(self):
        return f"{self.user.username} - {self.category.name if self.category else '全カテゴリ'}: {self.score}/{self.total_questions}"
