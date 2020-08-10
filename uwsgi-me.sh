#!/bin/bash
source venv/bin/activate
alembic upgrade head && uwsgi --http 0.0.0.0:5000 --master --module cebulany.app:app --processes 4
