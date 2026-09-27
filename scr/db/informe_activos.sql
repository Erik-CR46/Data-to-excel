-- Parametros esperados:
--   :fecha_inicio = '2026-09-24'
--   :fecha_fin    = '2026-09-27'
--   :estado       = NULL, 'OK', 'PENDIENTE' o 'REVISION'

WITH registros_filtrados AS (
	SELECT
		fecha,
		activo_id,
		nombre,
		estado,
		valor,
		LAG(valor) OVER (
			PARTITION BY activo_id
			ORDER BY fecha
		) AS valor_anterior,
		ROW_NUMBER() OVER (
			PARTITION BY activo_id
			ORDER BY fecha DESC
		) AS orden_reciente
	FROM activos_report
	WHERE fecha BETWEEN :fecha_inicio AND :fecha_fin
	  AND (:estado IS NULL OR estado = :estado)
),
resumen_activos AS (
	SELECT
		activo_id,
		MAX(nombre) AS nombre,
		COUNT(*) AS mediciones,
		MIN(fecha) AS primera_fecha,
		MAX(fecha) AS ultima_fecha,
		ROUND(SUM(valor), 2) AS valor_total,
		ROUND(AVG(valor), 2) AS valor_promedio,
		ROUND(MIN(valor), 2) AS valor_minimo,
		ROUND(MAX(valor), 2) AS valor_maximo,
		ROUND(MAX(valor) - MIN(valor), 2) AS variacion_absoluta,
		ROUND(
			100.0 * (MAX(valor) - MIN(valor)) / NULLIF(MIN(valor), 0),
			2
		) AS variacion_porcentual,
		SUM(CASE WHEN estado = 'OK' THEN 1 ELSE 0 END) AS lecturas_ok,
		SUM(CASE WHEN estado = 'PENDIENTE' THEN 1 ELSE 0 END) AS lecturas_pendientes,
		SUM(CASE WHEN estado = 'REVISION' THEN 1 ELSE 0 END) AS lecturas_revision
	FROM registros_filtrados
	GROUP BY activo_id
),
estado_reciente AS (
	SELECT
		activo_id,
		estado AS estado_actual,
		valor AS valor_actual,
		fecha AS fecha_actual
	FROM registros_filtrados
	WHERE orden_reciente = 1
),
informe_clasificado AS (
	SELECT
		resumen_activos.*,
		estado_reciente.estado_actual,
		estado_reciente.valor_actual,
		estado_reciente.fecha_actual,
		CASE
			WHEN estado_reciente.estado_actual = 'REVISION'
				THEN 'ALTO'
			WHEN estado_reciente.estado_actual = 'PENDIENTE'
				OR resumen_activos.variacion_porcentual >= 20
				THEN 'MEDIO'
			ELSE 'BAJO'
		END AS nivel_riesgo,
		ROUND(
			100.0 * resumen_activos.lecturas_ok / NULLIF(resumen_activos.mediciones, 0),
			2
		) AS porcentaje_ok
	FROM resumen_activos
	JOIN estado_reciente
		ON estado_reciente.activo_id = resumen_activos.activo_id
)
SELECT
	DENSE_RANK() OVER (
		ORDER BY valor_total DESC
	) AS ranking_valor_total,
	DENSE_RANK() OVER (
		ORDER BY porcentaje_ok DESC, valor_total DESC
	) AS ranking_confiabilidad,
	activo_id,
	nombre,
	mediciones,
	primera_fecha,
	ultima_fecha,
	estado_actual,
	fecha_actual,
	ROUND(valor_actual, 2) AS valor_actual,
	valor_total,
	valor_promedio,
	valor_minimo,
	valor_maximo,
	variacion_absoluta,
	variacion_porcentual,
	lecturas_ok,
	lecturas_pendientes,
	lecturas_revision,
	porcentaje_ok,
	nivel_riesgo
FROM informe_clasificado
ORDER BY
	CASE nivel_riesgo
		WHEN 'ALTO' THEN 1
		WHEN 'MEDIO' THEN 2
		ELSE 3
	END,
	valor_total DESC;
