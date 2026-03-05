# CloudServiceManager Wiki

> マルチクラウド環境を統一的に管理するCLIツール

## 🚀 クイックスタート

CloudServiceManagerは、AWS、GCP、Azureの複数のクラウドプロバイダーのリソースを、一つのコマンドで管理できるツールです。

### 最初のコマンド

```bash
# 全クラウドのリソースを一覧表示
cloudmgr list-services

# AWS のみを表示
cloudmgr list-services --provider aws

# JSON形式で出力
cloudmgr list-services --format json
```

詳しくは → **[はじめに (Getting Started)](Getting-Started)**

---

## 📚 ドキュメント

### 🎓 初心者向け
- **[はじめに](Getting-Started)** - インストールから最初のコマンド実行まで
- **[インストール方法](Installation)** - 詳細なセットアップ手順
- **[FAQ](FAQ)** - よくある質問とトラブルシューティング

### 👨‍💻 開発者向け
技術仕様や実装ガイドは、リポジトリ内のドキュメントを参照してください：

- **[開発環境セットアップ](https://github.com/PLAYER1-r7/CloudServiceManager/blob/master/docs_ja/04_SETUP.md)** - DevContainer環境の構築
- **[CLI設計仕様](https://github.com/PLAYER1-r7/CloudServiceManager/blob/master/docs_ja/03_API_DESIGN.md)** - コマンド仕様とAPI設計
- **[プロジェクト計画](https://github.com/PLAYER1-r7/CloudServiceManager/blob/master/docs_ja/02_PROJECT_PLAN.md)** - 全体のロードマップ
- **[前提条件](https://github.com/PLAYER1-r7/CloudServiceManager/blob/master/docs_ja/01_PREREQUISITES.md)** - 技術的制約と決定事項

### 🔧 プロジェクト管理
- **[AIエージェント運用ガイド](https://github.com/PLAYER1-r7/CloudServiceManager/blob/master/.github/AI_AGENT_PROJECT_GUIDE.md)** - AI支援による開発管理
- **[GitHub Projects](https://github.com/users/PLAYER1-r7/projects/1)** - タスク管理ボード
- **[Issues](https://github.com/PLAYER1-r7/CloudServiceManager/issues)** - 開発タスク一覧

---

## 🎯 チュートリアル（準備中）

Phase 1（CLI開発）完了後に公開予定：

- [ ] AWS リソースを一覧表示する
- [ ] 複数クラウドの統合管理
- [ ] カスタム出力フォーマット
- [ ] CSV出力でExcel分析

---

## 📊 プロジェクトの進捗

### ✅ Phase 1: CLI開発（2026年3月 - 進行中）

**進行中のタスク**:
- CloudService データモデル実装
- クラウドプロバイダー認証
- AWS/GCP/Azure プロバイダー実装
- `list-services` コマンド実装

**進捗**: [GitHub Project Board](https://github.com/users/PLAYER1-r7/projects/1) で確認

### 🔮 Phase 2: Webアプリケーション（計画中）

- REST API（FastAPI）
- リアルタイムダッシュボード（React）
- Webブラウザーでのリソース管理

詳細は [プロジェクト計画](https://github.com/PLAYER1-r7/CloudServiceManager/blob/master/docs_ja/02_PROJECT_PLAN.md) を参照

---

## 💡 サポートされるクラウドプロバイダー

| プロバイダー | ステータス | 主なサービス |
|------------|----------|------------|
| **AWS** | 🚧 開発中 | EC2, RDS, S3, Lambda |
| **GCP** | 🚧 開発中 | Compute Engine, Cloud Storage |
| **Azure** | 🚧 開発中 | Virtual Machines, Storage |

---

## 🤝 コントリビューション（準備中）

プロジェクトへの貢献に興味がある方は：

1. [Issues](https://github.com/PLAYER1-r7/CloudServiceManager/issues) でタスクを確認
2. 興味のあるIssueにコメント
3. Pull Requestを送信

詳細なガイドラインは Phase 1 完了後に公開予定です。

---

## 📄 ライセンス

このプロジェクトは [MIT License](https://github.com/PLAYER1-r7/CloudServiceManager/blob/master/LICENSE) の下で公開されています。

---

## 🔗 リンク

- **[GitHub リポジトリ](https://github.com/PLAYER1-r7/CloudServiceManager)**
- **[Issues](https://github.com/PLAYER1-r7/CloudServiceManager/issues)**
- **[Project Board](https://github.com/users/PLAYER1-r7/projects/1)**
- **[README](https://github.com/PLAYER1-r7/CloudServiceManager#readme)**

---

**最終更新**: 2026-03-05
