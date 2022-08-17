'''
Gabriel Quiroz 19255
Proyecto 1 Redes
'''

import logging
from getpass import getpass
from argparse import ArgumentParser
import slixmpp as xmpp
from Funciones import Cliente
from aioconsole import ainput

print("BIENVENIDO AL CHAT GRUPAL ALUMCHAT\n")
opcion = int(input("1. Login\n2. Registrar\n3. Salir\n"))

if opcion == 1:
    print("LOGIN\n")
    Cliente.login()
elif opcion == 2:
    print("REGISTRARSE\n")
    Cliente.register()
elif opcion == 3:
    print("SALIENDO...\n")
    exit()

