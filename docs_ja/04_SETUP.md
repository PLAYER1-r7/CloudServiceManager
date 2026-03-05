# セットアップガイド / Setup Guide

> **📖 読み取り順序**: 4番目 - 初回環境セットアップ時に参照

---

## **📋 ドキュメントメタデータ**

- **目的**: 開発環境のセットアップ手順を提供
- **対象読者**: 新規開発者、AIエージェント（環境構築時）
- **前提知識**: `01_PREREQUISITES.md` を読了していること
- **最終更新**: 2026-03-05

---

## **🎯 セットアップ概要**

このガイドでは以下をセットアップします：
1. ✅ Docker DevContainer 開発環境
2. ✅ Python 3.11+ と依存関係
3. ✅ クラウドプロバイダー認証情報（AWS/GCP/Azure）
4. ✅ 開発ツール（pytest, black, ruff など）

---

## **📋 前提要件**

以下がインストール済みであることを確認：

| 要件 | バージョン | 確認コマンド |
|------|-----------|-------------|
| **Docker** | 20.10+ | `docker --version` |
| **VS Code** | 最新版 | - |
| **Remote - Containers 拡張** | 最新版 | VS Code Extensions で確認 |
| **GitHub CLI** | 2.46+ | `gh --version` |

### GitHub アカウント設定
- GitHub アカウント（コード協力用）
- Fine-grained Personal Access Token（認証用）
- 下記の「Step 4: GitHub セットアップ」を参照

### クラウドアカウント（オプション）
実際のクラウドリソースを操作する場合：
- AWS アカウント
- GCP プロジェクト
- Azure サブスクリプション

---

## **🚀 セットアップ手順**

### Step 1: プロジェクトをVS Codeで開く

1. このプロジェクトフォルダをVS Codeで開く
   ```bash
   code /workspaces/CloudServiceManager
   ```

2. VS Code左下の **Remote Container アイコン** をクリック
   または `Ctrl+Shift+P`（Mac: `Cmd+Shift+P`）でコマンドパレットを開く

3. **"Remote-Containers: Reopen in Container"** を選択

4. コンテナビルド待機（初回: 2〜3分）

---

### Step 2: Python環境の確認

DevContainer内で以下を実行：

```bash
# Pythonバージョン確認（3.11+であること）
python --version
# 出力例: Python 3.11.x

# pip バージョン確認
pip --version

# Python仮想環境パス確認
which python
# 出力: /opt/venv/bin/python
```

**現在の環境**:
- Python: 3.11+
- 仮想環境: `/opt/venv`（自動アクティブ化済み）
- OS: Debian GNU/Linux 13 (trixie)

---

### Step 3: プロジェクト依存関係のインストール

```bash
# requirements.txt からパッケージをインストール
pip install -r requirements.txt

# インストール確認
pip list | grep -E "typer|boto3|google-cloud|azure"
```

**インストールされる主要パッケージ**:
- typer[all] - CLI フレームワーク
- boto3 - AWS SDK
- google-cloud-compute - GCP SDK  
- azure-mgmt-compute - Azure SDK
- rich - CLI出力
- pytest, pytest-cov - テストフレームワーク

---

## **🔐 クラウドプロバイダー認証設定**

### AWS 認証設定

#### 方法1: AWS認証情報ファイル（推奨）

`~/.aws/credentials` ファイルを作成：

```bash
mkdir -p ~/.aws
cat <<EOF > ~/.aws/credentials
[default]
aws_access_key_id = YOUR_ACCESS_KEY_ID
aws_secret_access_key = YOUR_SECRET_ACCESS_KEY
EOF
```

#### 方法2: 環境変数

```bash
export AWS_ACCESS_KEY_ID=your_access_key_id
export AWS_SECRET_ACCESS_KEY=your_secret_access_key
export AWS_DEFAULT_REGION=us-east-1  # オプション
```

**検証**:
```bash
# AWS CLIで認証確認（boto3も同じ認証情報を使用）
aws sts get-caller-identity
```

---

### GCP 認証設定

#### サービスアカウントキーの作成

1. GCP Console でサービスアカウント作成
2. キー（JSON）をダウンロード
3. 環境変数に設定

