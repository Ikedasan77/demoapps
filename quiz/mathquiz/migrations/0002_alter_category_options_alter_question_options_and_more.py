# Generated by Django 5.1.2 on 2024-12-15 03:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mathquiz', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': '問題種別', 'verbose_name_plural': '問題種別'},
        ),
        migrations.AlterModelOptions(
            name='question',
            options={'verbose_name': '登録した問題', 'verbose_name_plural': '登録した問題'},
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='question',
            name='algebra_expression',
            field=models.TextField(blank=True, help_text='問題に関連する数式を記述します（例: Σ, √, lim）。', verbose_name='数式表現'),
        ),
        migrations.AlterField(
            model_name='question',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mathquiz.category', verbose_name='カテゴリ'),
        ),
        migrations.AlterField(
            model_name='question',
            name='correct_answer',
            field=models.TextField(help_text='複数の正答をカンマ区切りで入力できます（例: √2, 1/2, ∞）。', verbose_name='正答'),
        ),
        migrations.AlterField(
            model_name='question',
            name='explanation',
            field=models.TextField(blank=True, help_text='解説を文章、数式、画像リンク、または埋め込み動画として記述できます。', verbose_name='解説'),
        ),
        migrations.AlterField(
            model_name='question',
            name='root_value',
            field=models.TextField(blank=True, help_text='複数解がある場合はカンマ区切りで入力します（例: 1, -1, √2）。', verbose_name='解の値'),
        ),
        migrations.AlterField(
            model_name='question',
            name='text',
            field=models.TextField(help_text='MathJaxを用いた数式を使用できます。', verbose_name='問題文'),
        ),
    ]