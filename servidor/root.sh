#!/usr/bin/env bash
set -euo pipefail

LOCKDOWN_FILE="/var/lib/betdown/lockdown"

touch "$LOCKDOWN_FILE"
chown root:root "$LOCKDOWN_FILE"
chmod 644 "$LOCKDOWN_FILE"

clear

cat <<'EOF'
============================================================
                 BETDOWN - INCIDENT RESPONSE
============================================================

[CRITICAL] Acesso root detectado.
[CRITICAL] Serviços internos comprometidos.
[CRITICAL] Painel administrativo indisponível.
[CRITICAL] API de apostas encerrada.
[CRITICAL] Sistema de autenticação desligado.

Grande parte dos serviços web da BetDown foi derrubada durante
a invasão.

Apenas um endpoint de contingência permanece disponível.

Acesse a página final no endpoint:

    /final

============================================================
EOF