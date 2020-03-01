#!/bin/bash
sudo systemctl stop jarvisactions.service
cd /home/tfg-biblio/Jarvis/
/home/tfg-biblio/janet_venv/bin/rasa run actions

