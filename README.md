# book-stand
***
## ★画面設計	
###	【ログイン】
 - 二ソリメンバー限定としたいため、ログイン画面を設ける
 - アカウントIDとPWによる認証とする
	
###	【書籍登録・更新画面】
- ブックスタンドに提供する書籍情報を登録する
- 登録する書籍情報は以下とする
	 - 提供者（必須）
 	- 提供開始日（必須）
 	- 書籍名（必須）
 	- 概要（任意）
- ユーザーが書籍情報を登録・編集する場合は、「保存」ボタンを押下する
	- 「保存」ボタン押下アクション 
	 	- 入力された情報を登録する
		- 現在の貸出ステータス＝「未設定」または「貸出可能」の場合、「貸出可能」に更新する
		- ※すでに登録されているかどうかや、文字種や桁数チェックは行わない
		- 現在の貸出ステータス＝「貸出中」または「提供終了」の場合、貸出ステータスの更新は行わない
	
###	【書籍一覧画面】
- ブックスタンドに提供されている書籍の一覧を表示する（登録されているすべての書籍を表示）
- 表示する書籍情報は以下とする
	- 書籍名
 	- 提供者
 	- 貸出ステータス
- 書籍ごとに[詳細][編集][削除]ボタンを表示する。ただし、[編集]ボタンはログインユーザー＝書籍登録者の場合のみ表示する
	- [削除]ボタンはログインユーザー＝書籍登録者かつ貸出ステータス＝貸出可能の場合のみ表示する
		- [詳細]ボタン押下アクション 
			- 【書籍詳細画面】に遷移する
		- [編集]ボタン押下アクション 
			- 【書籍登録・更新画面】に遷移する
		- [削除]ボタン押下アクション  
			- 【書籍提供終了画面】に遷移する
	
###	【書籍詳細画面】
- 書籍の詳細情報を表示する
- 書籍名、提供者、概要、貸出ステータスを表示する
- ユーザーが該当書籍を借りたい場合は、「貸出」ボタンを押下する
	- 「貸出」ボタンは貸出ステータス＝貸出可能かつ提供開始日＜TODAYの場合のみ表示する
	- 「貸出」ボタン押下アクション
		- ログインユーザーを「貸出者」として登録し、貸出ステータスを「貸出可能」→「貸出中」に更新する
		- 操作日を「貸出日」として登録する
- ユーザーが該当書籍を返却したい場合は、「返却」ボタンを押下する
	- 「返却」ボタンはログインユーザー＝貸出者の場合のみ表示する
 		- 「返却」ボタン押下アクション
		- 【貸出返却画面】に遷移する
	
###	【貸出申請結果画面】
※「貸出」ボタンアクションが成功した場合のみ遷移
- 「貸出が完了しました」の文言を表示
	
###	【貸出返却画面】
　※前提※ 提供者へ返却した後に実行する前提とする
- 書籍名、提供者、概要、貸出ステータスを表示する
- 「返却」ボタンを押下する
	- 「返却」ボタン押下アクション
	- 「貸出者」「貸出日」を初期値に更新する
	- 貸出ステータスを「貸出中」→「貸出可能」に更新する
	
###	【返却結果画面】
- 「返却が完了しました」の文言を表示
	
###	【書籍提供終了画面】
- ブックスタンドに提供した書籍の貸出の終了を登録する
- 表示する書籍情報は以下とする
	- 書籍名
	- 書籍概要
	- 貸出ステータス
- 「提供終了」ボタンを押下する
	- 「提供終了」ボタン押下アクション
	- 貸出ステータスを「貸出可能」→「提供終了」に更新する

***
## ★DB設計	
- 管理が必要な項目名のみ記載
	- 書籍名
	- 書籍概要
	- 提供者
	- 提供開始日
	- 提供終了日
	- 貸出者
	- 貸出日
	- 貸出ステータス
	
# ローカル環境構築手順

## 前提ソフトウェアツール
* git
* python
	* pip

## 構築手順
* 以下、mac環境の手順になります。Windows環境は適宜読み替えてください。
```
git clone https://github.com/kiriharat-bizsys/book-stand.git
cd book-stand
python -m venv env
source env/bin/activate
pip install -r requirements.txt
python manage.py runserver
```
