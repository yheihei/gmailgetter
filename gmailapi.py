# coding: UTF-8
from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import base64
import datetime

class GmailAPI:
  def __init__(self):
    # If modifying these scopes, delete the file token.json.
    self._SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'

  def ConnectGmail(self):
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', self._SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('gmail', 'v1', http=creds.authorize(Http()))
    return service

  def GetMessageList(self,DateFrom,DateTo,MessageFrom, MessageTo, Subject):

    #APIに接続
    service = self.ConnectGmail()

    MessageList = []

    query = ''
    # 検索用クエリを指定する
    if DateFrom != None and DateFrom !="":
      fromDatetime = datetime.datetime.strptime(DateFrom, '%Y-%m-%d %H:%M:%S')
      DateFromUnixTime = fromDatetime.strftime('%s')
      query += 'after:' + DateFromUnixTime + ' '
    if DateTo != None  and DateTo !="":
      toDatetime = datetime.datetime.strptime(DateTo, '%Y-%m-%d %H:%M:%S')
      DateToUnixTime = toDatetime.strftime('%s')
      query += 'before:' + DateToUnixTime + ' '
    if MessageFrom != None and MessageFrom !="":
      query += 'From:' + MessageFrom + ' '
    if MessageTo != None and MessageTo !="":
      query += 'To:' + MessageTo + ' '
    if Subject != None and Subject !="":
      query += 'Subject:' + Subject + ' '
    
    # print(query)

    # メールIDの一覧を取得する(最大1000件)
    messageIDlist = service.users().messages().list(userId='me',maxResults=1000,q=query).execute()
    #該当するメールが存在しない場合は、処理中断
    if messageIDlist['resultSizeEstimate'] == 0: 
      print("Message is not found")
      return MessageList
    
    #メッセージIDを元に、メールの詳細情報を取得
    for message in messageIDlist['messages']:
      row = {}
      row['ID'] = message['id']
      MessageDetail = service.users().messages().get(userId='me',id=message['id']).execute()

      # 日付、送信元、件名を取得する
      for header in MessageDetail['payload']['headers']:
        if header['name'] == 'Date':
          row['Date'] = header['value'] 
        elif header['name'] == 'From':
          row['From'] = header['value']
        elif header['name'] == 'Subject':
          row['Subject'] = header['value']
      
      # 本文の取得
      body = ''
      for part in MessageDetail['payload']['parts']:
        if part['mimeType'] != 'text/plain': # text/plain のものを本文だとみなす
          continue
        b64_encoded_body = part['body']['data']
        charset = 'UTF-8'
        b64_decoded_body_obj = base64.b64decode(b64_encoded_body)
        body = b64_decoded_body_obj.decode(str(charset), errors="replace") # オブジェクトからstring型へ
        break
      row['Body'] = body

      MessageList.append(row)
    return MessageList

if __name__ == '__main__':
  import sys

  args = sys.argv
  if len(args) != 6:
    # 引数が足りない場合エラー終了
    print('引数に DateFrom DateTo MessageFrom MessageTo Subject を指定してください');
    sys.exit(1)

  api = GmailAPI()
  #パラメータは、任意の値を指定する
  messages = api.GetMessageList(
    DateFrom=args[1],    # '2019-09-11 22:00:00'
    DateTo=args[2],      # '2019-09-12 00:00:00'
    MessageFrom=args[3], # 'example@gmail.com'
    MessageTo=args[4],   # 'example@gmail.com'
    Subject=args[5]      # '仕様変更の件について'
    )
  #結果を出力
  for message in messages:
    # 指定のフォーマットで出力
    print('@here')
    print('```')
    print(message['Body'])
    print('```')
    print('\n')