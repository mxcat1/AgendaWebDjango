# Proyecto para mi examen final de Lenguaje web 2 Instituto del Sur
Todo el contenido trabajado sobre el proyecto de AgendaWeb se encuentra aqui para mas detalle comunicarse al siguiente correo
c.n.vilca.apazagmail.com con el asunto de importante github

** Para usar o pner en marcha el proyecto se debe seguir los siguientes requisitos
1. Clonar el repositorio para tener una copia local:<br>
  ` $git clone https://github.com/mxcat1/AgendaWebDjango`<br>
2. Para actualizar la copia local para que este igual al master<br>
  ` $git pull origin master`<br>
3. Crear una rama o branch <br>
   `$ git branch tunombre`<br>
4. Cambiarse a la rama que crearon<br>
   `$ git checkout tunombre`<br>
5. Para comprobar que van a subir solo los archivos que modificaron <br>
   - utilizar el comando:<br> 
      `$ git status`<br>
6. Subir sus cambios a su rama<br>
   - Agregar los archivos<br>
        `$ git add .`<br>
   - Crear el commit con la descripción de lo que modificaron o avanzaron tienen que ser claros<br>
        `$ git commit -m "descripcion de lo que hice o modifique "`<br>
   - enviar todos los cambios<br>
        `$ git push origin nombre_de_tu_rama`<br>
7. Debes tener python y el entorno virtual de python instalado, laversion de python utilizada en este proyecto es la 3.9.0  
**Comandos para ejecutar el proyecto en windows
   1. Instalar el virtualenv Comando 
        `$pip install virtualenv"`<br>
   2. Activar el Entorno Virtual Python para eso debe estar situado en la carpeta raiz del proyecto y tener abierto un consola de powershell o cmd luego ejecutar el siguiente comando
        `$ .\\venv\Scripts\activate`
   3. Luego en esa consola o powershell ejecutar el siguiente comando 
        `$ python manage.py makemigrations`
      - este comando sirve para migrar la base de datos
   5. Despues ejecutar elcomando `$ python manage.py sqlmigrate AgendaWebDjango 0001`
   6. Por Ultimo ejecutar el comango `$ python manage.py migrate` para crear la abse de datos
   7. IMPORTANTE para mas detalle de la base de datos en la carpeta de DiseñoBD
   8. Como ultimo paso para ejecutar el proyecto ejecutar el comando en el cmd o powershell u otros `$ python manage.py runserver`