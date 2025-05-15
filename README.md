# GoogleHomeでVOICEVOXを使った読み上げをするやつ

VOICEVOXを使って作成した音声ファイルをGoogleHomeにキャストするためのツールです。

事前にVOICEVOX ENGINEを準備していて下さい。

また、ローカルファイルのキャストが不安定だったので自前のDufsにアップロードする仕様なのでそれも必要です。

設定は.env.exampleを見てください。

## インストール
```
git clone 
```

```
python3.11 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

```
cp .env.example .env
```

.envを編集

## 使い方
```
./voicecast.py "喋らせたい内容" --speed 2 --volume 5
```

