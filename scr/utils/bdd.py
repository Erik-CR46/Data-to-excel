import sqlite3 #Importamos sqlite para poder crear una bdd local
from pathlib import Path #Path una forma de trabajar con rutas de archivos y carpetas.

def dbb_creation():
    db_dir = Path(__file__).resolve().parents[1] / "db"
    db_dir.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(db_dir / "local.db") #Crea una connexion con sqlite3 y crea local.db en la ruta
    cursor = conn.cursor() #El cursor es el objeto que ejecuta las instrucciones SQL

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS activos_report (
        fecha TEXT,
        activo_id INTEGER,
        nombre TEXT,
        estado TEXT,
        valor REAL
    )
    """) #Con el cursor mas execute ejecutamos esta query para crear una tabla

    cursor.execute("SELECT COUNT(*) FROM activos_report") #El resultado no se obtiene directamente de execute
    count = cursor.fetchone()[0] #fetchone() obtiene la primera fila del resultado.
    #Por eso se usa [0] para obtener solamente el número

    if count < 21: #si la tabla no tiene los datos necesario creamos una lista con cada fila una tupla
        registros = [
                ("2026-09-24", 60758739, "Activo 60758739", "OK", 1250.50),
                ("2026-09-24", 60758740, "Activo 60758740", "OK", 980.00),
                ("2026-09-25", 60758739, "Activo 60758739", "OK", 1300.00),
                ("2026-09-25", 60758740, "Activo 60758740", "OK", 1025.75),
                ("2026-09-25", 60758741, "Activo 60758741", "OK", 875.25),
                ("2026-09-25", 60758742, "Activo 60758742", "PENDIENTE", 1430.00),
                ("2026-09-25", 60758743, "Activo 60758743", "OK", 2150.80),
                ("2026-09-25", 60758744, "Activo 60758744", "REVISION", 760.40),
                ("2026-09-25", 60758745, "Activo 60758745", "OK", 1895.60),
                ("2026-09-26", 60758741, "Activo 60758741", "OK", 910.00),
                ("2026-09-26", 60758742, "Activo 60758742", "OK", 1505.35),
                ("2026-09-26", 60758743, "Activo 60758743", "OK", 2200.10),
                ("2026-09-26", 60758744, "Activo 60758744", "PENDIENTE", 805.90),
                ("2026-09-26", 60758745, "Activo 60758745", "OK", 1930.45),
                ("2026-09-26", 60758746, "Activo 60758746", "OK", 1120.00),
                ("2026-09-26", 60758747, "Activo 60758747", "REVISION", 675.50),
                ("2026-09-27", 60758746, "Activo 60758746", "OK", 1185.30),
                ("2026-09-27", 60758747, "Activo 60758747", "OK", 720.00),
                ("2026-09-27", 60758748, "Activo 60758748", "OK", 1640.75),
                ("2026-09-27", 60758749, "Activo 60758749", "PENDIENTE", 990.20),
                ("2026-09-27", 60758750, "Activo 60758750", "OK", 2450.00),
            ]

        #ejecuta la misma sentencia varias veces, una vez por cada registro
        cursor.executemany("""
        INSERT INTO activos_report (fecha, activo_id, nombre, estado, valor)
        SELECT ?, ?, ?, ?, ?
        WHERE NOT EXISTS (
            SELECT 1
            FROM activos_report
            WHERE fecha = ? AND activo_id = ? AND nombre = ?
            AND estado = ? AND valor = ?
        )
        """, [registro + registro for registro in registros])

    conn.commit()
    conn.close()