import os
import shutil
import string
from pathlib import Path
import glob
import time
ACTIVITY_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FOLDER = os.path.join(ACTIVITY_FOLDER , "data")
INPUT_FOLDER= os.path.join(ACTIVITY_FOLDER, "temp", "input")
OUTPUT_FOLDER = os.path.join(ACTIVITY_FOLDER, "temp", "output")
SUBMISSION_FOLDER = os.path.join(ACTIVITY_FOLDER, "submission")

if os.path.exists(INPUT_FOLDER):
    for file in glob.glob(f"{INPUT_FOLDER}/*"):
        os.remove(file)

else:
    os.makedirs(INPUT_FOLDER)

# Generr copias del arvhivo en raw/

n = 1000
for file in glob.glob(f"{DATA_FOLDER}/*"):

    with open(file, "r", encoding="utf-8") as f:
        text = f.read()

    for i in range(1, n + 1):
        raw_filename_with_extension = os.path.basename(file)
        raw_filename_without_extension = os.path.splitext(raw_filename_with_extension)[
            0
        ]

        new_filename = f"{raw_filename_without_extension}_{i:05d}.txt"

        with open(f"{INPUT_FOLDER}/{new_filename}", "w", encoding="utf-8") as f2:
            f2.write(text)


# Como funciona un sistem hadoop

# Lectura de archivos

start_time = time.time()
sequence = []
files = glob.glob(f"{INPUT_FOLDER}/*")
for file in files:
    with open(file, "r", encoding="utf-8") as f:
        for line in f:
            sequence.append((file, line))

# Mapper
# Toma el texto y cada palabra la convierte en clave-valor
pairs_sequence = []
for _, line in sequence:
    line = line.lower() # convierte a minusculas
    line = line.translate(str.maketrans("", "", string.punctuation)) # elimina signos de puntuacion
    line = line.replace("\n", "") # reemplazar \n por " "
    words = line.split(" ") # Separa cada " " y hace lista
    pairs_sequence.extend([(word, 1) for word in words if word])

# shufle and sort: Agrupa y ordena los pares por clave

pairs_sequence = sorted(pairs_sequence)


# Reducer: Suma los valores de cada clave y genera un nuevo par clave-valor

result = []
for key, value in pairs_sequence:
    if result and result[-1][0] == key:
        result[-1] = (key, result[-1][1] + value)
    else:
        result.append((key, value))

# La carpeta de salida debe estar vacia

if os.path.exists(OUTPUT_FOLDER):
    for file in glob.glob(f"{OUTPUT_FOLDER}/*"):
        os.remove(file)
# Si la carpeta existe, en un sistema hadoop falla
else:
    os.makedirs(OUTPUT_FOLDER)

# Archivo con el conteo

with open(f"{OUTPUT_FOLDER}/part-00000", "w", encoding="utf-8") as f:
    for key, value in result:
        f.write(f"{key}\t{value}\n")

# Marcador de exito

with open(f"{OUTPUT_FOLDER}/_SUCCESS", "w", encoding="utf-8") as f:
    f.write("")
# Copiar el resultado desde HDFS simulado al disco local

if  os.path.exists(SUBMISSION_FOLDER):
    for file in glob.glob(f"{SUBMISSION_FOLDER}/*"):
        os.remove(file)
else:
    os.makedirs(SUBMISSION_FOLDER)

for file in glob.glob(f"{OUTPUT_FOLDER}/*"):
    shutil.copy2(file, SUBMISSION_FOLDER)

end_time = time.time()
print(f"Tiempo de ejecución: {end_time - start_time:.2f} segundos")