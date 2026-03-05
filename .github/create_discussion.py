#!/usr/bin/env python3
"""
GitHub Discussions 半自動投稿スクリプト

セッション内容を記述したMarkdownファイルからGitHub Discussionを作成します。

Usage:
    python .github/create_discussion.py <session_file.md> [--category "Category Name"]

Examples:
    python .github/create_discussion.py .github/EXAMPLE_AI_SESSION.md
    python .github/create_discussion.py .github/EXAMPLE_AI_SESSION.md --category "Ideas"
    python .github/create_discussion.py .github/EXAMPLE_AI_SESSION.md --category "AI Agent Sessions"

Requirements:
    - GitHub CLI (gh) のインストールと認証が必要
    - リポジトリでDiscussionsが有効化されていること

Authentication:
    GitHub CLI (gh) を使用 - プロジェクトポリシーに準拠
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Optional, Tuple


def check_gh_cli() -> bool:
    """GitHub CLIが利用可能かチェック"""
    try:
        result = subprocess.run(
            ["gh", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def get_repository_info() -> Tuple[str, str]:
    """gitリモートからリポジトリ情報を取得"""
    try:
        result = subprocess.run(
            ["git", "config", "--get", "remote.origin.url"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode != 0:
            raise ValueError("Git remote not found")
        
        remote_url = result.stdout.strip()
        
        # GitHub URLからowner/repoを抽出
        # 形式: https://github.com/owner/repo.git または git@github.com:owner/repo.git
        if "github.com" in remote_url:
            parts = remote_url.replace(".git", "").split("github.com")[-1].strip("/:").split("/")
            if len(parts) >= 2:
                return parts[0], parts[1]
        
        raise ValueError("Could not parse GitHub repository URL")
    
    except Exception as e:
        print(f"❌ Error detecting repository: {e}")
        sys.exit(1)


def get_repository_id(owner: str, repo: str) -> str:
    """GraphQL APIでリポジトリIDを取得"""
    query = """
    query($owner: String!, $repo: String!) {
      repository(owner: $owner, name: $repo) {
        id
        hasDiscussionsEnabled
      }
    }
    """
    
    try:
        result = subprocess.run(
            ["gh", "api", "graphql", "-f", f"query={query}", "-f", f"owner={owner}", "-f", f"repo={repo}"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode != 0:
            print(f"❌ GitHub API Error: {result.stderr}")
            sys.exit(1)
        
        data = json.loads(result.stdout)
        
        if not data.get("data", {}).get("repository", {}).get("hasDiscussionsEnabled"):
            print("❌ Discussions are not enabled for this repository")
            print("   Please enable Discussions in repository settings")
            sys.exit(1)
        
        return data["data"]["repository"]["id"]
    
    except Exception as e:
        print(f"❌ Error getting repository ID: {e}")
        sys.exit(1)


def get_category_id(owner: str, repo: str, category_name: str = "AI Agent Sessions", fallback: str = "Ideas") -> Tuple[Optional[str], str]:
    """
    指定されたカテゴリーのIDを取得
    
    Returns:
        Tuple[Optional[str], str]: (category_id, category_name used)
    """
    query = """
    query($owner: String!, $repo: String!) {
      repository(owner: $owner, name: $repo) {
        discussionCategories(first: 20) {
          nodes {
            id
            name
            emoji
          }
        }
      }
    }
    """
    
    try:
        result = subprocess.run(
            ["gh", "api", "graphql", "-f", f"query={query}", "-f", f"owner={owner}", "-f", f"repo={repo}"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode != 0:
            print(f"⚠️  Warning: Could not fetch categories: {result.stderr}")
            return None, ""
        
        data = json.loads(result.stdout)
        categories = data.get("data", {}).get("repository", {}).get("discussionCategories", {}).get("nodes", [])
        
        # カテゴリー名での検索（完全一致）
        for cat in categories:
            if category_name.lower() == cat["name"].lower():
                print(f"✅ Found category: {cat['emoji']} {cat['name']}")
                return cat["id"], cat["name"]
        
        # 部分一致検索
        for cat in categories:
            if category_name.lower() in cat["name"].lower():
                print(f"✅ Found category (partial match): {cat['emoji']} {cat['name']}")
                return cat["id"], cat["name"]
        
        # 指定されたカテゴリーが見つからない場合
        print(f"⚠️  Category '{category_name}' not found")
        print("\n📋 Available categories:")
        for cat in categories:
            print(f"   {cat['emoji']} {cat['name']}")
        
        # Fallbackカテゴリーを検索
        if fallback:
            print(f"\n💡 Trying fallback category: '{fallback}'")
            for cat in categories:
                if fallback.lower() == cat["name"].lower() or fallback.lower() in cat["name"].lower():
                    print(f"✅ Using fallback category: {cat['emoji']} {cat['name']}")
                    return cat["id"], cat["name"]
        
        # Fallbackも見つからない場合、最初のカテゴリーを使用
        if categories:
            first_cat = categories[0]
            print(f"\n💡 Using first available category: {first_cat['emoji']} {first_cat['name']}")
            return first_cat["id"], first_cat["name"]
        
        return None, ""
    
    except Exception as e:
        print(f"⚠️  Warning: Error getting category ID: {e}")
        return None, ""


def extract_title_from_content(content: str) -> str:
    """Markdown内容から最初のヘッダーをタイトルとして抽出"""
    for line in content.split("\n"):
        line = line.strip()
        if line.startswith("# "):
            return line[2:].strip()
    
    return "AI Agent Session"


def create_discussion(repo_id: str, category_id: Optional[str], category_name: str, title: str, body: str) -> str:
    """GraphQL APIでDiscussionを作成"""
    mutation = """
    mutation($repositoryId: ID!, $categoryId: ID!, $title: String!, $body: String!) {
      createDiscussion(input: {
        repositoryId: $repositoryId,
        categoryId: $categoryId,
        title: $title,
        body: $body
      }) {
        discussion {
          url
          number
          title
        }
      }
    }
    """
    
    if not category_id:
        print("❌ Cannot create discussion without a valid category")
        print("   Please check Discussions settings and create categories")
        sys.exit(1)
    
    try:
        # GraphQL変数をJSON形式で準備
        variables = {
            "repositoryId": repo_id,
            "categoryId": category_id,
            "title": title,
            "body": body
        }
        
        result = subprocess.run(
            [
                "gh", "api", "graphql",
                "-f", f"query={mutation}",
                "-F", f"repositoryId={repo_id}",
                "-F", f"categoryId={category_id}",
                "-F", f"title={title}",
                "-F", f"body={body}"
            ],
            capture_output=True,
            text=True,
            timeout=15
        )
        
        if result.returncode != 0:
            print(f"❌ Failed to create discussion: {result.stderr}")
            sys.exit(1)
        
        data = json.loads(result.stdout)
        discussion = data.get("data", {}).get("createDiscussion", {}).get("discussion", {})
        
        return discussion.get("url", "")
    
    except Exception as e:
        print(f"❌ Error creating discussion: {e}")
        sys.exit(1)


def main():
    """メイン処理"""
    # コマンドライン引数パーサー
    parser = argparse.ArgumentParser(
        description="GitHub Discussionを作成します",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
examples:
  python .github/create_discussion.py .github/EXAMPLE_AI_SESSION.md
  python .github/create_discussion.py session.md --category "Ideas"
  python .github/create_discussion.py session.md --category "AI Agent Sessions"
        """
    )
    parser.add_argument(
        "session_file",
        type=str,
        help="セッション内容が記述されたMarkdownファイル"
    )
    parser.add_argument(
        "--category",
        type=str,
        default="AI Agent Sessions",
        help="Discussion カテゴリー名 (デフォルト: AI Agent Sessions)"
    )
    parser.add_argument(
        "--fallback",
        type=str,
        default="Ideas",
        help="指定カテゴリーが見つからない場合のFallbackカテゴリー (デフォルト: Ideas)"
    )
    
    args = parser.parse_args()
    
    print("=" * 70)
    print("🤖 GitHub Discussions - AI Session Publisher")
    print("=" * 70)
    
    session_file = Path(args.session_file)
    
    if not session_file.exists():
        print(f"\n❌ Error: File not found: {session_file}")
        sys.exit(1)
    
    # GitHub CLIチェック
    print("\n📋 Checking prerequisites...")
    if not check_gh_cli():
        print("❌ GitHub CLI (gh) is not available")
        print("\n✅ Required: Install and authenticate GitHub CLI")
        print("   1. Install: https://cli.github.com/")
        print("   2. Authenticate: gh auth login")
        sys.exit(1)
    
    print("✅ GitHub CLI is available")
    
    # リポジトリ情報取得
    print("\n📋 Detecting repository...")
    owner, repo = get_repository_info()
    print(f"✅ Repository: {owner}/{repo}")
    
    # セッション内容読み込み
    print(f"\n📋 Reading session file: {session_file.name}")
    content = session_file.read_text(encoding="utf-8")
    title = extract_title_from_content(content)
    print(f"✅ Title: {title}")
    print(f"✅ Content length: {len(content)} characters")
    
    # リポジトリIDとカテゴリーID取得
    print("\n📋 Fetching repository information...")
    repo_id = get_repository_id(owner, repo)
    print(f"✅ Repository ID: {repo_id[:20]}...")
    
    print("\n📋 Fetching discussion categories...")
    category_id, used_category_name = get_category_id(owner, repo, args.category, args.fallback)
    
    # Discussion作成
    print("\n📋 Creating discussion...")
    discussion_url = create_discussion(repo_id, category_id, used_category_name, title, content)
    
    print("\n" + "=" * 70)
    print("✅ SUCCESS: Discussion created!")
    print("=" * 70)
    print(f"\n� Category: {used_category_name}")
    print(f"🔗 URL: {discussion_url}")
    print("\n💡 Next steps:")
    print("   - Review the discussion in GitHub")
    print("   - Add tags if needed")
    print("   - Pin if important")
    if used_category_name != args.category:
        print(f"   - Consider creating '{args.category}' category for future sessions")
    print()


if __name__ == "__main__":
    main()
