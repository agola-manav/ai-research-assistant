import os
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()

client = TavilyClient(
    api_key=os.getenv('TAVILY_API_KEY')
)


def web_search(question:str) -> list['dict']:
    """Search the web and return relevant results."""

    if not question or not question.strip():
        return [{"error": "A non-empty search query is required."}]

    try:
        response = client.search(
            query=question,
            max_results=5
        )

        search_data = []

        for result in response.get("results", []):
            item = {
                "title": result.get("title", ""),
                "content": result.get("content", ""),
                "url": result.get("url", "")
            }

            search_data.append(item)

        return search_data
    except Exception as e:
        return [{"error": str(e)}]