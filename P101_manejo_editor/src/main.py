import glob
import os.path
import shutil
import string
import time
from pathlib import Path

ACTIVITY_DIR = Path(__file__).resolve().parents[1]
DATA_FOLDER = ACTIVITY_DIR / "data"
FOLDER = ACTIVITY_DIR / "temp" / "input"
SUBMISSION_FOLDER = ACTIVITY_DIR / "submission"
folder = SUBMISSION_FOLDER

# La carpeta input/ debe existir y estar vacia.
# -----------------------------------------------------------------------------

def clear_folder(input_folder):
    for file in glob.glob(f"{input_folder}/*"):
        os.remove(file)

def initialize_folder(folder):
    if os.path.exists(folder):
        clear_folder(folder)
    else:
        os.makedirs(folder)


def delete_folder(folder):
    if os.path.exists(folder):
        shutil.rmtree(folder)


# Genera copias de los archivos en raw/
# -----------------------------------------------------------------------------

def generate_file_copies( n):
    for file in glob.glob(f"{DATA_FOLDER}/*.txt"):
        with open(file, "r", encoding="utf-8") as f:
            text = f.read()

        for i in range(1, n + 1):
            raw_filename_with_extension = os.path.basename(file)

            raw_filename_without_extension = os.path.splitext(raw_filename_with_extension)[
            0
        ]

            new_filename = f"{raw_filename_without_extension}_{i:05d}.txt"

            with open(f"{FOLDER}/{new_filename}", "w", encoding="utf-8") as f2:
                f2.write(text)



# Mapper
# -----------------------------------------------------------------------------

def mapper(sequence):
    pairs_sequence = []
    for _, line in sequence:
        line = line.lower()
        line = line.translate(str.maketrans("", "", string.punctuation))
        line = line.replace("\n", "")
        words = line.split()
        pairs_sequence.extend([(word, 1) for word in words])
    return pairs_sequence



# Reducer
# -----------------------------------------------------------------------------

def reducer(pairs_sequence):
    result = []
    for key, value in pairs_sequence:
        if result and result[-1][0] == key:
            result[-1] = (key, result[-1][1] + value)
        else:
            result.append((key, value))
    return result

#-------------------------------------------------------------------
def hadoop(
    input_folder,
    ouput_folder,
    mapper,
    reducer,


):
    def read_records_from_imput():
        sequence = []
        files = glob.glob(f"{input_folder}/*")
        for file in files:
            with open(file, "r", encoding="utf-8") as f:
                for line in f:
                    sequence.append((file, line))
        return sequence

    def shuffle_and_sort(pairs_sequence):
        pairs_sequence = sorted(pairs_sequence)
        return pairs_sequence


    def save_result_to_ouput( result):
        with open(f"{ouput_folder}/part-00000", "w", encoding="utf-8") as f:
            for key, value in result:
                f.write(f"{key}\t{value}\n")

    def create_sucess_file():
        with open(f"{ouput_folder}/_SUCCESS", "w", encoding="utf-8") as f:
            f.write("")


    sequence = read_records_from_imput()
    pairs_sequence = mapper(sequence)
    pairs_sequence = shuffle_and_sort(pairs_sequence)
    result = reducer(pairs_sequence)
    initialize_folder(ouput_folder)

    save_result_to_ouput(result)

    create_sucess_file()

# ----------------------------------------------------------------------------



n = 1000

initialize_folder(FOLDER)
generate_file_copies(n)

start_time = time.time()

hadoop(
    input_folder=FOLDER,
    ouput_folder=folder,
    mapper=mapper,
    reducer=reducer,
)

# Reporte de tiempo de ejecución
# -----------------------------------------------------------------------------

end_time = time.time()
print(f"Tiempo de ejecución: {end_time - start_time:.2f} segundos")
