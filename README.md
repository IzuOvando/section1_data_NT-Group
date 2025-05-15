## Setting Docker Compose 🐳

Por seguridad nunca se sube a un repositorio el archivo `.env`, creamos comunemente un `.env.local` pero por uso de variables y ejemplificar esta prueba se subira un ejemplode este archivo.

Para tener una instancia local de base de datos **PostgreSQL**, debes ejecutar:
```bash
docker-compose up --build
```
> [!IMPORTANT]
> Nosotros assumimos que se tiene Docker Instalado

Esto contenedor instalara los requerimientos necesarios y automaticamente correra `python-runner:entrypoint` el cual ejecutara una secuencia de scripts para cargar datos de nuestro ejemplo de excel a una base de datos postgres en nuestro contenedor.

para poder visualizar estos datos y la tabla se tendra que abrir una terminal y correr:

```bash
docker exec -it data-processing-nt_group-db-1 psql -U postgres -d mydb

\d

\dv 
```
`\dv` este comando ejecutara las views creadas en la base de datos.

## Notas y Obsevaciones

Por consistencia se crea un .gitignore al subir a un repo pero por ahora lo evitare ya que subire todos los archivos contenidos en al carpeta

Algunos problemas que enfrente fueron, primeramente en el documento de .docs en el cual vienen las instrucciones de los scripts que hay que desarrollar en la section 1 no era claro si cada punto era individual o era un asecuencia de flujo eso me llevo a armar una secuencia logica para extraer y subor la informacion ya que desde el punto 1.1 Craga de informacion ya mencionaba seleccionar y subir base de datos pero no esclarecia si primero habia que trasformarla o primero subir y despues trasformarla por secuencia logica primero la limpie antes de subirla a una tabla SQL.

Otro problema fue enfrentar a los issues que tenia la tabla de excel ya que los valores de la data no son consistentes y habia que darles consistencia.

Por cuestiones de tiempo y personales ya que tuve que ir a una consulta medica me hubiera gustado agregar tests o pruebas unitarias, pero describo aqui que los unicos test que he hecho son mediante la libreria de jest y creando mock data para poder correr cada script y asi enviar su comportamiento si esta devolviendo lo que se busca.

La otra manera ha sido con fixtures mediante el framework de django