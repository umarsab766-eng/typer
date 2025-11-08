import uuid, os

# RUN OPTIONS
FAVICON = "⌨️"
APP_NAME = "Typer"
# HOST = '127.0.0.1'
# PORT = int(os.environ.get("PORT", 8080))
SECRET = str(uuid.uuid4().hex)

# THEME
THEME_DEFAULT = dict(
    primary = "#4ad328",
    secondary = "#2f26a6",
    accent = '#9c27b0',
    dark = '#1d1d1d',
    success = '#21ba45',
    error = '#c10015',
    info = '#31ccec',
    warning = '#f2c037',
    btn = "#3d8fdb"
)

DB_CREDS = dict(
    ENGINE = 'sqlite',
    NAME = "database.sqlite",
)

MIGRATIONS_FOLDER = "db.Migrations"
