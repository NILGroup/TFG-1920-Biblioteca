#!/bin/bash
sudo systemctl stop janet.service
cd /home/tfg-biblio/Servidor/
/home/tfg-biblio/janet_venv/bin/python3 JanetServMain.py
