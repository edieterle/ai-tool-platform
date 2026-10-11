import re
from pathlib import Path
from mcp.server import MCPServer

mcp = MCPServer("ai-tool-platform")

ALLOWED_EXTENSIONS = [".txt", ".md", ".json", ".csv", ".py", ".log"]
MAX_FILE_SIZE = 1_000_000  # 1 MB


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


@mcp.tool()
def read_file(path: str) -> str:
    """Read a supported text file and return its contents."""
    file_path = Path(path).resolve()

    if file_path.suffix.lower() not in ALLOWED_EXTENSIONS:
        raise ValueError("Unsupported file type.")

    if not file_path.is_file():
        raise ValueError("File not found.")

    if file_path.stat().st_size > MAX_FILE_SIZE:
        raise ValueError("File is too large.")

    return file_path.read_text(encoding="utf-8")


if __name__ == "__main__":
    mcp.run()
    