# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
.PHONY: help test lint format typecheck docs-serve docs-build

help:
	@echo "Targets:"
	@echo "  test         Run the test suite (pytest -v)."
	@echo "  lint         Lint with ruff (whole repo, docs/examples included)."
	@echo "  format       Format with ruff (whole repo, docs/examples included)."
	@echo "  typecheck    Type-check with mypy."
	@echo "  docs-serve   Serve the zensical docs site locally."
	@echo "  docs-build   Build the zensical docs site into site/."

test:
	pytest -v

lint:
	ruff check .

format:
	ruff format .

typecheck:
	mypy

docs-serve:
	zensical serve

docs-build:
	zensical build
