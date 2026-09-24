import sqlite3
from pathlib import Path

db_dir = Path("scr/db")
db_dir.mkdir(exist_ok=True)

conn = sqlite3.connect(db_dir / "local.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS activos_report (
    fecha TEXT,
    activo_id INTEGER,
    nombre TEXT,
    estado TEXT,
    valor REAL
)
""")

cursor.execute("SELECT COUNT(*) FROM activos_report")
count = cursor.fetchone()[0]

if count == 0:
    cursor.executemany("""
    INSERT INTO activos_report (fecha, activo_id, nombre, estado, valor)
    VALUES (?, ?, ?, ?, ?)
    """, [
        ("2026-09-24", 60758739, "Activo 60758739", "OK", 1250.50),
            ("2026-09-24", 60758740, "Activo 60758740", "OK", 980.00),
            ("2026-09-25", 60758739, "Activo 60758739", "OK", 1300.00),
        ]
    )



conn.commit()
conn.close()