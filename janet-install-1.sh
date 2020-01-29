#!/bin/bash

DIRECTORY=$(cd `dirname $0` && pwd)

set -e

echo "Programa de instalación de Janet."
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

echo -n "Seguro que quieres instalar Janet (y/n)? "
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
export DEBIAN_FRONTEND=noninteractive
echo "Actualizando apt..."
apt-get update >/dev/null

echo "Instalando Python 3..."

apt-get install -yq python3-dev python3-pip python3-venv >/dev/null


echo "Instalando Janet..."
mkdir /home/tfg-biblio
mv * /home/tfg-biblio
cd /home/tfg-biblio
python3 -m venv ./janet_venv

echo ""
echo "Se ha cambiado el directorio de trabajo y generado una máquina virtual para instalar los paquetes necesarios"
echo "Para seguir con la instalación cambie su directorio a /home/tfg-biblio/:"
echo ""
echo "  cd /home/tfg-biblio"
echo ""
echo "Para activar el entorno virtual:"
echo ""
echo "  source janet_venv/bin/activate"
echo ""
echo "Una vez activado, siga con la instalación con:"
echo ""
echo "  ./janet-install-2.sh"
echo ""
