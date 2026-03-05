# 開発チェックリスト

> **📖 読み取り順序**: 5番目 - 開発進捗を追跡

---

## **📋 ドキュメントメタデータ**

- **目的**: 開発セットアップの進捗状況と次のステップを追跡
- **対象読者**: AIエージェント、開発者
- **前提知識**: `04_SETUP.md` に従って環境セットアップが完了していること
- **最終更新**: 2026-03-05

---

## **✅ 初期 DevContainer セットアップ**

### 自動セットアップ完了

- [x] Python 3.11 環境の `Dockerfile` を作成
- [x] `devcontainer.json` の設定完了:
  - Python 開発用 VS Code 拡張機能
  - Python フォーマット (Black) とリント (Ruff)
  - 保存時の自動フォーマット
  - Web 開発用のポート転送
- [x] 全依存関係を含む `requirements.txt` の作成
- [x] プロジェクト構造の設定

### ドキュメント作成完了 ✅

- [x] `00_README_DOCS.md` - ドキュメント読み取りガイド
- [x] `01_PREREQUISITES.md` - 前提条件と制約
- [x] `02_PROJECT_PLAN.md` - プロジェクト概要とロードマップ
- [x] `03_API_DESIGN.md` - CLI 設計ドキュメント
- [x] `04_SETUP.md` - 開発セットアップガイド
- [x] `05_DEVELOPMENT_CHECKLIST.md` - このファイル
- [x] `README.md` - メインプロジェクトドキュメント
- [x] `docs_ja/` - 日本語ドキュメント（同期済み）

### コード構造 ✅

- [x] CLI エントリーポイント (`src/cli/main.py`)
- [x] データモデル (`src/cli/models/service.py`)
- [x] AWS プロバイダー (`src/cli/providers/aws.py`)
- [x] GCP プロバイダー (`src/cli/providers/gcp.py`)
- [x] Azure プロバイダー (`src/cli/providers/azure.py`)
- [x] テスト構造 (`tests/`)

---

## **🎯 次のステップ**

### 1. DevContainer で開く

```bash
# VS Code で:
# 1. Ctrl+Shift+P (macOS では Cmd+Shift+P) を押す
# 2. 「Remote-Containers: Reopen in Container」と入力
# 3. コンテナのビルドを待つ（初回は 2〜3 分）
```

### 2. インストールの確認

```bash
python --version        # Python 3.11+ であること
pip list               # インストール済みパッケージが表示されること
pytest --version       # インストールされていること
```

### 3. クラウド認証情報の設定

プロバイダー固有のセットアップについては [04_SETUP.md](04_SETUP.md) を参照:

- AWS: `~/.aws/credentials` または `AWS_*` 環境変数を設定
- GCP: `GOOGLE_APPLICATION_CREDENTIALS` 環境変数を設定
- Azure: `AZURE_*` 環境変数を設定または `az login` を使用

### 4. セットアップのテスト

```bash
# CLI ヘルプを表示
python -m src.cli.main --help

# ユニットテストの実行
pytest tests/

# カバレッジ付きテストの実行
pytest --cov=src tests/
```

### 5. 開発の開始

- 概要については [02_PROJECT_PLAN.md](02_PROJECT_PLAN.md) を読む
- CLI コマンドについては [03_API_DESIGN.md](03_API_DESIGN.md) を確認
- クラウドプロバイダー機能の実装
- 新機能のテストを記述

---

## **🛠️ 開発コマンド**

```bash
# コードのフォーマット
black src/ tests/

# コードのリント
flake8 src/ tests/

# 型チェック
mypy src/

# テストの実行
pytest
pytest -v                    # 詳細出力
pytest --cov=src            # カバレッジレポート
pytest -k "aws"             # 特定のテストのみ実行

# CLI の使用
python -m src.cli.main list-services
python -m src.cli.main list-services --provider aws --format json
```

---

## **🔧 トラブルシューティング**

### コンテナがビルドできない

```bash
docker volume prune          # 古いボリュームをクリーンアップ
docker system prune         # 未使用のイメージ/コンテナをクリーンアップ
# その後、コンテナで再度開く
```

### 依存関係がインストールできない

```bash
pip cache purge
pip install -r requirements.txt --force-reinstall
```

### 認証情報が機能しない

```bash
# AWS 認証情報の確認
cat ~/.aws/credentials
echo $AWS_ACCESS_KEY_ID

# GCP 認証情報の確認
echo $GOOGLE_APPLICATION_CREDENTIALS
cat $GOOGLE_APPLICATION_CREDENTIALS

# Azure 認証情報の確認
az account show
```

### テストが失敗する

```bash
# 詳細モードでテストを実行
pytest -vv --tb=short

# 特定のテストのみ実行
pytest tests/test_main.py::test_specific_function -v
```

---

**最終更新日**: 2026-03-05  
**前のドキュメント**: [04_SETUP.md](04_SETUP.md)
