from .settings import *
DEBUG = True
#Crie secret key para seu ambiente de desenvolvimento
SECRET_KEY='ixb62ha#ts=ab4t2u%p1_62-!5w2j==j6d^3-j$!z(@*m+-h'
ALLOWED_HOSTS = ['*']
DATABASES={
    'default':  {
    'ENGINE':'django.db.backends.sqlite3',
    'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

CSRF_TRUSTED_ORIGINS = [
    'http://localhost:8000',
    'https://localhost:8000',
    'http://127.0.0.1:8000',
    'https://*.github.dev',
    'https://*.app.github.dev',
]