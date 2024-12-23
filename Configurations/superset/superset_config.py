# Flask application settings
FLASK_APP = 'superset.app:create_app()'
APP_DIR = '/home/master/spark_env/lib/python3.11/site-packages/superset'

# Superset specific config
ROW_LIMIT = 10000  # Ajusté à la valeur la plus élevée entre les deux fichiers
SQLLAB_ASYNC_TIME_LIMIT_SEC = 3600

# Timeouts configuration
SQLLAB_TIMEOUT = 3600  # Timeout des requêtes (1 heure)
SQLLAB_HARD_TIMEOUT = 3660  # Timeout légèrement plus long
SUPERSET_WEBSERVER_TIMEOUT = 3600  # Timeout serveur web
QUERY_TIMEOUT = 3600  # Timeout des requêtes
SQLALCHEMY_QUERY_TIMEOUT = 3600  # Timeout SQLAlchemy
CACHE_DEFAULT_TIMEOUT = 60 * 60 * 24  # 24 heures
SQLLAB_DOCKER_TIMEOUT = 3600  # Timeout spécifique Docker

# Flask App Builder configuration
SECRET_KEY = 'TdBVVxe3H5dmoJHL2ftGFY1AhH6Nq/7F2oruFOWfFYQ9/UfSGKWXLtrT'
PREVENT_UNSAFE_DB_CONNECTIONS = False
# Flask-WTF flag for CSRF
WTF_CSRF_ENABLED = True
WTF_CSRF_EXEMPT_LIST = []
WTF_CSRF_TIME_LIMIT = 60 * 60 * 24 * 365  # 1 an

# Client-side override
OVERRIDE_TIMEOUT = True  # Désactiver le timeout côté client

# Debugging and extra options
FLASK_APP_EXTRA_OPTIONS = {'debug': True}

# Comments:
# - Les paramètres de timeout sont alignés à 3600 (1 heure), sauf si des valeurs spécifiques sont justifiées.
# - ROW_LIMIT est défini à 10000 pour permettre plus de résultats, selon les besoins du second fichier.


