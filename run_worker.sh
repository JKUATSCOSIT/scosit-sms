#!/usr/bin/env bash
celery worker -A celery_worker.py --loglevel=info