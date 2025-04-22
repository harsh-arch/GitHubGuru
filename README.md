# GitHub Guru: One-Click GitHub Project Setup Assistant

**GitHub Guru** is a powerful tool designed to automate the process of setting up any GitHub project with just a few clicks. It simplifies cloning a GitHub repository, installing dependencies, and running the project—all with minimal user interaction. This tool automatically detects and installs project dependencies, handles virtual environments, and cleans up unnecessary files.

## Features
- **One-click GitHub project setup**: Simply provide the GitHub repository URL and let GitHub Guru do the rest!
- **Automatic dependency installation**: The tool checks for common project files like `Pipfile`, `setup.py`, and `pyproject.toml` to install dependencies.
- **Runs the project**: Automatically finds and runs the main entry point of the project (e.g., `main.py` or `app.py`).
- **Cleans up after setup**: Removes the `.git` directory and unnecessary files to keep the project clean.
- **Supports Multiple Project Types**: It supports various Python projects like Flask, Django, and general Python scripts.

## Installation

### Requirements:
- **Python 3.x**: GitHub Guru is built with Python and works on any system that supports Python.
- **Git**: Required to clone GitHub repositories.
- **pipenv** (optional): Used for managing dependencies if a `Pipfile` is found.

### Steps to Set Up:
1. **Clone the repository**:
   - Clone this repository to your local machine using Git:
     ```bash
     git clone https://github.com/harsh-arch/github-guru.git
     cd github-guru
     ```

2. **Install dependencies** (if necessary):
   - Ensure that Python and pip are installed on your system. If `pipenv` is required (for Pipfile-based projects), install it via:
     ```bash
     pip install pipenv
     ```

## How to Use GitHub Guru

1. **Run the setup script**:
   - Open your terminal or command prompt and run the setup script:
     ```bash
     python github_guru.py
     ```

2. **Provide the GitHub Repository URL**:
   - When prompted, enter the GitHub repository URL for the project you want to set up. The script will automatically clone the repository to your system.

3. **Select the project directory**:
   - You will be asked to choose a local directory where the project will be cloned. The tool will clone the repository into this directory.

4. **Automatic setup**:
   - GitHub Guru will:
     - Clone the repository.
     - Detect and install dependencies automatically based on `Pipfile`, `setup.py`, or `pyproject.toml`.
     - Look for a main entry point (such as `main.py` or `app.py`) and run it.

5. **Cleanup**:
   - After running the project, GitHub Guru will automatically clean up any unnecessary files, such as the `.git` directory, to leave your project clean and ready for use.

## Example Output

```bash
===============================================
  Welcome to GitHub Guru! The One-Click GitHub Project Setup Assistant
  This tool will guide you to clone, set up, and run any GitHub project effortlessly!
===============================================

Enter the GitHub repository URL: https://github.com/harsh-arch/sample-python-project
Please select a folder to clone the project into: /Users/username/Projects/

Cloning the repository from: https://github.com/harsh-arch/sample-python-project
Repository cloned into: /Users/username/Projects/sample-python-project

Looking for dependency files...
Pipfile detected! Installing dependencies with pipenv...
Dependencies installed using pipenv.

Running the project using main.py...
Project ran successfully!

Cleaning up...
Git directory removed to clean up the project.
Cleanup completed!
```
## Important Notes

- **Virtual Environment**: If a `Pipfile` is detected, dependencies will be installed using `pipenv` to create a virtual environment. Otherwise, the script will attempt to use the global Python environment for installation.

- **Supported Project Types**: The script supports detecting and running Python projects such as:
  - Django projects (detected via `manage.py`).
  - Flask projects (detected via `app.py`).
  - General Python scripts (detected via `main.py` or `app.py`).

- **No Dependency File?**: If no dependency file is found, the tool will inform the user that dependencies need to be installed manually.

- **Cleanup**: The `.git` directory will be removed automatically after the setup to avoid cluttering your project folder.

## Known Issues

- **Permission Issues**: On certain systems, you might run into permission errors when trying to clone the repository or install dependencies. Ensure you have the necessary permissions or try running the script as an administrator.

- **Dependency Installation Failures**: If a specific dependency manager (e.g., `pipenv` or `setup.py`) fails to install, you can manually install the dependencies using the corresponding package manager.

## Contributing

Contributions are welcome! Feel free to fork this project and submit pull requests for improvements or new features. Here are a few ways you can contribute:
- Improve error handling and edge case detection.
- Add support for additional project types (e.g., Node.js, Java, etc.).
- Improve the user interface and experience.
- Add more detailed logging for debugging.
---

Made with ❤️ by Harsh-Arch 
