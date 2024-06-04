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

# Download v1.9.12 of htmx
download-htmx:
	@echo "📥 Downloading htmx scripts..."
	curl -sL https://unpkg.com/htmx.org@1.9.12/dist/htmx.js -o static/js/htmx.js
	curl -sL https://unpkg.com/htmx.org@1.9.12/dist/htmx.min.js -o static/js/htmx.min.js
	@echo "✨ htmx scripts downloaded and saved!"

# Download color picker
download-color-picker:
	@echo "📥 Downloading color picker script and styles..."
	curl -sL https://cdn.jsdelivr.net/gh/mdbassit/Coloris@latest/dist/coloris.min.js -o static/js/coloris.min.js
	curl -sL https://cdn.jsdelivr.net/gh/mdbassit/Coloris@latest/dist/coloris.min.css -o static/css/coloris.min.css
	@echo "✨ color picker related scripts and styles downloaded and saved!"

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
	docker compose -f ./dev.yaml --env-file ./.env up -d --build
	@echo "✨ Development Docker compose started!"

# Stop development Docker compose
dev-stop:
	@echo "🛑 Stopping development Docker compose..."
	docker compose -f dev.yaml down
	@echo "✨ Local Docker compose stopped!"

# Watch development Docker compose logs
dev-logs:
	@echo "👀 Watching containers logs..."
	docker compose -f dev.yaml logs -f
	@echo "✨ Watching containers logs finished!"

# Remove and restart development Docker compose
dev-restart:
	@make dev-stop
	@make dev-start

# Setup project
setup:
	@make download-htmx
	@make download-color-picker
	poetry install
	pre-commit install
	pre-commit run --all-files
	@echo "✨ Project setup complete!"

# Start development environment
dev:
	@make dev-restart
	@make dev-logs
