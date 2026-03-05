# FAQ - よくある質問

CloudServiceManagerに関するよくある質問と回答をまとめています。

---

## 🔐 認証・セキュリティ

### Q1: 認証情報はどこに保存されますか？

**A**: CloudServiceManagerは独自に認証情報を保存しません。各クラウドプロバイダーの公式CLI（AWS CLI、gcloud、Azure CLI）が管理する認証情報を使用します。

- **AWS**: `~/.aws/credentials` または環境変数
- **GCP**: `~/.config/gcloud/` または Application Default Credentials
- **Azure**: `~/.azure/` または環境変数

### Q2: 複数のAWSアカウントを管理できますか？

**A**: はい、AWS CLIのプロファイル機能を使用できます。

```bash
# プロファイルを作成
aws configure --profile production
aws configure --profile development

# 使用するプロファイルを指定
export AWS_PROFILE=production
cloudmgr list-services --provider aws
```

### Q3: 読み取り専用の権限で使用できますか？

**A**: はい、推奨します。CloudServiceManagerは現在リソースの**読み取り専用**です。以下の最小権限で使用できます：

**AWS最小権限例**:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ec2:Describe*",
        "rds:Describe*",
        "s3:List*",
        "lambda:List*"
      ],
      "Resource": "*"
    }
  ]
}
```

---

## ⚙️ 使い方・機能

### Q4: どのクラウドサービスに対応していますか？

**A**: Phase 1（現在開発中）では以下に対応予定：

| プロバイダー | サービス | ステータス |
|------------|---------|----------|
| **AWS** | EC2, RDS, S3, Lambda | 🚧 開発中 |
| **GCP** | Compute Engine, Cloud Storage | 🚧 開発中 |
| **Azure** | Virtual Machines, Storage | 🚧 開発中 |

詳細は [プロジェクト計画](https://github.com/PLAYER1-r7/CloudServiceManager/blob/master/docs_ja/02_PROJECT_PLAN.md) を参照してください。

### Q5: リージョンを指定しない場合、どうなりますか？

**A**: 全リージョンのリソースを取得します。ただし、パフォーマンスを考慮して、通常使用するリージョンを指定することを推奨します。

```bash
# 全リージョン（遅い可能性あり）
cloudmgr list-services --provider aws

# 特定リージョン（推奨）
cloudmgr list-services --provider aws --region us-east-1
```

### Q6: 出力をファイルに保存できますか？

**A**: はい、標準的なリダイレクトを使用できます。

```bash
# テーブル形式で保存
cloudmgr list-services > output.txt

# JSON形式で保存
cloudmgr list-services --format json > output.json

# CSV形式で保存（Excelで開ける）
cloudmgr list-services --format csv > output.csv
```

### Q7: 特定のサービスタイプだけをフィルタできますか？

**A**: 現在、コマンドレベルのフィルタは未実装ですが、出力をパイプで処理できます。

```bash
# JSONで出力してjqでフィルタ
cloudmgr list-services --format json | jq '.[] | select(.service_type=="EC2")'

# grepでテーブル出力をフィルタ
cloudmgr list-services | grep "EC2"
```

将来のバージョンでは `--service-type` オプションを追加予定です。

---

## 🐛 トラブルシューティング

### Q8: "ModuleNotFoundError: No module named 'typer'" エラーが出ます

**A**: 依存関係がインストールされていません。

```bash
# 仮想環境を有効化
source venv/bin/activate

# 依存関係を再インストール
pip install -r requirements.txt
```

### Q9: "botocore.exceptions.NoCredentialsError" エラーが出ます

**A**: AWS認証情報が設定されていません。

**解決方法**:
```bash
# AWS CLIで設定
aws configure

# または環境変数を設定
export AWS_ACCESS_KEY_ID="your-key"
export AWS_SECRET_ACCESS_KEY="your-secret"

# 認証を確認
aws sts get-caller-identity
```

### Q10: GCPで "DefaultCredentialsError" が出ます

**A**: GCP認証情報が設定されていません。

**解決方法**:
```bash
# Application Default Credentialsを設定
gcloud auth application-default login

# プロジェクトを設定
gcloud config set project YOUR_PROJECT_ID

# 認証を確認
gcloud auth list
```

### Q11: Azureで "AzureCliCredential" エラーが出ます

**A**: Azure CLIにログインしていません。

**解決方法**:
```bash
# Azure CLIでログイン
az login

# サブスクリプションを確認
az account list

