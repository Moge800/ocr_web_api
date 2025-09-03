from flask import Flask, request, send_from_directory, render_template
import os
from ocr_core import process_file  # OCR処理を行う関数をインポート
from datetime import datetime

app = Flask(__name__)
UPLOAD_FOLDER = "static/result"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def upload_form():
    return render_template("upload.html")


@app.route("/upload", methods=["POST"])
def upload_file():
    file = request.files["file"]

    # 拡張子を取得
    ext = os.path.splitext(file.filename)[1]

    # 日時でファイル名を生成（例: 20250801_130245.pdf）
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}{ext}"

    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)
    print(filepath)

    # OCR処理
    result_path = process_file(filepath)  # 処理後ファイルのパスを返すようにする

    return send_from_directory("static/result", os.path.basename(result_path), as_attachment=True)


if __name__ == "__main__":
    from waitress import serve

    serve(app, host="0.0.0.0", port=8080)
