# プロジェクト計画 / Project Plan

> **📖 読み取り順序**: 2番目 - `01_PREREQUISITES.md` の後に読むこと

---

## **📋 ドキュメントメタデータ**

- **目的**: プロジェクト全体の計画、アーキテクチャ、開発ロードマップの提供
- **対象読者**: AIエージェント、プロジェクト管理者、新規開発者
- **前提知識**: `01_PREREQUISITES.md` を読了していること
- **最終更新**: 2026-03-05

---

## **🎯 プロジェクト概要**

### プロジェクト名
**Cloud Service Manager**

### ミッション
複数のクラウドプロバイダー（AWS、Azure、GCP）のリソースを統一的に検出・管理するツールの開発

### ビジョン
マルチクラウド環境におけるリソース管理の複雑さを解消し、統一されたインターフェースで全てのクラウドリソースを可視化・操作可能にする

---

## **📅 開発フェーズ**

### Phase 1: CLI Development（現在のフェーズ）⚡

**期間**: Week 1-4  
**ステータス**: 🚧 進行中

**目標**:
- ✅ CLIツールを実装してクラウドリソースを取得・一覧表示
- ✅ AWS、Azure、GCPをサポート
- ✅ 構造化された形式（JSON、テーブル、CSV）でサービスを表示
- ✅ Phase 2（Webアプリケーション）の基盤を構築

**成果物**:
- 動作するCLIツール (`cloudmgr` コマンド)
- 各プロバイダーの統合実装
- ユニットテスト（カバレッジ80%以上）
- ドキュメント一式

### Phase 2: Web Application（将来計画）🔮

**期間**: TBD（Phase 1完了後）  
**ステータス**: ⏸️ 未開始

**注意**: ⚠️ **Phase 2の機能は現時点で実装しないこと**

**計画概要**:
- FastAPI ベースのREST API
- React フロントエンド
- リアルタイムリソース監視
- ダッシュボード機能

---

## **🛠️ 技術スタック（確定）**

| カテゴリ | 技術 | バージョン | 選定理由 |
|---------|------|-----------|---------|
| **言語** | Python | 3.11+ | 型ヒント改善、パフォーマンス、最新機能 |
| **CLIフレームワーク** | Typer | latest | モダン、型安全、自動ドキュメント生成 |
| **AWS SDK** | boto3 | latest | AWS公式、網羅的なサービスカバレッジ |
| **GCP SDK** | google-cloud-compute | latest | GCP公式SDK |
| **Azure SDK** | azure-mgmt-compute | latest | Azure公式SDK |
| **開発環境** | Docker + DevContainer | - | 環境の統一、再現性 |
| **テスト** | pytest | latest | 標準的、豊富なプラグイン |
| **UI (CLI)** | rich | latest | 美しいテーブル、カラー出力 |

---

## **📁 プロジェクト構造（固定）**

```
/workspaces/CloudServiceManager/
├── docs/                           # ドキュメント
│   ├── 00_README_DOCS.md          # ドキュメント読み取りガイド ⭐
│   ├── 01_PREREQUISITES.md        # 前提条件（必読）⚠️
│   ├── 02_PROJECT_PLAN.md         # このファイル：プロジェクト計画
│   ├── 03_API_DESIGN.md           # CLI/API設計仕様
│   ├── 04_SETUP.md                # セットアップガイド
│   └── 05_DEVELOPMENT_CHECKLIST.md # 開発チェックリスト
├── .devcontainer/
│   ├── Dockerfile                 # Dev container イメージ
│   └── devcontainer.json          # Dev container 設定
├── src/
│   └── cli/
│       ├── __init__.py
│       ├── main.py                # ✅ CLIエントリーポイント（Typer）
│       ├── providers/             # クラウドプロバイダー実装
│       │   ├── __init__.py
│       │   ├── aws.py             # AWS実装（boto3）
│       │   ├── gcp.py             # GCP実装（google-cloud-compute）
│       │   └── azure.py           # Azure実装（azure-mgmt-compute）
│       └── models/
│           └── service.py         # ✅ データモデル（CloudService）
├── tests/                         # ユニットテスト
│   ├── __init__.py
│   └── test_main.py
├── config.py                      # アプリケーション設定
├── requirements.txt               # Python依存関係（必須）
├── pytest.ini                     # pytest設定
└── README.md                      # プロジェクトREADME
```

---

## **🎯 Phase 1 主要機能**

### 1. 統一サービス検出（Unified Service Discovery）
- **目的**: 全てのクラウドプロバイダーからリソースを取得
- **実装**: 各プロバイダーのSDKを使用して統一モデル（`CloudService`）に変換
- **対応リソース**: EC2, Compute Engine, Virtual Machines

### 2. 複数出力形式サポート
- **table**: デフォルト、Rich ライブラリ使用
- **json**: JSON配列形式（プログラマティックな利用向け）
- **csv**: CSV形式（スプレッドシート連携向け）

### 3. フィルタリング＆ソート
- プロバイダー別フィルタ (`--provider`)
- リージョン別フィルタ (`--region`)
- 将来: サービスタイプ、ステータスでのフィルタ

### 4. 認証情報管理
- 各プロバイダーの標準認証方法をサポート
- 環境変数、設定ファイルから読み込み
- **セキュリティ**: 認証情報をコードにハードコードしない

### 5. CLIドキュメント
- Typer自動生成ヘルプ
- `--help` オプション
- コマンド例の提供

---

## **🗓️ 開発ロードマップ**

### Week 1: プロジェクト初期化とCLIフレームワーク ✅
- [x] DevContainer セットアップ
- [x] プロジェクト構造作成
- [x] Typer CLI 基盤実装
- [x] ドキュメント初版作成

### Week 2: AWS プロバイダー実装 🚧
- [ ] boto3 統合
- [ ] EC2インスタンス一覧取得
- [ ] AWS認証実装
- [ ] ユニットテスト（AWS）

### Week 3: GCP & Azure プロバイダー実装 ⏳
- [ ] GCP Compute Engine 統合
- [ ] Azure Virtual Machines 統合
- [ ] 統一データモデルへの変換
- [ ] ユニットテスト（GCP, Azure）

### Week 4: テスト・ドキュメント・最適化 ⏳
- [ ] 統合テスト
- [ ] パフォーマンス最適化
- [ ] ドキュメント完成
- [ ] リリース準備

**凡例**: ✅完了 | 🚧進行中 | ⏳未開始

---

## **📋 開発要件**

### 必須環境
- ✅ Docker & DevContainer サポート
- ✅ Python 3.11+ 開発環境
- ✅ クラウドプロバイダー認証情報
- ✅ Git ワークフロー

### 品質要件
- **テストカバレッジ**: 80%以上
- **型ヒント**: 全ての関数・メソッドに付与
- **ドキュメント**: docstring（Google Style）
- **コード品質**: Black（フォーマット）、Ruff（リント）

---

**最終更新日**: 2026-03-05  
**次のドキュメント**: [03_API_DESIGN.md](03_API_DESIGN.md)
