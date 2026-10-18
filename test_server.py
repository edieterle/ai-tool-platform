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
        result = await client.call_tool("word_count", {"text": "Hello, world!"})
        assert not result.is_error

        response = json.loads(result.content[0].text)
        assert response == {
            "words": 2,
            "characters": 13,
        }


@pytest.mark.anyio
async def test_extract_urls_multiple_urls_with_punctuation():
    async with Client(mcp) as client:
        result = await client.call_tool(
            "extract_urls",
            {"text": "Visit http://test.org, then https://example.com."},
        )
        assert not result.is_error

        response = json.loads(result.content[0].text)
        assert response == {
            "urls": [
                "http://test.org",
                "https://example.com",
            ]
        }


@pytest.mark.anyio
async def test_read_file_returns_file_contents(tmp_path):
    file = tmp_path / "test.txt"
    file.write_text("Hello, world!", encoding="utf-8")

    async with Client(mcp) as client:
        result = await client.call_tool("read_file", {"path": str(file)})
        assert not result.is_error

        response = json.loads(result.content[0].text)
        assert response == {
            "filename": "test.txt",
            "content": "Hello, world!",
        }


@pytest.mark.anyio
async def test_web_search_returns_results():
    async with Client(mcp) as client:
        result = await client.call_tool(
            "web_search",
            {
                "query": "Python MCP tutorial",
                "max_results": 2,
            },
        )
        assert not result.is_error

        response = json.loads(result.content[0].text)
        assert response["query"] == "Python MCP tutorial"
        assert isinstance(response["results"], list)
        for item in response["results"]:
            assert "title" in item
            assert "url" in item
            assert "snippet" in item


@pytest.mark.anyio
async def test_fetch_webpage_returns_content():
    async with Client(mcp) as client:
        result = await client.call_tool(
            "fetch_webpage",
            {"url": "https://example.com"},
        )
        assert not result.is_error

        response = json.loads(result.content[0].text)
        assert response["url"] == "https://example.com"
        assert response["title"] == "Example Domain"
        assert response["content"]


@pytest.mark.anyio
async def test_list_documents_returns_documents():
    async with Client(mcp) as client:
        result = await client.call_tool(
            "list_documents",
            {"limit": 20},
        )
        assert not result.is_error

        response = json.loads(result.content[0].text)
        assert "documents" in response
        assert isinstance(response["documents"], list)
