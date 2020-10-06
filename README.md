# リモ奉行

オンラインコミュニケーションを円滑にするためのツール

## 各関数について
* todb.js
ESP32より送信されたデータをDBに記録する
* getdb.js
定期的にDBからデータ群を取得し、judge.pyに渡す
* judge.py
与えられたデータから、次に行動すべき人/行動の種類を決定し、判定結果をDBに登録/Slackに通知する。
* showresult.js
ESP32からのリクエストに基づき、最新の判定結果をDBから取得/JSONとして返却する。
* showresult2.js
デバック用API

## 参考
[Cosmos DB入出力バインドを使ったAzure FunctionsをJavaScriptで実装する - PaaSがかりの部屋](https://k-miyake.github.io/blog/functions-cosmosdb-bindings/)
