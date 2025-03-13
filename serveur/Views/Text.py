from flask import Response
from flask_restx import Namespace, Resource
from serveur.Model.SpeechToText import SpeechToText

ns = Namespace("text")
@ns.route("/<id_video>")
class Text(Resource):
    def get(self, id_video):
        """
        Permet d'obtenir la transcription écrite de la vidéo
        Attribut:
            id_video: représente la parti après "watch?v=". 
                        ex https://www.youtube.com/watch?v=Sw6BXNwbXlw => Sw6BXNwbXlw
    
        Returns:
            json: texte de la vidéo
        """
        url = "https://www.youtube.com/watch?v="+id_video
        return Response(SpeechToText(url, id_video).transcribe_live(), mimetype="text/plain")


    

