# 🚀 Mac Setup Guide for Google Agent Development Kit 

This guide walks you through setting up Python for working with the Google Agent Development Kit (ADK).
It assumes you have these installed:
- brew
- IntelliJ
  
---

## 1 Python Installation

We're using a slightly older version to avoid issue with Google ADK with newer versions
Pyenv lets you pick and choose from multiple versions of python if you that capability

```bash
brew install pyenv
```

Then add these to your shell's rc file (mine is .zshrc)
(I believe there is a better way to do this automatically from pyenv) 
```bash
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
```

Install the version of python we like
```bash
pyenv install 3.11.9
pyenv global 3.11.9
```
If you get an error like "python-build: tmpdir=/var/folders/zz/zyxvpxvq6csfxvn_n0000000000000/t is set to a non-accessible location" while running pyenv install command, edit ~/.zshrc and add the following line:
```bash
export TMPDIR="$HOME/tmp"
```

Launch new terminal and run pyenv install

Verify
```bash
python --version
```
Output should be
```bash
Python 3.11.9
```
## 2. Project Setup with Virtual Environment

Virtual envs isolate your installed packages from other projects
Lets create one for the adk called adkenv

In some folder for venvs
```bash

# Create virtual environment
python -m venv adkenv
```

To use the environment you have to activate **everytime** in any new command prompt.
Intellij can be configured to use it for a project.

```bash
# Activate environment
source ./adkenv/bin/activate
```

Check that the prompt looks like:
```bat
(adkenv) C:\Users\karav\google-adk-projects>
```

## 3. Install required packages

In adkenv's scope run this:

```bat
pip install --upgrade pip
pip install google-adk
pip install torch torchvision torchaudio
pip install litellm
```

## 4. Example Code
In intellij clone this repo to create a new project

```bat
https://github.com/nkaravadi/GoogleADKQuickStart
```

## 5. To run these sample you will need a .env file in each of the sub-projects

.env file has:
```properties

GOOGLE_GENAI_USE_VERTEXAI=0
GOOGLE_API_KEY=<API-KEY>
```

You can obtain your API key from:
👉 [Google AI Studio](https://aistudio.google.com/app/api-keys)


## 6. gcloud install
brew install google-cloud-sdk

gcloud auth login

gcloud config set project PROJECT_ID 


## 7. To create a project
In primetime

adk create <your_project>

```bash
(primetime) nkaravadi@Nagas-MacBook-Pro-2 primetime % adk create world_hello
Choose a model for the root agent:
1. gemini-2.5-flash
2. Other models (fill later)
Choose model (1, 2): 1
1. Google AI
2. Vertex AI
Choose a backend (1, 2): 2
```

## 8. Deploy

```bash
adk deploy agent_engine \
    --project=ccibt-hack25ww7-750 \
    --region=us-central1 \
    --staging_bucket gs://your-staging-bucket \
    world_hello
```

## 9. See it in gcloud

Look for "Agent Engine" in gcloud console search
Click playground and test
