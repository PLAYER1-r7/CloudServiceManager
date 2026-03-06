# CLI設計とAPI仕様 / CLI Design and API Specification

> **📖 読み取り順序**: 3番目 - 機能実装前に必ず読むこと

---

## **📋 ドキュメントメタデータ**

- **目的**: CLIコマンドとAPI仕様の詳細定義
- **対象読者**: AIエージェント、実装担当者
- **前提知識**: `01_PREREQUISITES.md`, `02_PROJECT_PLAN.md` を読了していること
- **最終更新**: 2026-03-05

---

## **🎯 CLI概要**

### コマンド名
**`cloudmgr`** - Cloud Manager の略

### 設計思想
- **統一インターフェース**: 全てのクラウドプロバイダーに対して同じコマンド体系
- **直感的**: 標準的なCLIパターンに従う（kubectl, aws-cli などと類似）
- **柔軟な出力**: ユーザーが用途に応じて出力形式を選択可能
- **型安全**: Typerを活用した型チェックと自動検証

---

## **📝 コマンド仕様**

### 1. list-services コマンド

#### 概要
指定したクラウドプロバイダーから全てのサービスを一覧表示

#### シグネチャ
```bash
cloudmgr list-services [OPTIONS]
```

#### オプション一覧

| オプション | 短縮形 | 型 | デフォルト | 説明 |
|-----------|-------|-----|-----------|-----|
| `--provider` | `-p` | Choice[aws\|gcp\|azure\|all] | `all` | 対象クラウドプロバイダー |
| `--region` | `-r` | str | `None` | リージョンフィルタ（プロバイダー固有） |
| `--format` | `-f` | Choice[json\|table\|csv] | `table` | 出力形式 |

#### 使用例

```bash
# 全プロバイダーの全サービスをテーブル形式で表示（デフォルト）
cloudmgr list-services

# AWSのみ、JSON形式で出力
cloudmgr list-services --provider aws --format json

# GCP、us-central1リージョンのみ
cloudmgr list-services -p gcp -r us-central1

# 全サービスをCSV形式で出力（エクスポート用）
cloudmgr list-services --format csv
```

#### 出力形式仕様

##### Table形式（デフォルト）
- **使用ライブラリ**: `rich.table.Table`
- **特徴**: 
  - カラー対応
  - 自動カラム幅調整
  - 罫線で見やすく整形

**出力例**:
```
CloudServices
┏━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━┓
┃ Provider ┃ Service Type ┃ Name                ┃ Region      ┃ Status  ┃
┡━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━┩
│ aws      │ EC2          │ i-0123456789abcdef0 │ us-east-1   │ running │
│ gcp      │ Compute      │ instance-1          │ us-central1 │ RUNNING │
│ azure    │ Virtual Mach │ vm-01               │ eastus      │ unknown │
└──────────┴──────────────┴─────────────────────┴─────────────┴─────────┘
```

##### JSON形式
- **形式**: JSON配列
- **用途**: プログラマティックな処理、パイプライン連携

**スキーマ**:
```json
[
  {
    "provider": "aws",
    "service_type": "EC2",
    "name": "i-0123456789abcdef0",
    "region": "us-east-1",
    "status": "running",
    "created_at": "2024-01-15T10:30:00Z",
    "metadata": {
      "instance_type": "t2.micro",
      "image_id": "ami-0123456789abcdef0"
    }
  }
]
```

**フィールド仕様**:
| フィールド | 型 | 必須 | 説明 |
|-----------|-----|------|------|
| `provider` | string | ✅ | "aws" \| "gcp" \| "azure" |
| `service_type` | string | ✅ | サービスタイプ（EC2, Compute, etc.） |
| `name` | string | ✅ | リソース名またはID |
| `region` | string | ✅ | リージョン名 |
| `status` | string | ✅ | ステータス（プロバイダー固有） |
| `created_at` | string | ✅ | ISO 8601形式の日時 |
| `metadata` | object | ✅ | プロバイダー固有の追加情報（辞書） |

##### CSV形式
- **形式**: ヘッダー行 + データ行
- **用途**: スプレッドシート、データ分析ツールへのインポート

**出力例**:
```csv
provider,service_type,name,region,status,created_at,metadata
aws,EC2,i-0123456789abcdef0,us-east-1,running,2024-01-15T10:30:00Z,"{""instance_type"": ""t2.micro""}"
gcp,Compute,instance-1,us-central1,RUNNING,2024-01-14T08:20:00Z,"{""machine_type"": ""n1-standard-1""}"
```

