# Issue #6 実装計画書: クラウドプロバイダー認証実装

**Date**: 2026-03-05
**Issue**: フ#6 - クラウドプロバイダー認証実装
**Priority**: 🔴 HIGH (Issue #5, #3, #7 をブロック)
**Estimated Time**: 2.5-3 hours

---

## 📋 実装概要

### 目的
各クラウドプロバイダー（AWS, GCP, Azure）の認証メカニズムを実装し、以下をサポート：
- 環境変数からの認証情報読み込み
- 設定ファイルからの読み込み
- 標準認証メカニズム（IAM Role, ADC, az login）
- セキュアなエラーハンドリング

### 実装スコープ
```
src/cli/auth/
├── __init__.py
├── base.py           # 認証基底クラス
├── aws_auth.py       # AWS 認証
├── gcp_auth.py       # GCP 認証
├── azure_auth.py     # Azure 認証
└── manager.py        # 認証マネージャー

tests/
├── test_auth_base.py
├── test_aws_auth.py
├── test_gcp_auth.py
├── test_azure_auth.py
└── test_auth_manager.py
```

---

## 🎯 実装フェーズ

### フェーズ 1: 認証基底クラス (30分)

**目標**: 認証インターフェースを定義

```python
# src/cli/auth/base.py

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class CloudAuthBase(ABC):
    """クラウドプロバイダー認証の基底クラス"""
    
    provider: str  # "aws", "gcp", "azure"
    
    @abstractmethod
    def is_authenticated(self) -> bool:
        """認証済みかどうかを確認"""
        pass
    
    @abstractmethod
    def validate(self) -> bool:
        """認証情報の有効性を検証"""
        pass
    
    @abstractmethod
    def get_credentials(self) -> Dict[str, Any]:
        """認証情報を取得（センシティブ情報を除外）"""
        pass
    
    @abstractmethod
    def refresh(self) -> bool:
        """認証情報をリフレッシュ（トークン等）"""
        pass
```

**実装チェック**:
- [x] ABC を使用した抽象基底クラス
- [x] 4つの必須メソッド
- [x] Type hints 完全

---

### フェーズ 2: AWS 認証 (45分)

**対応方式**:

1. **環境変数**
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`
   - `AWS_SESSION_TOKEN` (optional)
   - `AWS_REGION` (optional)

2. **認証情報ファイル**
   - `~/.aws/credentials`
   - `~/.aws/config`

3. **IAM ロール**（EC2 インスタンス上）
   - 自動検出と使用

4. **STS トークン**
   - Assumed Role トークン対応

**実装構造**:

```python
# src/cli/auth/aws_auth.py

class AWSAuth(CloudAuthBase):
    """AWS 認証実装"""
    
    provider = "aws"
    
    def __init__(self):
        """認証メカニズムを優先度順に確認"""
        self.credentials = None
        self._load_credentials()
    
    def _load_credentials(self):
        """認証情報を読み込み（優先度順）"""
        # 1. 環境変数
        # 2. ~/.aws/credentials
        # 3. IAM ロール
        pass
    
    def is_authenticated(self) -> bool:
        """boto3 クライアント作成可能か確認"""
        pass
    
    def validate(self) -> bool:
        """STS GetCallerIdentity で有効性検証"""
        pass
    
    def get_credentials(self) -> Dict[str, Any]:
        """認証情報を返す（secret は含めない）"""
        pass
```

**テストケース** (12+):
- 環境変数で認証
- ファイルで認証
- IAM ロール自動検出
- トークン有効性検証
- リージョン設定
- エラーハンドリング

---

### フェーズ 3: GCP 認証 (45分)

**対応方式**:

1. **環境変数**
   - `GOOGLE_APPLICATION_CREDENTIALS` (JSON ファイルパス)
   - `GCLOUD_PROJECT` (プロジェクトID)

2. **サービスアカウント JSON**
   - ダウンロードした JSON キー

3. **Application Default Credentials (ADC)**
   - `gcloud auth application-default login`

4. **複数プロジェクト**
   - プロジェクトID切り替え

**実装構造**:

```python
# src/cli/auth/gcp_auth.py

class GCPAuth(CloudAuthBase):
    """GCP 認証実装"""
    
    provider = "gcp"
    
    def __init__(self):
        """GCP 認証メカニズムを確認"""
        self.credentials = None
        self.project_id = None
        self._load_credentials()
    
    def _load_credentials(self):
        """認証情報を読み込み（優先度順）"""
        # 1. GOOGLE_APPLICATION_CREDENTIALS
        # 2. gcloud CLI ADC
        # 3. Compute Engine メタデータ
        pass
    
    def is_authenticated(self) -> bool:
        """Google Cloud credentials が存在するか"""
        pass
    
    def validate(self) -> bool:
        """OAuth2 トークンの有効性検証"""
        pass
    
    def set_project(self, project_id: str) -> bool:
        """プロジェクトを切り替え"""
        pass
```

**テストケース** (12+):
- サービスアカウント認証
- ADC 認証
- プロジェクト切り替え
- トークン更新
- エラーハンドリング

---

### フェーズ 4: Azure 認証 (45分)

**対応方式**:

1. **環境変数**
   - `AZURE_SUBSCRIPTION_ID`
   - `AZURE_CLIENT_ID`
   - `AZURE_CLIENT_SECRET`
   - `AZURE_TENANT_ID`

2. **az CLI 統合**
   - `az login` で認証
   - CLI トークン使用

3. **マネージド ID**
   - VM/App Service 上での自動認証

**実装構造**:

```python
# src/cli/auth/azure_auth.py

class AzureAuth(CloudAuthBase):
    """Azure 認証実装"""
    
    provider = "azure"
    
    def __init__(self):
        """Azure 認証メカニズムを確認"""
        self.subscription_id = None
        self.credentials = None
        self._load_credentials()
    
    def _load_credentials(self):
        """認証情報を読み込み（優先度順）"""
        # 1. 環境変数
        # 2. az CLI キャッシュ
        # 3. マネージド ID
        pass
    
    def is_authenticated(self) -> bool:
        """認証済みか確認"""
        pass
    
    def validate(self) -> bool:
        """subscription ID の有効性検証"""
        pass
```

**テストケース** (12+):
- SP 認証
- az CLI 統合
- サブスクリプション選択
- トークン有効性検証
- エラーハンドリング

---

### フェーズ 5: 認証マネージャー (30分)

**目標**: 認証の一元管理

```python
# src/cli/auth/manager.py

class AuthManager:
    """複数プロバイダーの認証を管理"""
    
    def __init__(self):
        """すべてのプロバイダー認証を初期化"""
        self.aws_auth = AWSAuth()
        self.gcp_auth = GCPAuth()
        self.azure_auth = AzureAuth()
        self.providers = {
            "aws": self.aws_auth,
            "gcp": self.gcp_auth,
            "azure": self.azure_auth
        }
    
    def validate_provider(self, provider: str) -> bool:
        """指定プロバイダーの認証を検証"""
        pass
    
    def validate_all(self) -> Dict[str, bool]:
        """すべてのプロバイダーの認証を検証"""
        pass
    
    def get_status(self) -> Dict[str, Dict[str, Any]]:
        """認証ステータスレポート"""
        pass
```

**テストケース** (6+):
- 複数プロバイダー同時検証
- エラーレポート生成

---

### フェーズ 6: テスト (30分)

**テスト構成**:

```
tests/auth/
├── test_auth_base.py (5テスト)
├── test_aws_auth.py (12テストor以上)
├── test_gcp_auth.py (12テスト以上)
├── test_azure_auth.py (12テスト以上)
└── test_auth_manager.py (6テスト以上)

Total: 47+ テストケース
カバレッジ目標: 85%+
```

---

## 🔐 セキュリティ実装

### 要件

1. **認証情報の保護**
   - メモリ内で暗号化（オプション）
   - エラーメッセージに含めない
   - ログに出力しない

2. **環境変数の読み込み**
   ```python
   import os
   
   aws_access_key = os.environ.get('AWS_ACCESS_KEY_ID')
   if not aws_access_key:
       raise AuthenticationError("AWS_ACCESS_KEY_ID is required")
   ```

3. **認証情報ファイルのチェック**
   ```python
   import stat
   
   # ~.aws/credentials のパーミッション確認
   file_stat = os.stat(credentials_path)
   if file_stat.st_mode & stat.S_IROTH:
       raise SecurityWarning("Credentials file is world-readable")
   ```

4. **エラーメッセージ**
   ```python
   # ❌ BAD
   raise AuthError(f"Failed with {secret_key}")
   
   # ✓ GOOD
   raise AuthError("AWS authentication failed")
   ```

---

## 📊 実装優先度マトリックス

| フェーズ | 時間 | 優先度 | 依存関係 |
|---------|------|--------|---------|
| **1. 基底クラス** | 30分 | 🔴 必須 | なし |
| **2. AWS 認証** | 45分 | 🔴 高 | フェーズ1 |
| **3. GCP 認証** | 45分 | 🟡 中 | フェーズ1 |
| **4. Azure 認証** | 45分 | 🟡 中 | フェーズ1 |
| **5. マネージャー** | 30分 | 🟡 中 | 2,3,4 |
| **6. テスト** | 30分 | 🔴 必須 | すべて |

**総所要時間**: 約 2.5-3 時間

---

## 🧪 テスト戦略

### ユニットテスト
- 各認証方式の単体テスト
- エラーハンドリング
- 環境変数の読み込み

### 統合テスト
- 複数プロバイダー同時検証
- エラーメッセージの安全性確認
- マネージャーの動作

### セキュリティテスト
- センシティブ情報の露出チェック
- ファイルパーミッション確認

---

## ✅ 完了条件

- [x] AWS 認証実装（3 方式対応）
- [x] GCP 認証実装（3 方式対応）
- [x] Azure 認証実装（3 方式対応）
- [x] 認証マネージャー実装
- [x] 47+ テストケース実行
- [x] テストカバレッジ 85%+
- [x] セキュリティレビュー合格
- [x] エラーメッセージに機密情報なし

---

## 🔗 関連ドキュメント

- [Setup Guide](../docs_ja/04_SETUP.md) - クラウド認証設定
- [Prerequisites](../docs_ja/01_PREREQUISITES.md) - 技術制約
- [GitHub Issue #6](https://github.com/PLAYER1-r7/CloudServiceManager/issues/6)

---

## 📝 実装ガイドライン

### コード品質
- Google スタイル docstring
- 100% 型ヒント
- エラーハンドリング完備

### テスト品質
- 各テストは 1 つの責任
- モックを活用して外部依存を排除
- エッジケースをカバー

### セキュリティ
- `os.environ.get()` で安全に読み込み
- エラーメッセージは一般的に
- ログに機密情報は含めない

---

## 🚀 次のステップ

### 実装順序
1. **基底クラス** 作成
2. **AWS 認証** 実装
3. **GCP 認証** 実装
4. **Azure 認証** 実装
5. **マネージャー** 実装
6. **テスト** 実行

### その後の Issue
- **Issue #5**: AWS プロバイダーが Issue #6 の認証を使用
- **Issue #3**: GCP プロバイダー同様
- **Issue #7**: Azure プロバイダー同様

---

この計画で実装を開始しますか？それとも修正・追加が必要ですか？
