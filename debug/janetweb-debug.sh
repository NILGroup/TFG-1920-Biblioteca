#!/bin/bash
sudo systemctl stop janetweb.service
cd /home/tfg-biblio/janetWeb/
/home/tfg-biblio/janet_venv/bin/python3 run.py
