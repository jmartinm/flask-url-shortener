"""WSGI entrypoint used e.g by gunicorn."""

from .app import application

if __name__ == "__main__":
    application.run()
