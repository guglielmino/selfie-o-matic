import os

# Indirizzo delle API
API_HOSTNAME = "admin.self-o-matic.com"
API_PORT = 80

# Storage delle immagini

LOCAL_IMAGE_PATTERN = os.environ.get("LOCAL_IMAGE_PATTERN", '/media/snapshot{0}.jpg')
PUBLISHED_FOLDER = os.environ.get("PUBLISHED_FOLDER", '/media/published')
