import os
import subprocess

def to_ocr(video_file, output_dir, ffmpeg_path, tesseract_path, frame_sampling_rate=30):

    # Comprova si existeix el directori de sortida
    if not os.path.exists(output_dir):
        print(f"El directori {output_dir} no existeix")
        exit()

    # Comprova si no hi ha dades a la carpeta de sortida
    if os.listdir(output_dir) :
        # si existeix el fitxer metadata.txt
        if not os.path.exists(f"{output_dir}/metadata.txt"):
            print(f"El directori {output_dir} no és buit i no conté el fitxer de metadades")
            exit()

        print(f"El directori {output_dir} no està buit, s'esborraran les dades")
        # Esborra tots els fitxers de la carpeta de sortida
        for file in os.listdir(output_dir):
            os.remove(os.path.join(output_dir, file))

    # Definir la comanda de ffmpeg
    ffmpeg_command = f"{ffmpeg_path} -i {video_file} -vf fps=1/{frame_sampling_rate} {output_dir}/frame_%03d.jpg"

    print (ffmpeg_command)

    # Executar la comanda de ffmpeg
    subprocess.call(ffmpeg_command, shell=True)

    # Recórrer tots els fitxers de la carpeta de sortida i fer OCR
    for file in os.listdir(output_dir):
        if file.endswith(".jpg"):
            # Definir la ruta completa de l'arxiu de la imatge
            image_path = os.path.join(output_dir, file)
            # Definir la ruta completa de l'arxiu de sortida del text OCR
            output_path = os.path.join(output_dir, file.replace(".jpg", ""))
            # Definir la comanda de Tesseract
            tesseract_command = f"{tesseract_path} {image_path} {output_path} -l eng"
            # Executar la comanda de Tesseract
            subprocess.call(tesseract_command, shell=True)

    # Escriu un fitxer amb metadates
    with open(f"{output_dir}/metadata.txt", "w", encoding="utf8") as f:
        f.write(f"Video file: {video_file} \n Frame sampling rate: {frame_sampling_rate}")