**注意**: metadata は JSON 文字列としてエスケープ

---

### 2. get-service コマンド（将来実装予定）

#### 概要
特定のクラウドサービスの詳細情報を取得

#### シグネチャ
```bash
cloudmgr get-service [OPTIONS]
```

#### オプション一覧

| オプション | 短縮形 | 型 | デフォルト | 説明 |
|-----------|-------|-----|-----------|-----|
| `--provider` | `-p` | Choice[aws\|gcp\|azure] | **必須** | 対象クラウドプロバイダー |
| `--id` | `-i` | str | **必須** | サービス識別子（インスタンスID等） |
| `--format` | `-f` | Choice[json\|table\|csv] | `json` | 出力形式 |

#### 使用例

```bash
# AWS EC2インスタンスの詳細を取得
cloudmgr get-service --provider aws --id i-0123456789abcdef0

# GCPインスタンスの詳細を取得
cloudmgr get-service -p gcp -i instance-1
```

---

### 3. init-config コマンド（将来実装予定）

#### 概要
クラウドプロバイダー認証情報の初期設定をガイド

#### シグネチャ
```bash
cloudmgr init-config
```

#### 目的
- ユーザーに対話的に認証情報の設定をガイド
- 設定ファイルの生成
- 認証情報の検証

---

## **🗂️ データモデル**

### CloudService（統一サービスモデル）

全てのクラウドプロバイダーのリソースをこのモデルに変換します。

```python
from dataclasses import dataclass
from typing import Optional, Dict, Any
from enum import Enum

@dataclass
class CloudService:
    """
    統一されたクラウドサービス表現
    
    全てのクラウドプロバイダー（AWS、GCP、Azure）のリソースを
    この共通モデルにマッピングします。
    """
    provider: str                   # "aws" | "gcp" | "azure"
    service_type: str               # "EC2", "Compute Engine", "Virtual Machine" など
    name: str                       # リソース名またはID
    region: str                     # リージョンまたはゾーン
    status: str                     # ステータス（プロバイダー固有）
    created_at: str                 # ISO 8601形式のタイムスタンプ
    metadata: Dict[str, Any]        # プロバイダー固有の追加情報
```

**フィールド詳細**:

| フィールド | 型 | 必須 | 説明 | 例 |
|-----------|-----|------|------|-----|
| `provider` | str | ✅ | プロバイダー識別子 | "aws", "gcp", "azure" |
| `service_type` | str | ✅ | サービスタイプ | "EC2", "Compute", "Virtual Machine" |
| `name` | str | ✅ | リソース名/ID | "i-0123abc", "instance-1", "vm-01" |
| `region` | str | ✅ | リージョン/ゾーン | "us-east-1", "us-central1-a", "eastus" |
| `status` | str | ✅ | リソースステータス | "running", "RUNNING", "stopped" |
| `created_at` | str | ✅ | 作成日時（ISO 8601） | "2024-01-15T10:30:00Z" |
| `metadata` | dict | ✅ | 追加情報（辞書形式） | `{"instance_type": "t2.micro"}` |

### CloudProvider（Enum）

```python
from enum import Enum

class CloudProvider(str, Enum):
    """サポートされるクラウドプロバイダー"""
    AWS = "aws"
    GCP = "gcp"
    AZURE = "azure"
```

---

## **⚠️ エラーハンドリング**

CLIは以下のエラーを適切に処理します：

### 認証エラー
- **原因**: 認証情報が未設定または無効
- **メッセージ例**: `Error: AWS credentials not found. Please configure credentials.`
- **終了コード**: 1

### リージョンエラー
- **原因**: 無効なリージョン指定
- **メッセージ例**: `Error: Invalid region 'us-invalid-1' for provider 'aws'`
- **終了コード**: 2

### ネットワークエラー
- **原因**: API接続失敗
- **メッセージ例**: `Error: Failed to connect to AWS API. Check network connection.`
- **終了コード**: 3

### プロバイダーエラー
- **原因**: サポートされていないプロバイダー
- **メッセージ例**: `Error: Unsupported provider 'oracle'`
- **終了コード**: 4

**エラーハンドリング原則**:
- ✅ 明確なエラーメッセージを表示
- ✅ 適切な終了コードを返す
- ✅ 可能であれば解決策を提示
- ✅ スタックトレースはデバッグモード時のみ表示

---

