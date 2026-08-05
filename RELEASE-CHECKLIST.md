# Release checklist

The repository can build and publish `forex-toolkit`, but publishing is an
owner action. Never create a release tag until every item below is complete.

## One-time PyPI setup

1. Confirm the name at <https://pypi.org/project/forex-toolkit/>. The official
   JSON endpoint returned HTTP 404 on 2026-08-05, so no public project currently
   uses it; availability is only final when PyPI accepts the first release.
2. Create the PyPI project/first release using the account that will own it.
3. In PyPI, open project **Publishing** and add a Trusted Publisher:
   owner `MukhammadAmir-Akbarov`, repository `forex-toolkit`, workflow
   `release.yml`; leave environment blank unless the workflow is updated to use one.
4. Keep 2FA and recovery codes configured. Do not add a PyPI API token to GitHub.

## Before every release

```bash
git status --short
.venv/bin/python -m pytest -q
.venv/bin/python -m build
.venv/bin/python -m twine check dist/*
```

Install the wheel in a fresh virtual environment and run `--help` for all eight
commands listed in `pyproject.toml`. Inspect wheel and sdist contents before tagging.

The tag must exactly match the version, for example version `0.1.0` uses tag
`v0.1.0`. The release workflow now rejects a mismatch before publishing.

## Owner action

Only after the checks and Trusted Publisher setup:

```bash
git tag -s v0.1.0 -m "forex-toolkit 0.1.0"
git push origin v0.1.0
```

That push publishes to PyPI and creates the GitHub Release. It is intentionally
not performed by routine project automation.
