"""Tests for vault namespacing (--namespace)."""

import json
from pathlib import Path

import pytest

from site2vault.config import RunConfig
from site2vault.orchestrator import (
    _write_namespaced_manifest,
    _update_namespace_index,
)


class TestWriteNamespacedManifest:
    def test_creates_manifest_in_namespace_dir(self, tmp_path):
        manifest = {
            "schema_version": 1,
            "seed_url": "https://docs.example.com",
            "notes": [{"file": "Page.md", "url": "https://docs.example.com/page"}],
        }
        config = RunConfig(seed_url="https://docs.example.com", out=tmp_path / "docs")

        _write_namespaced_manifest(tmp_path, "docs", config, manifest)

        manifest_path = tmp_path / ".site2vault" / "docs" / "manifest.json"
        assert manifest_path.exists()
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
        assert data["seed_url"] == "https://docs.example.com"
        assert len(data["notes"]) == 1

    def test_overwrites_existing_manifest(self, tmp_path):
        config = RunConfig(seed_url="https://example.com", out=tmp_path / "ns")
        old = {"schema_version": 1, "seed_url": "https://example.com", "notes": []}
        _write_namespaced_manifest(tmp_path, "ns", config, old)

        new = {"schema_version": 1, "seed_url": "https://example.com", "notes": [{"file": "A.md"}]}
        _write_namespaced_manifest(tmp_path, "ns", config, new)

        data = json.loads((tmp_path / ".site2vault" / "ns" / "manifest.json").read_text(encoding="utf-8"))
        assert len(data["notes"]) == 1


class TestUpdateNamespaceIndex:
    def test_creates_index_with_first_namespace(self, tmp_path):
        _update_namespace_index(tmp_path, "docs", "https://docs.example.com")

        index_path = tmp_path / ".site2vault" / "index.json"
        assert index_path.exists()
        data = json.loads(index_path.read_text(encoding="utf-8"))
        assert "docs" in data["namespaces"]
        assert data["namespaces"]["docs"]["seed_url"] == "https://docs.example.com"
        assert data["namespaces"]["docs"]["manifest"] == "docs/manifest.json"

    def test_adds_second_namespace(self, tmp_path):
        _update_namespace_index(tmp_path, "docs", "https://docs.example.com")
        _update_namespace_index(tmp_path, "blog", "https://blog.example.com")

        data = json.loads((tmp_path / ".site2vault" / "index.json").read_text(encoding="utf-8"))
        assert len(data["namespaces"]) == 2
        assert "docs" in data["namespaces"]
        assert "blog" in data["namespaces"]
        assert data["namespaces"]["blog"]["seed_url"] == "https://blog.example.com"

    def test_updates_existing_namespace(self, tmp_path):
        _update_namespace_index(tmp_path, "docs", "https://docs.example.com/v1")
        _update_namespace_index(tmp_path, "docs", "https://docs.example.com/v2")

        data = json.loads((tmp_path / ".site2vault" / "index.json").read_text(encoding="utf-8"))
        assert len(data["namespaces"]) == 1
        assert data["namespaces"]["docs"]["seed_url"] == "https://docs.example.com/v2"


class TestNamespaceOutputRedirect:
    @pytest.mark.asyncio
    async def test_namespace_redirects_output(self, tmp_path):
        """Namespace causes output dir to be redirected to subdirectory."""
        from site2vault.orchestrator import run

        out = tmp_path / "vault"
        out.mkdir()

        config = RunConfig(
            seed_url="https://example.com",
            out=out,
            namespace="docs",
            max_pages=0,
        )
        code = await run(config)
        assert code == 0

        # The namespace subdirectory should have been created
        assert (out / "docs").is_dir()
        # The state DB should be inside the namespace dir
        assert (out / "docs" / "log" / "site2vault.sqlite").exists()

    @pytest.mark.asyncio
    async def test_two_namespaces_coexist(self, tmp_path):
        """Two namespaces in the same vault don't conflict."""
        from site2vault.orchestrator import run

        out = tmp_path / "vault"
        out.mkdir()

        config1 = RunConfig(
            seed_url="https://docs.example.com",
            out=out,
            namespace="docs",
            max_pages=0,
            emit_manifest=False,
        )
        await run(config1)

        config2 = RunConfig(
            seed_url="https://blog.example.com",
            out=out,
            namespace="blog",
            max_pages=0,
            emit_manifest=False,
        )
        await run(config2)

        assert (out / "docs" / "log" / "site2vault.sqlite").exists()
        assert (out / "blog" / "log" / "site2vault.sqlite").exists()


class TestNamespaceCLI:
    def test_namespace_flag_sets_config(self):
        """The --namespace flag correctly populates RunConfig."""
        config = RunConfig(seed_url="https://example.com", namespace="my-ns")
        assert config.namespace == "my-ns"

    def test_namespace_none_by_default(self):
        config = RunConfig(seed_url="https://example.com")
        assert config.namespace is None
