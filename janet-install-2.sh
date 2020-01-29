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
if ! id "tfg-biblio" >/dev/null 2>&1; then
    useradd -m -d /home/tfg-biblio -s /sbin/nologin -U tfg-biblio
    echo "Ok"
else
    echo "El usuario 'tfg-biblio' ya existe, continúo..."
fi

echo "-----------------------------------"

echo "Instalando Janet..."
mv wskey.conf /home/tfg-biblio/Servidor/
chown -R tfg-biblio:tfg-biblio /home/tfg-biblio/Servidor
chmod -R 777 /home/tfg-biblio/Servidor

echo "Ok"
echo "-----------------------------------"

echo "Instalando web..."
chown -R tfg-biblio:tfg-biblio /home/tfg-biblio/janetWeb
chmod -R 777 /home/tfg-biblio/janetWeb

echo "Ok"
echo "-----------------------------------"

echo "Instalando dependencias..."
janet_venv/bin/pip install -U pip
#janet_venv/bin/pip install -r requirements.txt
#janet_venv/bin/pip install rasa
git clone https://github.com/RasaHQ/rasa.git
janet_venv/bin/pip install -r rasa/requirements.txt
janet_venv/bin/pip install -e rasa
janet_venv/bin/pip install spacy==2.2.3
janet_venv/bin/pip install bottle==0.12.18

echo "Ok"
echo "-----------------------------------"

echo "Instalando Jarvis..."

PYT=$(python3 --version 2>&1 | grep -oP '([0-9]).([0-9])')

#mv Jarvis/regex_featurizer.py /usr/local/lib/python$PYT/dist-packages/rasa_nlu/featurizers/regex_featurizer.py
chown -R tfg-biblio:tfg-biblio /home/tfg-biblio/Jarvis
chmod -R 777 /home/tfg-biblio/Jarvis

janet_venv/bin/python3 -m spacy download es_core_news_sm >/dev/null

echo "Ok"
echo "-----------------------------------"

echo "Preparando Base de datos..."

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

mongoimport --db janet --collection localizaciones --file /home/tfg-biblio/Servidor/bibliotecas.json

mongo <<EOF
use janet
db.localizaciones.createIndex({kw: "text"});
exit
EOF

echo "Ok"
echo "-----------------------------------"
echo "Creando daemons..."
#TODO hay que hacer que se compruebe si ya existe el servicio y se sustituya
mv /home/tfg-biblio/Servidor/janet.service /etc/systemd/system/janet.service
mv /home/tfg-biblio/Jarvis/jarvisactions.service /etc/systemd/system/jarvisactions.service
mv /home/tfg-biblio/Jarvis/jarvis.service /etc/systemd/system/jarvis.service
mv /home/tfg-biblio/janetWeb/janetweb.service /etc/systemd/system/janetweb.service

systemctl enable janet.service
systemctl enable jarvisactions.service
systemctl enable jarvis.service
systemctl enable janetweb.service

echo "Ok"
echo "-----------------------------------"
echo "Entrenando Jarvis por primera vez, esta operación durará varios minutos..."
cd /home/tfg-biblio/Jarvis/
../janet_venv/bin/python3 JarvisMain.py -t all

echo "Ok"
echo "-----------------------------------"
echo "Creando servicio del destructor imperial"
mycron=${TMPDIR:-/tmp}/xyz.$$
trap "rm -f $tmp; exit 1" 0 1 2 3 13 15
echo "*/15 * * * * tfg-biblio python3 /home/tfg-biblio/Servidor/DestructorImperial.py" >> $mycron
crontab -u tfg-biblio $mycron
rm -f $mycron

echo "Ok"
echo "-----------------------------------"
echo "Arrancando servicios"
systemctl start janet.service
systemctl start jarvisactions.service
systemctl start jarvis.service
systemctl start janetweb.service

echo "Web funcionando en el puerto 8081"
echo "Para hacer consultas dirigirse a la dirección 127.0.0.1:8081"
echo "-----------------------------------"

echo "Borrando archivos temporales"
#if [ -d "$DIRECTORY/Servidor" ]; then rm -Rf $DIRECTORY/Servidor; fi
#if [ -d "$DIRECTORY/Jarvis" ]; then rm -Rf $DIRECTORY/Jarvis; fi
#if [ -d "$DIRECTORY/Clientes" ]; then rm -Rf $DIRECTORY/Clientes; fi
#if [ -f "$DIRECTORY/.gitignore" ]; then rm $DIRECTORY/.gitignore; fi
#if [ -f "$DIRECTORY/README.md" ]; then rm $DIRECTORY/README.md; fi
#if [ -f "$DIRECTORY/LICENSE.md" ]; then rm $DIRECTORY/LICENSE.md; fi
#if [ -f "/home/tfg-biblio/Jarvis/bibliotecas.json" ]; then rm /home/tfg-biblio/Jarvis/bibliotecas.json; fi

echo "Ok"
echo "-----------------------------------"
echo "Instalación realizada con éxito!"
exit 0

