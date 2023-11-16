# Configuración del porfolio

Este proyecto de django sera alojado en una instancia virtual de EC2.
Las tecnologías que voy a utilizar son Nginx y Gunicorn.

## Grupo de seguridad (Security group)

Lo que se debe hacer primero es configurar un grupo de seguridad. Donde vamos a describir las reglas de los puertos de entrada y de salida que van a estar habilitados en nuestra instancia.
> Es un firewall virtual

En cuanto a las regla de salida, se debe habilitar la opción de dejar todo el trafico disponible que viene por defecto.

Para las reglas de entrada vamos a habilitar tres reglas.

- Tipo: SSH  Fuente: Anywhere 0.0.0.0/0
- Tipo: HTTP  Fuente: 0.0.0.0/0  (todo el trafico de direcciones IPV4 en el puerto 80)
- Tipo: HTTP Fuente: ::/0 (todo el trafico de direcciones IPV6 en el puerto 80)

Luego de especificado el nombre y la descripción, le damos a crear grupo de seguridad.

Esta configuración quedara guardada para luego ser utilizada en la creación de nuestra instancia.

## Creación de la instancia EC2

Se debe seleccionar Lanzar una nueva instancia. Donde se tendrá que seguir los pasos de configuración.

- Ingresar el nombre.
- Seleccionar la version del SO de la instancia (Ubuntu20.04 en este caso)
- Seleccionar el tipo de la instancia t2.micro (del free tier)
- Seleccionar la opción de `key pair` continuar sin un par de claves
- En Firewall(security groups), seleccionar el grupo de seguridad anteriormente creado

## Configurar el SO de la instancia

Lo primero es conectar a la instancia, ya sea con par de claves o con una pestaña en el navegador.

Una vez conectados a la instancia, es recomendable hacer un `sudo apt-get update` para verificar que paquetes del sistema pueden actualizarse, y luego actualizarlos con `sudo apt-get upgrade`.

> Aparecerán varios mensajes de que los `daemons` tienen que reiniciase, no es nada importante, solamente se debe apretar enter para que continue la instalación. Esto también puede pasar en la instalación de paquetes.
> Verificar la version de python con `python3 --version`

El siguiente paso es instalar `venv` para gestionar nuestro entorno separado al del sistema con el comando `sudo apt-get install python3-venv`

Crear el entorno virtual del proyecto con el comando `python3 -m venv env`

El siguiente paso es clonar el proyecto desde github.
`git clone https://github.com/agustin1996ra/porfolio.git`

Luego procede instalar los paquetes de dependencias del entorno. Para iniciar el entorno ejecutamos `source env/bin/activate`. Y para instalar las dependencias del entorno ejecutamos `pip install -r porfolio/requirements.txt`

## Variables de entorno en producción

Es necesario luego de clonar el proyecto crear el archivo .env dentro de la carpeta del proyecto. En este archivo se deberá setear la variable `SECRET_KEY`, generando una nueva key con el generador de claves de django.

Otra de las cosas que debemos hacer es cambiar los hosts permitidos, este va a ser el puerto o dirección con el que nos conectaremos al proyecto, para este caso sera `agustinrodriguez.com.ar`, pero esto cambiara si nos conectamos directamente desde una ipv4.

### Instalación de Nginx

El comando para instalar Nginx es `sudo apt-get install -y nginx`

#### Conectar a la dirección ipv4

Este procedimiento sirve para confirmar que hemos instalado correctamente Nginx y que nuestra instancia es accesible desde esta dirección y el puerto 80.

> Es recomendable pasarle a cloudflare la dirección ipv4 desde este punto para probar que el intermediario tiene acceso a la ip. Si la configuración fue correcta al ingresar a la dirección web debería dar el mismo resultado que al dirigirte a la dirección ipv4.

### Instalar gunicorn

Gunicorn nos va a permitir comunicar nuestro servidor web con los puertos del proyecto.

`pip install gunicorn`

### Instalar Supervisor

Este programa se encargar de ejecutar varios procesos de nuestro proyecto de forma persistente

`sudo apt-get install supervisor`

#### Configuración de Supervisor

Vamos a la carpeta `/etc/supervisor/conf.d/`

Aca crearemos el archivo de configuración que ejecutara el proceso gunicorn, con el comando `sudo touch gunicorn.conf`.
Para editarlo lo debemos abrir con `sudo nano gunicorn.conf`

```conf
[program:gunicorn]
directory=/home/ubuntu/porfolio
command=/home/ubuntu/env/bin/gunicorn --workers 3 --bind unix:/home/ubuntu/porfolio/app.sock app.wsgi:application  
autostart=true
autorestart=true
stderr_logfile=/var/log/gunicorn/gunicorn.err.log
stdout_logfile=/var/log/gunicorn/gunicorn.out.log

[group:guni]
programs:gunicorn
```

Se necesita crear los archivos de log con el siguiente comando `sudo mkdir /var/log/gunicorn`.

Y le damos la orden de releer las instrucciones a supervisor con el comando `sudo supervisorctl reread`. Si recibimos el mensaje `guni: available` quiere decir que se ejecuto correctamente el comando.

Para que supervisor empiece a ejecutar gunicorn en background ejecutamos `sudo supervisorctl update`. Deberemos recibir el siguiente mensaje `guni: added process group`

Para confirmar el estado de ejecución de los procesos de gunicorn usamos el comando `sudo supervisorctl status`

### Configuración de nginx

Entramos al directorio `/etc/nginx`.
Abrimos el archivo `nginx.conf`
Y cambiamos el usuario a `root`.
Gurdamos y cerramos el archivo.

Luego vamos a crear el archivo de configuración para nuestra aplicación django en la carpeta `sites-available`

Nos movemos a la carpeta `cd sites-available`
Creamos el archivo de configuración `sudo touch django.conf`
Ingresamos al archivo para editarlo `sudo nano django.conf`, y agregaremos el siguiente texto de configuración.

```conf
server {

    listen 80;
    server_name agustinrodriguez.com.ar;

    location / {

        include proxy_params;
        proxy_pass http://unix:/home/ubuntu/porfolio/app.sock;

    }

    location /static/ {
        alias /home/ubuntu/porfolio/static/;
    }

}
```

Una vez terminada la configuración, guardamos y salimos. Y para testear que la configuración ingresada es correcta podemos chequearlo con el comando `sudo nginx -t`.

Luego para vincular nuestro archivo de configuracion de la aplicacion django en la carpera de `/etc/nginx/sites-enabled` con el comando `sudo ln django.conf /etc/nginx/sites-enabled`.

Una vez realizados todos estos pasos podemos reiniciar el servicio de nginx con el comando `sudo service nginx restart`.

Ahora podremos ver la respuesta de nuestra aplicación django en la ip publica.