# はじめに - CloudServiceManager

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
