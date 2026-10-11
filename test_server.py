import json
import pytest
from mcp import Client

from server import mcp

@pytest.mark.anyio
async def test_health_check():
    async with Client(mcp) as client:
        result = await client.call_tool("health_check", {})
        assert not result.is_error
        response = json.loads(result.content[0].text)
        assert response == {"status": "ok"}

@pytest.mark.anyio
async def test_word_count():
    async with Client(mcp) as client:
        result = await client.call_tool("word_count", {"text": "hello, world!"})
        assert not result.is_error
        response = json.loads(result.content[0].text)
        assert response == {
            "words": 2,
            "characters": 13,
        }

@pytest.mark.anyio
async def extract_urls_multiple_urls_with_punctuation():
    async with Client(mcp) as client:
        result = await client.call_tool(
            "extract_urls", 
            {
                "text": 
                "Visit https://test.org, then http://example.com."
            },
        )
        assert not result.is_error
        response = json.loads(result.content[0].text)
        assert response == {
            "urls": [
                "https://test.org",
                "http://example.com",
            ]
        }

@pytest.mark.anyio
async def extract_urls_returns_empty_list_when_no_urls():
    async with Client(mcp) as client:
        result = await client.call_tool(
            "extract_urls", 
            {
                "text": "This text has no URLs."
            }
        )
        assert not result.is_error
        response = json.loads(result.content[0].text)
        assert response == {"urls": []}
