class Question(models.Model):
    CATEGORY_CHOICES = (
        ('integer_calculation', '整数計算'),
        ('algebraic_expression', '文字式の計算'),
        ('simultaneous_equations', '連立方程式'),
        ('expansion', '展開'),
        ('factorization', '因数分解'),
        ('root_operations', 'ルート計算'),
    )
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)  # 問題の種類
    text = models.CharField(max_length=255)  # 問題文
    correct_answer = models.IntegerField()  # 正解の数値（整数計算用）
    explanation = models.TextField()  # 解説文

    # 追加フィールド例（カテゴリによって使い分け）
    algebra_expression = models.CharField(max_length=255, blank=True, null=True)  # 文字式用
    root_value = models.FloatField(blank=True, null=True)  # ルート計算用

    def __str__(self):
        return f"{self.get_category_display()} - {self.text}"  # 管理画面で表示される文字列