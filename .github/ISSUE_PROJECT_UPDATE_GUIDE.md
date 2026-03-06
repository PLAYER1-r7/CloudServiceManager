# GitHub Issue & Project 更新ガイドライン

> **目的**: Phase完了時の Issue/Project 更新を標準化し、プロジェクト状態を常に最新に保つ

---

## 📋 Phase完了時の必須タスク

## 🛠️ ツール運用ルール（必須）

- 必要なソフトウェアが未導入の場合は、まずインストールする（例: `gh`, `jq`, `ripgrep`）
- 代替手段は原則使わない。やむを得ない場合のみ一時的に利用する
- 代替手段を使った場合は、IssueコメントまたはPRコメントに理由を記録する
- 制約（権限、ネットワーク、ポリシー）が解消したら、代替運用を終了し正式ツールへ戻す

---

### 1. Issue の更新

#### ✅ 完了したIssueをクローズ

Phase内で実装された全Issueをクローズし、完了コメントを追加：

```bash
# 個別Issueをクローズ
gh issue close <ISSUE_NUMBER> --repo PLAYER1-r7/CloudServiceManager \
  --comment "✅ 完了 (vX.X.X)

実装内容:
- 機能1
- 機能2

**テスト結果**: XX tests, XX% coverage
**関連ファイル**: src/xxx.py, tests/test_xxx.py"
```

**クローズコメントに含めるべき情報:**
- ✅ 完了マーク
- バージョン番号
- 実装された主要機能リスト
- テスト結果（テスト数、カバレッジ）
- 関連ファイル
- 関連コミットハッシュ（該当する場合）

#### ✅ Phase完了Issue を作成

各Phase完了時に記録用Issueを作成：

```bash
gh issue create --repo PLAYER1-r7/CloudServiceManager \
  --title "Phase X: [Phase名] (vX.X.X) ✅" \
  --label "enhancement" \
  --body "## Phase X 完了報告

### 📦 バージョン: vX.X.X

[Phase の概要説明]

---

## ✅ 実装された機能

### 1. [機能カテゴリ1]
- ✅ 機能A
- ✅ 機能B

### 2. [機能カテゴリ2]
...

---

## 📊 統計

- **総テスト数**: XXX passed, X skipped
- **カバレッジ**: XX%
- **セキュリティ問題**: X issues

---

## 📚 ドキュメント

- [関連ドキュメント1](URL)
- [関連ドキュメント2](URL)

---

## 🔗 関連コミット

- \`hash1\` - commit message 1
- \`hash2\` - commit message 2

---

**Status**: ✅ COMPLETED"
```

作成後すぐにクローズ：

```bash
gh issue close <NEW_ISSUE_NUMBER> --repo PLAYER1-r7/CloudServiceManager \
  --comment "Phase X は完了しました。このIssueは完了報告として作成され、即座にクローズされます。"
```

---

### 2. GitHub Projects の更新

**⚠️ 注意**: Projects更新には `read:project` および `write:project` スコープが必要

#### トークンスコープの確認

```bash
gh auth status
```

必要なスコープ:
- `repo` (既存)
- `workflow` (既存)
- `read:project` ⬅️ 必要
- `write:project` ⬅️ 必要

#### トークン再作成（スコープ不足の場合）

1. https://github.com/settings/tokens/new にアクセス
2. 以下のスコープを選択:
   - `repo` (フルアクセス)
   - `workflow`
   - `read:org`
   - `project` (フルアクセス) ⬅️ 重要
3. トークンを生成してコピー
4. 再認証:
   ```bash
   gh auth logout
   echo "YOUR_NEW_TOKEN" | gh auth login --with-token
   ```

#### Project更新手順（GraphQL API使用）

**Projectの取得:**

```bash
gh api graphql -f query='
{
  user(login: "PLAYER1-r7") {
    projectsV2(first: 10) {
      nodes {
        id
        title
        number
      }
    }
  }
}'
```

**Project内のアイテム一覧:**

```bash
gh api graphql -f query='
{
  node(id: "PROJECT_ID") {
    ... on ProjectV2 {
      items(first: 20) {
        nodes {
          id
          content {
            ... on Issue {
              number
              title
              state
            }
          }
        }
      }
    }
  }
}'
```

**アイテムのステータス更新:**

```bash
# Issue完了時にProjectのステータスを "Done" に更新
gh api graphql -f query='
mutation {
  updateProjectV2ItemFieldValue(
    input: {
      projectId: "PROJECT_ID"
      itemId: "ITEM_ID"
      fieldId: "STATUS_FIELD_ID"
      value: {
        singleSelectOptionId: "DONE_OPTION_ID"
      }
    }
  ) {
    projectV2Item {
      id
    }
  }
}'
```

---

### 3. ドキュメントの更新

#### ✅ 開発チェックリスト (docs/05_DEVELOPMENT_CHECKLIST.md)

Phase完了時に更新:

