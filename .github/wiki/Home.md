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

**現在のバージョン**: `1.0.1.7`（2026年3月5日）

**完了したタスク**:
- ✅ **Issue #2**: CloudService データモデル完成・テスト
  - Pydantic BaseModel への移行完了
  - **95% テストカバレッジ達成**（目標: 80%以上）
  - 31 テスト合格（27 ユニット + 6 統合）
  - ISO 8601 タイムスタンプ検証実装
  - PR #17 でマージ完了

**進行中のタスク**:
- 🚧 **Issue #6**: クラウドプロバイダー認証実装
  - AWS/GCP/Azure 認証メカニズム
  - 環境変数ハンドリング
  - 認証情報の検証

**今後のタスク**:
- 📋 Issue #5: Week 2: AWS プロバイダー実装
- 📋 Issue #1: list-services コマンド実装完成
- 📋 Issue #3: Week 3: GCP プロバイダー実装
- 📋 Issue #7: Week 3: Azure プロバイダー実装
- 📋 Issue #4: Week 4: 統合テストと最適化

**進捗**: [GitHub Project Board](https://github.com/users/PLAYER1-r7/projects/1) で確認（1/7 Issues 完了、14%）

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
