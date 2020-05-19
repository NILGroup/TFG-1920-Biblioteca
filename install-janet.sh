#!/bin/bash

DIRECTORY=$(cd `dirname $0` && pwd)
INSTALL_PATH="/home/tfg-biblio"
USER="tfg-biblio"

usage="Usage: $(basename "$0") [-h] [-d] [-u]

Este script instala y actualizaJanet, el cliente web y sus dependencias

Donde:
    -h  muestra esta ayuda
    -d  selecciona el directorio base para la instalación
    -u  selecciona el usuario para el que se instala."

while getopts "hu:d:" opt; do
  case $opt in
    h) echo "$usage"
       exit
       ;;
    d) INSTALL_PATH="$OPTARG"
       ;;
    u) USER="$OPTARG"
       ;;
    \?) echo "$usage"
        exit
        ;;
  esac
done

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

set -e
if [ ! -d $INSTALL_PATH ] ; then
    mkdir $INSTALL_PATH
    if [ $? -ne 0 ] ; then
        echo "Fatal error: Could not create or access the install directory $INSTALL_PATH"
    fi
else
    if [ -d $INSTALL_PATH/Servidor ] && [ -d $INSTALL_PATH/janetWeb ] && [ -d $INSTALL_PATH/Jarvis ] && [ -d $INSTALL_PATH/janet_venv ] ; then
        echo "Instalación de Janet encontrada"
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
        rm -R $INSTALL_PATH/janetWeb
        rm -R $INSTALL_PATH/Jarvis
        rm -R $INSTALL_PATH/Servidor
        cp -r * $INSTALL_PATH

        cp wskey.conf $INSTALL_PATH/Servidor/
        chown -R $USER:$USER $INSTALL_PATH/Servidor
        chmod -R 777 $INSTALL_PATH/Servidor

        chown -R $USER:$USER $INSTALL_PATH/janetWeb
        chmod -R 777 $INSTALL_PATH/janetWeb
        echo "Ok"
        echo "-----------------------------------"
        echo "Instalando dependencias..."
        cd $INSTALL_PATH
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

        chown -R $USER:$USER $INSTALL_PATH/Jarvis
        chmod -R 777 $INSTALL_PATH/Jarvis

        echo "Actualización realizada con éxito!"
        exit 0
    fi
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
mv * $INSTALL_PATH
cd $INSTALL_PATH
CWD=$(pwd)

python3 -m venv ./janet_venv

source janet_venv/bin/activate

echo "Instalando Git..."

apt-get -yq install git-all >/dev/null

echo "Ok"
echo "-----------------------------------"
echo "Instalando MongoDB..."

if ! [ -x "$(command -v mongo)" ]; then
    apt-get -yq install dirmngr >/dev/null
    apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 9DA31620334BD75D9DCB49F368818C72E52529D4

    source /etc/os-release

    if [ $ID == 'debian' ]; then
        if [ $VERSION_ID == "9" ]; then
            echo "deb http://repo.mongodb.org/apt/debian stretch/mongodb-org/4.0 main" >  /etc/apt/sources.list.d/mongodb-org-4.0.list
        else
            echo "deb http://repo.mongodb.org/apt/debian jessie/mongodb-org/4.0 main" >  /etc/apt/sources.list.d/mongodb-org-4.0.list
        fi
    else
        if [ $VERSION_ID == "18.04" ]; then
            echo "deb http://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.0 multiverse" >  /etc/apt/sources.list.d/mongodb-org-4.0.list
        elif [ $VERSION_ID == "16.04" ]; then
            echo "deb http://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/4.0 multiverse" >  /etc/apt/sources.list.d/mongodb-org-4.0.list
        else
            echo "deb http://repo.mongodb.org/apt/ubuntu trusty/mongodb-org/4.0 multiverse" >  /etc/apt/sources.list.d/mongodb-org-4.0.list
        fi
    fi

    apt-get update >/dev/null
    apt-get install -yq mongodb-org >/dev/null

    printf "[Unit]\nDescription=High-performance, schema-free document-oriented database\nAfter=network.target\n\n[Service]\nUser=mongodb\n ExecStart=/usr/bin/mongod --quiet --config /etc/mongod.conf\n\n[Install]\nWantedBy=multi-user.target" > /etc/systemd/system/mongodb.service

    systemctl enable mongodb
    systemctl start mongodb
fi


