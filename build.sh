#!/usr/bin/env bash
# Script de build usado pelo Render (Build Command: bash build.sh)
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate
python manage.py popular_banco

# Cria o superusuário a partir das variáveis DJANGO_SUPERUSER_USERNAME,
# DJANGO_SUPERUSER_EMAIL e DJANGO_SUPERUSER_PASSWORD (se estiverem definidas).
if [ -n "$DJANGO_SUPERUSER_USERNAME" ]; then
  python manage.py createsuperuser --no-input || true
fi
