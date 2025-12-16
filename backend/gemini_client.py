import os
from typing import List, Dict
import google.generativeai as genai
from dotenv import load_dotenv
from duckduckgo_search import DDGS

# Load environment variables
load_dotenv()


def perform_web_search(query: str, max_results: int = 5) -> List[Dict[str, str]]:
    """Perform a DuckDuckGo web search"""
    results = []

    try:
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=max_results):
                results.append({
                    "title": r.get("title", ""),
                    "href": r.get("href", ""),
                    "body": r.get("body", "")
                })
    except Exception as e:
        print("Search error:", e)

    return results


class GeminiClient:
    def __init__(self):
        try:
            genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
            self.model = genai.GenerativeModel("gemini-2.5-flash")
            self.chat = self.model.start_chat(history=[])
        except Exception as e:
            print("Gemini init error:", e)
            self.chat = None

    def generate_response(self, user_input: str) -> str:
        if not self.chat:
            return "Gemini service not available."

        try:
            lower = user_input.lower().strip()

            # Search trigger
            if lower.startswith("search:") or lower.startswith("/search"):
                query = user_input.split(" ", 1)[-1]
                results = perform_web_search(query)

                if not results:
                    return "No web results found."

                context = "\n\n".join(
                    f"[{i+1}] {r['title']} - {r['href']}\n{r['body']}"
                    for i, r in enumerate(results)
                )

                prompt = f"""
You are an AI study assistant.
Use the web results below to answer the question.
Cite sources like [1], [2].

Question:
{query}

Web Results:
{context}
"""
                response = self.chat.send_message(prompt)
                return response.text

            # Normal chat
            response = self.chat.send_message(user_input)
            return response.text

        except Exception as e:
            print("Response error:", e)
            return "Error generating response."
