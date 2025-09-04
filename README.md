# OCR Web API

## 概要
FlaskベースのOCR（光学文字認識）Webアプリケーションです。画像やPDFファイルをアップロードして、日本語対応のOCR処理を行い、結果をCSVとHTMLファイルでダウンロードできます。

## 機能
- 画像（PNG, JPG, JPEG）およびPDFファイルのアップロード
- yomitokuライブラリを使用した高精度な日本語OCR処理
- OCR結果のCSVおよびHTML形式での出力
- 処理結果のZIPファイルでの一括ダウンロード
- Webインターフェースによる簡単操作

## セットアップ

### 必要な環境
- Python 3.7以上
- Windows環境（PowerShellスクリプト使用）

### インストール手順

1. リポジトリをクローン
```bash
git clone <repository-url>
cd ocr_web_api
```

2. PowerShellスクリプトで自動セットアップ・実行
```powershell
.\launch.ps1
```

このスクリプトは以下を自動実行します：
- 仮想環境の作成（.venv）
- 仮想環境のアクティベート
- 依存関係のインストール（requirements.txt）
- アプリケーションの起動

### 手動セットアップ
```bash
# 仮想環境作成
python -m venv .venv

# 仮想環境アクティベート（Windows）
.venv\Scripts\activate

# 依存関係インストール
pip install -r requirements.txt

# アプリケーション起動
python app.py
```

## 使用方法

1. アプリケーションを起動後、ブラウザで `http://localhost:8080` にアクセス
2. ファイルアップロードページ（web_page.png参照）で画像またはPDFファイルを選択
3. 「アップロードしてOCR処理」ボタンをクリック
4. 処理完了後、結果がZIPファイルとして自動ダウンロード

## ファイル構成

```
ocr_web_api/
├── app.py                 # メインのFlaskアプリケーション
├── ocr_core.py           # OCR処理のコア機能
├── requirements.txt      # Python依存関係
├── launch.ps1           # 自動セットアップ・起動スクリプト
├── templates/
│   └── upload.html      # ファイルアップロード用HTMLテンプレート
├── static/
│   └── result/          # 処理結果ファイル保存用ディレクトリ
├── export/              # OCR処理中間ファイル保存用（自動生成）
└── web_page.png         # アップロードページのスクリーンショット
```

## 主要な依存関係

- **Flask**: Webアプリケーションフレームワーク
- **yomitoku**: 日本語OCRライブラリ
- **waitress**: WSGIサーバー
- **opencv-python**: 画像処理
- **pypdfium2**: PDF処理
- **reportlab**: PDF生成

## 出力ファイル

OCR処理後、以下のファイルが含まれたZIPファイルがダウンロードされます：

- **csv/**: OCR結果のCSVファイル（Shift_JIS エンコーディング）
- **html/**: OCR結果のHTMLファイル（可視化付き）
- **original/**: アップロードした元ファイル

## 技術仕様

- **ポート**: 8080
- **ホスト**: 0.0.0.0（全インターフェースでリッスン）
- **文字エンコーディング**: Shift_JIS（CSV出力）
- **デバイス**: CPU使用（yomitoku設定）
- **ファイル命名**: タイムスタンプベース（YYYYMMDD_HHMMSS）

## 備考

- PDFファイルの場合、各ページごとに個別にOCR処理を実行
- 処理時間はファイルサイズと内容の複雑さに依存
- アップロードファイルは `static/result/` に一時保存され、処理後にZIP化
- 中間ファイルは `export/` フォルダに保存（タイムスタンプ付きフォルダ）