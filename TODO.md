# CloudServiceManager - 実装ToDoリスト

> **作成日**: 2026-03-05  
> **仕様ドキュメント基準**: 01_PREREQUISITES.md, 02_PROJECT_PLAN.md, 03_API_DESIGN.md

---

## 📋 概要

このドキュメントは、仕様書（docs フォルダ）から抽出した実装タスクを管理します。複数のウィークリーマイルストーンに分割されています。

---

## ✅ Week 1: プロジェクト初期化と CLI フレームワーク（完了）

- [x] DevContainer セットアップ
- [x] プロジェクト構造作成
- [x] Typer CLI 基盤実装
- [x] ドキュメント作成（docs/, docs_ja/）
- [x] requirements.txt 設定

**ステータス**: ✅ 完了

---

## 🚧 Week 2: AWS プロバイダー実装

### Issue #1: Week 2: AWS プロバイダー実装

#### 📝 説明
AWS プロバイダーの実装を完了します。EC2 インスタンスの検出と統一モデルへの変換を実現します。

#### 🎯 実装タスク

- [ ] boto3 を使用した AWS API 統合実装
- [ ] EC2 インスタンスリスト機能の実装
- [ ] CloudService データモデルへの変換ロジック
- [ ] AWS 認証メカニズムの実装（環境変数、IAM ロール対応）
- [ ] ユニットテスト作成（80%+ カバレッジ）
- [ ] エラーハンドリング実装
- [ ] 複数リージョン対応

#### 📝 技術仕様

**ファイル**: `src/cli/providers/aws.py`  
**使用SDK**: boto3  
**対応リソース**: EC2 インスタンス  
**出力**: CloudService 統一モデル  

#### 📌 ドキュメント参照
- 01_PREREQUISITES.md - 技術スタック
- 02_PROJECT_PLAN.md - 開発ロードマップ
- 03_API_DESIGN.md - API 仕様

#### ✅ 完了条件
- [ ] すべてのテストが成功
- [ ] ドキュメント更新完了
- [ ] コード審査パス

**ラベル**: `week-2`, `aws`, `provider`

---

## 🚧 Week 3: GCP & Azure プロバイダー実装

### Issue #2: Week 3: GCP プロバイダー実装

#### 📝 説明
GCP プロバイダーの実装を完了します。Compute Engine インスタンスの検出と統一モデルへの変換を実現します。

#### 🎯 実装タスク

- [ ] google-cloud-compute SDK 統合実装
- [ ] Compute Engine インスタンスリスト機能の実装
- [ ] CloudService データモデルへの変換ロジック
- [ ] GCP 認証メカニズムの実装（サービスアカウント、GOOGLE_APPLICATION_CREDENTIALS）
- [ ] ユニットテスト作成（80%+ カバレッジ）
- [ ] エラーハンドリング実装
- [ ] 複数リージョン/ゾーン対応

#### 📝 技術仕様

**ファイル**: `src/cli/providers/gcp.py`  
**使用SDK**: google-cloud-compute  
**対応リソース**: Compute Engine インスタンス  
**出力**: CloudService 統一モデル  

#### 📌 ドキュメント参照
- 01_PREREQUISITES.md - 技術スタック
- 02_PROJECT_PLAN.md - 開発ロードマップ
- 03_API_DESIGN.md - API 仕様

#### ✅ 完了条件
- [ ] すべてのテストが成功
- [ ] ドキュメント更新完了
- [ ] コード審査パス

**ラベル**: `week-3`, `gcp`, `provider`

---

### Issue #3: Week 3: Azure プロバイダー実装

#### 📝 説明
Azure プロバイダーの実装を完了します。Virtual Machines インスタンスの検出と統一モデルへの変換を実現します。

#### 🎯 実装タスク

- [ ] azure-mgmt-compute SDK 統合実装
- [ ] Virtual Machines リスト機能の実装
- [ ] CloudService データモデルへの変換ロジック
- [ ] Azure 認証メカニズムの実装（環境変数、サービスプリンシパル）
- [ ] ユニットテスト作成（80%+ カバレッジ）
- [ ] エラーハンドリング実装
- [ ] 複数リージョン対応

#### 📝 技術仕様

