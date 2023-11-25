# vpsc
さくらのVPSの**非公式**クライアントです。  
公開APIの情報をコマンドラインもしくはPython上で容易に扱えるようにすることを目標にしています。  


# 利用方法
## APIキーの定義
環境変数で `VPS_API_KEY` にAPIキーを設定するか、 `~/.vpsc` フォルダに該当変数を記録して利用します。  
オプションでリクエスト先のホストを変更することもできます。  

```shell
VPS_API_KEY=xxx
VPS_API_HOST="https://secure.sakura.ad.jp/vps/api/v7"

```


# その他
## さくらのVPSマニュアル(API)
https://manual.sakura.ad.jp/vps/api/index.html
