import firebase_admin
from firebase_admin import credentials, firestore
import asyncio
import discord
from time import time
from random import randint
from termcolor import colored
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

    async def update_data(self):
        while True:
            await asyncio.sleep(300)

            self.update_now()
            
            print(colored("System: ", "red") + colored("Database updated!", "green"))

    async def prison_check(self):
        while True:
            await asyncio.sleep(60)

            for prisoner, data in self.prisoners.items():
                if data["time"] <= time():
                    await self.release_prisoner(prisoner)

    
    def update_now(self):
        def update():
            print(colored("System: ", "red") + colored("Database updating...", "green"))

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
        
            print(colored("System: ", "red") + colored("Database updated!", "green"))
    
        Thread(target=update).start()
    
    def exists(self, user: discord.Member):
        doc = self.db.collection('users').document(str(user.id))
        return doc.get().exists
    
    async def release_prisoner(self, prisoner):
        await prisoner.remove_roles(prisoner.guild.get_role(1046101250468487168))
        await prisoner.add_roles(prisoner.guild.get_role(1039442856177307658))

        self.db.collection('prisoners').document(prisoner.id).delete()

        delay_words = self.data[str(prisoner.id)]["delayed"]

        words = self.data[str(prisoner.id)]["words"] + delay_words

        if words <= 25:
            words += randint(50, 100)

        self.data[str(prisoner.id)]["words"] = words
        self.data[str(prisoner.id)]["delayed"] = 0

        words = self.data[str(prisoner.id)]["words"]

        await prisoner.edit(nick=f"[{words}] {prisoner.name}")

        self.prisoners.pop(prisoner)

        print(colored("Prison: ", "yellow") + colored("Prisoner released!", "green"))