**ファイル**: `src/cli/providers/azure.py`  
**使用SDK**: azure-mgmt-compute  
**対応リソース**: Azure Virtual Machines  
**出力**: CloudService 統一モデル  

#### 📌 ドキュメント参照
- 01_PREREQUISITES.md - 技術スタック
- 02_PROJECT_PLAN.md - 開発ロードマップ
- 03_API_DESIGN.md - API 仕様

#### ✅ 完了条件
- [ ] すべてのテストが成功
- [ ] ドキュメント更新完了
- [ ] コード審査パス

**ラベル**: `week-3`, `azure`, `provider`

---

## 🎯 共通機能実装タスク

### Issue #4: list-services コマンド実装完成

#### 📝 説明
`cloudmgr list-services` コマンドを完全に実装し、すべてのクラウドプロバイダーからのリソース検出を統一インターフェースで提供します。

#### 🎯 実装タスク

- [ ] CLI コマンド定義（Typer ベース）
- [ ] --provider オプション実装（aws|gcp|azure|all）
- [ ] --region オプション実装（フィルタリング）
- [ ] --format オプション実装（json|table|csv）
- [ ] Table 出力形式実装（rich を使用）
- [ ] JSON 出力形式実装
- [ ] CSV 出力形式実装
- [ ] エラーハンドリング
- [ ] ユニットテスト実装

#### 📝 技術仕様

**コマンド**: `cloudmgr list-services [OPTIONS]`

**オプション**:
- `--provider (-p)`: all|aws|gcp|azure (デフォルト: all)
- `--region (-r)`: リージョンでフィルタ
- `--format (-f)`: table|json|csv (デフォルト: table)

**出力フォーマット**:
- Table: Rich を使用した美しい表示
- JSON: プログラマティック処理向け
- CSV: スプレッドシート統合向け

#### 📌 ドキュメント参照
- 03_API_DESIGN.md - list-services コマンド仕様

#### ✅ 完了条件
- [ ] すべてのオプション組み合わせがテスト済み
- [ ] 出力フォーマット正確
- [ ] エラーハンドリング実装済み

**ラベル**: `feature`, `list-services`, `cli`

---

### Issue #5: CloudService データモデル完成・テスト

#### 📝 説明
統一クラウドサービスモデル `CloudService` を完全に定義し、すべてのプロバイダーからのリソースを正確に映射できるようにします。

#### 🎯 実装タスク

- [ ] CloudService データクラス完全定義
- [ ] 必須フィールド実装（provider, service_type, name, region, status, created_at, metadata）
- [ ] 型ヒント完全実装
- [ ] docstring 実装（Google スタイル）
- [ ] JSON シリアライゼーション実装
- [ ] CSV エクスポート対応
- [ ] バリデーションロジック実装
- [ ] ユニットテスト作成
- [ ] 各プロバイダーへの変換テスト

#### 📝 技術仕様

**ファイル**: `src/cli/models/service.py`

**必須フィールド**:
- `provider`: str (aws|gcp|azure)
- `service_type`: str (EC2, Compute Engine, Virtual Machine など)
- `name`: str (リソース名またはID)
- `region`: str (リージョン名)
- `status`: str (プロバイダー固有のステータス)
- `created_at`: str (ISO 8601 形式)
- `metadata`: dict (プロバイダー固有情報)

#### 📌 ドキュメント参照
- 03_API_DESIGN.md - CloudService データモデル仕様

#### ✅ 完了条件
- [ ] すべてのフィールドに型ヒント付き
- [ ] docstring 完備
- [ ] テストカバレッジ 80% 以上

**ラベル**: `feature`, `model`, `data`

---

### Issue #6: クラウドプロバイダー認証実装

#### 📝 説明
各クラウドプロバイダーの認証メカニズムを実装し、セキュアかつ柔軟な認証方式をサポートします。

#### 🎯 実装タスク

##### AWS
- [ ] AWS_ACCESS_KEY_ID 環境変数対応
- [ ] AWS_SECRET_ACCESS_KEY 環境変数対応
- [ ] ~/.aws/credentials ファイル対応
- [ ] IAM ロール自動検出
- [ ] STS トークン対応
- [ ] エラーハンドリング

