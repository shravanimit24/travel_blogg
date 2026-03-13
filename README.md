# Travel Blog Application

A comprehensive travel blog application built with Flask, featuring both database-oriented and service-oriented architecture.

## Features

- **Travel Blog Posts**: Create, read, update, and delete travel blog posts
- **Travel Itineraries**: Generate and customize travel itineraries with day-wise activities
- **REST API**: Full REST API endpoints for programmatic access
- **Database Migrations**: Proper database versioning with Flask-Migrate
- **Modular Architecture**: Service-oriented design with separate layers

## Architecture

### Database-Oriented Design
- **Models** (`models.py`): SQLAlchemy models with relationships and serialization methods
- **Database Migrations**: Version-controlled database schema changes
- **Configuration Management**: Environment-based configuration (`config.py`)

### Service-Oriented Architecture
- **Services** (`services/`): Business logic layer with PostService and ItineraryService
- **Routes/Blueprints** (`routes/`): Organized routing with separate blueprints for different features
- **API Endpoints**: RESTful API for all operations
- **Error Handling**: Proper error responses and validation

## Project Structure

```
travel_blogg/
├── app.py                 # Main application factory
├── models.py             # Database models
├── config.py             # Configuration management
├── requirements.txt      # Python dependencies
├── Procfile              # For deployment
├── instance/             # Instance-specific files
├── services/             # Business logic services
│   ├── post_service.py
│   └── itinerary_service.py
├── routes/               # Route blueprints
│   ├── posts_blueprint.py
│   └── itineraries_blueprint.py
└── templates/            # Jinja2 templates
    ├── index.html
    └── itinerary.html
```

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd travel_blogg
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variables** (optional)
   ```bash
   export SECRET_KEY=your-secret-key
   export DATABASE_URL=sqlite:///travel_blog.db
   export GOOGLE_MAPS_API_KEY=your-maps-api-key
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

## Database Setup

The application uses SQLite by default. For production, configure a different database URL.

### Initialize Database
```bash
flask db init
flask db migrate
flask db upgrade
```

## API Endpoints

### Posts
- `GET /api/posts` - Get all posts
- `POST /api/posts` - Create a new post
- `GET /api/posts/<id>` - Get a specific post
- `PUT /api/posts/<id>` - Update a post
- `DELETE /api/posts/<id>` - Delete a post

### Itineraries
- `GET /api/itineraries` - Get all itineraries
- `POST /api/itineraries` - Create a new itinerary
- `GET /api/itineraries/<id>` - Get a specific itinerary
- `PUT /api/itineraries/<id>` - Update itinerary days
- `DELETE /api/itineraries/<id>` - Delete an itinerary

## Usage

1. **Web Interface**: Visit `http://localhost:5000` to use the web application
2. **Add Posts**: Use the form to create travel blog posts
3. **Generate Itineraries**: Create customized travel itineraries
4. **API Access**: Use the REST API endpoints for programmatic access

## Development

### Adding New Features
1. Create service methods in the appropriate service class
2. Add routes in the corresponding blueprint
3. Update templates if needed
4. Add API endpoints following REST conventions

### Database Changes
1. Modify models in `models.py`
2. Create migration: `flask db migrate -m "description"`
3. Apply migration: `flask db upgrade`

## Deployment

The application includes a `Procfile` for deployment platforms like Heroku.

### Environment Variables
- `SECRET_KEY`: Flask secret key
- `DATABASE_URL`: Database connection string
- `GOOGLE_MAPS_API_KEY`: Google Maps API key
- `PAYMENT_LINK`: Payment/donation link

## Technologies Used

- **Flask**: Web framework
- **SQLAlchemy**: Database ORM
- **Flask-Migrate**: Database migrations
- **Jinja2**: Template engine
- **SQLite**: Database (configurable)

## Contributing

1. Follow the modular architecture
2. Add tests for new features
3. Update documentation
4. Use meaningful commit messages