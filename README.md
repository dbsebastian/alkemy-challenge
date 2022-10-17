<div id='id-section1'/>

## Alkemy Challenge Data Analytics

Este es un Proyecto-Challenge de evaluación para la aceleración de Alkemy.



## Tabla de contenido
- [Enunciado - Intro](#id-section1)
- [Instalación - Guía de uso](#id-guia_uso)
- [Sobre el proyecto](#id-sobre-el)
- [Contacto](#id-contacto) 


<div id='id-guia_uso'/>  

## Instalación - Guía de uso
1. Descargar repositorio.

2. Crear un nuevo entorno virtual.

```
# Ejemplo
conda create -n Nombre_del_projecto python
```  

3. Una vez creado el entorno virtual, activarlo.
```
# Ejemplo
conda activate Nombre_del_projecto
```  

4. Con el entorno virtual creado y activado, ejecutar **requirements.txt** para instalar las librerías que el proyecto necesita para ser ejecutado correctamente.
   
```
# Ejemplo
## para ejecutar "requirements.txt"

pip install -r requirements.txt

```

5. Configurando el archivo **.env** que debe estar presente en el **/root** o **"Directorio Base"**.
```
# contenido del archivo ".env" que debe estar presente en el "/root" del proyecto

POSTGRES_HOST="" # Aquí, como string, debe ir el nombre del host de Pgadmin4
POSTGRES_PORT="" # Aquí, como string, debe ir el número de host de PgAdmin4
POSTGRES_USER="" # Aquí, como string, debe ir el nombre del user de PgAdmin4
PASSWORD=""      # Aquí, como string, debe ir el password, de la database de PgAdmin4 (no de la app)
```

6. Hasta ahora, ya se configuró tanto las librerías necesarias, como la database y los datos necesarios para su conexión.
7. Llegado a éste punto, sólo queda por ejecutar el archivo **"main.py"** presente en el directorio **"/alkemy"**
  


<div id='id-sobre-el'/>  

## Sobre el proyecto
* El proyecto toma las URLs presentes en el archivo **"list of urls.txt"**, de la carpeta **"/alkemy/"**, dichas URLs están en el formato de una url por renglón, identificando de éstas los renglones vacíos de los que no, y a partir de estas URLs, darles el formato necesario para descargarlos de google sheets.
* El proyecto creará la carpeta **"/logs/"** en la cual se guardarán los logs del proyecto, se guardarán hasta un log anterior, y los subsiguientes se irán eliminando automáticamente.
* El proyecto creará la carpeta **"/datos/"** en los cuales se guardarán según puntos establecidos por el Challenge-Reto, los directorios correspondientes a cada archivo .csv que debe descargarse.
* En la carpeta **"/sql_files/"** se guardan los **"".sql""** necesarios para crear las tablas en la base de datos.


<div id='id-contacto'/>  

## Contacto
* Autor = Diego Sebastian Barrios
* Email = sebastiann_db@gmail.com
* [Linkedin](https://www.linkedin.com/in/dsebastianb)
* [Github](https://dbsebastian.github.io/)
