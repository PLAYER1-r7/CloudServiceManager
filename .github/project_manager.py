#!/usr/bin/env python3
"""
GitHub Projects Management Script

This script provides automated project management capabilities for AI agents.
It integrates with GitHub CLI to manage project items, statuses, and workflows.
"""

import json
import subprocess
import sys
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


class ProjectStatus(Enum):
    """Project item status options"""
    BACKLOG = "Backlog"
    TODO = "Todo"
    IN_PROGRESS = "In Progress"
    IN_REVIEW = "In Review"
    DONE = "Done"


class Priority(Enum):
    """Issue priority levels"""
    HIGH = "🔴 High"
    MEDIUM = "🟡 Medium"
    LOW = "🟢 Low"


@dataclass
class ProjectConfig:
    """Project configuration"""
    owner: str = "PLAYER1-r7"
    repo: str = "CloudServiceManager"
    project_number: int = 1


class GitHubProjectManager:
    """Manage GitHub Projects via CLI"""
    
    def __init__(self, config: Optional[ProjectConfig] = None):
        self.config = config or ProjectConfig()
    
    def _run_gh_command(self, args: List[str]) -> Dict:
        """Execute gh command and return JSON result"""
        try:
            result = subprocess.run(
                ["gh"] + args,
                capture_output=True,
                text=True,
                check=True
            )
            if result.stdout.strip():
                return json.loads(result.stdout)
            return {}
        except subprocess.CalledProcessError as e:
            print(f"❌ Error executing gh command: {e.stderr}", file=sys.stderr)
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"❌ Error parsing JSON: {e}", file=sys.stderr)
            sys.exit(1)
    
    def get_project_items(self) -> List[Dict]:
        """Get all items in the project"""
        result = self._run_gh_command([
            "project", "item-list",
            str(self.config.project_number),
            "--owner", self.config.owner,
            "--format", "json",
            "--limit", "100"
        ])
        return result.get("items", [])
    
    def get_issue_details(self, issue_number: int) -> Dict:
        """Get detailed information about an issue"""
        result = self._run_gh_command([
            "issue", "view",
            str(issue_number),
            "--repo", f"{self.config.owner}/{self.config.repo}",
            "--json", "number,title,state,labels,body,assignees,milestone,url"
        ])
        return result
    
    def update_item_status(self, item_id: str, status: ProjectStatus) -> bool:
        """Update project item status"""
        try:
            subprocess.run([
                "gh", "project", "item-edit",
                "--project-id", str(self.config.project_number),
                "--owner", self.config.owner,
                "--id", item_id,
                "--field-id", "Status",
                "--text", status.value
            ], check=True, capture_output=True)
            return True
        except subprocess.CalledProcessError:
            return False
    
    def add_issue_to_project(self, issue_number: int) -> bool:
        """Add an issue to the project"""
        try:
            subprocess.run([
                "gh", "project", "item-add",
                str(self.config.project_number),
                "--owner", self.config.owner,
                "--url", f"https://github.com/{self.config.owner}/{self.config.repo}/issues/{issue_number}"
            ], check=True, capture_output=True)
            return True
        except subprocess.CalledProcessError:
            return False
    
    def display_project_status(self):
        """Display current project status in a formatted way"""
        items = self.get_project_items()
        
        print("\n" + "="*80)
        print(f"📊 GitHub Project Status: {self.config.repo}")
        print("="*80 + "\n")
        
        # Group by status
        status_groups = {}
        for item in items:
            status = item.get("status", "Unknown")
            if status not in status_groups:
                status_groups[status] = []
            status_groups[status].append(item)
        
        # Display by status
        status_order = ["Todo", "In Progress", "In Review", "Backlog", "Done"]
        
        for status in status_order:
            if status in status_groups:
                items_in_status = status_groups[status]
                icon = self._get_status_icon(status)
                print(f"\n{icon} {status} ({len(items_in_status)} items)")
                print("-" * 80)
                
                for item in items_in_status:
                    content = item.get("content", {})
                    number = content.get("number", "?")
                    title = item.get("title", content.get("title", "Unknown"))
                    labels = ", ".join(item.get("labels", []))
                    
                    print(f"  #{number} {title}")
                    if labels:
                        print(f"      Labels: {labels}")
        
        print("\n" + "="*80 + "\n")
    
    @staticmethod
    def _get_status_icon(status: str) -> str:
        """Get emoji icon for status"""
        icons = {
            "Backlog": "📋",
            "Todo": "📝",
            "In Progress": "🚀",
            "In Review": "🔍",
            "Done": "✅"
        }
        return icons.get(status, "❓")
    
    def recommend_next_tasks(self) -> List[Dict]:
        """Recommend which tasks to work on next based on priority"""
        items = self.get_project_items()
        
        # Get items in Backlog or Todo
        actionable = [
            item for item in items 
            if item.get("status") in ["Backlog", "Todo"]
        ]
        
        # Define priority order (based on labels and issue numbers)
        priority_map = {
            2: Priority.HIGH,  # CloudService model
            6: Priority.HIGH,  # Authentication
            5: Priority.MEDIUM,  # AWS provider
            1: Priority.MEDIUM,  # list-services
            3: Priority.LOW,   # GCP provider
            7: Priority.LOW,   # Azure provider
            4: Priority.LOW    # Integration tests
        }
        
        recommendations = []
        for item in actionable:
            content = item.get("content", {})
            number = content.get("number")
            priority = priority_map.get(number, Priority.LOW)
            
            recommendations.append({
                "number": number,
                "title": item.get("title"),
                "priority": priority,
                "status": item.get("status"),
                "labels": item.get("labels", [])
            })
        
        # Sort by priority
        priority_order = {Priority.HIGH: 0, Priority.MEDIUM: 1, Priority.LOW: 2}
        recommendations.sort(key=lambda x: priority_order[x["priority"]])
        
        return recommendations
    
    def display_recommendations(self):
        """Display task recommendations"""
        recommendations = self.recommend_next_tasks()
        
        print("\n" + "="*80)
        print("🎯 Recommended Next Tasks")
        print("="*80 + "\n")
        
        current_priority = None
        for rec in recommendations:
            if rec["priority"] != current_priority:
                current_priority = rec["priority"]
                print(f"\n{current_priority.value}")
                print("-" * 80)
            
            print(f"  #{rec['number']} {rec['title']}")
            print(f"      Status: {rec['status']}")
            if rec['labels']:
                print(f"      Labels: {', '.join(rec['labels'])}")
        
        print("\n" + "="*80 + "\n")
        
        # Provide actionable advice
        if recommendations:
            top_tasks = [r for r in recommendations if r["priority"] == Priority.HIGH]
            if top_tasks:
                print("💡 Recommendation: Start with high-priority tasks:")
                for task in top_tasks:
                    print(f"   - Issue #{task['number']}: {task['title']}")
                print()
    
    def generate_progress_report(self) -> str:
        """Generate a progress report"""
        items = self.get_project_items()
        total = len(items)
        
        status_counts = {}
        for item in items:
            status = item.get("status", "Unknown")
            status_counts[status] = status_counts.get(status, 0) + 1
        
        done = status_counts.get("Done", 0)
        in_progress = status_counts.get("In Progress", 0)
        in_review = status_counts.get("In Review", 0)
        
        completion_rate = (done / total * 100) if total > 0 else 0
        
        report = f"""
📊 Project Progress Report
{'='*80}

Total Issues: {total}
✅ Done: {done} ({done/total*100:.1f}%)
🚀 In Progress: {in_progress}
🔍 In Review: {in_review}
📋 Backlog/Todo: {status_counts.get('Backlog', 0) + status_counts.get('Todo', 0)}

Overall Completion: {completion_rate:.1f}%
{'='*80}
"""
        return report


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="GitHub Projects Management for AI Agents"
    )
    parser.add_argument(
        "command",
        choices=["status", "recommend", "report", "all"],
        help="Command to execute"
    )
    parser.add_argument(
        "--owner",
        default="PLAYER1-r7",
        help="GitHub owner/organization"
    )
    parser.add_argument(
        "--repo",
        default="CloudServiceManager",
        help="Repository name"
    )
    parser.add_argument(
        "--project",
        type=int,
        default=1,
        help="Project number"
    )
    
    args = parser.parse_args()
    
    config = ProjectConfig(
        owner=args.owner,
        repo=args.repo,
        project_number=args.project
    )
    
    manager = GitHubProjectManager(config)
    
    if args.command == "status":
        manager.display_project_status()
    elif args.command == "recommend":
        manager.display_recommendations()
    elif args.command == "report":
        print(manager.generate_progress_report())
    elif args.command == "all":
        manager.display_project_status()
        manager.display_recommendations()
        print(manager.generate_progress_report())


if __name__ == "__main__":
    main()
