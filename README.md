# Sistema Tinbet - Registro de usuarios, televisores y apuestas

Prototipo en Python para Tinbet, KING TECH CORPORATION S.A.C.

## Que hace

- Registra usuarios (DNI, nombre, lugar, edad) y rechaza a menores de 18 anios.
- Genera un codigo unico de 12 numeros por usuario.
- Dos tipos de ingreso: administrador (con clave) y operador.
- Solo administradores: camaras, bitacora y reportes, editar y eliminar usuarios, resolver eventos.
- Televisores: se elige el televisor y luego el canal (HBO Max, Disney+, DirecTV GO, ESPN y mas).
- Apuestas: deposito de saldo, eventos con cuotas, apuestas y pago al cerrar el evento. Todo se guarda en archivos de texto.
- Reporte diario en un archivo de texto.
- Todo queda registrado en archivos de texto dentro de la carpeta `datos/`.

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
| bitacora.txt | Todo lo que ocurre en el sistema, con fecha y hora de Peru |
| equipos.txt | Estado de las camaras |
| televisores.txt | Televisores, canal elegido y usuario |
| saldos.txt | Saldo de cada usuario |
| apuestas.txt | Tickets de apuestas |
| resultados.txt | Eventos cerrados |
| reporte_FECHA.txt | Reporte diario |
| administradores.txt | Administradores (clave cifrada) |

## Modulos y responsables

| Archivo | Que hace | Responsable |
|---|---|---|
| utilidades.py | DNI, codigo de 12 numeros y busquedas en listas | Jheimy |
| entradas.py | Lectura segura de numeros, textos y confirmaciones | Jheimy |
| archivos.py | Rutas y lectura y escritura de todos los .txt | Jheimy |
| seguridad.py | Login de administrador y control de acceso | Diego |
| registro.py | Registrar, editar y eliminar usuarios | Diego |
| log.py | Escritura y lectura de la bitacora | Diego |
| consultas.py | Mostrar, listar y buscar usuarios | Oscar |
| bitacora.py | Bitacora, busquedas y reporte diario (admin) | Oscar |
| camaras.py | Camaras de seguridad (admin) | Oscar |
| equipos.py | Televisores: elegir televisor y canal | Erick |
| canales.py | Lista y eleccion de canales | Erick |
| apuestas.py | Depositos, eventos, apuestas y pagos | Erick |
| main.py | Menu principal y resumen general | Misael |
| pantalla.py | Titulos y formato de pantalla | Misael |
| fechas.py | Fecha y hora de Peru y duracion | Misael |
