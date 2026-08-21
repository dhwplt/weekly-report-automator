import os
from pathlib import Path
from git import Repo, InvalidGitRepositoryError
import config
from core.system_mapper import map_system_name

def find_git_repos(parent_dirs: list[Path], max_depth: int = 2) -> list[Path]:
    """
    Recursively finds .git repositories up to max_depth levels.
    """
    repos = []
    for parent_dir in parent_dirs:
        if not parent_dir.exists() or not parent_dir.is_dir():
            continue
            
        start_level = str(parent_dir).count(os.sep)
        for root, dirs, files in os.walk(parent_dir):
            current_level = root.count(os.sep)
            if current_level - start_level > max_depth:
                del dirs[:] # Don't go deeper
                continue
                
            if '.git' in dirs:
                repos.append(Path(root))
                dirs.remove('.git') # don't traverse inside .git
    return repos

def collect_git_data() -> list[dict]:
    """
    Collects today's git commits and diffs across discovered repositories.
    """
    repos_paths = find_git_repos(config.PARENT_PROJECTS_DIRS)
    all_data = []
    
    for repo_path in repos_paths:
        try:
            repo = Repo(repo_path)
            # Find commits since midnight
            commits = list(repo.iter_commits(since='midnight'))
            if not commits:
                continue
                
            repo_data = {
                "system_name": map_system_name(str(repo_path)),
                "path": str(repo_path),
                "commits": []
            }
            
            for commit in commits:
                commit_info = {
                    "hash": commit.hexsha[:7],
                    "message": commit.message.strip(),
                    "author": commit.author.name,
                    "date": commit.committed_datetime.isoformat(),
                    "stats": commit.stats.total
                }
                repo_data["commits"].append(commit_info)
            
            # Check for test failures in root
            test_files = list(repo_path.glob("*.log"))
            failed_tests = [f.name for f in test_files if "fail" in f.name.lower() or "error" in f.name.lower()]
            if failed_tests:
                repo_data["test_flags"] = f"Found potential failure logs: {', '.join(failed_tests)}"
                
            all_data.append(repo_data)
        except InvalidGitRepositoryError:
            pass
        except Exception as e:
            print(f"Error processing {repo_path}: {e}")
            
    return all_data
