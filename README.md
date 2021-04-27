# AgroAnalysis Cajamar 2021

## Datos Utilizados

Todos los datos utilizados están accesibles y explicados en [AgroMuki](https://agromuki.maparla.es),
mediante los apartados de `Referencias` y `Metodología`.

## Reproducibilidad

### Análisis y recopilación de datos

Para poder utilizar/replicar la página web presentada como medio de comunicación
del análisis en el proyecto utilizaremos el proyecto [docker](https://www.docker.com/)
para automatizar el despliegue de la aplicación y que sea más sencillo. Una vez instalado
(dejamos una guía [aquí](https://docs.docker.com/get-docker/)), únicamente deberemos clonar este repositorio, 
construir y desplegar la imagen de la siguiente forma:

```shell
docker build -t agro-muki-local .
docker run -d --name agro-muki-local-container -p 8042:5000 agro-muki-local
```

Con esto crearemos un contenedor en nuestro entorno local desplegando la página y siendo accesible
desde un navegador web en la dirección `0.0.0.0:8042`.

(Nota: Si tenemos ocupado el puerto 8042, poner uno a conveniencia sustituyendo dicho número en la orden `docker run`)

Una vez explorada la aplicación, si deseamos pararla para liberar el puerto y eliminarla:

```shell
docker stop agro-muki-local-container
docker rm agro-muki-local-container
```

#### Compilando Tailwind

(Nota: Esta información solo es necesaria desde el punto de vista de desarrollo y no para reproducir los resultados
de la aplicación ni recrear el 'entorno app')

Para dotar de estilos a nuestra aplicación hemos utilizado el framework TailwindCSS. Debido a que extendemos su
funcionalidad y aplicamos estilos propios como conjunción de varias clases de las que nos provee, 
es necesario utilizar npm para compilar los estilos deseados.

Aquí dejamos algunas instrucciones útiles:

```shell
npm init -y
npm install tailwindcss autoprefixer
npm install postcss-cli
```

Esto nos crear varios ficheros. Iremos a `package.json` y modificaremos la entrada 'scripts' con:
```javascript
"build": "postcss ./static/css/tailwind.css -o ./static/css/tailwind_compiled.css"
```

Donde en el fichero `./static/css/tailwind.css` escribiremos nuestros estilos que se basen en clases de Tailwind
(mirar el ejemplo de este app para comprender mejor). 

Finalmente compilaremos nuestro Tailwind y este rellenará el archivo especificado `./static/css/tailwind_compiled.css`
que deberemos haber referenciado en nuestro código fuente. 

```shell
npm run build
```

#### Deployment

Para desplegar la aplicación en tu servidor utilizando [nginx-proxy](https://github.com/nginx-proxy/nginx-proxy)
primero debemos modificar en el fichero Dockerfile las apariciones del número 5000 por 80. Tras esto:

```shell
docker build -t agromuki-container .
docker run -d -e VIRTUAL_HOST=agromuki.maparla.es --name agromuki agromuki-container
```


### Otros

Se ha tenido en cuenta hasta el mínimo detalle. Si por despiste llegáis a una página que no debierais, se os 
redireccionará a una página de error 404 diseñada especialmente para este Datathon (te animamos a probarlo).

Ejemplo: [https://agromuki.maparla.es/noexisto](https://agromuki.maparla.es/noexisto)