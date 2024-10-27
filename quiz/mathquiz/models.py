from django.db import models

# 問題のモデルクラス
class Question(models.Model):
    text = models.CharField(max_length=255)  # 問題文
    correct_answer = models.IntegerField()  # 正解の数値
    explanation = models.TextField()  # 解説文

    def __str__(self):
        return self.text  # 管理画面などで表示される文字列