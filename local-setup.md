# Local Python Environment Setup

## Python Environment (IMPORTANT)

Each example, where applicable, includes environment setup for that example within it's own repository. Each of those includes everything you need to install an exact duplicate Python environment as used during the example creation.

### Installing Python Venvs

These packages are managed using the [uv](https://github.com/astral-sh/uv) package manager, and so we must install `uv` as a prerequisite for the course. We do so by following the [installation guide](https://docs.astral.sh/uv/#getting-started). For Mac users, as of 22 Oct 2024 enter the following in your terminal:

```
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Once `uv` is installed and available in your terminal you can navigate to your chosen chapter directory and execute:

```
cd example-chapter
uv python install 3.12.7
uv venv --python 3.12.7
uv sync
```

> ❗️ You may need to restart the terminal if the `uv` command is not recognized by your terminal.

With that we have our chapter venv installed. When working through the code for a specific chapter, always create a new venv to avoid dependency hell.

### Using Venv in VS Code / Cursor

To use our new venv in VS Code or Cursor we simply execute:

```
cd example-chapter
cursor .  # run via Cursor
code .    # run via VS Code
```

This command will open a new code window, from here you open the relevant files (like Jupyter notebook files), click on the top-right **Select Environment**, click **Python Environments...**, and choose the top `.venv` environment provided.

### Uninstalling Venvs

Naturally, we might not want to keep all of these venvs clogging up the memory on our system, so after completing a chapter we recommend removing the venv with:

```
cd example-chapter
deactivate
rm -rf .venv -r
```

## Ollama

Many chapters use local LLMs via Ollama. To use Ollama you must go to [ollama.com](https://ollama.com/) and install Ollama for your respective OS (MacOS is recommended).

Whenever an LLM is used via Ollama you must:

1. Ensure Ollama is running by executing `ollama serve` in your terminal or running the Ollama application. Make sure to keep note of the port the server is running on, by default Ollama runs on `http://localhost:11434`

2. Download the LLM being used in your current chapter using `ollama pull`. For example, to download Llama 3.2 3B, we execute `ollama pull llama 3.2:3b` in our terminal.