# 開発チェックリスト

> **📖 読み取り順序**: 5番目 - 開発進捗を追跡

---

## **📋 ドキュメントメタデータ**

- **目的**: 開発セットアップの進捗状況と次のステップを追跡
- **対象読者**: AIエージェント、開発者
- **前提知識**: `04_SETUP.md` に従って環境セットアップが完了していること
- **最終更新**: 2026-03-06

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
- [x] データモデル (`src/cli/models/service.py`) - **Issue #2 ✅ 完了 (95%カバレッジ)**
- [x] AWS プロバイダー (`src/cli/providers/aws.py`)
- [x] GCP プロバイダー (`src/cli/providers/gcp.py`)
- [x] Azure プロバイダー (`src/cli/providers/azure.py`)
- [x] テスト構造 (`tests/`)

### Issue 完了状況 📊

#### ✅ 完了済み

- **Issue #2**: CloudService Pydantic モデル (完了)
  - 7つの必須フィールドを持つ Pydantic CloudService モデルを作成
  - ISO 8601 日時検証
  - 95% テストカバレッジ (31 テスト成功)
  - バージョン: 1.0.0.0 → 1.0.1.8

- **Issue #6**: クラウドプロバイダー認証実装 (完了 - PR #18 マージ済み)
  - CloudAuthBase 抽象基底クラス (84行)
  - AWSAuth 実装 (156行) - boto3 Session、環境変数、credentials ファイル、IAM ロール
  - GCPAuth 実装 (179行) - Application Default Credentials、サービスアカウント
  - AzureAuth 実装 (168行) - DefaultAzureCredential チェーン
  - マルチクラウド管理用 CloudAuthManager (217行)
  - 包括的なテストスイート (46テスト、62%カバレッジ)
  - 依存関係追加: azure-mgmt-resource
  - バージョン: 1.0.1.8 → 1.0.2.0

- **Issue #5**: AWS プロバイダー実装 (完了)
  - AWSAuth 統合済み AWSProvider クラス (99行)
  - 単一または全リージョンでの EC2 インスタンス一覧取得
  - 包括的メタデータを含む CloudService モデル変換
  - 未承認リージョンや存在しないインスタンスのエラーハンドリング
  - AWSAuth 経由の複数認証方法サポート
  - 包括的テストスイート (17テスト、85%カバレッジ)
  - `test_aws_provider.py` を完全なテストカバレッジで作成
  - すべてのテストがパス (130 パス、3 スキップ)
  - バージョン: 1.0.2.0 → 1.0.3.0

- **Issue #3**: GCP プロバイダー実装 (完了)
  - GCPAuth 統合済み GCPProvider クラス (255行)
  - 単一または全ゾーンでの Compute Engine インスタンス一覧取得
  - 包括的メタデータを含む CloudService モデル変換
  - 包括的テストスイート (17テスト、79%カバレッジ)
  - `test_gcp_provider.py` を作成
  - バージョン: 1.0.3.0 → 1.0.4.0

- **Issue #7**: Azure プロバイダー実装 (完了)
  - AzureAuth 統合済み AzureProvider クラス (310行)
  - 複数リソースグループ/リージョンでの VM 一覧取得
  - Power state 抽出を含む CloudService モデル変換
  - 包括的テストスイート (16テスト、83%カバレッジ)
  - `test_azure_provider.py` を作成
  - バージョン: 1.0.4.0 → 1.0.5.0

- **Issue #1**: list-services コマンド実装 (完了)
  - `aws|gcp|azure|all` の厳密な provider 選択を実装
  - マルチプロバイダー集約と部分失敗時の警告表示を実装
  - JSON / table / CSV 出力を統一モデルで実装
  - CLI のユニットテストを追加
  - バージョン: 1.0.5.0 → 1.0.6.0

- **Issue #4**: 統合テストと最適化 (完了)
  - CLI 統合テスト (`tests/test_cli_integration.py`) を追加
  - region 引き渡しと provider dispatch の統合検証を追加
  - 出力順の決定性と CSV 出力を最適化
  - フルテスト結果: 172 passed, 1 skipped
  - バージョン: 1.0.6.0 → 1.0.7.0

