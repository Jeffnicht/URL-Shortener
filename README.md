# URL Shortener

A lightweight URL shortening service built with Flask, Redis, and Nginx, fully containerized using Docker and Docker Compose.

Shortens long URLs, tracks compression stats, and exposes both a web interface and a JSON API.

## Features

* Shorten URLs via web form or JSON API
* Redirect shortened URLs to original URLs
* Track compression statistics (saved characters, ratio)
* Supports custom expiration for shortened URLs
* Runs behind Nginx reverse proxy with Gunicorn for production
* Containerized with Docker & Docker Compose for easy deployment

## Tech Stack

* **Backend:** Python 3.11, Flask, Gunicorn
* **Database:** Redis
* **Reverse Proxy:** Nginx
* **Containerization:** Docker & Docker Compose
* **Frontend:** HTML templates with inline CSS/JS

## Project Structure

```
project/
├── app/
│   ├── __init__.py       # Initializes the Flask app and configurations
│   ├── routes.py         # Defines all the routes for web and API
│   ├── redis_service.py  # Redis helper functions
│   ├── templates/
│   │   ├── index.html    # Main page template
│   │   └── error.html    # Error page template
├── Dockerfile            # Builds Flask/Gunicorn container
├── docker-compose.yml    # Orchestrates Flask, Redis, and Nginx
├── nginx.conf            # Nginx reverse proxy configuration
├── requirements.txt      # Python dependencies
└── README.md
```

## Installation

Clone the repo:

```bash
git clone https://github.com/Jeffnicht/URL-shortener.git
cd URL-shortener
```

Build and run the containers:

```bash
docker-compose up --build -d
```

* Flask app runs inside Docker with Gunicorn
* Redis runs as a service for storage
* Nginx reverse-proxies requests to Flask

Access the app:

```
http://<host>/
```

Example: `http://192.168.248.35/`

## API Usage

### Shorten a URL

**POST** `/api/shorten`

**Request JSON:**

```json
{
  "url": "https://www.example.com",
  "retain": "1H"  // optional, defaults to 1 hour if not specified
}
```

**Retention codes:**

* H = Hour
* D = Day
* W = Week
* Multiples allowed (e.g., `2H` for 2 hours)

**Response JSON:**

```json
{
  "shortened_url": "http://<host>/abc123",
  "short_code": "abc123",
  "original_url": "https://www.example.com",
  "retain": "1H",
  "saved_characters": 23,
  "compression_ratio_percent": 62.5
}
```

### Retrieve original URL

**GET** `/api/<short_code>`

**Response JSON:**

```json
{
  "short_code": "abc123",
  "original_url": "https://www.example.com"
}
```

## Local Development

Create a `.env` file (optional) with environment variables:

```
REDIS_URL=redis://redis:6379
FLASK_ENV=development
BASE_URL=http://localhost/
```

Run Flask locally without Docker (optional):

```bash
export FLASK_APP=app
flask run
```

## Notes

* Shortened URLs are generated dynamically using the host that accessed the service (`request.host_url`).
* For production, always access via Nginx using your host IP or domain to avoid `localhost` in URLs.
* Redis volumes are not persistent by default but can be made persistent by mapping volumes in `docker-compose.yml`. Example:

```yaml
volumes:
  redis-data:
services:
  redis:
    image: redis:latest
    volumes:
      - redis-data:/data
```

* Web form usage: Access the main page (`/`) to input a URL and receive a shortened link instantly.


**TODO**

* Could implement swagger-UI for API documentation (in my opinion overkill for such a small project).
* Add TLS certs 
