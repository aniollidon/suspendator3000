import os
#import cv2

def find_text(input_dir, forbidden_words):
    # Comprova si existeix el directori d'entrada
    if not os.path.exists(input_dir):
        print(f"El directori {input_dir} no existeix")
        exit()

    # Comprova si existeix el fitxer de metadades
    if not os.path.exists(f"{input_dir}/metadata.txt"):
        print(f"El fitxer de metadades {input_dir}/metadata.txt no existeix")
        exit()

    # Obre un fitxer amb metadates
    with open(f"{input_dir}/metadata.txt", "r", encoding="utf8") as f:
        metadata = f.read()
        # Llegeix el sample rate
        frame_sampling_rate = int(metadata.split("\n")[1].split(":")[1].strip())

    detections = []

    # Recórrer tots els fitxers de la carpeta d'entrada
    for file in os.listdir(input_dir):
        if file.endswith(".txt") and not file == "metadata.txt":
            # Definir la ruta completa de l'arxiu de text
            text_path = os.path.join(input_dir, file)
            # Obrir l'arxiu de text i llegir el contingut
            with open(text_path, "r", encoding="utf8") as f:
                text = f.read()
                # Obtindre el número de frame de l'arxiu d'imatge a partir del nom del fitxer de text
                frame_number = int(file.replace("frame_", "").replace(".txt", ""))

                local_dets = []
                # Comprovar si hi ha alguna de les paraules prohibides
                for word in forbidden_words:
                    if word in text.lower():
                        local_dets.append(word)
                
                if(len(local_dets) > 0):
                    detections.append({"frame":frame_number, "words":  ", ".join(local_dets)})

    return {"detections": detections, "frame_sampling_rate": frame_sampling_rate, "origin": metadata.split("\n")[0].split(":")[1].strip()}