import firebase_admin
from firebase_admin import credentials, firestore
from time import sleep
from threading import Thread
import discord
import time


class Base:
    def __init__(self):
        cred = credentials.Certificate("database/serviceAccountKey.json")
        try:
            firebase_admin.initialize_app(cred)
        except:
            firebase_admin.get_app()

        self.db = firestore.client()
        self.data = {
            "imnotfunny": {
                "id": 732876803412328499,
                "words": 11,
                'latest daily': int(time.time() - 86401),
                'streak': 0
            }
        }
        self.links = {}

        thread = Thread(target=self.update_data, daemon=False)
        thread.start()
        
    
    def update_data(self):
        while True:
            for doc, dat in self.data.items():
                doc_ref = self.db.collection('users').document(doc)
                
                if doc_ref.get().exists:
                    doc_ref.update(dat)
                else:
                    doc_ref.set(dat)
        
            sleep(600)
    
    def update_now(self):
        for doc, dat in self.data.items():
            doc_ref = self.db.collection('users').document(doc)
            
            if doc_ref.get().exists:
                doc_ref.update(dat)
            else:
                doc_ref.set(dat)
    
    def exists(self, user: discord.Member):
        doc = self.db.collection('users').document(user.name)
        return doc.get().exists