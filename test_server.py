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
