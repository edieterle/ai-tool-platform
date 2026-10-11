import re
from mcp.server import MCPServer

mcp = MCPServer("ai-tool-platform")

@mcp.tool()
def health_check() -> dict:
    """Check if the AI tool platform is running."""
    return {"status": "ok"}

@mcp.tool()
def word_count(text: str) -> dict:
    """Count the number of words and the number of characters in text."""
    return {
        "words": len(text.split()),
        "characters": len(text),    
    }

@mcp.tool()
def extract_urls(text: str) -> dict:
    """Extract URLs from text, removing trailing punctuation."""
    pattern = r"https?://[^\s]+"
    matches = re.findall(pattern, text)
    urls = [url.rstrip(".,!?;:)]}") for url in matches]
    return {"urls": urls}


if __name__ == "__main__":
    mcp.run()
    