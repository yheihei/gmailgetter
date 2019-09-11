# gmailgetter

## 何をするものか

* GMail APIを使って、自分のGmailアカウント宛のメールを任意の検索条件で取得  
* 取得したメールをローカルに出力する

## requirements

* python 3.x

## インストール方法

使用に必要なファイル、パッケージのインストールをします

### 認証情報
[Python Quickstart  |  Gmail API       |  Google Developers](https://developers.google.com/gmail/api/quickstart/python)

1. 上記リンクのstep1より”Enable the Gmail API”ボタンをクリック
2. ”+ Create a new project”を選択し、新規プロジェクトを作成（名前は何でも良い）
3. ”DOWNLOAD CLIENT CONFIGURATION”をクリックして、”credentials.json”をダウンロード。”credentials.json”は、認証に使用します
4. credentials.json を本プロジェクトのルートに配置する

### 必要なパッケージのインストール

```
$ pip install --upgrade google-api-python-client oauth2client
```

## 使い方

### コマンドを叩く

```
python gmailapi.py 検索開始時刻 検索終了時刻 Fromアドレス Toアドレス 件名に含む文字列
```

### OAuth認証をする

コンソールに、URLが表示されるのでそちらをクリックし、OAuth認証を完了させる

### 出力結果例

記載中

### 使用例
```
$ python gmailapi.py '2019-09-11 22:00:00' '2019-09-12 00:00:00' 'example@gmail.com' 'example@gmail.com' 'テスト件名'
```
