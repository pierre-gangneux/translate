import os
import shutil
import time
import whisper
import warnings

warnings.filterwarnings("ignore", message="FP16 is not supported on CPU")

from serveur.Model.DownloadYT import DownloadYT
from serveur.Model.SplitAudio import SplitAudio


class SpeechToText:
    def __init__(self, url, id_video, type_model="small", file_name = "./serveur/data/audio_video.wav"):
        self.text_file = "./serveur/data/text/"+id_video+".txt"
        if not os.path.exists(self.text_file):
            self.audio = DownloadYT(url).download_audio()
            self.model = whisper.load_model(type_model) # Choisir entre "tiny", "base", "small", "medium", "large"
            self.file_name = file_name
            self.present = False
            self.text = None
        else:
            self.present = True
            with open(self.text_file, "r", encoding="utf-8") as f:
                self.text = f.read()



    def audio_to_text(self) -> str:
        if self.present:
            return self.text
        text_file = "./serveur/data/text/"+self.id_video+".txt"
        # Vérifier si le fichier texte existe déjà
        if os.path.exists(text_file):
            with open(text_file, "r", encoding="utf-8") as f:
                return f.read()  # Retourne directement le texte
        if self.audio:
            print("audio ok")
            result = self.model.transcribe(self.file_name) 
            with open(text_file, "w") as f:
                f.write(result["text"])
            return result

        return "Erreur lors de l'extraction audio. Vérifiez l'URL fournie."
    
    def transcribe_live(self):
        if self.present:
            yield self.text
            print("pass")
            return
        if self.audio:  # Vérifie si l'audio est téléchargé et split
            split = SplitAudio(180)
            chunk_files = split.split_audio_lineaire()
            print(chunk_files)
            print("Audio téléchargé, début de la transcription...")

            temps = time.time()

            with open(self.text_file, "w", encoding="utf-8") as f:
                pass
            
            for path in chunk_files:
                temps_temp = time.time()
                result = self.model.transcribe(path)
                for segment in result["segments"]:
                    start_time = segment["start"]
                    end_time = segment["end"]
                    text = segment["text"]

                    # Affichage immédiat dès qu'un segment est prêt
                    print(f"[{start_time:.2f}s - {end_time:.2f}s] {text}")
                    # Écriture immédiate dans le fichier pour sauvegarde progressive
                    with open(self.text_file, "a", encoding="utf-8") as f:
                        f.write(f"[{start_time:.2f}s - {end_time:.2f}s] {text}\n")   
                        yield f"[{start_time:.2f}s - {end_time:.2f}s] {text}\n"
                print("ségment ok !")
                print("temps : "+ str(time.time()-temps_temp))
            print("temps total: "+ str(time.time()-temps))

            if os.path.exists("./serveur/data/chunks/"):
                shutil.rmtree("./serveur/data/chunks/")
        else:
            yield "Erreur lors de l'extraction audio. Vérifiez l'URL fournie."
        
    