# 使用するサブスクリプションを設定
az account set --subscription "YOUR_SUBSCRIPTION_ID"

# 認証を確認
az account show
```

### Q12: 応答が非常に遅いです

**A**: 複数の原因が考えられます：

1. **全リージョンを検索している** → リージョンを指定
   ```bash
   cloudmgr list-services --provider aws --region us-east-1
   ```

2. **リソースが大量にある** → プロバイダーを指定
   ```bash
   cloudmgr list-services --provider aws
   ```

3. **ネットワーク遅延** → タイムアウト設定を調整（将来のバージョンで対応予定）

### Q13: "Permission denied" エラーが出ます

**A**: IAM権限が不足しています。

**確認事項**:
- AWSの場合: IAMユーザー/ロールに `ec2:Describe*` などの権限があるか
- GCPの場合: サービスアカウントに `compute.instances.list` 権限があるか
- Azureの場合: Reader ロール以上が割り当てられているか

管理者に権限の付与を依頼してください。

---

## 💻 開発・貢献

### Q14: バグを見つけました。どうすればいいですか？

**A**: [GitHub Issues](https://github.com/PLAYER1-r7/CloudServiceManager/issues) で報告してください。

**報告内容**:
- エラーメッセージ
- 実行したコマンド
- 環境情報（OS、Pythonバージョン）

### Q15: 新機能をリクエストしたいです

**A**: [GitHub Issues](https://github.com/PLAYER1-r7/CloudServiceManager/issues) で Feature Request を作成してください。

テンプレート：
1. **機能の説明**: 何をしたいか
2. **ユースケース**: なぜ必要か
3. **提案する実装**: どう実装するか（任意）

### Q16: プロジェクトに貢献したいです

**A**: 歓迎します！Phase 1完了後に詳細なコントリビューションガイドを公開予定です。

**現在できること**:
1. [Issues](https://github.com/PLAYER1-r7/CloudServiceManager/issues) を確認
2. "good first issue" ラベルのタスクを探す
3. 興味のあるIssueにコメント

---

## 📊 制限事項

### Q17: 現在の制限事項は何ですか？

**A**: Phase 1（CLI開発フェーズ）の現在：

**機能制限**:
- ✅ **リソースの読み取りのみ** - 作成/変更/削除は不可
- ✅ **基本的なサービスのみ** - EC2、Compute Engine、VMなど
- ⏳ **リアルタイム監視なし** - Phase 2で実装予定
- ⏳ **Web UIなし** - Phase 2で実装予定

**パフォーマンス**:
- 大量のリソース（1000+）がある場合、応答に時間がかかる可能性
- 将来のバージョンでキャッシング機能を追加予定

### Q18: Webブラウザーで使用できますか？

**A**: 現在はCLI（コマンドライン）のみです。Phase 2でWebアプリケーションを開発予定です。

**Phase 2計画**:
- ブラウザーベースのダッシュボード
- リアルタイムリソース監視
- グラフィカルな可視化

詳細: [プロジェクト計画](https://github.com/PLAYER1-r7/CloudServiceManager/blob/master/docs_ja/02_PROJECT_PLAN.md#phase-2-web-application将来計画)

---

## 🔍 その他

### Q19: ライセンスは何ですか？

**A**: MIT Licenseです。商用利用も可能です。

詳細: [LICENSE](https://github.com/PLAYER1-r7/CloudServiceManager/blob/master/LICENSE)

### Q20: サポートはありますか？

**A**: コミュニティベースのサポートを提供しています：

- **GitHub Issues**: バグ報告、機能リクエスト
- **GitHub Discussions**: 使い方の質問（準備中）
- **このWiki**: ドキュメントとFAQ

商用サポートは提供していません。

---

## ❓ この質問がない場合

### 問題が解決しない場合

1. **[GitHub Issues](https://github.com/PLAYER1-r7/CloudServiceManager/issues)** で既存の Issue を検索
2. 見つからない場合は、新しい Issue を作成
3. **[GitHub Discussions](https://github.com/PLAYER1-r7/CloudServiceManager/discussions)** で質問（準備中）

### ドキュメントを改善したい場合

このFAQを改善する提案がある場合：
- Wiki を直接編集（権限がある場合）
- [Issues](https://github.com/PLAYER1-r7/CloudServiceManager/issues) で提案

---

**最終更新**: 2026-03-05
**貢献**: このページへの追加・修正を歓迎します！
