from django.db import models

# 問題の種類カテゴリモデル
class Category(models.Model):
    name = models.CharField(max_length=100)  # カテゴリ名（例：正負の数、文字式、連立方程式など）

    def __str__(self):
        return self.name

# 問題のモデルクラス
class Question(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # カテゴリモデルとの外部キー関係
    text = models.CharField(max_length=255)  # 問題文
    correct_answer = models.IntegerField()  # 正解の数値（整数計算用）
    explanation = models.TextField()  # 解説文

    # 追加フィールド例（カテゴリによって使い分け）
    algebra_expression = models.CharField(max_length=255, blank=True, null=True)  # 文字式用
    root_value = models.FloatField(blank=True, null=True)  # ルート計算用

    def __str__(self):
        return f"{self.category.name} - {self.text}"  # 管理画面で表示される文字列
