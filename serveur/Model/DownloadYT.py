import os
import subprocess


class DownloadYT:

    def __init__(self, url):
        self.url = url


        
    def download_audio(self):
        """
        Extrait l'audio d'une vidéo YouTube au format wav.
        Utilise des options pour contourner certains problèmes de téléchargement.
        """
        try:
            # Supprimer l'ancien fichier si présent
            audio_file = "./serveur/data/audio_video.wav"
            if os.path.exists(audio_file):
                os.remove(audio_file)

            # Commande yt-dlp
            command = [
                "yt-dlp",
                "-f", "bestaudio",
                "--output", "./serveur/data/audio_video.webm",
                self.url
            ]
            subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)

            # conversion
            input_file = "./serveur/data/audio_video.webm"  
            output_file = "./serveur/data/audio_video.wav"
            command_convert = [
                "ffmpeg",
                "-i", input_file,  # Fichier source
                output_file  # Fichier de destination en wav
            ]
            subprocess.run(command_convert, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)

            return True
        except subprocess.CalledProcessError as e:
            print(f"Erreur lors du téléchargement : {e.stderr.decode()}")
            return False
        except Exception as e:
            print(f"Erreur inattendue : {e}")
            return False


    


    

if __name__ == "__main__":
    download = DownloadYT("https://www.youtube.com/watch?v=fo-mVfOsC-E")
    print(download.audio_to_text())
    



    