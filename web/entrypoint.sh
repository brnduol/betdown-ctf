#!/bin/bash
set -e

ssh-keygen -A 2>/dev/null || true
/usr/sbin/sshd

cd /app
exec python app.py
