from mcp.server import MCPServer

mcp = MCPServer("ai-tool-platform")

@mcp.tool()
def health_check() -> dict:
    """Check whether the AI tool platform is running."""
    return {"status": "ok"}

@mcp.tool()
def word_count(text: str) -> dict:
    """Count the number of words and the number of characters in `text`."""
    return {
        "words": len(text.split()),
        "characters": len(text),    
    }

if __name__ == "__main__":
    mcp.run()
    