- **Phase 2**: Web API スケルトン (進行中)
  - FastAPI アプリケーションスケルトンを作成 (`src/api/main.py`)
  - コアエンドポイントを実装:
    - `GET /health` - ヘルスチェックエンドポイント
    - `GET /services` - プロバイダー/リージョンフィルタ付きサービス一覧
    - `GET /services/{provider}/{service_id}` - 特定サービスの詳細取得
  - フォールトトレラントなプロバイダー初期化（利用不可プロバイダーをスキップ）
  - API テストスイートを作成 (`tests/test_api_main.py`、4テスト通過）
  - API 起動スクリプトを作成 (`scripts/start_api.sh`)
  - README.md に API 利用方法を追記
  - 依存関係追加: fastapi, uvicorn, httpx
  - インタラクティブ API ドキュメント (`/docs` と `/redoc`) 利用可能
  - バージョン: 1.0.7.0 → 2.0.0-alpha

#### 🚧 実装中
なし（Phase 1 対象はすべて完了）

#### 📋 保留中
なし

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

## **📊 現在の開発状況**

### 現在のバージョン

**VERSION: 1.0.7.0**（2026年3月6日現在）

バージョン形式: `W.X.Y.Z`
- W (Major): ユーザー指示による戦略的変更
- X (Minor): ユーザー指示による機能追加
- Y (Development): develop ブランチへのプッシュごとに増加
- Z (Commit): コミットごとに増加

詳細なバージョニングルールは [01_PREREQUISITES.md](01_PREREQUISITES.md) を参照。

### ✅ 完了した作業

#### Issue #2: CloudService データモデル完成・テスト（完了）
- **ステータス**: ✅ 完了、develop にマージ済み
- **PR**: [#17](https://github.com/PLAYER1-r7/CloudServiceManager/pull/17)
- **達成内容**:
  - dataclass から Pydantic BaseModel への移行
  - 厳格なフィールド検証の実装
  - ISO 8601 タイムスタンプ検証の追加
  - シリアライゼーション/デシリアライゼーションメソッドの作成
  - **テストカバレッジ**: 95%（目標: 80%以上）
  - **テスト**: 27 ユニットテスト + 6 統合テスト = 31 passed、2 skipped
- **変更ファイル**: 39 ファイル（+7,016/-34 行）
- **バージョン**: 1.0.0.1 → 1.0.0.6（6 コミット）
- **マージ日**: 2026年3月5日

**主な成果物**:
- `src/cli/models/service.py` - Pydantic ベースの CloudService モデル
- `tests/test_models.py` - 包括的なユニットテスト
- `tests/test_aws_integration.py` - AWS プロバイダー統合テスト

#### プロジェクト管理自動化（完了）
- **ステータス**: ✅ 実装完了
- **ツール**: `.github/scripts/update_project_status.sh`
- **ルール**: Issue 開始/完了時のステータス更新が必須
- **ワークフロー**: Backlog → In progress → In review → Done
- **ドキュメント**: [.github/PROJECT_WORKFLOW.md](../.github/PROJECT_WORKFLOW.md)

#### 開発環境の改善（完了）
- **ステータス**: ✅ 完了
- **追加**: Ruff リンター（Flake8 の最新代替）
- **更新**: `requirements.txt`、`Dockerfile`
- **利点**: より高速なリント、より良いエラーメッセージ

#### GitHub インフラストラクチャ（完了）
- **ステータス**: ✅ 完了
- **追加内容**:
  - CI/CD ワークフロー（`.github/workflows/ci.yml`）
  - 自動ラベル付き Issue テンプレート
  - GitHub Discussion 自動化スクリプト
  - ブランチ保護ルール（develop + main）
  - セットアップ自動化スクリプト

### 🚧 進行中

- なし。Phase 1 の Issue #1 - #7 はすべて完了。

### 📅 今後の作業

1. Phase 2 API 設計タスクの整理
2. FastAPI エンドポイントとデータ契約の提案作成
3. Phase 1 完了のリリースノートとタグ準備

### 📈 進捗メトリクス

- **完了 Issue**: 7/7（100%）
- **全体テストカバレッジ**: 85%（`src` 全体）
- **CLIカバレッジ**: 85%（`src/cli/main.py` の unit + integration）
- **テスト結果**: 172 passed, 1 skipped
- **バージョン**: 1.0.7.0

---

## **🛠️ 開発コマンド**

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

**最終更新日**: 2026-03-06  
**前のドキュメント**: [04_SETUP.md](04_SETUP.md)
