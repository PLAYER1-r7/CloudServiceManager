# GitHub Setup Script - Quick Start Guide

このガイドは、GitHubリポジトリの自動セットアップスクリプトの使用方法を簡単に説明します。

## 🚀 最も簡単な方法（推奨）

### GitHub CLI を使う

```bash
# 1. GitHub CLI にログイン（初回のみ）
gh auth login
# → ブラウザで認証を行う

# 2. スクリプトを実行
cd /workspaces/CloudServiceManager
python .github/setup_github.py
```

**これだけです！** スクリプトが自動的に：
- ✅ GitHub CLI から認証トークンを取得
- ✅ git remote から リポジトリ情報を自動検出
- ✅ すべての設定を自動実行

## 📊 認証方法の比較

| 方法 | 安全性 | 簡単さ | トークン管理 | プロジェクトルール |
|------|--------|--------|------------|------------------|
| **GitHub CLI** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 自動 | ✅ **必須** |
| **Fine-grained PAT** | ⭐⭐⭐⭐ | ⭐⭐⭐ | 手動 | ❌ **禁止** |
| **Classic PAT** | ⭐⭐ | ⭐⭐⭐ | 手動 | ❌ **禁止** |
| **GitHub Actions Token** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 自動 | ✅ CI/CDのみ許可 |

## 🔐 認証方法の詳細

### 方法 1: GitHub CLI（最推奨）

**メリット：**
- トークンの手動作成・管理が不要
- OAuth認証で安全
- すべてのリポジトリで使い回し可能
- トークンの自動ローテーション

**セットアップ：**
```bash
# インストール（まだの場合）
# macOS
brew install gh

# Linux (Debian/Ubuntu)
sudo apt install gh

# 認証
gh auth login

# 認証状態確認
gh auth status
```

**使用方法：**
```bash
# スクリプト実行（それだけ！）
python .github/setup_github.py
```

---

### 方法 2: Fine-grained Personal Access Token ⚠️ プロジェクトルールで禁止

**⚠️ このプロジェクトでは使用禁止**

`docs_ja/01_PREREQUISITES.md` - "GitHub 認証ルール（必須）"により：
- ❌ Personal Access Token (Fine-grained) は**禁止**
- ✅ GitHub CLI (`gh`) を使用してください
- 例外: CI/CDでのGitHub Actions組み込みトークンのみ

**作成方法：**
1. https://github.com/settings/tokens?type=beta にアクセス
2. "Generate new token" をクリック
3. 以下を設定：
   - **Token name**: `CloudServiceManager Setup`
   - **Expiration**: `7 days`（ワンタイムセットアップ用）
   - **Repository access**: "Only select repositories" → このリポジトリを選択
   - **Permissions**:
     - ☑️ Administration: Read and write
     - ☑️ Contents: Read and write
     - ☑️ Issues: Read and write
     - ☑️ Metadata: Read-only
     - ☑️ Projects: Read and write
     - ☑️ Pull requests: Read and write
4. "Generate token" をクリック
5. トークンをコピー（`github_pat_` で始まる）

**使用方法：**
```bash
export GITHUB_TOKEN="github_pat_xxxxxxxxxxxx"
export GITHUB_OWNER="your_username"
export GITHUB_REPO="CloudServiceManager"

python .github/setup_github.py
```

---

### 方法 3: Classic Personal Access Token ⚠️ プロジェクトルールで厳格に禁止

**⚠️ このプロジェクトでは厳格に禁止**

`docs_ja/01_PREREQUISITES.md` - "GitHub 認証ルール（必須）"により：
- ❌ Personal Access Token (Classic) は**厳格に禁止**
- ✅ GitHub CLI (`gh`) を使用してください

<details>
<summary>歴史的参考のみ（使用しないでください）</summary>

1. https://github.com/settings/tokens/new にアクセス
2. 以下のスコープを選択：
   - ☑️ `repo`
   - ☑️ `admin:repo_hook`
   - ☑️ `project`
