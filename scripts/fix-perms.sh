#!/bin/bash
# Corrige permissões da pasta site do MkDocs

SITE_DIR="/opt/mkdocs/site"

echo "[$(date)] Corrigindo permissões do MkDocs em: $SITE_DIR" | tee -a /var/log/fix-perms.log

chown -R root:mkdocs "$SITE_DIR"
chmod -R g+w "$SITE_DIR"

