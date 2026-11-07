#!/usr/bin/env bash
# Undo what I put on hetzner-pc (not our server): the key, the code folder and the archive.
set -u
ssh -o BatchMode=yes hetzner-pc bash -s <<'REMOTE'
d="$HOME/.config/adaption"
[ -f "$d/api_key" ] && shred -u "$d/api_key"
rmdir "$d" 2>/dev/null
rmdir "$HOME/.config" 2>/dev/null
[ -d "$HOME/ff" ] && find "$HOME/ff" -depth -delete
[ -f "$HOME/ff-code.tgz" ] && unlink "$HOME/ff-code.tgz"
echo "left: $(ls -d "$HOME/.config" "$HOME/ff" "$HOME/ff-code.tgz" 2>/dev/null | tr '\n' ' ')(empty means all gone)"
REMOTE
