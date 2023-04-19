# suspendator3000

Cal descarregar i descomprimir [ffmpeg.exe](https://www.gyan.dev/ffmpeg/builds/packages/ffmpeg-2023-03-20-git-57afccc0ef-full_build.7z) a la carpeta ext.

També caldrà descarregar i instal·lar la llibrereia d'OCR [tesseract](https://tesseract-ocr.github.io/tessdoc/Installation.html). Possiblement caldrà actualitzar el fitxer `main.py` amb la ruta corresponent d'aquests dos executables.

## Execució

Comandes disponibles:
```cmd
python main.py --help

positional arguments:
  input_dir             Carpeta on es troben els vídeos

options:
  -h, --help            show this help message and exit
  -o OUTPUT_DIR, --output_dir OUTPUT_DIR
                        Directori on es guarden les dades processades
  -r SAMPLING_RATE, --sampling-rate SAMPLING_RATE
                        Freqüencia de mostreig dels vídeos (segons)
  -f FORBIDDEN_WORDS, --forbidden-words FORBIDDEN_WORDS
                        Llista de paraules prohibides (separades per comes)
  -s, --skip            Evita calcular OCR de nou
```

Exemple per processar una carpeta de vídeos tot agafant el frame cada 30s i filtrar per les paraules "chat", "google" i "boscdelacoma.cat":
```cmd
python main.py carpeta/amb/videos/alumnes -r30 -f chat,google,boscdelacoma.cat
```

Fer-ho de nou evitant recalcular l'OCR, (només volem canviar el filtre).
```cmd
python main.py carpeta/amb/videos/alumnes --skip -f patata
```