3. トークンを生成してコピー

```bash
export GITHUB_TOKEN="ghp_xxxxxxxxxxxx"
python .github/setup_github.py
```
</details>

---

## 🎯 実行例

### GitHub CLI使用時（最もシンプル）

```bash
$ python .github/setup_github.py

============================================================
🚀 GitHub Repository Automatic Setup
============================================================

🔐 Checking authentication methods...
✓ Found GitHub CLI authentication
✓ Successfully retrieved token from GitHub CLI
✓ Auto-detected repository: myusername/CloudServiceManager

✓ Authenticated as: myusername
✓ Repository: myusername/CloudServiceManager

📋 Creating labels...
  ✅ Created label: bug
  ✅ Created label: enhancement
  ... (8 labels total)

📅 Creating milestones...
  ✅ Created milestone: v1.0.0
  ✅ Created milestone: v1.1.0
  ✅ Created milestone: v2.0.0

📊 Creating GitHub Project board...
  ✅ Created GitHub Project: Development Tracking

🔒 Configuring branch protection...
  ✅ Configured protection for: develop
  ✅ Configured protection for: main

📝 Creating first GitHub Issue...
  ✅ Created first issue: https://github.com/myusername/CloudServiceManager/issues/1

============================================================
✅ GitHub Setup Complete!
============================================================
```

---

## ❓ よくある質問

### Q1: GitHub CLI がインストールされているか確認する方法は？

```bash
gh --version
```

正常にインストールされている場合：
```
gh version 2.40.0 (2024-01-15)
https://github.com/cli/cli/releases/tag/v2.40.0
```

### Q2: GitHub CLI で認証されているか確認する方法は？

```bash
gh auth status
```

認証されている場合：
```
✓ Logged in to github.com as YOUR_USERNAME
✓ Token: gho_************************************
```

### Q3: Fine-grained PAT と Classic PAT の見分け方は？

- **Fine-grained PAT**: `github_pat_` で始まる
- **Classic PAT**: `ghp_` で始まる

### Q4: トークンはどのくらいの期間有効にすべき？

- **ワンタイムセットアップ**: 7日間
- **GitHub CLI**: 自動管理（期限なし）
- **継続的に使用**: 90日 + 自動更新リマインダー設定

### Q5: スクリプトは何度も実行できますか？

はい。スクリプトは **冪等性** があります：
- すでに存在するラベルはスキップ
- すでに存在するマイルストーンはスキップ
- すでに存在するプロジェクトは再利用
- 重複したIssueは作成されない

### Q6: エラーが出た場合は？

詳細なドキュメントを参照：
- [.github/SETUP_SCRIPT.md](.github/SETUP_SCRIPT.md) - 完全なドキュメント
- トラブルシューティングセクションで一般的なエラーの解決方法を確認

---

## 📚 関連ドキュメント

- **[.github/SETUP_SCRIPT.md](.github/SETUP_SCRIPT.md)** - 完全な使用方法ガイド
- **[.github/INITIAL_SETUP.md](.github/INITIAL_SETUP.md)** - 手動セットアップのチェックリスト
- **[.github/GITHUB_SETUP.md](.github/GITHUB_SETUP.md)** - GitHub設定の詳細ガイド
- **[README.md](../README.md)** - プロジェクト全体の README

---

## ✅ セットアップ完了後の確認

スクリプト実行後、以下を GitHub UI で確認：

1. **Issues → Labels**: 8個のラベルが作成されているか
2. **Issues → Milestones**: v1.0.0, v1.1.0, v2.0.0 が作成されているか
3. **Projects**: "Development Tracking" プロジェクトが存在するか
4. **Settings → Branches**: `develop` と `main` が保護されているか
5. **Issues**: Issue #1 が作成されているか

すべて ✅ なら、セットアップ完了です！

---

**Last Updated**: 2026-03-05  
**Version**: 2.0.0 (GitHub CLI support added)
