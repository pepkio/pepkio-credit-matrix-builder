"""Unit tests for PepkioClient with mocked HTTP."""

from __future__ import annotations

import httpx
import pytest

from pepkio_credit_matrix_builder.client import PepkioClient
from pepkio_credit_matrix_builder.config import resolve_api_key, resolve_base_url
from pepkio_credit_matrix_builder.exceptions import PepkioAPIError


def test_resolve_base_url_default():
    assert resolve_base_url() == "https://tools.pepkio.com"
    assert resolve_base_url("https://tools.localtest.me/") == "https://tools.localtest.me"


def test_resolve_api_key(monkeypatch):
    monkeypatch.setenv("PEPKIO_API_KEY", "prod_key_123")
    monkeypatch.setenv("LOCAL_PEPKIO_API_KEY", "local_key_123")

    assert resolve_api_key(base_url="https://tools.pepkio.com") == "prod_key_123"
    assert resolve_api_key(base_url="https://tools.localtest.me") == "local_key_123"
    assert resolve_api_key("override_key") == "override_key"


def test_client_missing_api_key(monkeypatch):
    monkeypatch.delenv("PEPKIO_API_KEY", raising=False)
    monkeypatch.delenv("LOCAL_PEPKIO_API_KEY", raising=False)
    client = PepkioClient(api_key=None, base_url="https://tools.pepkio.com")
    with pytest.raises(ValueError, match="API key required"):
        client.run({"action": "generate"})


def test_get_manifest_success(mock_manifest):
    def handle_request(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/tools/v1/tools/credit-matrix-builder/manifest"
        return httpx.Response(200, json=mock_manifest)

    transport = httpx.MockTransport(handle_request)
    with PepkioClient(api_key="test_key", base_url="https://tools.pepkio.com") as client:
        client._http = httpx.Client(base_url=client.base_url, transport=transport)
        manifest = client.get_manifest()
        assert manifest["tool_id"] == "credit-matrix-builder"
        assert len(client.list_examples()) == 2
        assert "generate_example" in client.list_examples()

        ex_input = client.get_example_input("generate_example")
        assert ex_input["action"] == "generate"


def test_run_success(mock_run_response):
    def handle_request(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/tools/v1/tools/credit-matrix-builder/run"
        assert request.headers.get("Authorization") == "Bearer test_key"
        return httpx.Response(200, json=mock_run_response)

    transport = httpx.MockTransport(handle_request)
    with PepkioClient(api_key="test_key", base_url="https://tools.pepkio.com") as client:
        client._http = httpx.Client(
            base_url=client.base_url,
            headers={"Authorization": "Bearer test_key"},
            transport=transport,
        )
        result = client.run(
            {"action": "generate"},
            label="test-run",
        )
        assert result.status == "completed"
        assert result.run_id == "run_credit123"
        assert "statement" in result.result


def test_get_run_success(mock_run_response):
    def handle_request(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/tools/v1/runs/run_credit123"
        return httpx.Response(200, json=mock_run_response)

    transport = httpx.MockTransport(handle_request)
    with PepkioClient(api_key="test_key", base_url="https://tools.pepkio.com") as client:
        client._http = httpx.Client(
            base_url=client.base_url,
            headers={"Authorization": "Bearer test_key"},
            transport=transport,
        )
        result = client.get_run("run_credit123")
        assert result.status == "completed"
        assert result.run_id == "run_credit123"


def test_api_error_response():
    def handle_request(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            400,
            json={"error": {"message": "Invalid action", "code": "INVALID_INPUT"}},
        )

    transport = httpx.MockTransport(handle_request)
    with PepkioClient(api_key="test_key", base_url="https://tools.pepkio.com") as client:
        client._http = httpx.Client(
            base_url=client.base_url,
            headers={"Authorization": "Bearer test_key"},
            transport=transport,
        )
        with pytest.raises(PepkioAPIError) as exc_info:
            client.run({"action": "invalid_action"})
        assert exc_info.value.status_code == 400
        assert "Invalid action" in str(exc_info.value)
