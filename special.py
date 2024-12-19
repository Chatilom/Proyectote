import os
import string
import datetime

def encrypt(password, displacement):
    encrypt_text = ""
    for character in password:
        if character == "ñ":  # La ñ no es cifrada en este caso
            encrypt_text += character
        elif character.isalpha():  # Verifica si el carácter es una letra
            base = ord("A") if character.isupper() else ord("a")
            # Aplica el desplazamiento y ajusta el rango para cifrar y descifrar correctamente
            encrypt_text += chr((ord(character) - base + displacement) % 26 + base)
        elif character.isdigit():
            base = ord("0")
            encrypt_text += chr((ord(character) - base + displacement) %10 + base)
        else:
            encrypt_text += chr((ord(character) + displacement) % 128)
    return encrypt_text

def check(): #se llama durante la ejecucion login o create account en caso de que la base de datos se elimine durante la ejecucion
    global database , users_file , admins_file , history_file , admins , users , admin_history
    directory = os.path.dirname(os.path.abspath(__file__))

    #BASE DE DATOS
    database = os.path.join(directory , "DataBase")
    if not os.path.exists(database):
        os.makedirs(database)
    #ARCHIVOS DE TEXTO PRINCIPALES
    users_file = os.path.join(database , "users.txt")
    if not os.path.isfile(users_file):
        with open(users_file , "w") as f:
            f.write("")

    admins_file = os.path.join(database , "admins.txt")
    if not os.path.isfile(admins_file):
        with open(admins_file , "w") as f:
            f.write("")

    history_file = os.path.join(database , "history.txt")#historial de: creacion/eliminación de cuentas e incios de sesión
    if not os.path.isfile(history_file):
        with open(history_file , "w") as f:
            f.write("")

    #CARPETAS PRINCIPALES
    admins = os.path.join(database , "Admins")
    if not os.path.exists(admins):
        os.makedirs(admins)

    users = os.path.join(database , "Users")
    if not os.path.exists(users):
        os.makedirs(users)

    admin_history = os.path.join(admins , "admin_history.txt")
    if not os.path.exists(admin_history):
        with open(admin_history , "w") as f:
            f.write("")

def security_check(password):#minimo 6 caracteres, un caracter especial, un numer #de momento no se usa en el codigo
        numbers = list(string.digits)
        special = list(string.punctuation)
        check_number = False
        check_special = False
        if len(password) < 6:
            return False
        for i in password:
            if i in numbers:
                check_number = True
                break
        for i in password:
            if i in special:
                check_special = True
                break
        if check_number and check_special:
            return True
        else:
            return False
        
def add_general_history(send):
    moment = datetime.datetime.strftime(datetime.datetime.now() , "%d:%m:%Y - %H:%M:%S")
    with open(history_file , "a" , encoding="utf-8") as f:
        f.write(f'{moment}: {send}\n')
    return

def add_user_history(send , user):
    moment = datetime.datetime.strftime(datetime.datetime.now() , "%d:%m:%Y - %H:%M:%S")
    file = os.path.join(users , user , "history.txt")
    with open(file , "a" , encoding="utf-8") as f:
        f.write(f'{moment}: {send}\n')
    return

def add_admin_history(send):
    moment = datetime.datetime.strftime(datetime.datetime.now() , "%d:%m:%Y - %H:%M:%S")
    with open(admin_history , "a" , encoding="utf-8") as f:
        f.write(f'{moment}: {send}\n')
        
def create_user(user , password):
    with open(users_file , "a") as file: #escribir en la base de datos de usuarios
        file.write(f'{user} {encrypt(password , 4)}\n')
        #crear la carpeta del usuario
    
    user_file = os.path.join(users , user) #crea una carpeta para el usuario
    os.makedirs(user_file)

    files = os.path.join(user_file , "files")
    os.makedirs(files)

    user_text = os.path.join(files , "text.txt")
    with open(user_text , "w") as f:
        f.write("")

    user_history_file = os.path.join(user_file , "history.txt")
    with open(user_history_file , "w") as f:
        f.write("")

def add_admin(user , password):
    with open(admins_file , "a") as f:
        f.write(f'{user} {encrypt(password , 4)}')
    os.makedirs(os.path.join(admins , f'{user}'))

def get_admin_list(): #se usa para la verificacion de usuarios
    admin_list = []
    with open(admins_file , "r") as f:
        for line in f.readlines():
            admin_list.append(line.split(" " , 1)[0])#se divide la linea en dos partes separadas con el primer hueco vacio
    return admin_list                                  #y se elige el primer elementos

def get_users_list():
    users_list = []
    with open(users_file , "r") as f:
        for line in f.readlines():
            users_list.append(line.split(" " , 1)[0])
    return users_list

def get_user_files(user): #obtener la lista de archivos ORDENADOS
    files = os.listdir(os.path.join(users , user , "files"))
    return files







