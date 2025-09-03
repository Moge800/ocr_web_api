
$venvPath = ".\.venv"
$activateScript = "$venvPath\Scripts\Activate.ps1"
$requirementsFile = "requirements.txt"
$scriptToRun = "app.py"  # 実行したいPythonスクリプト名

# .venv フォルダが存在するか確認
if (-Not (Test-Path $venvPath)) {
    Write-Host "仮想環境が存在しません。作成します..."
    python -m venv $venvPath
}

# 仮想環境をアクティベート
Write-Host "仮想環境をアクティベートします..."
& $activateScript

# 仮想環境のPythonパスを取得
$pythonExe = Join-Path $venvPath "Scripts\python.exe"

# requirements.txt が存在する場合はインストール
if (Test-Path $requirementsFile) {
    Write-Host "依存関係をインストールします..."
    & $pythonExe -m pip install --upgrade pip
    & $pythonExe -m pip install -r $requirementsFile
}

# Pythonスクリプトを仮想環境で実行
Write-Host "Pythonスクリプトを実行します..."
& $pythonExe $scriptToRun
