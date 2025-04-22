import os
import subprocess
import sys
import shutil
import platform
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from tkinter.simpledialog import askstring
import logging
import git
from pathlib import Path
from dotenv import load_dotenv
import requests
from tqdm import tqdm

# Configure logging
logging.basicConfig(filename="setup_project.log", level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

ENTRY_POINTS = ['main.py', 'app.py', 'run.py', 'server.py']
DOCKERFILE_NAME = 'Dockerfile'
DOCKER_COMPOSE_FILE = 'docker-compose.yml'
GITHUB_ACTIONS_DIR = '.github/workflows'
LICENSE_FILE = 'LICENSE'
CONTRIBUTING_FILE = 'CONTRIBUTING.md'

# Constants for environment files
ENV_FILE_NAME = '.env'

def print_welcome_message():
    """Prints a beautiful welcome message to the user."""
    print("\n" + "="*50)
    print("  Welcome to the Advanced GitHub Project Setup Assistant!")
    print("  This tool will guide you to clone, set up, and run any GitHub project intelligently.")
    print("  Made by: Harsh-Arch")
    print("="*50)

def select_directory(message="Select a folder to clone the project into"):
    """Prompts the user to select a directory for project setup."""
    root = tk.Tk()
    root.withdraw()  # Hide the root Tkinter window
    target_dir = filedialog.askdirectory(title=message)
    
    if not target_dir:
        messagebox.showerror("Error", "No directory selected! Please try again.")
        return None
    
    return target_dir

def select_github_repository():
    """Prompts the user to input a GitHub repository URL via a GUI."""
    root = tk.Tk()
    root.withdraw()  # Hide the root Tkinter window
    
    repo_url = askstring("Enter GitHub Repository URL", "Please paste the repository URL here:")
    if not repo_url:
        messagebox.showerror("Error", "No repository URL entered! Please try again.")
        return None
    
    return repo_url

def github_authentication():
    """Optionally authenticate with GitHub for private repositories (using Personal Access Token)."""
    root = tk.Tk()
    root.withdraw()
    
    auth_token = askstring("GitHub Authentication", "Enter your GitHub personal access token (leave blank for public repos):")
    if auth_token:
        return auth_token
    return None

def clone_repo(github_url, target_dir, branch="main", auth_token=None):
    """Clones the GitHub repository into the target directory."""
    print(f"\nCloning the repository from: {github_url} (branch: {branch})")
    try:
        # Clone with authentication if needed
        if auth_token:
            clone_url = github_url.replace("https://", f"https://{auth_token}@")
        else:
            clone_url = github_url
        
        # Use gitpython for handling submodules and cloning with progress bar
        repo = git.Repo.clone_from(clone_url, target_dir, branch=branch, recursive=True)
        logging.info(f"Repository cloned into: {target_dir}")
        print(f"Repository cloned into: {target_dir}")
    except Exception as e:
        logging.error(f"Failed to clone repository. Error: {e}")
        print("\nError: Failed to clone the repository. Please check the GitHub URL.")
        return False
    return True

def create_virtualenv(target_dir):
    """Creates a virtual environment for the project."""
    print("\nCreating a virtual environment...")
    try:
        python_cmd = sys.executable
        env_path = os.path.join(target_dir, 'venv')
        subprocess.run([python_cmd, '-m', 'venv', env_path], check=True)
        logging.info(f"Virtual environment created at {env_path}")
        print("Virtual environment created successfully!")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to create virtual environment. Error: {e}")
        print("\nError: Failed to create a virtual environment.")
        return False
    except Exception as e:
        logging.error(f"Unexpected error occurred while creating virtual environment: {e}")
        print("\nError: Unexpected error occurred while creating the virtual environment.")
        return False
    return True

def install_dependencies(target_dir):
    """Installs the dependencies from requirements.txt or Pipfile if available."""
    requirements_file = os.path.join(target_dir, 'requirements.txt')
    pipfile = os.path.join(target_dir, 'Pipfile')

    if os.path.exists(requirements_file):
        print("\nInstalling dependencies from requirements.txt...")
        try:
            pip_cmd = [os.path.join(target_dir, 'venv', 'Scripts', 'pip') if platform.system() == 'Windows' else os.path.join(target_dir, 'venv', 'bin', 'pip'), 'install', '-r', 'requirements.txt']
            subprocess.run(pip_cmd, check=True)
            logging.info("Dependencies installed from requirements.txt.")
            print("Dependencies installed successfully!")
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to install dependencies. Error: {e}")
            print("\nError: Failed to install dependencies.")
            return False
    elif os.path.exists(pipfile):
        print("\nInstalling dependencies from Pipfile...")
        try:
            subprocess.run(["pipenv", "install"], check=True)
            logging.info("Dependencies installed from Pipfile.")
            print("Dependencies installed successfully!")
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to install dependencies from Pipfile. Error: {e}")
            print("\nError: Failed to install dependencies from Pipfile.")
            return False
    else:
        print("\nNo 'requirements.txt' or 'Pipfile' found. You may need to install dependencies manually.")
    return True

def find_project_type(target_dir):
    """Attempts to determine the type of project (e.g., Flask, Django, FastAPI, Jupyter)."""
    if os.path.exists(os.path.join(target_dir, 'manage.py')):
        return 'Django'
    elif os.path.exists(os.path.join(target_dir, 'app.py')):
        return 'Flask'
    elif os.path.exists(os.path.join(target_dir, 'main.py')) and "fastapi" in open(os.path.join(target_dir, 'main.py')).read():
        return 'FastAPI'
    elif os.path.exists(os.path.join(target_dir, 'notebooks')):
        return 'Jupyter Notebook'
    elif os.path.exists(os.path.join(target_dir, 'requirements.txt')) or os.path.exists(os.path.join(target_dir, 'Pipfile')):
        return 'Python Script'
    return 'Unknown'

def setup_django_project(target_dir):
    """Set up a Django project."""
    print("\nThis appears to be a Django project.")
    if not install_dependencies(target_dir):
        return False
    
    print("\nRunning migrations...")
    try:
        subprocess.run([os.path.join(target_dir, 'venv', 'Scripts', 'python') if platform.system() == 'Windows' else os.path.join(target_dir, 'venv', 'bin', 'python'), 'manage.py', 'migrate'], check=True)
        logging.info("Django migrations run successfully.")
        print("Django migrations completed successfully!")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to run migrations. Error: {e}")
        print("\nError: Failed to run Django migrations.")
        return False
    return True

def setup_flask_project(target_dir):
    """Set up a Flask project."""
    print("\nThis appears to be a Flask project.")
    if not install_dependencies(target_dir):
        return False
    
    print("\nSetting up Flask app...")
    return True

def setup_fastapi_project(target_dir):
    """Set up a FastAPI project."""
    print("\nThis appears to be a FastAPI project.")
    if not install_dependencies(target_dir):
        return False
    
    print("\nSetting up FastAPI app...")
    return True

def run_docker_project(target_dir):
    """If Dockerfile exists, build and run the Docker container."""
    dockerfile_path = os.path.join(target_dir, DOCKERFILE_NAME)
    if os.path.exists(dockerfile_path):
        print(f"\nDockerfile detected! Building and running the Docker container...")
        try:
            subprocess.run(['docker', 'build', '-t', 'project_image', target_dir], check=True)
            subprocess.run(['docker', 'run', '-d', '-p', '8000:8000', 'project_image'], check=True)
            logging.info(f"Docker container started successfully.")
            print("Docker container started successfully!")
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to build and run Docker container. Error: {e}")
            print("\nError: Failed to build and run Docker container.")
            return False
    else:
        print("\nNo Dockerfile found. Skipping Docker setup.")
    return True

def fetch_github_release_notes(github_url):
    """Fetch and display the latest release notes from the GitHub repository."""
    print("\nFetching the latest release notes...")
    api_url = github_url.replace("https://github.com", "https://api.github.com/repos") + "/releases/latest"
    response = requests.get(api_url)
    if response.status_code == 200:
        release_data = response.json()
        print("\nLatest Release: ", release_data['name'])
        print("Release Notes: ", release_data['body'])
    else:
        print("\nError: Could not fetch release notes.")

def setup_github_actions(target_dir):
    """Set up GitHub Actions if configuration files are found."""
    github_actions_dir = os.path.join(target_dir, GITHUB_ACTIONS_DIR)
    if os.path.exists(github_actions_dir):
        print("\nGitHub Actions configuration found! Setting up CI/CD...")
        # You can add more logic to set up or modify workflows as needed.
        return True
    return False

def cleanup(target_dir):
    """Cleans up temporary files like the .git directory."""
    print("\nCleaning up...")
    git_dir = os.path.join(target_dir, '.git')
    if os.path.exists(git_dir):
        try:
            shutil.rmtree(git_dir)
            logging.info("Removed .git directory.")
            print("Git directory removed to clean up the project.")
        except Exception as e:
            logging.error(f"Failed to remove .git directory. Error: {e}")
            print("\nError: Failed to remove .git directory.")
    print("Cleanup completed!")

def setup_project():
    """Guides the user through the entire project setup process."""
    github_url = select_github_repository()
    if not github_url:
        return
    
    target_dir = select_directory("Select a folder to clone the project into")
    if not target_dir:
        return
    
    # Authentication for private repositories
    auth_token = github_authentication()

    # Option to choose branch
    branch = simpledialog.askstring("Git Branch", "Enter the branch to clone (default is 'main'):", initialvalue="main")
    if not branch:
        branch = "main"

    if not clone_repo(github_url, target_dir, branch, auth_token):
        return
    
    if not create_virtualenv(target_dir):
        return
    
    project_type = find_project_type(target_dir)
    if project_type == 'Django':
        if not setup_django_project(target_dir):
            return
    elif project_type == 'Flask':
        if not setup_flask_project(target_dir):
            return
    elif project_type == 'FastAPI':
        if not setup_fastapi_project(target_dir):
            return
    elif project_type == 'Jupyter Notebook':
        print("\nThis appears to be a Jupyter Notebook project.")
    elif project_type == 'Python Script':
        print("\nThis appears to be a basic Python script project.")
    else:
        print("\nProject type unknown. You might need to configure it manually.")
    
    # Docker setup
    if not run_docker_project(target_dir):
        return
    
    # Check for GitHub Actions setup
    if not setup_github_actions(target_dir):
        print("\nNo GitHub Actions configuration found.")
    
    # Fetch release notes
    fetch_github_release_notes(github_url)
    
    # Cleanup
    cleanup(target_dir)

    print("\nProject setup completed successfully!")

# Run the setup
if __name__ == "__main__":
    print_welcome_message()
    setup_project()
