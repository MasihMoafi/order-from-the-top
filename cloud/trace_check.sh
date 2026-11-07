#!/usr/bin/env bash
# Read-only: what traces of today's session remain on hetzner-pc (Masih asked to check).
ssh -o BatchMode=yes hetzner-pc bash -s <<'REMOTE'
echo "== sshd logins today (journal)"; journalctl -u ssh -u sshd --since today --no-pager 2>/dev/null | grep -c 'Accepted publickey'
journalctl -u ssh -u sshd --since today --no-pager 2>/dev/null | grep 'Accepted publickey' | tail -8
echo "== auth.log lines today"; grep -c "$(date '+%b %e')" /var/log/auth.log 2>/dev/null || echo "no auth.log"
echo "== shell history mentions"; grep -n -E 'ff-code|adaption|ff/\.venv|pytest' ~/.bash_history 2>/dev/null | tail -5 || true; echo "(end)"
echo "== audit / accounting"; systemctl is-active auditd 2>/dev/null; ls /var/log/audit 2>/dev/null | head -2; ls /var/log/account 2>/dev/null | head -2; echo "(end)"
echo "== files changed in /root, /tmp today"; find /root /tmp -maxdepth 2 -newermt "$(date +%F)" 2>/dev/null | head -20
echo "== pip cache"; ls -d ~/.cache/pip 2>/dev/null && find ~/.cache/pip -newermt "$(date +%F)" | head -3; echo "(end)"
echo "== lastlog root"; last -n 5 root 2>/dev/null | head -6
REMOTE
