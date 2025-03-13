import os
import subprocess
import librosa


class SplitAudio():
    

    def __init__(self, duration_of_clip, input_file="./serveur/data/audio_video.wav", output_folder="./serveur/data/chunks" ):
        self.input_file=input_file
        self.output_folder=output_folder
        self.duration_of_clip = duration_of_clip
        # Charger l'audio pour obtenir sa durée
        self.audio, self.sr = librosa.load(self.input_file, sr=None)
        self.src_duration = int(len(self.audio) / self.sr)  # Durée totale en secondes
         # Créer le dossier s'il n'existe pas
        os.makedirs(self.output_folder, exist_ok=True)

    def split_audio_lineaire(self):    
        chunk_files = []
        count = 0

        for start_time in range(0, self.src_duration, self.duration_of_clip):
            end_time = min(start_time + self.duration_of_clip, self.src_duration)  # Ne pas dépasser la durée totale
            output_file = os.path.join(self.output_folder, f"chunk_{count}.wav")

            # Utilisation de FFmpeg directement
            command = [
                "ffmpeg", "-y",  # -y pour écraser les fichiers existants sans demander confirmation
                "-i", self.input_file,  # Fichier source
                "-ss", str(start_time),  # Début du segment
                "-to", str(end_time),  # Fin du segment
                "-c", "copy",  # Copier directement sans réencoder
                output_file  # Nom du fichier de sortie
            ]
            subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

            # Vérifier si le fichier a bien été créé et a du contenu
            if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
                chunk_files.append(output_file)
                count += 1
            else:
                print(f"Erreur : {output_file} est vide.")
            

        print(f"Découpage terminé ! {len(chunk_files)} morceaux créés.")
        return chunk_files  # Retourne la liste des fichiers
    
    def split_audio_double(self):    
        chunk_files = []
        count = 0
        init_duration_of_clip = self.duration_of_clip

        

        start_time=0
        while start_time <= self.src_duration:
            end_time = min(start_time + self.duration_of_clip, self.src_duration)  # Ne pas dépasser la durée totale
            output_file = os.path.join(self.output_folder, f"chunk_{count}.wav")

            # Utilisation de FFmpeg directement
            command = [
                "ffmpeg", "-y",  # -y pour écraser les fichiers existants sans demander confirmation
                "-i", self.input_file,  # Fichier source
                "-ss", str(start_time),  # Début du segment
                "-to", str(end_time),  # Fin du segment
                "-c", "copy",  # Copier directement sans réencoder
                output_file  # Nom du fichier de sortie
            ]
            subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

            # Vérifier si le fichier a bien été créé et a du contenu
            if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
                chunk_files.append(output_file)
                count += 1
            else:
                print(f"Erreur : {output_file} est vide.")

            #init le start_time
            start_time = start_time + self.duration_of_clip

            # double la durée du prochain clip
            self.duration_of_clip *= 2

        self.duration_of_clip = init_duration_of_clip
        print(f"Découpage terminé ! {len(chunk_files)} morceaux créés.")
        return chunk_files  # Retourne la liste des fichiers
    
    