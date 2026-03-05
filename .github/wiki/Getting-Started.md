# はじめに - CloudServiceManager

> マルチクラウド環境を統一的に管理する CLI ツール

**現在のステータス**: Phase 1（CLI開発）進行中 - バージョン 1.0.1.7

---

## 📖 このガイドについて

CloudServiceManagerは現在開発中のプロジェクトです。このガイドでは、開発者がプロジェクトに参加するための手順を説明します。

**⚠️ 注意**: エンドユーザー向けの機能は Phase 1 完了後に利用可能になります。

---

## 🎯 前提条件

### 必須ツール

- **Docker** と **Docker Compose**
- **VS Code** と **Remote Containers 拡張機能**
- **Git** (2.30+)
- **GitHub アカウント**

### 推奨環境

- Linux、macOS、または WSL2 上の Windows
- 8GB+ RAM
- 10GB+ ディスク空き容量

---

## 🚀 セットアップ手順

### 1. リポジトリのクローン

```bash
git clone https://github.com/PLAYER1-r7/CloudServiceManager.git
cd CloudServiceManager
```

### 2. DevContainer で開く

```bash
# VS Code でプロジェクトを開く
code .

# コマンドパレットを開く (Ctrl+Shift+P または Cmd+Shift+P)
# 「Remote-Containers: Reopen in Container」を選択

# コンテナのビルドを待つ（初回は 2〜3 分）
```

### 3. インストールの確認

DevContainer が起動したら、ターミナルで確認:

```bash
# Python バージョン確認
python --version
# 出力: Python 3.11.x

# 依存関係確認
pip list | grep -E "boto3|pydantic|pytest"

# テスト実行
pytest tests/ -v
# 出力: 31 passed, 2 skipped
```

---

## 🧪 現在利用可能な機能

### CloudService データモデル（✅ 完了）

```python
from src.cli.models.service import CloudService, CloudProvider

# CloudService インスタンスの作成
service = CloudService(
    provider=CloudProvider.AWS,
    service_type="EC2",
    resource_id="i-1234567890abcdef0",
    name="web-server-01",
    region="us-east-1",
    status="running",
    created_at="2026-03-05T10:00:00Z"
)

# JSON にシリアライズ
json_data = service.model_dump_json()

# 辞書から復元
service_dict = service.model_dump()
restored = CloudService(**service_dict)
```

**テストカバレッジ**: 95%（31 テスト合格）

---

## 📚 開発ドキュメント

### 必読ドキュメント（順番に読む）

