"""Pytest fixtures for pepkio-credit-matrix-builder tests."""

from __future__ import annotations

import pytest


@pytest.fixture
def mock_manifest() -> dict:
    return {
        "schema_version": "1.0",
        "tool_id": "credit-matrix-builder",
        "title": "CREdiT Matrix Builder",
        "description": "Contributor Roles Taxonomy statement generator and audit matrix",
        "examples": [
            {
                "name": "generate_example",
                "input": {
                    "action": "generate",
                    "articleType": "empirical",
                    "authors": [
                        {"id": "author-1", "name": "Dr. Elena Vasquez", "corresponding": True},
                    ],
                    "assignments": {
                        "author-1": {"conceptualization": {"assigned": True, "degree": "lead"}},
                    },
                },
                "output": {"statement": "Conceptualization"},
            },
            {
                "name": "export_csv",
                "input": {
                    "action": "export",
                    "format": "csv",
                    "authors": [{"id": "author-1", "name": "Dr. Elena Vasquez"}],
                    "assignments": {"author-1": {"conceptualization": {"assigned": True}}},
                },
                "output": {"mime_type": "text/csv"},
            },
        ],
    }


@pytest.fixture
def mock_run_response() -> dict:
    return {
        "run_id": "run_credit123",
        "status": "completed",
        "result": {
            "statement": "Conceptualization: E.V.; Writing - original draft: E.V.",
            "authors": [{"id": "author-1", "name": "Dr. Elena Vasquez"}],
            "roleCounts": {"conceptualization": 1, "writing-original-draft": 1},
        },
        "error": None,
        "result_url": "https://tools.pepkio.com/api/tools/v1/runs/run_credit123",
        "permalink": "https://tools.pepkio.com/r/run_credit123",
    }
