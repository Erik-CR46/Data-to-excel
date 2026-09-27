# Data to Excel

Este proyecto lo hice para practicar un flujo de datos de principio a fin: guardar registros en una base de datos local, consultarlos con SQL y pasar el resultado a una plantilla de Excel.

No se conecta a un servicio externo. La base de datos es SQLite y los registros que incluye son datos de ejemplo.

## Qué hace

Al ejecutar `main.py`, el programa:

1. Se asegura de que exista la base `scr/db/local.db` y la tabla `activos_report`.
2. Lee y ejecuta la consulta de `scr/db/informe_activos.sql`.
3. Filtra los registros por fechas y, si se indica, por estado.
4. Resume la información por activo: calcula valores totales y promedios, mediciones, estado reciente, porcentajes, rankings y nivel de riesgo.
5. Abre `scr/templates/Activos_Report.xlsx` y escribe el resultado en la hoja `Sheet1`, empezando en la celda `A4`.
6. Guarda el informe terminado en `output/Informe.xlsx`.

La consulta vive en el archivo `.sql`, no está escrita dentro de Python. `main.py` le pasa sus parámetros y usa `pandas` para recoger el resultado. `openpyxl` se encarga de escribirlo en el Excel.

## Archivos principales

```text
main.py                   Ejecuta el proceso y genera el informe
requirements.txt                Dependencias de Python
scr/db/informe_activos.sql      Consulta del informe
scr/db/local.db                 Base de datos SQLite local
scr/templates/Activos_Report.xlsx  Plantilla de Excel
scr/utils/bdd.py                Crea la tabla y prepara datos de ejemplo
scr/utils/utils.py              Copia las filas del resultado a una hoja Excel
output/                         Carpeta donde se guarda el informe
```

## Prepararlo en Windows

Abre PowerShell en la carpeta del proyecto. Puedes crear y activar un entorno virtual para instalar las dependencias sin mezclarlas con las de otros proyectos:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Si PowerShell bloquea la activación del entorno, permite scripts solo durante esa sesión y vuelve a activarlo:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
```

## Probarlo

Con el entorno virtual activado, ejecuta:

```powershell
python .\main.py
```

Sin argumentos, usa como fecha final el día actual y como fecha inicial dos días antes. También puedes dar las fechas manualmente, en formato `AAAA-MM-DD`:

```powershell
python .\main.py 2026-09-24 2026-09-27
```

El tercer argumento es opcional y filtra por estado. Los estados de los datos de ejemplo son `OK`, `PENDIENTE` y `REVISION`:

```powershell
python .\main.py 2026-09-24 2026-09-27 REVISION
```

Al terminar, la consola muestra la ruta del Excel creado. Cada ejecución guarda el informe en `output/Informe.xlsx`, reemplazando el informe anterior.

## Para seguir practicando

- Añadir registros propios y comprobar cómo cambian los resultados.
- Probar el filtro con cada estado y comparar los informes.
- Cambiar la consulta SQL y añadir una métrica nueva.
- Dar formato a los encabezados y a los valores desde la plantilla o desde `utils.py`.
- Añadir validaciones para fechas mal escritas o para estados que no existan.
- Hacer que el nombre del informe incluya las fechas, para guardar varias ejecuciones sin sobrescribirlas.

## Notas

- Las fechas se comparan como texto en formato `AAAA-MM-DD`; mantén ese formato para que el filtro funcione correctamente.
- La hoja de la plantilla debe llamarse `Sheet1`, porque ese es el nombre que usa el programa.
- `bdd.py` contiene datos de ejemplo. Es una base para practicar, no una carga automática de datos reales.
