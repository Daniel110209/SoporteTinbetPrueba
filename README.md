# Sistema Tinbet - Registro de usuarios y control de equipos

Prototipo en Python (version 2) para Tinbet, KING TECH CORPORATION S.A.C.

## Que hace

- Registra usuarios (DNI, nombre, lugar, edad) y rechaza a menores de 18 anios.
- Genera un codigo unico de 12 numeros por usuario.
- Dos tipos de ingreso: administrador (con clave) y operador.
- Camaras de seguridad y bitacora: solo para administradores.
- Televisores disponibles y ocupados: se elige el televisor y luego el canal (HBO Max, Disney+, DirecTV GO, ESPN y mas) para el usuario registrado.
- Todo queda registrado en archivos de texto dentro de la carpeta `datos/`.
- No incluye el proceso de apuestas.

## Como ejecutarlo

```
python main.py
```

Administrador inicial: usuario `admin`, clave `tinbet2026`.

## Archivos de texto (carpeta datos)

| Archivo | Contenido |
|---|---|
| usuarios.txt | Usuarios aceptados |
| rechazados.txt | Menores rechazados |
| bitacora.txt | Todo lo que ocurre en el sistema, con fecha y hora |
| equipos.txt | Estado de las camaras |
| televisores.txt | Televisores, canal elegido y usuario |
| administradores.txt | Administradores (clave cifrada) |

## Modulos y responsables

| Archivo | Que hace | Responsable |
|---|---|---|
| utilidades.py | DNI, codigo de 12 numeros y busquedas en listas | Jheimy |
| entradas.py | Lectura segura de numeros, textos y confirmaciones | Jheimy |
| archivos.py | Guardar y cargar usuarios, camaras y televisores | Jheimy |
| seguridad.py | Login de administrador y control de acceso | Diego |
| registro.py | Registro de usuarios y rechazo de menores | Diego |
| log.py | Escritura y lectura de la bitacora | Diego |
| consultas.py | Mostrar, listar y buscar usuarios | Oscar |
| bitacora.py | Ver y buscar en la bitacora (admin) | Oscar |
| camaras.py | Camaras de seguridad (admin) | Oscar |
| equipos.py | Televisores: elegir televisor y canal | Erick |
| canales.py | Lista y eleccion de canales | Erick |
| rutas.py | Carpeta y rutas de los archivos de texto | Erick |
| main.py | Menu principal y resumen general | Misael |
| pantalla.py | Titulos y formato de pantalla | Misael |
| fechas.py | Fecha y hora de Peru y duracion | Misael |
