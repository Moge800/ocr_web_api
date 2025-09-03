import os
from yomitoku import DocumentAnalyzer
from yomitoku.data.functions import load_image, load_pdf
from datetime import datetime
from zipfile import ZipFile
import shutil

analyzer = DocumentAnalyzer(configs={}, visualize=True, device="cpu")


def make_zip(folder_path: str, zip_path: str):
    with ZipFile(zip_path, "w") as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                full_path = os.path.join(root, file)
                arcname = os.path.relpath(full_path, folder_path)
                zipf.write(full_path, arcname)


def ocr_process(img, i, original_filename, export_csv, export_html):
    results, ocr_vis, layout_vis = analyzer(img)
    base_name = os.path.splitext(original_filename)[0]
    if i is None:
        output_csv = os.path.join(export_csv, f"{base_name}.csv")
        output_html = os.path.join(export_html, f"{base_name}.html")
    else:
        output_csv = os.path.join(export_csv, f"{base_name}[{i}].csv")
        output_html = os.path.join(export_html, f"{base_name}[{i}].html")
    results.to_csv(output_csv, img=img, encoding="shift_jis")
    results.to_html(output_html, img=img)


def process_file(file_path: str) -> str:
    # 日時ベースのフォルダ名を生成
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    export_base = f"./export/{timestamp}"
    export_csv = os.path.join(export_base, "csv")
    export_html = os.path.join(export_base, "html")
    export_original = os.path.join(export_base, "original")
    os.makedirs(export_csv, exist_ok=True)
    os.makedirs(export_html, exist_ok=True)
    os.makedirs(export_original, exist_ok=True)

    # オリジナルファイルを保存
    original_filename = os.path.basename(file_path)
    shutil.copy(file_path, os.path.join(export_original, original_filename))

    if file_path.lower().endswith(".pdf"):
        imgs = load_pdf(file_path)
        for i, img in enumerate(imgs, start=1):
            ocr_process(img, i, original_filename, export_csv, export_html)
    else:
        img = load_image(file_path)[0]
        ocr_process(img, None, original_filename, export_csv, export_html)

    # ZIPファイルに圧縮（static/result に保存）
    zip_filename = f"{timestamp}.zip"
    zip_path = os.path.join("static", "result", zip_filename)

    make_zip(export_base, zip_path)

    return zip_path
