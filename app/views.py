from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.http import request
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django_filters.views import FilterView
from django.http import HttpResponse

import logging
import requests

from .filters import ItemFilterSet
from .forms import ItemForm
from .models import Item
from users.models import User


# 未ログインのユーザーにアクセスを許可する場合は、LoginRequiredMixinを継承から外してください。
#
# LoginRequiredMixin：未ログインのユーザーをログイン画面に誘導するMixin
# 参考：https://docs.djangoproject.com/ja/2.1/topics/auth/default/#the-loginrequired-mixin

class ItemFilterView(LoginRequiredMixin, FilterView):
    """
    ビュー：一覧表示画面

    以下のパッケージを使用
    ・django-filter 一覧画面(ListView)に検索機能を追加
    https://django-filter.readthedocs.io/en/master/
    """
    model = Item

    # django-filter 設定
    filterset_class = ItemFilterSet
    # django-filter ver2.0対応 クエリ未設定時に全件表示する設定
    strict = False

    # 1ページの表示
    paginate_by = 10

    def get(self, request, **kwargs):
        """
        リクエスト受付
        セッション変数の管理:一覧画面と詳細画面間の移動時に検索条件が維持されるようにする。
        """

        # 一覧画面内の遷移(GETクエリがある)ならクエリを保存する
        if request.GET:
            request.session['query'] = request.GET
        # 詳細画面・登録画面からの遷移(GETクエリはない)ならクエリを復元する
        else:
            request.GET = request.GET.copy()
            if 'query' in request.session.keys():
                for key in request.session['query'].keys():
                    request.GET[key] = request.session['query'][key]

        return super().get(request, **kwargs)

    def get_queryset(self):
        """
        ソート順・デフォルトの絞り込みを指定
        """
        # デフォルトの並び順として、登録時間（降順）をセットする。
        return Item.objects.all().order_by('-created_at')

    def get_context_data(self, *, object_list=None, **kwargs):
        """
        表示データの設定
        """
        # 表示データを追加したい場合は、ここでキーを追加しテンプレート上で表示する
        # 例：kwargs['sample'] = 'sample'
        return super().get_context_data(object_list=object_list, **kwargs)


class ItemDetailView(LoginRequiredMixin, DetailView):
    """
    ビュー：詳細画面
    """
    model = Item

    # def rakuten_book_api(request):
    #     API_Key = '1079306613313679135'
    #     ISBN = '9784802511193'
    #     url = 'https://app.rakuten.co.jp/services/api/BooksBook/Search/20170404'
    #     query = {
    #         format : 'json',
    #         isbn : ISBN,
    #         applicationId : API_Key
    #     }

    #     r = requests.get(url, params=query)
    #     print("response", r.json())

    def get_context_data(self, **kwargs):
        """
        表示データの設定
        """
        # 表示データの追加はここで 例：
        # kwargs['sample'] = 'sample'
        # self.rakuten_book_api()
        return super().get_context_data(**kwargs)


class ItemCreateView(LoginRequiredMixin, CreateView):
    """
    ビュー：登録画面
    """
    model = Item
    form_class = ItemForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        """
        登録処理
        """

        item = form.save(commit=False)
        item.provider=self.request.user.id
        item.created_by = self.request.user
        item.created_at = timezone.now()
        item.updated_by = self.request.user
        item.updated_at = timezone.now()
        item.save()


        return HttpResponseRedirect(self.success_url)

class ItemUpdateView(LoginRequiredMixin, UpdateView):
    """
    ビュー：更新画面
    """
    model = Item
    form_class = ItemForm
    success_url = reverse_lazy('index')

    def get_update_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('update', kwargs={'pk': pk})

    def form_valid(self, form):
        logger=logging.getLogger('development')
        logger.info(self.request.POST.get('rent_status'))  
        logger.info(self.request.user.id)
        logger.info(self.request.POST.get('renter'))  
        logger.info(self.request.POST.get('provider'))

        pk = self.kwargs['pk']
        renter = Item.objects.values('renter').get(pk=pk)

        """
        更新処理
        """
        
        #貸出ステータス＝10（貸出可能）へ更新する場合
        if self.request.POST.get('rent_status') == "10" :

            #ログインユーザー＝貸出者の場合
            if self.request.user.id == renter.get('renter'):

                logger=logging.getLogger('development')
                aaa = Item.objects.values('renter').get(pk=pk)
                logger.info(type(aaa.get('renter')))
                logger.info(type(self.request.user.id))

                item = form.save(commit=False)
                item.renter = None
                item.updated_by = self.request.user
                item.updated_at = timezone.now()
                item.save()
                messages.success(self.request,"返却処理が成功しました")
                return HttpResponseRedirect(self.success_url, messages)

            #ログインユーザー≠貸出者の場合
            else:
                messages.error(self.request,"貸出者以外は貸出ステータスを「貸出中」に更新できません！")
                return HttpResponseRedirect(self.get_update_url(), messages)

        #貸出ステータス＝30（提供終了）の場合
        elif self.request.POST.get('rent_status') == "30":
            #ログインユーザー=提供者の場合
            if str(self.request.user.id) == renter.get('provider'):
                item = form.save(commit=False)
                item.updated_by = self.request.user
                item.updated_at = timezone.now()
                item.save()
                messages.success(self.request,"ご提供ありがとうございました。")
                return HttpResponseRedirect(self.success_url, messages)
            #ログインユーザー≠貸出者の場合
            else:
                messages.error(self.request,"提供者以外は貸出ステータスを「提供終了」に更新できません！")
                return HttpResponseRedirect(self.get_update_url(), messages)


        #貸出ステータス=20（貸出中）へ更新する場合
        else:
            item = form.save(commit=False)
            item.renter=self.request.user.id
            item.updated_by = self.request.user
            item.updated_at = timezone.now()
            item.save()
            messages.success(self.request,"貸出処理が成功しました")
            return HttpResponseRedirect(self.success_url, messages)


class ItemDeleteView(LoginRequiredMixin, DeleteView):
    """
    ビュー：削除画面
    """
    model = Item
    success_url = reverse_lazy('index')

    def delete(self, request, *args, **kwargs):
        """
        削除処理
        """
        item = self.get_object()
        item.delete()

        return HttpResponseRedirect(self.success_url)
