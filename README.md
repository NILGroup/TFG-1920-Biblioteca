# TFG Biblioteca
Repositorio del TFG "Mejorando el acceso a la biblioteca de la UCM".
Facultad de Informática de la Universidad Complutense de Madrid.
Curso 2019-2020.

Autores: Manuel María Guerrero Serrano, Miguel Ángel Castillo Moreno y Mario Torres Cabañas.
Directores: Alberto Díaz Esteban y Antonio Fernando García Sevilla.

Este repositorio es una continuación de otro desarrollado el curso anterior llamado: "Asistente virtual para servicios de la biblioteca de la UCM", cuyo repositorio puede encontrarse [aquí](https://github.com/NILGroup/TFG-1819-Biblioteca)
 
**Instalación en servidor**

El instalador proporcionado en este repositorio ha sido diseñado para:

 - Debian 'Jessie' y 'Stretch'
 - Ubuntu 'Trusty', 'Xenial' y 'Bionic'

*Es necesario ejecutar el script de instalación como superusuario.

Para realizar la instalación ejecutar "install-janet.sh", este script se encarga de instalar todos los componentes del sistema.

IMPORTANTE! Una vez instalado uno de los módulos parciales, no debe ejecutarse el instalador completo, en su lugar, utiliza el otro instalador parcial.

Para instalar el sistema es necesario disponer de las carpetas Servidor y/o Jarvis (en función del tipo de instalación) y el fichero 'wskey.conf'. Todos estos ficheros deben estar en el mismo directorio que el script de instalación. En caso de no encontrarse alguno de estos ficheros la instalación no continuará.

El archivo 'wskey.conf' no se proporciona en este repositorio, dado que contiene información confidencial. Para conseguir este fichero, ponte en contacto con los directores del proyecto.

**Instalación en dispositivos móviles**

En iOS puedes instalar la aplicación entrando en la App Store y escribiendo en el buscador "Janet ucm". También puedes acceder directamente pulsando [aquí](https://itunes.apple.com/us/app/janet/id1451052771?l=es&ls=1&mt=8)

En Android puedes instalar la aplicación entrando en la Play Store y escribiendo en el buscador "Janet". También puedes acceder directamente pulsando [aquí](https://play.google.com/store/apps/details?id=es.ucm.fdi.janet&hl=es_419)

Si no quieres instalar la aplicación a través de la Play Store, puedes instalar el apk directamente descargándolo desde este repositorio, en la sección [Releases](https://github.com/NILGroup/TFG-1920-Biblioteca/releases)

**Versión Web de Janet**

Para dirigirse a la versión Web de Janet haga click [aquí](https://holstein.fdi.ucm.es/tfg-biblio2/)
