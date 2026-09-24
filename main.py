import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from dotenv import load_dotenv, find_dotenv
import snowflake.connector
import pandas as pd
from openpyxl import load_workbook
from src.utils.utils import paste_to_excel
from datetime import datetime

from snowflake_pk import get_private_key_bytes


def generar_informe(fecha: str, activos: str):
    """
    Genera el informe Medea Vays.

    Args:
        fecha: Fecha en formato 'YYYY-MM-DD'
        activos: Identificadores de activos separados por coma (ej: '60758739,60758740')
    """
    load_dotenv(find_dotenv())

    # Parámetros no-secretos con default: en local se sobrescriben con .env,
    # en Airflow (donde no llega .env por estar en .gitignore) se usan estos.
    conn_kwargs = {
        "user": os.getenv('DB_USER'),
        "account": os.getenv('DB_ACCOUNT', 'VWBXCZT-YM10366'),
        "warehouse": os.getenv('DB_WAREHOUSE', 'WH_DATA_OFFICE'),
        "database": os.getenv('DB_DATABASE', 'SVH_REPORT_DB'),
        "schema": os.getenv('DB_SCHEMA', 'SOCIAL_HOUSING'),
    }

    role = os.getenv('DB_ROLE')
    if role:
        conn_kwargs["role"] = role

    conn_kwargs["private_key"] = get_private_key_bytes()

    conn = snowflake.connector.connect(**conn_kwargs)

    # Construir la llamada al procedimiento con los parámetros recibidos
    query = f"CALL SVH_REPORT_DB.SOCIAL_HOUSING.PROC_MEDEA_VAYS_TEST('{fecha}'::DATE, '{activos}');"

    try:
        cursor = conn.cursor()
        cursor.execute(query)

        # Obtener los resultados de la tabla de salida
        cursor.execute("SELECT * FROM SVH_REPORT_DB.SOCIAL_HOUSING.DM_SH_INTERF_ACTIVOS_TEST")
        df = cursor.fetch_pandas_all()
    finally:
        conn.close()

    # Rutas resueltas respecto a la ubicación de main.py para que funcione
    # tanto en local como en Airflow (donde el cwd no es la raíz del proyecto).
    base_dir = Path(__file__).resolve().parent
    template_path = base_dir / "src" / "templates" / "TemplateMedea.xlsx"

    workbook = load_workbook(template_path)

    paste_to_excel(
        df,
        workbook,
        worksheet="Hoja1",
        start_row_cell=2,
        start_column_cell=1
    )

    # OUTPUT_DIR permite redirigir la salida en Airflow (p.ej. /tmp/output o
    # un volumen compartido). En local usa ./output junto al proyecto.
    output_dir = Path(os.getenv("OUTPUT_DIR", base_dir / "output"))
    output = output_dir / "Informe.xlsx"
    output.parent.mkdir(parents=True, exist_ok=True)

    workbook.save(output)
    return str(output)


if __name__ == "__main__":
    fecha = sys.argv[1] if len(sys.argv) > 1 else datetime.today().strftime('%Y-%m-%d')
    activos = sys.argv[2] if len(sys.argv) > 2 else ''

    file_list = generar_informe(fecha, activos)
    print(file_list)