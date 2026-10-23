import glob
import os
import subprocess
import yaml

prefix="src"

def add_git_submodule(repo_name, repo_url, repo_version):
    subprocess.call(['git', 'submodule', 'add', '-b', repo_version, repo_url, repo_name])

def is_submodule(repo_name):
    try:
        subprocess.check_output(['git', 'submodule', 'status', repo_name], stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False 

def parse_repos_file(file_path):
    with open(file_path, 'r') as file:
        repos_data = yaml.safe_load(os.path.expandvars(file.read()))
        repositories = repos_data['repositories']
        
        for repo_name, repo_info in repositories.items():
            if 'type' in repo_info and repo_info['type'] == 'git':
                repo_url = repo_info['url']
                repo_version = repo_info['version']
                submodule_name = os.path.join(prefix, repo_name)

                if not is_submodule(submodule_name):
                    add_git_submodule(submodule_name, repo_url, repo_version)
                    print(f"Added {repo_name} as a submodule.")

# Find .repos files within the src directory
repos_files = glob.glob('src/**/*.repos', recursive=True)

# Process each .repos file
for repos_file in repos_files:
    parse_repos_file(repos_file)
