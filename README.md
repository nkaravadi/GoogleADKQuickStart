# 🚀 Windows Setup Guide for Google Agent Development Kit 

> [!NOTE]
> For Mac: go to: [README_mac.md](README_mac.md)

This guide walks you through setting up Python, IntelliJ, and required tools on Windows for working with the Google Agent Development Kit (ADK).

---

## 1. Verify PATH

Keep this handy in case the PATH gets messed up:

```bat
echo %PATH%
```

## 2. Environment Variables
Add these entries to your User PATH.
⚠️ Order matters — these should be the first entries:

```bat
%USERPROFILE%\.pyenv\pyenv-win\bin
%USERPROFILE%\.pyenv\pyenv-win\shims
```

Other entries:
```bat
%LOCALAPPDATA%\Programs\Git\cmd
PYENV=%USERPROFILE%\.pyenv\pyenv-win
PYENV_ROOT=%USERPROFILE%\.pyenv\pyenv-win
PYENV_HOME=%USERPROFILE%\.pyenv\pyenv-win
```

## 3. Basic Tools & Python

### 3.1 Notepad++, Git
```bat
# Notepad++
winget install notepad++

# Git
winget install Git.Git

```

### 3.2 Python Installation

We're using a slightly older version to avoid issue with Google ADK with newer versions
Pyenv lets you pick and choose from multiple versions of python if you that capability

```bat
git clone "https://github.com/pyenv-win/pyenv-win.git" %USERPROFILE%\.pyenv

pyenv install 3.11.9
pyenv global 3.11.9
```

Verify
```bat
python --version
```
Output should be
```bat
Python 3.11.9
```

## 4. Intellij Idea CE
```bat
winget install JetBrains.IntelliJIDEA.Community
```
After installation:

- Open IntelliJ.
- Install the Python plugin

## 5. Project Setup with Virtual Environment

Virtual envs isolate your installed packages from other projects
Lets create one for the adk called adkenv

```bat
md %USERPROFILE%\google-adk-projects
cd %USERPROFILE%\google-adk-projects

# Create virtual environment
python -m venv adkenv
```

To use the environment you have to activate **everytime** in any new command prompt.
Intellij can be configured to use it for a project.

```bat
# Activate environment
adkenv\Scripts\activate
```

Check that the prompt looks like:
```bat
(adkenv) C:\Users\karav\google-adk-projects>
```

## 6. Install required packages

In adkenv's cope run this:

```bat
pip install --upgrade pip
pip install google-adk
pip install torch torchvision torchaudio
pip install litellm
```

## 7. Example Code
In intellij clone this repo to create a new project

```bat
https://github.com/nkaravadi/GoogleADKQuickStart
```

## 8. To run these sample you will need a .env file in each of the sub-projects

.env file has:
```properties

GOOGLE_GENAI_USE_VERTEXAI=0
GOOGLE_API_KEY=<API-KEY>
```

You can obtain your API key from:
👉 [Google AI Studio](https://aistudio.google.com/app/api-keys)