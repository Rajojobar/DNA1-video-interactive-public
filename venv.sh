#!/usr/bin/env bash
VENV_DIR="venv"

if ! command -v python3 &> /dev/null; then
    echo "Erreur : Python3 n'est pas installé." >&2
    exit 1
fi

# Crée le venv s'il n'existe pas déjà
if [ ! -d "$VENV_DIR" ]; then
    echo "Création de venv..."
    python3 -m venv "$VENV_DIR"
else
    echo "venv déjà présent."
fi

# Active le venv
echo "Activation venv..."
# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"

# Confirme l'activation
echo "venv activé : $(which python)"