```markdown
- **Phase X**: [Phase名] (完了 - Version vX.X.X)
  - [実装内容の詳細リスト]
  - **テスト & 品質保証:**
    - [テスト結果]
  - **デプロイメント:**
    - [デプロイ関連の成果]
  - **セキュリティ & CI/CD:**
    - [セキュリティ・CI関連の成果]
  - 全テスト成功: XXX passed, X skipped
  - バージョン: vX.X.X-alpha → vX.X.X-beta → vX.X.X
```

#### ✅ バージョン履歴 (docs/VERSION_HISTORY.md)

新しいバージョンセクションを追加:

```markdown
## Version X.X.X - Phase X Complete (YYYY-MM-DD)

### Major Features

**[カテゴリ1]:**
- ✅ 機能A
- ✅ 機能B

**[カテゴリ2]:**
- ✅ 機能C

### Commits

- \`hash1\` - commit message 1
- \`hash2\` - commit message 2

### Statistics

- Total Tests: XXX passed, X skipped
- Coverage: XX%
- Security Issues: X
```

#### ✅ Wiki の更新

**Home.md:**
- バージョン番号を更新
- Phase完了ステータスを更新
- 新機能セクションを追加

**Getting-Started.md:**
- 新機能の使用例を追加
- API/CLI の使い方を更新

**新規ページ作成（必要に応じて）:**
- デプロイメントガイド
- 新機能のチュートリアル

---

## 🔄 ワークフロー例: Phase完了時

### Phase 2 完了時の実際の手順

```bash
# 1. 完了したIssueをクローズ（Phase 1の残りIssue）
gh issue close 1 --comment "✅ 完了 - list-services implementation"
gh issue close 3 --comment "✅ 完了 - GCP provider"
gh issue close 4 --comment "✅ 完了 - Integration tests"
gh issue close 7 --comment "✅ 完了 - Azure provider"

# 2. Phase完了Issueを作成＆クローズ
gh issue create --title "Phase 2: Production-Ready Web API (v2.0.0) ✅" \
  --label "enhancement" \
  --body "[詳細な完了報告]"
# → #20 が作成される

gh issue close 20 --comment "Phase 2 完了報告"

# 3. ドキュメント更新
# - docs/05_DEVELOPMENT_CHECKLIST.md
# - docs/VERSION_HISTORY.md
# - docs_ja/ (日本語版も同期)
# - wiki-repo/Home.md
# - wiki-repo/Getting-Started.md
# - wiki-repo/[新規ページ].md

git add docs/ docs_ja/ wiki-repo/
git commit -m "docs: update documentation for Phase X completion"
git push origin develop

# 4. Wiki を push（サブモジュール）
cd wiki-repo
git add .
git commit -m "docs: update wiki for Phase X completion"
git push origin master
cd ..

git add wiki-repo
git commit -m "chore: update wiki submodule reference"
git push origin develop

# 5. GitHub Projects を更新（read:project スコープ必要）
# Web UI で手動更新、または GraphQL API を使用
```

---

## 📝 チェックリスト

Phase完了時に以下を確認：

### Issue管理
- [ ] 完了したIssueすべてに完了コメントを追加
- [ ] 完了したIssueをすべてクローズ
- [ ] Phase完了記録Issueを作成＆クローズ
- [ ] Issueに適切なラベルを付与

### Project管理
- [ ] トークンに `project` スコープがあることを確認
- [ ] Project内の完了アイテムを "Done" に移動
- [ ] Project概要を更新（完了率など）

### ドキュメント
- [ ] `docs/05_DEVELOPMENT_CHECKLIST.md` を更新
- [ ] `docs/VERSION_HISTORY.md` に新バージョンを追加
- [ ] `docs_ja/` も同期して更新
- [ ] Wiki の `Home.md` を更新
- [ ] Wiki の `Getting-Started.md` を更新
- [ ] 必要に応じて新規 Wiki ページを作成
- [ ] Wiki 変更を commit & push
- [ ] メインリポジトリの wiki サブモジュール参照を更新

### Git操作
- [ ] すべての変更を commit
- [ ] develop ブランチに push
- [ ] CI/CD が成功することを確認

---

## 🚨 よくある問題と解決方法

### 問題1: トークンスコープ不足

**症状:**
```
Your token has not been granted the required scopes
```

**解決:**
https://github.com/settings/tokens から新しいトークンを生成し、必要なスコープを追加

### 問題2: ラベルが存在しない

**症状:**
```
could not add label: 'phase-X' not found
```

**解決:**
既存のラベル（`enhancement`, `documentation`など）を使用するか、Web UIでラベルを作成

### 問題3: Wiki push が失敗

**症状:**
```
remote: Permission denied
```

**解決:**
Wiki リポジトリのクローンURLを確認。HTTPS認証を使用している場合、トークンが必要

---

## 📚 参考資料

- [GitHub CLI Manual](https://cli.github.com/manual/)
- [GitHub GraphQL API](https://docs.github.com/en/graphql)
- [GitHub Projects API](https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project)
- [Personal Access Tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)

---

**最終更新**: 2026-03-06
**適用開始**: Phase 2完了以降
