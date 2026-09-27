from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl import Workbook
import pandas as pd

def paste_to_excel(
    df_to_paste: pd.DataFrame, #El data frame con los resultados
    workbook: Workbook, #El archivo excel que ya abrio desde la plantilla
    worksheet: str, #Nombre de la sheet
    start_row_cell: int = 1, #Fila y columnas iniciales
    start_column_cell: int = 1,
    include_header: bool = False, #Opcion para indicar si se escriben los nombres de las columnas
) -> None:
    worksheet_obj = workbook[worksheet] #obtiene la hoja indicada

    rows_df = list( #Convierte el dataframe en filas
        dataframe_to_rows(
            df_to_paste,
            index=False, #no añade los números de índice de pandas
            header=include_header #incluye los nombres de las columnas.
            )
        )

    for r_idx, row in enumerate(rows_df, start_row_cell):

        #rows_df contiene las filas que se van a escribir.
        #row es la fila actual, por ejemplo ["Nombre", "Valor"].
        #r_idx es la fila de Excel donde se escribirá.
        #start_row_cell indica desde qué fila empezar.
        #Si start_row_cell=4, las vueltas empiezan así:

        #r_idx	    row
        #4	        ["Nombre", "Valor"]
        #5	        ["Casa A", 100]
        #6	        ["Casa B", 200]


        for c_idx, value in enumerate(row, start_column_cell):
            worksheet_obj.cell(row=r_idx, column=c_idx, value=value)

            #row es la fila actual.
            #value es el valor actual de esa fila.
            #c_idx indica en qué columna de Excel se escribe.
            #start_column_cell indica desde qué columna empezar.

            #.cell escribe value en la celda ubicada en la fila r_idx y columna c_idx.