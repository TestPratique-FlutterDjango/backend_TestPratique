import os
from decouple import config

# Déterminer quel fichier de settings utiliser
ENVIRONMENT = config('ENVIRONMENT', default='development')

if ENVIRONMENT == 'production':
    from .production import *
else:
    from .development import *