## **🔧 実装ガイドライン**

### プロバイダー実装パターン

各プロバイダーは以下のインターフェースを実装：

```python
from abc import ABC, abstractmethod
from typing import List

class CloudProviderBase(ABC):
    """クラウドプロバイダーの基底クラス"""
    
    @abstractmethod
    def list_services(self, region: Optional[str] = None) -> List[CloudService]:
        """
        サービス一覧を取得
        
        Args:
            region: リージョンフィルタ（省略可）
            
        Returns:
            CloudServiceオブジェクトのリスト
        """
        pass
    
    @abstractmethod
    def get_service(self, service_id: str) -> CloudService:
        """
        特定のサービス詳細を取得
        
        Args:
            service_id: サービス識別子
            
        Returns:
            CloudServiceオブジェクト
        """
        pass
```

### 実装チェックリスト

新しいプロバイダー実装時：
- [ ] `CloudProviderBase` を継承
- [ ] `list_services()` メソッドを実装
- [ ] `get_service()` メソッドを実装
- [ ] プロバイダー固有のSDKを使用
- [ ] 統一モデル（`CloudService`）に変換
- [ ] エラーハンドリングを実装
- [ ] ユニットテスト作成（モック使用）
- [ ] docstring 記述（型ヒント含む）

---

**最終更新日**: 2026-03-05  
**次のドキュメント**: [04_SETUP.md](04_SETUP.md)

---

## **🌐 Phase 2 API スケルトン（FastAPI）**

Phase 2 として、最小構成の FastAPI バックエンドを開始しました。

### 基本実装

- エントリーポイント: `src/api/main.py`
- フレームワーク: FastAPI
- 方針: 既存のプロバイダー実装を API から再利用

### 初期エンドポイント

#### `GET /health`
- 目的: Liveness / Readiness チェック
- レスポンス:

```json
{
  "status": "ok"
}
```

#### `GET /services`
- 目的: 単一または全プロバイダーからサービス一覧を取得
- クエリパラメータ:
  - `provider`: `aws | gcp | azure | all`（デフォルト: `all`）
  - `region`: 任意のリージョン/ゾーンフィルタ
  - `status`: 任意のステータスフィルタ（例: `running`, `stopped`）
  - `service_type`: 任意のサービスタイプフィルタ（例: `EC2`, `Compute Engine`）
  - `sort_by`: ソートフィールド - `name | provider | status | created_at | region | service_type`（デフォルト: `name`）
  - `sort_order`: ソート順 - `asc | desc`（デフォルト: `asc`）
- レスポンス: `CloudService[]`
- 使用例:
  ```bash
  # ステータスでフィルタ
  GET /services?status=running
  
  # サービスタイプでフィルタ
  GET /services?service_type=EC2
  
  # 作成日時で降順ソート
  GET /services?sort_by=created_at&sort_order=desc
  
  # 組み合わせ: 実行中の EC2 インスタンスを名前順
  GET /services?provider=aws&service_type=EC2&status=running&sort_by=name
  ```

#### `GET /services/{provider}/{service_id}`
- 目的: 指定プロバイダーから特定サービスを取得
- パスパラメータ:
  - `provider`: `aws | gcp | azure`
  - `service_id`: プロバイダー固有ID
- レスポンス: `CloudService`
- エラー:
  - `400`: 未対応プロバイダー
  - `404`: サービス未検出

### テストカバレッジ

- 追加テスト: `tests/test_api_main.py`
- 検証内容:
  - `/health` の成功応答
  - `/services` の一覧応答
  - `/services` のステータスフィルタ
  - `/services` のサービスタイプフィルタ
  - `/services` のソート機能（昇順/降順）
  - `/services` のフィルタとソートの組み合わせ
  - `/services/{provider}/{service_id}` の成功応答
  - `/services/{provider}/{service_id}` の 404 応答

**最終更新日**: 2026-03-06

- Missing or invalid credentials
- Network errors
- Invalid service IDs
- Unauthorized access
- Provider-specific errors

All errors are displayed in user-friendly format with exit code 1.

## Future Enhancements

- **Filtering**: Advanced filtering by service type, tags, labels
- **Output**: Additional formats (YAML, HTML, SQL)
- **Caching**: Cache results to reduce API calls
- **Monitoring**: Real-time status monitoring
- **Actions**: Start, stop, delete services
- **Web API**: Convert to FastAPI backend for web application
- **Authentication**: Support for SAML, OAuth flows
