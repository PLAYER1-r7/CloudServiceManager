# GitHub Wiki セットアップガイド

このガイドでは、作成したWikiページをGitHub Wikiに公開する手順を説明します。

---

## 📋 準備完了したWikiページ

以下の3つのページが `.github/wiki/` ディレクトリに準備されています：

1. **Home.md** - Wikiのトップページ（必須）
2. **Getting-Started.md** - はじめに（初心者向けガイド）
3. **FAQ.md** - よくある質問

---

## 🚀 方法1: GitHub Web UIで作成（最も簡単）

### ステップ 1: Wikiを初期化

1. ブラウザーでリポジトリにアクセス:
   ```
   https://github.com/PLAYER1-r7/CloudServiceManager
   ```

2. 上部の **"Wiki"** タブをクリック

3. **"Create the first page"** ボタンをクリック

### ステップ 2: Homeページを作成

1. タイトルは **"Home"** のまま（変更しない）

2. 以下のファイルの内容をコピー:
   ```
   .github/wiki/Home.md
   ```

3. エディタにペースト

4. 下部の **"Save Page"** をクリック

### ステップ 3: 追加ページを作成

**Getting Started ページ**:
1. Wiki画面右上の **"New Page"** をクリック
2. タイトル: `Getting-Started`
3. `.github/wiki/Getting-Started.md` の内容をペースト
4. **"Save Page"** をクリック

**FAQ ページ**:
1. **"New Page"** をクリック
2. タイトル: `FAQ`
3. `.github/wiki/FAQ.md` の内容をペースト
4. **"Save Page"** をクリック

---

## 🔧 方法2: Gitコマンドで一括アップロード（推奨・自動化）

### ステップ 1: Wikiリポジトリをクローン

まず、GitHub上でWikiを初期化する必要があります（Web UIで1ページ作成）。

その後：

```bash
# 一時ディレクトリに移動
cd /tmp

# Wikiリポジトリをクローン
git clone https://github.com/PLAYER1-r7/CloudServiceManager.wiki.git
cd CloudServiceManager.wiki
```

### ステップ 2: Wikiページをコピー

```bash
# プロジェクトの wiki ファイルをコピー
cp /workspaces/CloudServiceManager/.github/wiki/*.md .

# ファイルを確認
ls -la
# 出力: Home.md, Getting-Started.md, FAQ.md
```

### ステップ 3: コミットしてプッシュ

```bash
# 全ファイルを追加
git add .

# コミット
git commit -m "docs: 初期Wikiページを追加 (Home, Getting Started, FAQ)"

# プッシュ
git push origin master
```

### ステップ 4: 確認

ブラウザーでWikiを確認:
```
https://github.com/PLAYER1-r7/CloudServiceManager/wiki
```

---

## 🎨 Wikiページのリンク構造

作成したページは以下のように相互リンクされています：

```
Home (Wikiトップ)
├── Getting Started (はじめに)
│   ├── インストール手順
│   ├── 認証設定
│   ├── 最初のコマンド
│   └── トラブルシューティング → FAQ
├── FAQ (よくある質問)
│   ├── 認証・セキュリティ
│   ├── 使い方・機能
│   ├── トラブルシューティング
│   └── 開発・貢献
└── 技術ドキュメント (リポジトリへのリンク)
    ├── CLI設計仕様
    ├── プロジェクト計画
    └── 開発環境セットアップ
```

---

## ✨ Wikiの利点

### vs. `/docs` ディレクトリ

| 特徴 | `/docs` | Wiki |
|------|---------|------|
| **バージョン管理** | Git（厳密） | Git（独立リポジトリ） |
| **編集の容易さ** | Pull Request必要 | Web UIで直接編集可 |
| **用途** | 技術仕様・設計書 | ユーザーガイド・FAQ |
| **外部貢献** | ハードル高い | 簡単 |
| **検索性** | リポジトリ内 | Wiki専用検索 |