echo "Ok"
echo "-----------------------------------"
echo "Creando grupo y usuario..."
if ! id $USER >/dev/null 2>&1; then
    useradd -m -s /sbin/nologin -U $USER
    echo "Ok"
else
    echo "El usuario $USER ya existe, continúo..."
fi

echo "-----------------------------------"

echo "Instalando Janet..."
mv wskey.conf $INSTALL_PATH/Servidor/
chown -R $USER:$USER $INSTALL_PATH/Servidor
chmod -R 777 $INSTALL_PATH/Servidor

echo "Ok"
echo "-----------------------------------"

echo "Instalando web..."
chown -R $USER:$USER $INSTALL_PATH/janetWeb
chmod -R 777 $INSTALL_PATH/janetWeb

echo "Ok"
echo "-----------------------------------"

echo "Instalando dependencias..."
janet_venv/bin/pip install -U pip
janet_venv/bin/pip install -r requirements.txt
janet_venv/bin/pip install git+https://github.com/OCLC-Developer-Network/oclc-auth-python
echo "Ok"
echo "-----------------------------------"
echo "Instalando Jarvis..."
PYT=$(python3 --version 2>&1 | grep -oP '([0-9]).([0-9])')

chown -R $USER:$USER $INSTALL_PATH/Jarvis
chmod -R 777 $INSTALL_PATH/Jarvis
echo "Descargando modelo del lenguaje..."
janet_venv/bin/python3 -m spacy download es_core_news_md
janet_venv/bin/python3 -m spacy link es_core_news_md es > /dev/null

echo "Ok"
echo "-----------------------------------"

echo "Preparando Base de datos..."
#TODO No crearlo si ya existe
mongo admin <<EOF
use admin
var user = {
    "user" : "rasa",
    "pwd" : "Pitonisa46",
    roles : [{
        "role" : "readWrite",
        "db" : "rasa"
    }]
}
db.createUser(user);
exit
EOF

mongoimport --db janet --collection localizaciones --file $INSTALL_PATH/Servidor/bibliotecas.json

mongo <<EOF
use janet
db.localizaciones.createIndex({kw: "text"});
exit
EOF

echo "Ok"
echo "-----------------------------------"
echo "Creando daemons..."

echo "[Unit]
Description=Bottled Janet Service
After=network.target

[Service]
Type=simple
User=$USER
Group=$USER
WorkingDirectory=$CWD/Servidor/
ExecStart=$CWD/janet_venv/bin/python3 JanetServMain.py

[Install]
WantedBy=multi-user.target" > /etc/systemd/system/janet.service

echo "[Unit]
Description=Jarvis Actions Service
After=network.target

[Service]
Type=simple
User=$USER
Group=$USER
WorkingDirectory=$CWD/Jarvis/
ExecStart=$CWD/janet_venv/bin/rasa run actions

[Install]
WantedBy=multi-user.target" > /etc/systemd/system/jarvisactions.service

echo "[Unit]
Description=Janet Web Service
After=network.target

[Service]
Type=simple
User=$USER
Group=$USER
WorkingDirectory=$CWD/janetWeb/
ExecStart=$CWD/janet_venv/bin/python3 run.py

[Install]
WantedBy=multi-user.target" > /etc/systemd/system/janetweb.service

systemctl enable janet.service
systemctl enable jarvisactions.service
systemctl enable janetweb.service

echo "Ok"
echo "-----------------------------------"
echo "Creando servicio del destructor imperial"
mycron=${TMPDIR:-/tmp}/xyz.$$
trap "rm -f $tmp; exit 1" 0 1 2 3 13 15
echo "*/15 * * * * $USER python3 $INSTALL_PATH/Servidor/DestructorImperial.py" >> $mycron
crontab -u $USER $mycron
rm -f $mycron

echo "-----------------------------------"
echo "Arrancando servicios"
systemctl start janet.service
systemctl start jarvisactions.service
systemctl start janetweb.service

echo "Web funcionando en el puerto 8081"
echo "Para hacer consultas dirigirse a la dirección 127.0.0.1:8081"
echo "-----------------------------------"

echo "Borrando archivos temporales"
echo "Ok"
echo "-----------------------------------"
echo "Instalación realizada con éxito!"
exit 0
tweb.service

echo "Web funcionando en el puerto 8081"
echo "Para hacer consultas dirigirse a la dirección 127.0.0.1:8081"
echo "-----------------------------------"

echo "Borrando archivos temporales"
echo "Ok"
echo "-----------------------------------"
echo "Instalación realizada con éxito!"
exit 0

