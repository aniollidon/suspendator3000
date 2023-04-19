import ocr_onvideo as ocr
import find_text as ft
import os
import argparse

# Definir els paràmetres de configuració per defecte
ffmpeg_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ext\\ffmpeg.exe")
tesseract_path = f"C:\\Users\\user\\AppData\\Local\\Programs\\Tesseract-OCR\\tesseract.exe"

# Crear el parser d'arguments
parser = argparse.ArgumentParser(description='Suspendator 2000')
parser.add_argument('input_dir', type=str, help='Carpeta on es troben els vídeos')
parser.add_argument('-o', '--output_dir', type=str, help='Directori on es guarden les dades processades', default="")
parser.add_argument('-r', '--sampling-rate', type=str, help='Freqüencia de mostreig dels vídeos (segons)', default=10)
parser.add_argument('-f', '--forbidden-words', type=str, help='Llista de paraules prohibides (separades per comes)', 
                    default="chat,claude,dragon,sage,poe")

parser.add_argument('-s','--skip', action="store_true", help='Evita calcular OCR de nou', default=False)

# Analitzar els arguments de la línia d'ordres
args = parser.parse_args()

if(args.output_dir == ""):
    args.output_dir = os.path.join(args.input_dir, "out")

forbidden_words = args.forbidden_words.split(",")

videos = os.listdir(args.input_dir)

if (videos.__len__() == 0):
    print("No hi ha vídeos a processar")
    exit(0)

# Si output_dir no existeix, crear-lo
if not os.path.exists(args.output_dir):
    os.makedirs(args.output_dir)

results = []

for video in videos:
    ext = os.path.splitext(video)[-1]
    if ext in [".mp4", ".avi", ".mov", ".mkv"]:
        video_path = f"{args.input_dir}/{video}"
        
        # Definir la ruta del directori de sortida dels fitxers de text OCR
        output_dir = os.path.join(args.output_dir, os.path.splitext(video)[0])

        # Si output_dir no existeix, crear-lo
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        if(not args.skip):
            print(f"Processant {video_path}")
            ocr.to_ocr(video_path, output_dir, ffmpeg_path, tesseract_path, args.sampling_rate)

    results.append(ft.find_text(output_dir, forbidden_words))

for res in results:
    frame_sampling_rate = res["frame_sampling_rate"]
    video = res["origin"]

    print(f"Results on {video}")

    for det in res["detections"]:

        frame = det["frame"]

        # Calculem el temps en segons del frame
        timestamp_seconds = frame * frame_sampling_rate
                                        
        # Calculem els minuts i segons del frame
        hours = timestamp_seconds // 3600
        minutes = (timestamp_seconds % 3600) // 60
        seconds = timestamp_seconds % 60

        text = f"Frame {frame}: {hours:02d}:{minutes:02d}:{seconds:02d} - {det['word']}"

        print(text)


 