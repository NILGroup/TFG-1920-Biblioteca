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
mv * /home/tfg-biblio
cd /home/tfg-biblio

cp wskey.conf /home/tfg-biblio/Servidor/
chown -R tfg-biblio:tfg-biblio /home/tfg-biblio/Servidor
chmod -R 777 /home/tfg-biblio/Servidor

chown -R tfg-biblio:tfg-biblio /home/tfg-biblio/janetWeb
chmod -R 777 /home/tfg-biblio/janetWeb

echo "Ok"
echo "-----------------------------------"

#mv Jarvis/regex_featurizer.py /usr/local/lib/python$PYT/dist-packages/rasa_nlu/featurizers/regex_featurizer.py
chown -R tfg-biblio:tfg-biblio /home/tfg-biblio/Jarvis
chmod -R 777 /home/tfg-biblio/Jarvis

echo "-----------------------------------"
echo "Entrenando Jarvis, esta operación durará varios minutos..."
cd /home/tfg-biblio/Jarvis/
../janet_venv/bin/rasa train --config config/config.yml
echo "Ahora se puede hablar usando \"/home/tfg-biblio/janet_venv/bin/rasa shell --endpoints /home/tfg-biblio/Jarvis/config/endpoint.yml\""
echo "-----------------------------------"
echo "Instalación realizada con éxito!"
exit 0

