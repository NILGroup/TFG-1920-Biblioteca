#!/bin/bash
DIRECTORY=$(cd `dirname $0` && pwd)

set -e

echo "Programa de actualización de Janet."
echo "-----------------------------------"

if ! [ $(id -u) = 0 ]; then
   echo "Este script solo puede ser ejecutado por un superusuario." >&2
   exit 1
fi

if [ $SUDO_USER ]; then
    real_user=$SUDO_USER
else
    real_user=$(whoami)
fi

echo -n "Seguro que quieres actualizar Janet (y/n)? "
read answer
if [ "$answer" != "${answer#[Nn]}" ] ;then
	exit 0
fi

echo "-----------------------------------"
echo "Comprobando integridad de ficheros"


if [ ! -d "Servidor" ] || [ ! -d "Jarvis" ] || [ ! -f "wskey.conf" ]; then
    echo "ERROR! No se localizan los ficheros de instalación." >&2
    exit 1
else
    echo "Ok"
fi

echo "-----------------------------------"
echo "Actualizando Janet..."
rm -R /home/tfg-biblio/janetWeb
rm -R /home/tfg-biblio/Jarvis
rm -R /home/tfg-biblio/Servidor
cp -r * /home/tfg-biblio

cp wskey.conf /home/tfg-biblio/Servidor/
chown -R tfg-biblio:tfg-biblio /home/tfg-biblio/Servidor
chmod -R 777 /home/tfg-biblio/Servidor

chown -R tfg-biblio:tfg-biblio /home/tfg-biblio/janetWeb
chmod -R 777 /home/tfg-biblio/janetWeb
echo "Ok"
echo "-----------------------------------"
echo "Instalando dependencias..."
cd /home/tfg-biblio
source janet_venv/bin/activate
janet_venv/bin/pip install -U pip
janet_venv/bin/pip install -r requirements.txt
janet_venv/bin/python3 -m spacy download es_core_news_md
janet_venv/bin/python3 -m spacy link es_core_news_md es > /dev/null

echo "Ok"
echo "-----------------------------------"
FILE=/etc/systemd/system/jarvis.service
if test -f "$FILE"; then
    echo "Eliminando servicio de Jarvis deprecado..."
    systemctl stop jarvis.service
    rm /etc/systemd/system/jarvis.service
    echo "Ok"
    echo "-----------------------------------"
fi

echo "Reiniciando los servicios..."
systemctl restart janet.service
systemctl restart jarvisactions.service
systemctl restart janetweb.service
echo "Ok"
echo "-----------------------------------"

chown -R tfg-biblio:tfg-biblio /home/tfg-biblio/Jarvis
chmod -R 777 /home/tfg-biblio/Jarvis

echo "Instalación realizada con éxito!"
exit 0