### 期待される効果

1. **新規ユーザーの参入障壁を下げる**
   - コードを見ずに使い方がわかる
   - インストールから実行まで一貫したガイド

2. **FAQで質問を削減**
   - よくある問題を事前に解決
   - Issue の重複を防ぐ

3. **コミュニティの成長**
   - ユーザーがWikiを編集・改善
   - ベストプラクティスを共有

4. **ドキュメントの役割分担**
   - `/docs`: 開発者・実装者向け（技術的）
   - Wiki: エンドユーザー向け（わかりやすい）

---

## 📝 今後の追加ページ案

### Phase 1 完了後に追加するページ

1. **Installation** - 詳細なインストールガイド
   - OS別の手順
   - Docker環境での実行
   - トラブルシューティング

2. **Tutorials** - 実践的なチュートリアル
   - AWS リソース一覧を取得
   - 複数クラウドの統合管理
   - CSV出力でExcel分析

3. **Command-Reference** - コマンドリファレンス
   - 全コマンドの詳細
   - オプション一覧
   - 使用例

4. **Architecture** - アーキテクチャ概要（簡易版）
   - システム構成図
   - データフロー
   - セキュリティモデル

### Phase 2 以降

5. **API-Documentation** - Web API仕様
6. **Dashboard-Guide** - ダッシュボード使用ガイド
7. **Contributing** - コントリビューションガイド
8. **Use-Cases** - ユースケース集

---

## 🔗 Wikiへのリンク

Wikiを作成したら、以下の場所にリンクを追加すると良いでしょう：

### 1. README.md

```markdown
## 📚 ドキュメント

- **[Wiki](https://github.com/PLAYER1-r7/CloudServiceManager/wiki)** - ユーザーガイド・チュートリアル
- **[Getting Started](https://github.com/PLAYER1-r7/CloudServiceManager/wiki/Getting-Started)** - はじめに
- **[FAQ](https://github.com/PLAYER1-r7/CloudServiceManager/wiki/FAQ)** - よくある質問
```

### 2. GitHub Issuesテンプレート

```markdown
質問する前に [FAQ](https://github.com/PLAYER1-r7/CloudServiceManager/wiki/FAQ) を確認してください。
```

### 3. GitHub Discussions（準備中）

Discussionsを有効化する際、Wikiへのリンクを追加

---

## 🎯 次のステップ

1. **Wikiを公開**
   - 上記の方法1または方法2で実行

2. **README.mdにWikiリンクを追加**
   ```bash
   # README.md を編集
   vim /workspaces/CloudServiceManager/README.md
   ```

3. **Phase 1完了後にチュートリアルを追加**
   - 実際の動作スクリーンショット
   - 具体的な使用例

4. **ユーザーフィードバックを反映**
   - FAQ を拡充
   - トラブルシューティングを充実

---

## 💡 ベストプラクティス

### Wikiの運用

- **定期的な更新**: 機能追加時はWikiも更新
- **スクリーンショット**: 可能な限りビジュアルを追加
- **シンプル**: 技術的詳細は `/docs` に、理解しやすさ重視
- **検索最適化**: よく検索されるキーワードを含める

### コミュニティ貢献の促進

- Wikiページにフッターを追加:
  ```markdown
  ---
  **このページを改善**: [編集を提案](リンク)
  ```

- Issue テンプレートで案内:
  ```markdown
  ドキュメントの改善提案は [Wiki](リンク) の該当ページで直接編集できます。
  ```

---

## ✅ チェックリスト

Wikiセットアップが完了したら確認:

- [ ] Home ページが作成されている
- [ ] Getting Started ページが作成されている
- [ ] FAQ ページが作成されている
- [ ] 各ページのリンクが正しく動作する
- [ ] README.md から Wiki へのリンクを追加
- [ ] Wiki がリポジトリのトップナビゲーションに表示される

---

**最終更新**: 2026-03-05
