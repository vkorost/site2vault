# Development

## Setup

```bash
git clone https://github.com/vkorost/site2vault.git
cd site2vault
python -m venv .venv
.venv\Scripts\activate
pip install -e ".[dev]"
```

Optional JS rendering:

```bash
pip install -e ".[js]"
playwright install chromium
```

## Running tests

```bash
python -m pytest                      # All tests
python -m pytest -v                   # Verbose
python -m pytest tests/test_canonical.py
python -m pytest -k "manifest"        # Filter
```

## Building the standalone exe

```bash
pip install pyinstaller
python -m PyInstaller site2vault.spec --noconfirm
# Output: dist/site2vault.exe
```

See [architecture.md section 16.2](architecture.md) for why each hidden import is required.

## Releasing

1. Tag: `git tag vX.Y.Z`
2. Push tag: `git push --tags`
3. The release workflow builds the exe and attaches it to the GitHub Release with auto-generated notes from commits.
