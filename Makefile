.PHONY: help install test lint typecheck build clean dev docs

help: ## Mostra esta ajuda
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Instala dependências de desenvolvimento
	uv pip install -e ".[all,dev]"

test: ## Roda testes
	uvx pytest -n auto --tb=short

test-unit: ## Roda testes unitários apenas
	uvx pytest tests/unit -n auto --tb=short

test-integration: ## Roda testes de integração
	uvx pytest tests/integration -n auto --tb=short

lint: ## Roda linter (ruff)
	uvx ruff check .
	uvx ruff format --check .

lint-fix: ## Corrige formatação automaticamente
	uvx ruff check --fix .
	uvx ruff format .

typecheck: ## Roda type checker (mypy)
	uvx mypy agent damon_cli gateway tools cron scripts --ignore-missing-imports

build: ## Build do pacote
	uv build

clean: ## Limpa arquivos de build
	rm -rf dist build *.egg-info .pytest_cache .mypy_cache .ruff_cache

dev: ## Ambiente de desenvolvimento
	uv pip install -e ".[all,dev]"
	mkdir -p ~/.damon/{cron,sessions,logs,memories,skills}
	cp -n cli-config.yaml.example ~/.damon/config.yaml || true

run: ## Roda Damon CLI
	./damon

run-gateway: ## Roda Gateway
	./damon gateway start

docs: ## Serve documentação local (mkdocs)
	uvx mkdocs serve

docker-build: ## Build da imagem Docker
	docker build -t damon-agent:latest .

docker-run: ## Roda container Damon
	docker run -it --rm -v ~/.damon:/home/damon/.damon damon-agent:latest

install-system: ## Instala system-wide (via pipx)
	pipx install -e .

uninstall: ## Desinstala
	pipx uninstall damon-agent
