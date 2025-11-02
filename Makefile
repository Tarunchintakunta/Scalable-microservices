.PHONY: help initdb migrate seed clean test

help:
	@echo "E-Commerce MVP - Makefile Commands"
	@echo "===================================="
	@echo "make initdb    - Create PostgreSQL databases"
	@echo "make migrate   - Run Alembic migrations for all services"
	@echo "make seed      - Seed demo data for all services"
	@echo "make clean     - Clean up databases and virtual environments"
	@echo "make test      - Run all tests"
	@echo "make dev       - Start all services (requires tmux or run manually)"

initdb:
	@echo "Creating PostgreSQL databases..."
	-createdb ecom_identity_commerce
	-createdb ecom_catalog_fulfillment
	@echo "Databases created successfully!"

migrate:
	@echo "Running migrations for Service A..."
	cd services/service-a-identity-commerce && \
		. .venv/bin/activate && \
		alembic upgrade head
	@echo "Running migrations for Service B..."
	cd services/service-b-catalog-fulfillment && \
		. .venv/bin/activate && \
		alembic upgrade head
	@echo "Migrations completed!"

seed:
	@echo "Seeding Service A..."
	cd services/service-a-identity-commerce && \
		. .venv/bin/activate && \
		python scripts/seed.py
	@echo "Seeding Service B..."
	cd services/service-b-catalog-fulfillment && \
		. .venv/bin/activate && \
		python scripts/seed.py
	@echo "Seed data loaded!"

clean:
	@echo "Cleaning up..."
	-dropdb ecom_identity_commerce
	-dropdb ecom_catalog_fulfillment
	rm -rf services/service-a-identity-commerce/.venv
	rm -rf services/service-b-catalog-fulfillment/.venv
	rm -rf services/service-c-notifications-serverless/.venv
	@echo "Cleanup completed!"

test:
	@echo "Running Service A tests..."
	cd services/service-a-identity-commerce && \
		. .venv/bin/activate && \
		pytest
	@echo "Running Service B tests..."
	cd services/service-b-catalog-fulfillment && \
		. .venv/bin/activate && \
		pytest
	@echo "Running Frontend tests..."
	cd frontend && npm test
	@echo "All tests completed!"
