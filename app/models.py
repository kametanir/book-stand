from django.db import models

from users.models import User

from django.utils import timezone

from django.conf import settings

class Item(models.Model):
    """
    データ定義クラス
      各フィールドを定義する
    参考：
    ・公式 モデルフィールドリファレンス
    https://docs.djangoproject.com/ja/2.1/ref/models/fields/
    """
    # 項目１　書籍名
    book_name = models.CharField(
        verbose_name='書籍名',
        max_length=100,
        blank=False,
        null=False,
        default='',
    )

    # 項目２　書籍説明
    description = models.TextField(
        verbose_name='書籍説明',
        blank=True,
        null=True,
    )

    # 項目４ 提供開始日
    provide_start_date = models.DateField(
        verbose_name='提供開始日',
        blank=False,
        null=False,
        default=timezone.now, 
    )
    
     # 項目５　貸出ステータス
    STATUS_CHOICES = (
            (10, '貸出可能'),
            (20, '貸出中'),
            (30, '提供終了'),
        )

    rent_status = models.IntegerField(
        verbose_name='貸出ステータス',
        blank=False,
        null=False,
        default=10,
        choices = STATUS_CHOICES,
       )

    # 項目６　貸出者
    renter = models.CharField(
        verbose_name='貸出者',
        max_length=50,
        blank=True,
        null=True,
    )

    # 項目７ 貸出日
    rent_date = models.DateField(
        verbose_name='貸出日',
        blank=True,
        null=True,
    )

    # 以下、管理項目
    # 提供者
    provider = models.CharField(
        verbose_name='提供者',
        max_length=50,
        blank=False,
        null=False,
        default='',
        editable=False,
    )

    # 提供者ID
    provide_by = models.ForeignKey(
        User,
        verbose_name='提供者ID',
        blank=False,
        null=False,
        default=1,
        editable=False,
        on_delete=models.CASCADE,
    )

    # 作成者(ユーザー)
    created_by = models.ForeignKey(
        User,
        verbose_name='作成者',
        blank=True,
        null=True,
        related_name='CreatedBy',
        on_delete=models.SET_NULL,
        editable=False,
    )

    # 作成時間
    created_at = models.DateTimeField(
        verbose_name='作成時間',
        blank=True,
        null=True,
        editable=False,
    )

    # 更新者(ユーザー)
    updated_by = models.ForeignKey(
        User,
        verbose_name='更新者',
        blank=True,
        null=True,
        related_name='UpdatedBy',
        on_delete=models.SET_NULL,
        editable=False,
    )


    # 更新時間
    updated_at = models.DateTimeField(
        verbose_name='更新時間',
        blank=True,
        null=True,
        editable=False,
    )



    def __str__(self):
        """
        リストボックスや管理画面での表示
        """
        return self.book_name

    class Meta:
        """
        管理画面でのタイトル表示
        """
        verbose_name = 'ブックスタンドマネージャー'
        verbose_name_plural = 'ブックスタンドマネージャー'