```bash
# サービスアカウントキーのパスを設定
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account-key.json"

# 永続化（.bashrc または .zshrc に追記）
echo 'export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account-key.json"' >> ~/.bashrc
```

**検証**:
```bash
# gcloud で認証確認
gcloud auth list
```

---

### Azure 認証設定

#### 方法1: Azure CLI（推奨）

```bash
# Azure CLIでログイン
az login

# サブスクリプション確認
az account show
```

#### 方法2: サービスプリンシパル（環境変数）

```bash
export AZURE_SUBSCRIPTION_ID=your_subscription_id
export AZURE_CLIENT_ID=your_client_id
export AZURE_CLIENT_SECRET=your_client_secret
export AZURE_TENANT_ID=your_tenant_id
```

**検証**:
```bash
# Azure リソースグループ一覧
az group list
```

---

## **🧪 セットアップ検証**

### 動作確認コマンド

```bash
# CLI ヘルプ表示
python -m src.cli.main --help

# テスト実行
pytest

# テスト（詳細出力）
pytest -v

# カバレッジ付きテスト
pytest --cov=src tests/
```

**期待される出力例**:
```
======================== test session starts ========================
collected X items

tests/test_main.py::test_example PASSED                        [100%]

======================== X passed in 0.XXs =========================
```

---

## **🛠️ 開発ツールの使用**

### コードフォーマット（Black）

```bash
# src/ と tests/ をフォーマット
black src/ tests/

# ドライラン（変更を確認のみ）
black --check src/ tests/
```

### リント（Ruff）

```bash
# リント実行
ruff check src/ tests/

# 自動修正
ruff check --fix src/ tests/
```

### 型チェック（mypy）

```bash
# 型チェック実行
mypy src/
```

---

## **📝 よく使うコマンド一覧**

| 目的 | コマンド |
|------|---------|
| CLIヘルプ | `python -m src.cli.main --help` |
| サービス一覧 | `python -m src.cli.main list-services` |
| テスト全実行 | `pytest` |
| テスト（詳細） | `pytest -v` |
| カバレッジ | `pytest --cov=src` |
| コードフォーマット | `black src/ tests/` |
| リント | `ruff check src/` |
| 型チェック | `mypy src/` |

---

## **🔧 トラブルシューティング**

### 問題: Python が見つからない
```bash
# 解決策: 仮想環境を手動でアクティブ化
source /opt/venv/bin/activate
```

### 問題: 依存関係エラー
```bash
# 解決策: requirements.txt を再インストール
pip install --upgrade -r requirements.txt
```

### 問題: AWS認証エラー
```bash
# 解決策: 認証情報ファイルを確認
cat ~/.aws/credentials

# または環境変数を確認
echo $AWS_ACCESS_KEY_ID
```

### 問題: テストが失敗する
```bash
# 解決策: テストを詳細モードで実行
pytest -vv --tb=short

# 特定のテストのみ実行
pytest tests/test_main.py::test_specific_function -v
```

---

**最終更新日**: 2026-03-05  
**次のドキュメント**: [05_DEVELOPMENT_CHECKLIST.md](05_DEVELOPMENT_CHECKLIST.md)
black src/                # Format code
flake8 src/               # Lint code
mypy src/                 # Type check
```

## VS Code Extensions in Container

Automatically installed:

- Python (ms-python.python)
- Pylance (intelligent code completion)
- Black Formatter (code formatter)
- Ruff (fast linter)

## Troubleshooting

### Container won't build

- Ensure Docker daemon is running: `docker ps`
- Rebuild container: Delete `.devcontainer` volume and reopen

### Python dependencies installation fails

- Clear pip cache: `pip cache purge`
- Try installing individually: `pip install <package-name>`

### Credentials not working in container

- Copy credentials to container mount path
- Use environment variables or AWS profile setup
- Check permissions on credential files

## Next Steps

1. **Read the Project Plan**: See `docs/PROJECT_PLAN.md`
2. **Check API Design**: See `docs/API_DESIGN.md` (coming soon)
3. **Start developing**: Begin with AWS provider implementation
4. **Write tests**: Keep test coverage >80%
