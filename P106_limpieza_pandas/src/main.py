# Para limpiar data nesesito dos programas, uno que limpie y uno que me permita revisar, porque es implosible revisar a ajo en cantidades de datos grandes
from pathlib import Path
import pandas as pd


ACTIVITY_DIR = Path(__file__).resolve().parents[1]
INPUT_FILE = ACTIVITY_DIR / "data" / "ventas.csv"
OUTPUT_FILE = ACTIVITY_DIR / "submission" / "ventas.csv"
def clean_column_names(df):

# Nunca se debe decir que hace, pero siempre decir el porque se hace
# Casos tipicos en las columnas
# ' Supplier ID ' -> 'supplier_id'  
# 'City ' -> 'city'
# 'Purchase Date' -> 'purchase_date'
  
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    return df

# Unificar cadenas de texto
# Corona S.A.S --- Corona SAS
# Se hace un diccionario con todos los correctos e incorrectos
# Mantedremos el caso Mayusculas conminusculas
SUPPLIER_REPLACEMENTS = {
    "BANCOLOMBIA S.A.": "Bancolombia S.A.",
    "Corona SAS": "Corona S.A.S.",
    "Ecopetrol  S.A.": "Ecopetrol S.A.",
    "GOOGLE COLOMBIA LTDA.": "Google Colombia Ltda.",
    "Grupo  Éxito  S.A.": "Grupo Exito S.A.",
    "Grupo Éxito S.A.": "Grupo Exito S.A.",
    "MICROSOFT COLOMBIA INC.": "Microsoft Colombia Inc.",
    "POSTOBÓN S.A.": "Postobon S.A.",
    "SAP Colombia SAS": "SAP Colombia S.A.S.",
    "Schneider  Electric": "Schneider Electric",
    "Sura  S.A.": "Sura S.A.",
    "Telefónica  Colombia": "Telefónica Colombia",
    "SIEMENS S.A.S.": "Siemens S.A.S.",
    "siemens s.a.s.": "Siemens S.A.S.",
    "oracle colombia ltda.": "Oracle Colombia Ltda.",
    "ibm colombia s.a.s.": "IBM Colombia S.A.S.",
    "IBM Colombia SAS.": "IBM Colombia S.A.S.",
    "nutresa s.a.": "Nutresa S.A.",
    "Nutresa SA": "Nutresa S.A.",
    "amazon web services colombia": "Amazon Web Services Colombia",
    "Cementos Argos SA": "Cementos Argos S.A.",
    "cementos argos s.a.": "Cementos Argos S.A.",

}
def clean_supplier_column(df):
    df['supplier'] = df['supplier'].str.strip() # Se eliminan los espacios en blanco al inicio y al final para evitar diferencias accidentales en los nombres
    
    df['supplier'] = df['supplier'].replace(SUPPLIER_REPLACEMENTS)
    return df





def main():
    df = pd.read_csv(INPUT_FILE)
    df = clean_column_names(df)
    df = clean_supplier_column(df)
    df.to_csv(OUTPUT_FILE, index=False)
    

if __name__ == "__main__":
    main()
