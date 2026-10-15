.PHONY: help install test backend-test frontend-build docker-up docker-down docker-logs tf-init tf-plan helm-lint load-test

help:
	@echo "FinPilot DevOps Capstone Commands:"
	@echo "  make install         Install backend and frontend dependencies"
	@echo "  make test            Run backend automated tests (pytest)"
	@echo "  make docker-up       Start local environment (frontend, backend, postgres)"
	@echo "  make docker-down     Stop and clean local Docker environment"
	@echo "  make docker-logs     Stream Docker Compose logs"
	@echo "  make helm-lint       Validate and lint FinPilot Helm chart"
	@echo "  make load-test       Execute HPA CPU stress test"

install:
	cd backend && pip install -r requirements.txt
	cd frontend && npm install

test: backend-test

backend-test:
	cd backend && pytest --tb=short -v --cov=app --cov-report=term-missing

frontend-build:
	cd frontend && npm run build

docker-up:
	docker compose up -d --build

docker-down:
	docker compose down -v

docker-logs:
	docker compose logs -f

helm-lint:
	helm lint ./helm/finpilot

load-test:
	python scripts/load_test.py http://localhost:8000/api/transactions 20 120
