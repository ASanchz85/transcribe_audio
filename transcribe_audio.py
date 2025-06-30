#!/usr/bin/env python3

import argparse
import subprocess
import sys
import os
import time

def check_ffmpeg():
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except FileNotFoundError:
        return False

def check_whisper():
    try:
        import whisper
        return True
    except ImportError:
        return False

def install_ffmpeg():
    print("⚠️  ffmpeg no está instalado.")
    confirm = input("¿Deseas instalar ffmpeg automáticamente? [S/n]: ").strip().lower()
    if confirm in ["s", "sí", "y", ""]:
        if sys.platform.startswith("linux"):
            subprocess.run(["sudo", "apt", "update"])
            subprocess.run(["sudo", "apt", "install", "-y", "ffmpeg"])
        elif sys.platform == "darwin":
            subprocess.run(["brew", "install", "ffmpeg"])
        elif sys.platform == "win32":
            print("🔗 Por favor, descarga manualmente ffmpeg desde https://ffmpeg.org/download.html")
            sys.exit(1)
        else:
            print("❌ Sistema operativo no soportado para instalación automática de ffmpeg.")
            sys.exit(1)

def install_whisper():
    print("⚠️  El paquete whisper no está instalado.")
    confirm = input("¿Deseas instalar whisper automáticamente? [S/n]: ").strip().lower()
    if confirm in ["s", "sí", "y", ""]:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "git+https://github.com/openai/whisper.git"])

def transcribe(file: str, model_name: str, output: str):
    import whisper

    print(f"🔄 Cargando modelo '{model_name}'...")
    model = whisper.load_model(model_name)

    print(f"🎧 Transcribiendo archivo: {file}")
    result = model.transcribe(file)

    with open(output, "w", encoding="utf-8") as f:
        f.write(result["text"])

    print(f"✅ Transcripción guardada en: {output}")

def main():
    parser = argparse.ArgumentParser(description="Transcribe audio using OpenAI Whisper.")
    parser.add_argument("-f", "--file", type=str, default="audio.mp3", help="Archivo de audio (por defecto: audio.mp3)")
    parser.add_argument("-m", "--model", type=str, default="base", choices=["tiny", "base", "small", "medium", "large"], help="Modelo a usar (por defecto: base)")
    parser.add_argument("-o", "--output", type=str, help="Nombre del archivo de salida (.txt)")

    args = parser.parse_args()

    if not os.path.isfile(args.file):
        print(f"❌ Archivo no encontrado: {args.file}")
        sys.exit(1)

    if not check_ffmpeg():
        install_ffmpeg()
        time.sleep(2)

    if not check_whisper():
        install_whisper()
        time.sleep(2)

    output_file = args.output or f"{os.path.splitext(args.file)[0]}.txt"
    transcribe(args.file, args.model, output_file)

if __name__ == "__main__":
    main()
