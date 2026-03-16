#!/bin/bash

# Starte den Ollama-Dienst im Hintergrund
ollama serve &

# Warte, bis der Dienst erreichbar ist
echo "Warte auf Ollama..."
until curl -s http://localhost:11434 > /dev/null; do
  sleep 1
done

# Ziehe das Modell nur, wenn es noch nicht vorhanden ist
if ! ollama list | grep -q "^phi"; then
  echo "Lade Modell phi..."
  ollama pull phi
fi

# Starte den Flask-Server
echo "Starte API-Server..."
exec python3 ex_08_api_server.py
