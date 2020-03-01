#!/bin/bash
sudo systemctl stop jarvis.service
cd  /home/tfg-biblio/Jarvis/
/home/tfg-biblio/janet_venv/bin/rasa run --endpoints config/endpoint.yml --enable-api

