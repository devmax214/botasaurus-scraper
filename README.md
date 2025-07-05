# Django Web Scraper

A Django-based web scraping application that provides API endpoints for scraping web content.

## Features

- RESTful API for web scraping operations
- Error logging with screenshots and HTML captures
- JSON output storage for scraped data
- Django admin interface for management
- Configurable scraping parameters

## Project Structure

```
scraper/
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── db.sqlite3              # SQLite database
├── scraper/                # Django project settings
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── scraping_api/           # Django app for scraping functionality
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   └── tests.py
├── output/                 # Scraped data output (gitignored)
│   ├── scrape.json
│   ├── scrape_hotes.json
│   ├── scrape_html.json
│   ├── scrape_title.json
│   └── scrape_heading_task.json
└── error_logs/            # Error logs with screenshots (gitignored)
    └── [timestamp]/
        ├── error.log
        ├── page.html
        └── screenshot.png
```

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd scraper
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

## Usage

### Starting the Development Server

```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

### API Endpoints

The application provides RESTful API endpoints for web scraping operations. Check the `scraping_api/views.py` file for available endpoints.

### Admin Interface

Access the Django admin interface at `http://127.0.0.1:8000/admin/` to manage the application.

## Configuration

### Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///db.sqlite3
```

### Settings

Key settings can be modified in `scraper/settings.py`:

- `DEBUG`: Enable/disable debug mode
- `ALLOWED_HOSTS`: Configure allowed hosts
- `DATABASES`: Database configuration
- `STATIC_URL`: Static files configuration

## Output and Logging

### Scraped Data

Scraped data is saved in JSON format in the `output/` directory:
- `scrape.json`: General scraping results
- `scrape_hotes.json`: Hotel-specific data
- `scrape_html.json`: HTML content
- `scrape_title.json`: Page titles
- `scrape_heading_task.json`: Heading extraction results

### Error Logging

When scraping errors occur, detailed logs are created in `error_logs/[timestamp]/`:
- `error.log`: Error details and stack traces
- `page.html`: HTML content at time of error
- `screenshot.png`: Screenshot of the page when error occurred

## Development

### Running Tests

```bash
python manage.py test
```

### Code Style

This project follows PEP 8 style guidelines. Consider using tools like:
- `black` for code formatting
- `flake8` for linting
- `isort` for import sorting

### Database Management

```bash
# Create new migration
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Reset database (development only)
python manage.py flush
```

## Dependencies

Key dependencies include:
- Django: Web framework
- SQLite: Database (can be changed to PostgreSQL/MySQL)
- Additional scraping libraries (see `requirements.txt`)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

[Add your license information here]

## Support

For issues and questions, please create an issue in the repository or contact the development team. 