import os #permite leer la variable de entorno OUTPUT_DIR
import sqlite3 #conecta el programa con la base de datos SQLite local.
import sys #lee los argumentos que escribes al ejecutar el script
from datetime import date, timedelta #obtiene la fecha de hoy y calcula una fecha anterior
from pathlib import Path #construye rutas de archivos y carpetas

import pandas as pd #recibe el resultado del SQL en una tabla de datos, el DataFrame
from openpyxl import load_workbook #abre la plantilla de Excel existente

from scr.utils.bdd import dbb_creation
from scr.utils.utils import paste_to_excel


def generar_informe(
	fecha_inicio: str, #fecha inicial que se enviará al SQL
	fecha_fin: str,
	estado: str | None = None, #filtro opcional. Si vale None, no se filtra por estado.
) -> str:
	base_dir = Path(__file__).resolve().parent #encuentra la carpeta donde está main_local.py
	
    #Rutas
	db_path = base_dir / "scr" / "db" / "local.db"
	query_path = base_dir / "scr" / "db" / "informe_activos.sql"
	template_path = base_dir / "scr" / "templates" / "Activos_Report.xlsx"
	output_dir = Path(os.getenv("OUTPUT_DIR", base_dir / "output"))
	output_dir.mkdir(parents=True, exist_ok=True)

	dbb_creation()
	query = query_path.read_text(encoding="utf-8") #Lee el contenido del archivo sql y lo guarda en query
	params = {
		"fecha_inicio": fecha_inicio,
		"fecha_fin": fecha_fin,
		"estado": estado,
	} #prepara los valores para los parámetros que aparecen en el SQL

    #abre la conexión a SQLite y la cierra al terminar el bloque
	with sqlite3.connect(db_path) as connection:
		#df va a ser un pd que lee el sql de nuestra query, con nuestra conexion y los parametros
		df = pd.read_sql_query(query, connection, params=params)

	workbook = load_workbook(template_path) #Abre la plantilla con la ruta
	paste_to_excel(
		df, #El dataframe, los datos que se van a copiar
		workbook, #El excell que acabamos de abrir
		worksheet="Sheet1", #La hoja donde se escribira
		start_row_cell=4,
		start_column_cell=1,
		include_header=True, #solicita que también se escriban los nombres de las columnas.
	)

	output = output_dir / "Informe.xlsx" #define el archivo final, Informe.xlsx
	workbook.save(output) #guarda el Excel rellenado
	return str(output)  #devuelve la ruta del informe generado


if __name__ == "__main__": #ejecuta lo siguiente solo cuando lanzas este archivo directamente.
	fecha_fin = sys.argv[2] if len(sys.argv) > 2 else date.today().isoformat()
    #sys: módulo de Python que permite acceder a información y argumentos del programa
	#argv: lista de argumentos recibidos al ejecutar el script. Incluye también el nombre del script en la posición 0.
    #[2]: obtiene el elemento de la posición 2 de esa lista, es decir, el segundo argumento del usuario. La numeración empieza en cero:
    
    #sys.argv[0]: nombre del script.
    #sys.argv[1]: primer argumento del usuario.
    #sys.argv[2]: segundo argumento del usuario.
	
    #.isoformat(): convierte esa fecha en texto con formato AAAA-MM-DD, por ejemplo 2026-09-26
    
	fecha_inicio = (
		sys.argv[1]
		if len(sys.argv) > 1
		else (date.today() - timedelta(days=2)).isoformat()
	)
    #Eso calcula la fecha de hace dos días. Por ejemplo, si hoy es 2026-09-26, 
    # el resultado es 2026-09-24. Luego .isoformat() 
    # la convierte al texto "2026-09-24" para pasarla como fecha_inicio al informe.
    
	estado = sys.argv[3] if len(sys.argv) > 3 and sys.argv[3] else None
    #estado =: guarda el resultado en la variable estado.
    #sys.argv: lista de valores escritos al ejecutar el programa. La posición 0 es el nombre del script.
    #len(sys.argv) > 3: comprueba que haya al menos tres argumentos del usuario: fechas inicial y final, más el estado.
    #and: exige que también se cumpla la siguiente condición.
    #sys.argv[3]: obtiene el tercer argumento del usuario, que en este caso será el estado.
    #sys.argv[3] usado como condición: comprueba que ese texto no esté vacío.
    #if ... else ...: si ambas condiciones son verdaderas, usa el estado; si no, usa None.

	print(generar_informe(fecha_inicio, fecha_fin, estado))