##### GCP
- [ ] GOOGLE_APPLICATION_CREDENTIALS 環境変数対応
- [ ] サービスアカウント JSON キー対応
- [ ] アプリケーション default credentials
- [ ] 複数プロジェクト対応
- [ ] エラーハンドリング

##### Azure
- [ ] AZURE_SUBSCRIPTION_ID 環境変数対応
- [ ] AZURE_CLIENT_ID 環境変数対応
- [ ] AZURE_CLIENT_SECRET 環境変数対応
- [ ] AZURE_TENANT_ID 環境変数対応
- [ ] `az login` 統合
- [ ] エラーハンドリング

#### 🔐 セキュリティ要件

- ❌ 認証情報をコードに埋め込まない
- ✅ 環境変数から読み込む
- ✅ 設定ファイルから読み込む
- ✅ 標準認証メカニズムを使用
- ✅ エラーメッセージに認証情報を含めない

#### 📌 ドキュメント参照
- 01_PREREQUISITES.md - 技術制約
- 04_SETUP.md - セットアップガイド

#### ✅ 完了条件
- [ ] すべてのプロバイダーの認証方式実装済み
- [ ] 認証テスト成功
- [ ] セキュリティ審査パス

**ラベル**: `security`, `authentication`, `aws`, `gcp`, `azure`

---

## 🚧 Week 4: テスト、ドキュメント、最適化

### Issue #7: Week 4: 統合テストと最適化

#### 📝 説明
すべての機能の統合テスト、パフォーマンス最適化、ドキュメント完成を実施します。Phase 1 のリリース準備を完了します。

#### 🎯 実装タスク

- [ ] 統合テストスイート作成
- [ ] エッジケーステスト実装
- [ ] パフォーマンス測定・最適化
- [ ] キャッシング戦略実装（必要に応じて）
- [ ] エラーメッセージの改善
- [ ] ログ出力実装
- [ ] ドキュメント最終化
- [ ] API ドキュメント完成
- [ ] 使用例の追加
- [ ] CHANGELOG 作成
- [ ] リリース 1.0.0-beta 準備

#### 📝 テスト対象

- すべてのコマンドオプション組み合わせ
- クラウドプロバイダーエラーシナリオ
- 認証失敗時の処理
- 大量データセット処理
- 複数プロバイダー間の整合性

#### 📌 ドキュメント参照
- 02_PROJECT_PLAN.md - 開発ロードマップ

#### ✅ 完了条件
- [ ] テストカバレッジ: 80%+
- [ ] すべての統合テスト成功
- [ ] ドキュメント 100% 完成
- [ ] リリース予定の確認

**ラベル**: `week-4`, `testing`, `documentation`

---

## 📊 進捗サマリー

| フェーズ | タスク数 | 完了 | 進行中 | 未開始 | ステータス |
|---------|---------|------|--------|--------|-----------|
| Week 1  | 5       | 5    | -      | -      | ✅ 完了   |
| Week 2  | 7       | 0    | 0      | 7      | ⏳ 未開始 |
| Week 3  | 14      | 0    | 0      | 14     | ⏳ 未開始 |
| 共通機能| 6       | 0    | 0      | 6      | ⏳ 未開始 |
| Week 4  | 11      | 0    | 0      | 11     | ⏳ 未開始 |
| **合計**| **43**  | **5**| **0** | **38** | 🚧 進行中 |

---

## 🔗 関連ドキュメント

- [README.md](README.md) - プロジェクト概要
- [docs/00_README_DOCS.md](docs/00_README_DOCS.md) - ドキュメントガイド
- [docs/01_PREREQUISITES.md](docs/01_PREREQUISITES.md) - 前提条件と制約
- [docs/02_PROJECT_PLAN.md](docs/02_PROJECT_PLAN.md) - プロジェクト計画
- [docs/03_API_DESIGN.md](docs/03_API_DESIGN.md) - API 設計
- [docs/04_SETUP.md](docs/04_SETUP.md) - セットアップガイド
- [docs/05_DEVELOPMENT_CHECKLIST.md](docs/05_DEVELOPMENT_CHECKLIST.md) - 開発チェックリスト

---

## 📝 更新履歴

- **2026-03-05**: 初回作成 - 仕様ドキュメント基準の ToDoリスト作成

