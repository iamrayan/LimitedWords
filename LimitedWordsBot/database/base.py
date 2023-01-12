import firebase_admin
from firebase_admin import credentials, firestore
from time import sleep
import asyncio
import discord
from time import sleep, time
from threading import Thread

class Base:
    def __init__(self):
        cred = credentials.Certificate("database/serviceAccountKey.json")
        try:
            firebase_admin.initialize_app(cred)
        except:
            firebase_admin.get_app()

        self.db = firestore.client()
        self.data = {}
        self.links = {}
        self.prisoners = {}

        Thread(target=self.update_data).start()
        Thread(target=self.prison_check).start()
        
    
    def update_data(self):
        while True:
            sleep(300)

            for doc, dat in self.data.items():
                doc_ref = self.db.collection('users').document(doc)
                
                if doc_ref.get().exists:
                    doc_ref.update(dat)
                else:
                    doc_ref.set(dat)

            for prisoner, data in self.prisoners.items():
                doc_ref = self.db.collection('prisoners').document(str(prisoner.id))
                
                if doc_ref.get().exists:
                    doc_ref.update(data)
                else:
                    doc_ref.set(data)
    
    async def prison_check(self):
        while True:
            sleep(60)

            for prisoner, data in self.prisoners.items():
                if data["time"] <= time():
                    self.release_prisoner(prisoner)
    
    def update_now(self):
        for doc, dat in self.data.items():
            doc_ref = self.db.collection('users').document(doc)
            
            if doc_ref.get().exists:
                doc_ref.update(dat)
            else:
                doc_ref.set(dat)
        
        for prisoner, data in self.prisoners.items():
                doc_ref = self.db.collection('prisoners').document(str(prisoner.id))

                if doc_ref.get().exists:
                    doc_ref.update(data)
                else:
                    doc_ref.set(data)
    
    def exists(self, user: discord.Member):
        doc = self.db.collection('users').document(str(user.id))
        return doc.get().exists
    
    async def release_prisoner(self, prisoner):
        await prisoner.remove_roles(prisoner.guild.get_role(1046101250468487168))
        await prisoner.add_roles(prisoner.guild.get_role(1039442856177307658))
        delay_words = self.data[str(prisoner.id)]["delayed"]
        self.data[str(prisoner.id)]["words"] = self.data[str(prisoner.id)]["words"] + delay_words
        self.data[str(prisoner.id)]["delayed"] = 0

        words = self.data[str(prisoner.id)]["words"]

        asyncio.run(prisoner.edit(nick=f"[{words}] {prisoner.name}"))

        self.prisoners.pop(prisoner)