1. **[前提条件](https://github.com/PLAYER1-r7/CloudServiceManager/blob/develop/docs_ja/01_PREREQUISITES.md)** - 技術スタックと制約
2. **[プロジェクト計画](https://github.com/PLAYER1-r7/CloudServiceManager/blob/develop/docs_ja/02_PROJECT_PLAN.md)** - 全体のロードマップ
3. **[CLI設計](https://github.com/PLAYER1-r7/CloudServiceManager/blob/develop/docs_ja/03_API_DESIGN.md)** - コマンド仕様
4. **[セットアップガイド](https://github.com/PLAYER1-r7/CloudServiceManager/blob/develop/docs_ja/04_SETUP.md)** - 開発環境構築
5. **[開発チェックリスト](https://github.com/PLAYER1-r7/CloudServiceManager/blob/develop/docs_ja/05_DEVELOPMENT_CHECKLIST.md)** - 進捗状況

### プロジェクト管理

- **[GitHub Project Board](https://github.com/users/PLAYER1-r7/projects/1)** - タスク管理
- **[GitHub Issues](https://github.com/PLAYER1-r7/CloudServiceManager/issues)** - 開発タスク一覧
- **[Pull Requests](https://github.com/PLAYER1-r7/CloudServiceManager/pulls)** - コードレビュー

---

## 🔄 開発ワークフロー

### Issue の選択

```bash
# 利用可能な Issue を確認
gh issue list --repo PLAYER1-r7/CloudServiceManager

# 特定の Issue を表示
gh issue view 6 --repo PLAYER1-r7/CloudServiceManager
```

### Issue 開始時（必須）

```bash
# Project のステータスを "In progress" に更新
bash .github/scripts/update_project_status.sh 6 "In progress"
```

### ブランチ作成とコミット

```bash
# feature ブランチを作成
git checkout -b feature/issue-6-authentication

# 変更をコミット（バージョンを増やす）
# config.py の VERSION を更新してからコミット
git add .
git commit -m "feat(#6): implement AWS authentication

Version: 1.0.1.X"
```

### PR 作成

```bash
# ブランチをプッシュ
git push -u origin feature/issue-6-authentication

# PR を作成
gh pr create --base develop --title "feat: Issue #6 Authentication" --body "Closes #6"

# ステータスを更新
bash .github/scripts/update_project_status.sh 6 "In review"
```

### マージ後

```bash
# ステータスを更新
bash .github/scripts/update_project_status.sh 6 "Done"
```

詳細: [PROJECT_WORKFLOW.md](https://github.com/PLAYER1-r7/CloudServiceManager/blob/develop/.github/PROJECT_WORKFLOW.md)

---

## 🧪 テストの実行

```bash
# すべてのテストを実行
pytest tests/ -v

# カバレッジ付きで実行
pytest --cov=src --cov-report=term-missing tests/

# 特定のテストファイルのみ
pytest tests/test_models.py -v
```

**現在のカバレッジ**: 95%（CloudService モデル）

---

## 📦 バージョン管理

**形式**: `W.X.Y.Z`（例: 1.0.1.7）

- **W** (Major): ユーザー指示による戦略的変更
- **X** (Minor): ユーザー指示による機能追加
- **Y** (Development): develop ブランチへのプッシュごとに +1
- **Z** (Commit): 各コミットで +1

**ルール**: 各コミット前に `config.py` の `VERSION` を更新

---

## 🔧 トラブルシューティング

### DevContainer が起動しない

```bash
# Docker を再起動
sudo systemctl restart docker

# コンテナを再ビルド
# VS Code: Remote-Containers: Rebuild Container
```

### テストが失敗する

```bash
# 依存関係を再インストール
pip install -r requirements.txt --upgrade

# キャッシュをクリア
pytest --cache-clear tests/
```

### 詳細は [FAQ](FAQ) を参照

---

## 🤝 コントリビューション

1. [Issue を選ぶ](https://github.com/PLAYER1-r7/CloudServiceManager/issues)
2. Project ステータスを "In progress" に更新
3. feature ブランチで実装
4. テストを書く（カバレッジ 80%以上）
5. PR を作成
6. マージ後、ステータスを "Done" に更新

---

## 📞 サポート

- **Issues**: [GitHub Issues](https://github.com/PLAYER1-r7/CloudServiceManager/issues)
- **Discussions**: [GitHub Discussions](https://github.com/PLAYER1-r7/CloudServiceManager/discussions)

---

## ⏭️ 次のステップ

- [FAQ](FAQ) でよくある質問を確認
- [開発チェックリスト](https://github.com/PLAYER1-r7/CloudServiceManager/blob/develop/docs_ja/05_DEVELOPMENT_CHECKLIST.md) で現在の進捗を確認
- [GitHub Project Board](https://github.com/users/PLAYER1-r7/projects/1) で次の Issue を選ぶ

このガイドでは、CloudServiceManagerのインストールから最初のコマンド実行までを説明します。

---

## 📋 前提条件

CloudServiceManagerを使用する前に、以下が必要です：

### 必須項目

- **Python 3.11以上** - モダンなPython機能を使用
- **Git** - ソースコードのクローン用
- **クラウドプロバイダーアカウント** - AWS、GCP、またはAzureのいずれか

### オプション

- **Docker** - DevContainer環境での開発（開発者向け）
- **VS Code** - 推奨エディタ（開発者向け）

---

## 🚀 インストール手順

### ステップ 1: リポジトリをクローン

```bash
git clone https://github.com/PLAYER1-r7/CloudServiceManager.git
cd CloudServiceManager
```

### ステップ 2: 仮想環境を作成

```bash
# 仮想環境を作成
python3 -m venv venv

# 仮想環境を有効化
# Linux/Mac:
source venv/bin/activate

# Windows:
venv\Scripts\activate
```

### ステップ 3: 依存関係をインストール

```bash
pip install -r requirements.txt
```

### ステップ 4: CLIツールをインストール（開発モード）

```bash
pip install -e .
```

---

## 🔑 クラウド認証の設定

CloudServiceManagerを使用するには、各クラウドプロバイダーの認証情報が必要です。

### AWS認証

**方法1: AWS CLI設定を使用（推奨）**

```bash
# AWS CLIをインストール（未インストールの場合）
pip install awscli

# 認証情報を設定
aws configure
```

入力する情報：
- **AWS Access Key ID**: あなたのアクセスキー
- **AWS Secret Access Key**: あなたのシークレットキー
- **Default region name**: `us-east-1` など
- **Default output format**: `json`

**方法2: 環境変数を使用**

```bash
export AWS_ACCESS_KEY_ID="your-access-key"
export AWS_SECRET_ACCESS_KEY="your-secret-key"
export AWS_DEFAULT_REGION="us-east-1"
```

### GCP認証

```bash
# GCP CLIをインストール（未インストールの場合）
curl https://sdk.cloud.google.com | bash

# 認証
gcloud auth application-default login

# プロジェクトを設定
gcloud config set project YOUR_PROJECT_ID
```

### Azure認証

```bash
# Azure CLIをインストール（未インストールの場合）
pip install azure-cli

# ログイン
az login

# サブスクリプションを設定（複数ある場合）
az account set --subscription "YOUR_SUBSCRIPTION_ID"
```

---

## ✨ 最初のコマンド実行

### 基本的な使い方

すべてのクラウドプロバイダーのリソースを一覧表示：

```bash
cloudmgr list-services
```

**期待される出力**:

```
CloudServices
┏━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━┓
┃ Provider ┃ Service Type ┃ Name                ┃ Region      ┃ Status  ┃
┡━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━┩
│ aws      │ EC2          │ i-0123456789abcdef0 │ us-east-1   │ running │
│ gcp      │ Compute      │ instance-1          │ us-central1 │ RUNNING │
│ azure    │ Virtual Mach │ vm-01               │ eastus      │ Running │
└──────────┴──────────────┴─────────────────────┴─────────────┴─────────┘
```

### プロバイダーを指定

特定のクラウドプロバイダーのみを表示：

```bash
# AWSのみ
cloudmgr list-services --provider aws

# GCPのみ
cloudmgr list-services --provider gcp

# Azureのみ
cloudmgr list-services --provider azure
```

### 出力形式を変更

#### JSON形式（プログラム処理向け）

```bash
cloudmgr list-services --format json
```

**出力例**:
```json
[
  {
    "provider": "aws",
    "service_type": "EC2",
    "name": "i-0123456789abcdef0",
    "region": "us-east-1",
    "status": "running"
  }
]
```

#### CSV形式（Excelで開く）

```bash
cloudmgr list-services --format csv > services.csv
```

CSVファイルをExcelで開いて分析できます。

### リージョンでフィルタ

特定のリージョンのリソースのみ表示：

```bash
# AWS us-east-1リージョンのみ
cloudmgr list-services --provider aws --region us-east-1

# GCP us-central1リージョンのみ
cloudmgr list-services --provider gcp --region us-central1
```

---

## 🎯 よくあるユースケース

### ケース1: 全リソースの棚卸し

月次レポート用に全クラウドのリソースをCSVで出力：

```bash
cloudmgr list-services --format csv > monthly-report-$(date +%Y-%m).csv
```

### ケース2: AWS開発環境の確認

開発用AWSアカウントのus-west-2リソースを確認：

```bash
cloudmgr list-services --provider aws --region us-west-2
```

### ケース3: コスト分析の準備

全リソースをJSON形式で取得して、別のツールで分析：

```bash
cloudmgr list-services --format json | jq '.[] | select(.provider=="aws")'
```

---

## ❓ トラブルシューティング

### エラー: "認証情報が見つかりません"

**原因**: クラウドプロバイダーの認証が未設定

**解決方法**: 
1. 上記の「クラウド認証の設定」セクションを参照
2. AWS/GCP/Azure CLIで正しくログインしているか確認
3. 環境変数が正しく設定されているか確認

```bash
# AWS認証を確認
aws sts get-caller-identity

# GCP認証を確認
gcloud auth list

# Azure認証を確認
az account show
```

### エラー: "cloudmgrコマンドが見つかりません"

**原因**: CLIツールが正しくインストールされていない

**解決方法**:
```bash
# 仮想環境を有効化
source venv/bin/activate

# 開発モードで再インストール
pip install -e .
```

### エラー: "Python 3.11が必要です"

**原因**: Pythonバージョンが古い

**解決方法**:
```bash
# Pythonバージョンを確認
python3 --version

# Python 3.11以上をインストール（Ubuntu/Debian）
sudo apt update
sudo apt install python3.11

# macOS (Homebrew)
brew install python@3.11
```

### リソースが表示されない

**確認項目**:
1. 正しいリージョンを指定しているか
2. 認証アカウントに権限があるか
3. 実際にリソースが存在するか

```bash
# 全リージョンを確認（リージョン指定なし）
cloudmgr list-services --provider aws

# 詳細ログを有効化（準備中）
cloudmgr list-services --verbose
```

---

## 📚 次のステップ

基本的な使い方を理解したら、次のページを参照してください：

- **[コマンドリファレンス](Command-Reference)** - 全コマンドの詳細（準備中）
- **[チュートリアル](Tutorials)** - 実践的な活用例（準備中）
- **[FAQ](FAQ)** - よくある質問と回答（準備中）

---

## 🔗 関連リンク

- **[CLI設計仕様（技術者向け）](https://github.com/PLAYER1-r7/CloudServiceManager/blob/master/docs_ja/03_API_DESIGN.md)**
- **[開発者向けセットアップ](https://github.com/PLAYER1-r7/CloudServiceManager/blob/master/docs_ja/04_SETUP.md)**
- **[GitHub Issues](https://github.com/PLAYER1-r7/CloudServiceManager/issues)**

---

**最終更新**: 2026-03-05
