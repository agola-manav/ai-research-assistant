# AI Research Assistant

An AI-powered research assistant that can search the web, synthesize findings, and generate a structured Markdown report. Built as a portfolio project to demonstrate LLM integration, tool calling, retrieval from web search results, streaming responses, and a lightweight UI.

## Features

- **Research workflow:** accepts a natural-language question and produces a structured report.
- **LLM tool calling:** uses the OpenAI Responses API to decide when web search is useful.
- **Web search:** uses Tavily through a `web_search` tool.
- **Tool transparency:** displays status messages when the agent invokes a tool.
- **Streaming report:** streams report text into the Streamlit interface as it is generated.
- **Source-aware reporting:** passes search results and URLs to the report writer.
- **Export:** copy the Markdown report or download it as a `.md` file.
- **Session-specific history:** keeps the conversation history separate for each Streamlit session.
- **Configurable setup:** API keys are loaded from environment variables.

## Demo

The app flow:

1. Enter a research question.
2. The agent decides whether to call `web_search`.
3. Tavily results are returned to the agent.
4. The report service creates a structured Markdown report.
5. The report streams to the browser and can be copied or downloaded.

## Tech stack

- Python
- OpenAI Responses API (`gpt-4.1-mini`)
- Tavily Search API
- Streamlit
- `python-dotenv`

## Project structure

```text
ai-research-assistant/
├── app.py                     # Streamlit interface
├── agent.py                   # Agent loop and tool execution
├── requirements.txt           # Python dependencies
├── .env.example               # Environment variable template
├── .gitignore                 # Excludes secrets and local files
├── services/
│   ├── __init__.py
│   └── report_service.py      # Streaming Markdown report generation
└── tools/
    └── web_search.py          # Tavily web search integration
```

## Requirements

- Python 3.10 or newer
- An OpenAI API key
- A Tavily API key
- Internet access

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/ai-research-assistant.git
cd ai-research-assistant
```

Replace `YOUR_USERNAME` with your GitHub username and use the repository URL you create.

### 2. Create and activate a virtual environment

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows PowerShell**

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure API keys

Copy `.env.example` to `.env`.

**macOS / Linux**

```bash
cp .env.example .env
```

**Windows PowerShell**

```powershell
Copy-Item .env.example .env
```

Open `.env` and replace the placeholders with your own API keys:

```env
OPENAI_API_KEY=your_openai_api_key
TAVILY_API_KEY=your_tavily_api_key
```

Never commit `.env` or publish API keys in screenshots, logs, or source code.

### 5. Run the application

```bash
streamlit run app.py
```

Open the local URL printed by Streamlit (usually `http://localhost:8501`).

## Example questions

- Research the benefits and risks of AI agents for small businesses.
- Compare popular Python frameworks for building REST APIs.
- Research practical applications of generative AI in education.
- Summarize current trends in retrieval-augmented generation (RAG).

## How it works

```text
User question
     |
     v
OpenAI Responses API
     |
     +---- decides to use web_search? ----+
     |                                   |
     | no                                v yes
     |                              Tavily Search
     |                                   |
     |                         Search results + URLs
     |                                   |
     +---------------<-------------------+
                     |
                     v
              Research findings
                     |
                     v
             Report generation
               (streaming)
                     |
                     v
         Markdown report in Streamlit
             /              \
        Copy report      Download .md
```

## Security and limitations

- API keys must be stored in `.env`, which is excluded by `.gitignore`.
- This is a portfolio/demo application, not a production multi-user service.
- Conversation history is stored in Streamlit session memory and is not a persistent database.
- The report writer receives search results and source URLs, but the project does not independently verify every claim against each source.
- Search quality depends on Tavily results and the question asked.
- API usage may incur charges according to the providers' pricing and account limits.
- Do not use the generated report as a substitute for professional advice in high-stakes areas.

## Troubleshooting

### Missing API key

Check that `.env` exists in the project root and contains both `OPENAI_API_KEY` and `TAVILY_API_KEY`. Restart Streamlit after changing environment variables.

### Import errors

Activate your virtual environment and run:

```bash
pip install -r requirements.txt
```

Run `streamlit run app.py` from the project root so Python can resolve `tools` and `services`.

### Search returns no results

Check the Tavily key, network access, and the search query. A search result may be empty even when the integration is working.

## Roadmap

- Add unit tests for tool execution and source deduplication.
- Improve citation-to-claim validation.
- Add report history and persistent storage.
- Add configurable research depth and source limits.
- Add deployment configuration and CI checks.

## License

No license has been added yet. Add a license file if you want to explicitly permit reuse of this project.
