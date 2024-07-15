# Delete all compiled Python files
clean:
	@echo "🧹 Cleaning up..."
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete
	@echo "✨ Clean up complete!"

# Run format with Ruff and djhtml
format:
	@echo "🔍 Formatting..."
	ruff check . --fix
	djhtml .
	@echo "✨ Format complete!"

# Run pre-commit
lint:
	@echo "🔍 Linting..."
	pre-commit run --all-files
	@echo "✨ Linting complete!"

# Check using Django's system-check
check:
	@echo "🔍 Running system checks..."
	python manage.py check
	python manage.py check --deploy
	python manage.py check --tag security
	@echo "✨ All checks done!"

# Update dependencies and pre-commit
update:
	@echo "🔄 Updating dependencies and pre-commit..."
	poetry update
	pre-commit autoupdate
	@echo "✨ Update complete!"

# Run tests
test:
	@echo "🧪 Running all tests..."
	python manage.py test
	@echo "✨ All tests complete!"

# Collect static files
collect:
	@echo "📦 Collecting static files..."
	python manage.py collectstatic
	@echo "✨ Static files collected!"

# Start development Docker compose
dev-start:
	@echo "🚀 Starting development Docker compose..."
	docker compose --profile development up
	@echo "✨ Development Docker compose started!"

# Stop development Docker compose
dev-stop:
	@echo "🛑 Stopping development Docker compose..."
	docker compose --profile development down
	@echo "✨ Local Docker compose stopped!"

# Watch development Docker compose logs
dev-logs:
	@echo "👀 Watching containers logs..."
	docker compose --profile development logs -f
	@echo "✨ Watching containers logs finished!"

# Setup project
setup:
	poetry install
	pre-commit install
	pre-commit run --all-files
	@echo "✨ Project setup complete!"

# Start development environment
dev:
	@make dev-stop
	@make dev-start
	@make dev-logs
