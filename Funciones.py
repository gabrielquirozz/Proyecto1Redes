'''
Gabriel Quiroz 19255
Proyecto 1 Redes
'''

import logging
from getpass import getpass
from argparse import ArgumentParser
import slixmpp as xmpp
import xmpp as xm
from slixmpp.exceptions import IqError, IqTimeout
from aioconsole import ainput


class Cliente(xmpp.ClientXMPP):
    def __init__(self, jid, password):
        xmpp.ClientXMPP.__init__(self, jid, password)
        self.jid = jid
        self.password = password
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("register", self.registration)
        self.add_event_handler("message", self.mensajes)
        self.add_event_handler('changed_status', self.changedStatus)
        self.add_event_handler('got_offline', self.userOffline)
        self.add_event_handler('presence_subscribed', self.userSubscribed)

    async def start(self, event):
        self.send_presence()

        def message():
            to = input("Para: ")
            msg = input("Mensaje: ")
            self.send_message(mto= to, mbody= msg, mtype='chat')
            print("Se envio el mensaje\n")

        def cerra_sesion():
            self.disconnect()
            print("Se cerro sesion\n")

        def newContact():
            usuario = input("Usuario:\n")
            self.send_presence_subscription(pto=usuario)
            print("Se agrego el contacto\n")

        def deleteAccount():
            self.register_plugin('xep_0030') 
            self.register_plugin('xep_0004')
            self.register_plugin('xep_0077')
            self.register_plugin('xep_0199')
            self.register_plugin('xep_0066')

            eliminar = self.Iq()
            eliminar['type'] = 'set'
            eliminar['from'] = self.boundjid.user
            eliminar['register']['remove'] = True
            eliminar.send()
            
            self.disconnect()
            print("Se elimino la cuenta\n")

        def showContacts():
            print('Contactos\n')
            print()
            contactos = self.client_roster.groups()
            for contacto in contactos:
                for jid in contactos[contacto]:
                 
                    usuario = self.client_roster[jid]['name']
                    if usuario:
                        pass
                    else:
                        print('Usuario: ', jid)

                
                    conectados = self.client_roster.presence(jid)
                    for res, presencia in conectados.items():
                        show = 'conectado'
                        if presencia['show']:
                            show = presencia['show']
                        print("     INFO:")
                        print('        ', show)
                        if presencia['status']:
                            print('     Estado: ', presencia['status'])
        
        def changeState():
            estado = input("Ingresar estado:\n")
            info = input("Ingresar informacion:\n")
            self.send_presence(pshow=info, pstatus=estado)
            print("Se cambio el estado\n")

        def detailAccount():
            self.get_roster()
            usuario = input("Usuario: ")
            contactos = self.client_roster.presence(usuario)
            for res, presencia in contactos.items():
                show = 'chat'
                if presencia['show']:
                    show = presencia['show']
                print('        ', show)
                print('     Estado: ', presencia['status'])


            
       
        menu = True
        while menu:
            opcion = input("1. Chat\n2. Chat grupal\n3. Anadir Contacto\n4. Detalles de un contacto\n5. Mostrar todos los contactos\n6. Cambiar estado\n7. Eliminar cuenta\n8. Cerrar sesion\n")
            if opcion == "1":
                message()

            elif opcion == "2":
                print("----------------------------------CHAT GRUPAL-------------------------------------")
                sop = input("1. Unirse a grupo\n2. Enviar mensaje\n")
                if(sop == "1"):
                    print()
                    grupo = input("Ingrese el nombre del grupo: ")
                    alias = input("Ingrese el alias: ")
                    self.joinGroup(grupo,alias)
                if(sop== "2"):
                    grupo = input("Ingrese el nombre del grupo: ")
                    mensaje = input("Ingrese el mensaje: ")
                    self.chatGroup(grupo,mensaje)


            elif opcion == "3":
                newContact()

            elif opcion == "4":
                detailAccount()

            elif opcion == "5":
                showContacts()

            elif opcion == "6":
                changeState()

            elif opcion == "7":
                deleteAccount()

            elif opcion == "8":
                cerra_sesion()
                menu = False

            await self.get_roster()

    def changedStatus(self, presencia):
        print(str(presencia["from"]) + " Cambio el estado a " + str(presencia["show"])+"\n")


    def userOffline(self, presencia):
        print(str(presencia["from"]) + " Se desconecto\n")

    def userSubscribed(self, presencia):
        print(str(presencia["from"]) + " Te envio solicitud de amistad\n")

    def joinGroup(self, grupo, alias):
        self.plugin['xep_0045'].join_muc(grupo, alias)
        print("Ahora perteneces al grupo\n")

    def chatGroup(self, recipiente, mensaje):
        try:
            self.send_message(mto=recipiente, mbody=mensaje, mtype='groupchat')
            print('Se envio el mensaje\n')
        except IqError:
            print('Error al enviar el mensaje')
        except IqTimeout:
            print('No hay respuesta del server')
        
    async def mensajes(self, mensaje):
        logging.info(mensaje)
        print()
        print("            CHAT           ")
        usuario = str(mensaje["from"]).split("/")
        usuario_mostar = usuario[0]
        mensaje = mensaje["body"]
        print(usuario_mostar , ": ", mensaje)
        print()

    async def registration(self, iq):
        self.send_presence()
        self.get_roster()

        resp = self.Iq()
        resp['type'] = 'set'
        resp['register']['username'] = self.boundjid.user
        resp['register']['password'] = self.password

        try:
            await resp.send()
            logging.info("Account created for %s!" % self.boundjid)
        except IqError as e:
            logging.error("Could not register account: %s" %
                    e.iq['error']['text'])
            self.disconnect()

    def login():
        # Setup the command line arguments.
        parser = ArgumentParser(description=Cliente.__doc__)

        # Output verbosity options.
        parser.add_argument("-q", "--quiet", help="set logging to ERROR",
                            action="store_const", dest="loglevel",
                            const=logging.ERROR, default=logging.INFO)
        parser.add_argument("-d", "--debug", help="set logging to DEBUG",
                            action="store_const", dest="loglevel",
                            const=logging.DEBUG, default=logging.INFO)

        usuario = input("Usuario: ")
        password = getpass("Contraseña: ")

        xmpp = Cliente(usuario, password)
        xmpp.register_plugin('xep_0030') 
        xmpp.register_plugin('xep_0199')
        xmpp.register_plugin('xep_0045') 

        # Connect to the XMPP server and start processing XMPP stanzas.
        xmpp.connect(disable_starttls=True)
        xmpp.process(forever=False)

    def register():
        usuario = input("Ingresa el usuario a registrar: ")
        password = input("Contrasena: ")
        jid = xm.JID(usuario)
        cli = xm.Client(jid.getDomain(), debug=[])
        cli.connect()

        if xm.features.register(cli, jid.getDomain(), {'username': jid.getNode(), 'password': password}):
            print("Registrado correctamente\n")
            return True
        else:
            return False
