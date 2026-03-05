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

### GitHub リポジトリセットアップ ✅

- [x] GitHub CLI (`gh`) のインストール
- [x] GitHub で認証（Fine-grained トークン）
- [x] リモートリポジトリを作成: https://github.com/PLAYER1-r7/CloudServiceManager
- [x] 初回コミットをプッシュ
- [x] 開発追跡用に 7 件の GitHub Issue を作成
  - CloudService データモデル実装
  - クラウド認証メカニズム
  - AWS/GCP/Azure プロバイダー実装
  - list-services コマンド実装
  - 統合テストと最適化

---

## **🎯 次のステップ**

### 1. 開発タスク一覧を表示

すべての開発タスクは GitHub Issues として追跡管理されています：

```bash
# すべての Issue を表示
gh issue list --repo PLAYER1-r7/CloudServiceManager

# Issue の詳細を表示
gh issue view 5 --repo PLAYER1-r7/CloudServiceManager  # 例: Week 2 - AWS 実装

# ラベルでフィルタリング
gh issue list --repo PLAYER1-r7/CloudServiceManager --label "week-2"
```

**作成された開発 Issue**：
- [#1](https://github.com/PLAYER1-r7/CloudServiceManager/issues/1) - CloudService データモデル完成・テスト
- [#2](https://github.com/PLAYER1-r7/CloudServiceManager/issues/2) - クラウド認証メカニズム実装
- [#3](https://github.com/PLAYER1-r7/CloudServiceManager/issues/3) - Week 3: GCP プロバイダー実装
- [#4](https://github.com/PLAYER1-r7/CloudServiceManager/issues/4) - Week 4: 統合テストと最適化
- [#5](https://github.com/PLAYER1-r7/CloudServiceManager/issues/5) - Week 2: AWS プロバイダー実装
- [#6](https://github.com/PLAYER1-r7/CloudServiceManager/issues/6) - list-services コマンド実装完成
- [#7](https://github.com/PLAYER1-r7/CloudServiceManager/issues/7) - Week 3: Azure プロバイダー実装

詳細は [GitHub Issues ページ](https://github.com/PLAYER1-r7/CloudServiceManager/issues) をご覧ください。

### 2. DevContainer で開く

```bash
# VS Code で:
# 1. Ctrl+Shift+P (macOS では Cmd+Shift+P) を押す
# 2. 「Remote-Containers: Reopen in Container」と入力
# 3. コンテナのビルドを待つ（初回は 2〜3 分）
```

### 3. インストールの確認

```bash
python --version        # Python 3.11+ であること
pip list               # インストール済みパッケージが表示されること
pytest --version       # インストールされていること
```

### 4. クラウド認証情報の設定

プロバイダー固有のセットアップについては [04_SETUP.md](04_SETUP.md) を参照:

- AWS: `~/.aws/credentials` または `AWS_*` 環境変数を設定
- GCP: `GOOGLE_APPLICATION_CREDENTIALS` 環境変数を設定
- Azure: `AZURE_*` 環境変数を設定または `az login` を使用

### 5. セットアップのテスト

```bash
# CLI ヘルプを表示
python -m src.cli.main --help

# ユニットテストの実行
pytest tests/

# カバレッジ付きテストの実行
pytest --cov=src tests/
```

### 6. プロジェクト管理ツールの活用

```bash
# 次に取り組むべきタスクを確認
python .github/project_manager.py all

# タスク推奨事項を表示
python .github/project_manager.py recommend

# 進捗状況を追跡
python .github/project_manager.py report
```

**AI エージェントガイド**: [.github/AI_AGENT_PROJECT_GUIDE.md](../.github/AI_AGENT_PROJECT_GUIDE.md) を参照

### ⚠️ GitHub Project ステータス管理（必須）

**ルール: Issue 作業開始時は必ず Project のステータスを更新してください**

```bash
# Issue 作業開始時
bash .github/scripts/update_project_status.sh <ISSUE番号> "In progress"

# PR 作成後（レビュー待ち）
bash .github/scripts/update_project_status.sh <ISSUE番号> "In review"

# PR Merge 後（完了）
bash .github/scripts/update_project_status.sh <ISSUE番号> "Done"
```

利用可能なステータス: `Backlog`, `Ready`, `In progress`, `In review`, `Done`

詳細なワークフローガイド: [.github/PROJECT_WORKFLOW.md](../.github/PROJECT_WORKFLOW.md)

### 7. 開発の開始

- 概要については [02_PROJECT_PLAN.md](02_PROJECT_PLAN.md) を読む
- CLI コマンドについては [03_API_DESIGN.md](03_API_DESIGN.md) を確認
- プロジェクトマネージャーからの優先順位推奨に従う
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
