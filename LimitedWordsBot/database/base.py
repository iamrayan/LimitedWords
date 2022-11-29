import firebase_admin
from firebase_admin import credentials, firestore
from time import sleep
import asyncio
import discord
from discord.ext import commands
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
            str(732876803412328499): {
                "words": float("inf"),
                'latestdaily': int(time.time() - 86401),
                'streak': 0
            }
        }
        self.links = {}
        self.prisoners = {}

        asyncio.run(self.update_data())
        asyncio.run(self.prison_check())
        
    
    async def update_data(self):
        while True:
            for doc, dat in self.data.items():
                doc_ref = self.db.collection('users').document(doc)
                
                if doc_ref.get().exists:
                    doc_ref.update(dat)
                else:
                    doc_ref.set(dat)

            for prisoner, data in self.prisoners.items():
                doc_ref = self.db.collections('prisoners').document(prisoner.id)

                if doc_ref.get().exists:
                    doc_ref.update(data)
                else:
                    doc_ref.set(data)
            
            await asyncio.sleep(600)
    
    async def prison_check(self):
        while True:
            await asyncio.sleep(60)

            for prisoner, data in self.prisoners.items():
                if data["time"] >= time.time():
                    await prisoner.remove_roles(prisoner.guild.get_role(1046101250468487168))

                    del self.prisoners[prisoner]
    
    def update_now(self):
        for doc, dat in self.data.items():
            doc_ref = self.db.collection('users').document(doc)
            
            if doc_ref.get().exists:
                doc_ref.update(dat)
            else:
                doc_ref.set(dat)
        
        for prisoner, data in self.prisoners.items():
                doc_ref = self.db.collections('prisoners').document(prisoner.id)

                if doc_ref.get().exists:
                    doc_ref.update(data)
                else:
                    doc_ref.set(data)
    
    def exists(self, user: discord.Member):
        doc = self.db.collection('users').document(str(user.id))
        return doc.get().exists