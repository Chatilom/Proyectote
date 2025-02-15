from tkinter import *
import os
import datetime
import shutil
from special import *

#versión que incluye: mejoras en los sistemas de historiales

#AÑADIR VERIFICACIÓN AL CREAR NOMBRE CON CARACTERES ESPECIALES : / \ ...

#Funciones del administrador:
#-Eliminar cuentas a través de interfaz
#-congelar la ventana principal en la creación de administradores

#sistema se gestión de archivos de texto:
#-ordenar los archivos - tope chungo

#reconstruccion de los historiales:
#-añadir la codificación
#-barra de scroll
#-hacer el historial mas grande
#-crear función principal para el historial

#escribir con caracteres especiales ALT - en proceso...
#sistema de roles para un usuario administrador - EN PROCESO...
#sistema de gestión de varios archivos - en porceso... 
#reconstruccion de los historiales - en proceso...
#añadir que al pulsar enter en determinadas ventanas salte al proximo entry
#nuevas funciones para el usuario: ver sus estadísticas / personalizar su interfaz


def text_interface(user , password):
    files = get_user_files(user)
    ubication = os.path.join(users , user , "files")

    def text(user , password , file):
        select_text.destroy()
        user_file = os.path.join(users , user , "files") #carpeta donde se guardan los archivos
        file_write = os.path.join(user_file , f'{file}') #ruta del archivo en el que se escribe
        original_name = file[:-4] #nombre del archivo en el que se está escribiendo

        def info(send):
            info_label.config(text=send , font=("Arial" , 12))
            return

        def text_exit():
            text_root.destroy()
            text_interface(user , password)
            
        def set_text(): #elimina el texto antiguo y crea el nuevo
            insert = ""
            with open(file_write , "r" , encoding="utf-8") as f:
                insert = f.read()
            return insert
            
        def save():
            nonlocal original_name
            text_name = file_name_entry.get().strip() #obtiene el nombre del archivo

            def make_change():
                nonlocal file_write
                os.remove(file_write)
                save_text = user_text.get("1.0" , END)
                file_write = os.path.join(user_file , f'{text_name}.txt')
                with open(file_write , "w" , encoding="utf-8") as f:
                    f.write(save_text)
                add_user_history(send=f'You edited the file: {text_name}' , user=user)
                hour = datetime.datetime.strftime(datetime.datetime.now() , "%H:%M:%S")
                info(send=f'Text saved at {hour}')
            
            if text_name == original_name:
                make_change()
                return
            if (text_name + ".txt") in (get_user_files(user)):
                info(send="Name not disponible")
                return
            else:
                add_user_history(user=user , send=f'Name file changed: from {original_name} to {text_name}')
                make_change()
                original_name = text_name
        
        def delete_file_alert():
            delete_counter = 0
            
            def confirm_delete():
                nonlocal delete_counter
                delete_counter += 1
                if delete_counter < 2:
                    info_label.config(text="Press again to confirm")
                elif delete_counter >= 2:
                    os.remove(file_write)
                    alert_root.destroy()
                    text_root.destroy()
                    add_user_history(user=user , send=f'You deleted the file: {file[:-4]}')
                    text_interface(user , password)
                    

            alert_root = Toplevel(text_root)
            alert_root.title("Delete file window")
            alert_root.geometry("500x500+600+150")
            alert_root.resizable(False , False)
            alert_root.transient(text_root) #mantiene esta ventana por encima de del texto. SOLO FUNCIONA CON TOPLEVEL
            alert_root.grab_set() #hace que solo se pueda interacturar con esta vetnana(en el entorno tkinter solo)

            text_alert = Label(alert_root , text="Are you sure?" , font=("Arial" , 20) , padx=30 , pady=10)
            text_alert.grid(column=0 , row=0)

            confirm_button = Button(alert_root , text="DELETE FILE" , width=12 , height=1 , command=confirm_delete)
            confirm_button.grid(column=0 , row=1)

            info_label = Label(alert_root , text="" , font=("Aral" , 15))
            info_label.grid(column=0 , row=2)
            alert_root.geometry("")

            
        text_root = Tk()
        text_root.geometry("300x150+550+150")
        text_root.resizable(False , False)

        file_name_text = Label(text_root , text=f'Text name:' , anchor="e")
        file_name_text.grid(column=2 , row=0)

        file_name_entry = Entry(text_root)
        file_name_entry.insert(0 , original_name)
        file_name_entry.grid(column=3 , row=0 , sticky="nsew")

        delete_file_button = Button(text_root , text="Delete file" , width=12 , height=1 , command=delete_file_alert)
        delete_file_button.grid(column=1 , row=0)

        margin1 = Label(text_root , text="" , padx=10)
        margin1.grid(column=0 , row=0)

        margin2 = Label(text_root , text="" , padx=10)
        margin2.grid(column=5 , row=0)

        user_text = Text(text_root , wrap="word" , undo=True)
        user_text.grid(column=1 , columnspan=4 , row=1)
        user_text.insert("1.0" , set_text())

        scrollbar = Scrollbar(command=user_text.yview , orient="vertical")
        scrollbar.grid(column=5 , row=1 , sticky="nsew")
        user_text.config(yscrollcommand=scrollbar.set)
        
        save_button = Button(text_root , text="Save" , width=12 , height=1 , command=save)
        save_button.grid(column=1 , row=2)

        info_label = Label(text_root , text="" , font=("Arial" , 12))
        info_label.grid(column=2 , columnspan=2 , row=2)

        exit_button = Button(text_root , text="Exit" , width=12 , height=1 , command=text_exit)
        exit_button.grid(column=4 , row=2)

        text_root.geometry("")

    def create_file():
        if len(files) > 10:
            files_number.config(text="Max of files created")
            return
        create_try = os.path.join(ubication , "new file.txt")
        counter = 0
        controler = False
        while not controler:
            if os.path.exists(create_try):
                create_try = os.path.join(ubication , f'new file({counter}).txt')
                counter += 1
            else:
                with open(create_try , "w" , encoding="utf-8") as f:
                    f.write("")
                    controler = True
                    add_user_history(send=f'New file created' , user=user)
                    select_text.destroy()
                    text_interface(user , password)

    def exit():
        select_text.destroy()
        user_interface(user , password)

    select_text = Tk()
    select_text.resizable(False , False)
    select_text.title("Select a file")
    select_text.geometry("500x500+600+125")

    select_text_title = Label(select_text , text="Choose your file please" , font=("Arial" , 25))
    select_text_title.grid(column=0 , row=0)

    new_file = Button(select_text , text="New text file" , height=2 , width=20 , command=create_file)
    new_file.grid(column=0 , row=2)

    your_files = Label(select_text , text="Your files" , font=("Arial" , 15))
    your_files.grid(column=0 , row=3)

    counter = 0
    for i in range(0 , len(files)):
        counter += 1
        file = files[i]
        file_button = Button(select_text , text=file[:file.rfind(".")] , height=2 , command=lambda f=file: text(user , password , f)) #da el nombre SIN la extensión
        file_button.grid(column=0 , row=(i + 4) , sticky="nsew")

    files_number = Label(select_text , text=f'{len(files)} files' , font=("Arial" , 15))
    files_number.grid(column=0 , row=(counter + 5))

    exit_button = Button(select_text , text="Exit" , height=2 , width=15 , command=exit)
    exit_button.grid(column=0 , row=(counter + 6))

    select_text.geometry("")

def user_interface(user , password):
    global user_root

    def change_password(user , password):
        user_root.destroy()
        global need_change
        need_change = 0
        def change_info(send):
            change_password_info.config(text=send)

        def change():
            global need_change , temporary_password
            real_name = user
            real_password = password #contraseña cifrada
            actual_password = encrypt(change_password_entry1.get().strip() , 4) # se cifra
            new_password = encrypt(change_password_entry2.get().strip() , 4) #se cifra
            confirm_password = encrypt(str(change_password_entry3.get().strip()) , 4)
            if (actual_password == ""):
                change_info(send="Please, indicate your actual password")
                need_change = 0
                return
            if (real_password != actual_password):
                change_info(send="Your actual password is incorrect")
                need_change = 0
                return
            if new_password  == "":
                change_info(send="Indicate your new password in both spaces")
                need_change = 0
                return
            if confirm_password == "":
                change_info(send="Indicate your new password in both spaces")
                need_change = 0
                return
            if confirm_password != new_password:
                change_info(send="Passwords must match")
                need_change = 0
                return
            if new_password == real_password:
                change_info(send="Please, don't use the same password")
                need_change = 0
                return
            #if not security_check(new_password):
                #change_info(send="Password must contain 6 characters\n1 number and 1 special character")
                #return #SE OMITE PARA AGILIZAR LAS PRUEBAS
            if need_change == 1 and new_password != temporary_password:
                change_info(send="Error, diference with de previus password")
                need_change = 0
                temporary_password = ""
                return
            if (need_change < 2):
                change_info(send="Press again to confirm")
                temporary_password = new_password
                need_change += 1
                if need_change == 2:
                    identify = f'{real_name} {real_password}\n' #nombre para cambiar
                    password_change = f'{real_name} {new_password}\n' #nombre nuevo
                    with open(users_file , "r") as f:
                        lines = f.readlines()
                    with open(users_file , "w") as f:
                        for line in lines:
                            if line == identify:
                                add_user_history(send=f'You changed your password' , user=user)
                                f.write(password_change)
                            else:
                                f.write(line)
                    change_password_root.destroy()
                    user_interface(user , new_password)
                else:
                    return

        change_password_root = Tk()
        change_password_root.title("Change your password")
        change_password_root.resizable(False , False)
        change_password_root.geometry("300x150+500+250")
        

        def change_password_exit():
            change_password_root.destroy()
            user_interface(user , password)

        #change_password_root.protocol("WM_DELETE_WINDOW" , change_password_exit)
        change_password_title = Label(change_password_root , text=f'Change your password "{user}"' , font=("Arial" , 30) , padx=5 , pady=5)
        change_password_title.grid(column= 0 , columnspan=2 , row=0)

        change_password_label1 = Label(change_password_root , text="Actual password" , font=("Arial" , 15))
        change_password_label1.grid(column=0 , row=1)

        change_password_entry1 = Entry(change_password_root , show="*")
        change_password_entry1.grid(column=1 , row=1)
        
        change_password_label2 = Label(change_password_root , text="New password" , font=("Arial" , 15))
        change_password_label2.grid(column=0 , row=2)

        change_password_entry2 = Entry(change_password_root , show="*")
        change_password_entry2.grid(column =1 , row =2)

        change_password_label3 = Label(change_password_root , text="Confirm your password" , font=("Arial" , 15))
        change_password_label3.grid(column=0 , row=3)

        change_password_entry3 = Entry(change_password_root , show="*")
        change_password_entry3.grid(column=1 , row=3)

        change_password_button_confirm = Button(change_password_root , text="Change" , width = 15 , pady=10 , command=change)
        change_password_button_confirm.grid(column=0 , columnspan=2 , row=4)
        
        change_password_info = Label(change_password_root , text="Complete both gaps" , font=("Arial" , 15))
        change_password_info.grid(column=0 , columnspan=2 , row=5)

        change_password_exit = Button(change_password_root , text="Exit" , width=15 , pady = 10 , command=change_password_exit)
        change_password_exit.grid(column=0 , columnspan=2 , row=6)

        change_password_root.geometry("")
        return

    def delete_account(user , password):
        user_root.destroy()
        global need #necesario para el contador
        need = 0
        
        def password_error(send): #mensaje al seleccionar mas la contraseña de eliminacion de cuenta
            password_info.config(text=send)

        def delete(password): #recibe por parametro la contraseña encryptada
            global need #necesario para e contador para confirmar la eliminacion
            password = encrypt(password , -4) #se desencripta la contraseña
            password_check = confirm_delete_entry.get().strip() #obtiene la contraseña de confirmacion

            def check_password(password): #verifica que la contraseña sea correcta
                global need
                if (password_check == ""):
                    password_error(send="Please indicate your password")
                    need = 0
                    return
                if (password_check != password):
                    password_error(send="Your password is incorrect...")
                    need = 0
                    return
                if (password_check == password):
                    if need < 2:
                        password_error(send="Press again to confirm...")
                        need += 1 #compruba si tras la segunda confirmacion se cumple la variable need
                        if need == 2:
                            make_delete(password)

            def make_delete(password):
                password = encrypt(password , 4)
                identify = f'{user} {password}\n' #usuario y contraseña encriptada para volver a buscarlos en la lista
                with open(users_file , "r") as f:
                    lines = f.readlines()
                    f.close()
                with open(users_file , "w") as file:
                    for line in lines:
                        if line == identify:
                            add_general_history(send=f'User deleted: {user}') #añadir eliminación al historial
                            continue
                        else:
                            file.write(line)
                    file.close()
                delete_file = os.path.join(users , f'{user}')
                shutil.rmtree(delete_file)
                advert.destroy()
                main_root()

                
            check_password(password) #comienza el checkeo de la contraseña

        advert = Tk()
        advert.resizable(False , False)
        advert.geometry("300x150+500+250")
        advert_title = Label(advert , text="WARNING" , font=("Arial" , 30))
        advert_title.grid(column = 0 , row = 0 , columnspan=2)
        
        def exit_delete_button():
            advert.destroy()
            user_interface(user , password)

        advert_title2 = Label(advert , text="Are your sure you want to delete your account?" , font=("Arial" , 17))
        advert_title2.grid(column=0 , columnspan=2 , row=1)

        confirm_delete_label = Label(advert , text="Confirm your password" , font=("Arial" , 20))
        confirm_delete_label.grid(column=0 , row=2)

        confirm_delete_entry = Entry(advert , show="*")
        confirm_delete_entry.grid(column=1 , row=2)
        
        confirm_delete_button = Button(advert , text="DELETE" , width=15 , pady=10 , command=lambda: delete(password))
        confirm_delete_button.grid(column=0 , columnspan=2 , row=3)

        password_info = Label(advert , font=("Arial" , 15))
        password_info.grid(column=0 , columnspan=2 , row=4)

        exit_button = Button(advert , text="Exit" , width=15 , pady=10 , command=exit_delete_button)
        exit_button.grid(column=0 , columnspan=2 , row=5)

        advert.geometry("")

    def check_user_history(user , password):
        user_root.destroy()
        history = os.path.join(users , user , "history.txt")

        def exit_history():
            check_history_root.destroy()
            user_interface(user , password)
            return
        
        def set_text():
            nonlocal history
            with open(history , "r") as f:
                insert = f.read()
            return insert

        check_history_root = Tk()
        check_history_root.geometry("400x400+475+150")
        check_history_root.resizable(False , False)
        check_history_root.title("Checking history")

        margin1 = Label(check_history_root , text="")
        margin1.grid(column=0 , row=0)

        show_text = Text(check_history_root , state=NORMAL)
        show_text.grid(column=1 , row=0)
        show_text.insert("1.0" , set_text())
        show_text.config(state="disabled")

        margin2 = Label(check_history_root , text="")
        margin2.grid(column=3 , row=0)

        exit_button = Button(check_history_root , width=20 , pady=10 , text="Exit" , command=exit_history)
        exit_button.grid(column=1 , row=1)

        check_history_root.geometry("")
        return

    def go_text_interface(user , password):
        user_root.destroy()
        text_interface(user , password)

    def log_out():
        user_root.destroy()
        add_general_history(send=f'{user} has logged out')
        add_user_history(send="Your logged out" , user=user)
        main_root()
    
    user_root = Tk() #se crea una raiz independiente para independizarla de la principal y poder cerrarla
    user_root.title(f'Welcome {user}')
    user_root.resizable(False , False)
    user_root.geometry("300x150+500+250")

    user_title = Label(user_root , text=f'Welcome {user}' , font=("Arial" , 35) , padx=10 , pady=5)
    user_title.grid(column=0 , columnspan=2 , row=0)

    user_choose_label = Label(user_root , text="Choose your option" , font=("Arial" , 25) , padx=50 , pady=5)
    user_choose_label.grid(column=0 , columnspan=2 , row=1)

    delete_button = Button(user_root , text="Delete account" , width=15 , command=lambda: delete_account(user , password) , padx=5 , pady=10)
    delete_button.grid(column=0 , row=3)                                                #lambda es usado para que solo se ejecute al pulsar el boton

    change_password_button = Button(user_root , text="Change password" , width=15 , command=lambda: change_password(user , password) , padx=5 , pady=10)
    change_password_button.grid(column=1 , row=3)                                     #envia la funcion de cambio de contraseña y la CONTRASEÑA CIFRADA
    
    files_gestor_button = Button(user_root , text="Text file" , width=12 , padx=15 , command=lambda: go_text_interface(user , password) , pady=10)
    files_gestor_button.grid(column=0 , row=4)

    check_history_button = Button(user_root , text="History" , width=12 , padx=15 , pady=10 , command=lambda: check_user_history(user , password))
    check_history_button.grid(column=1 , row=4)

    customize_button = Button()

    stadistic_button = Button()

    log_out_button = Button(user_root , text="Log out" , width=12 , height=1 , command=log_out , padx=5 , pady=10)
    log_out_button.grid(column=0 , row=6 , columnspan=2)

    user_root.geometry("")
 
def admin_user(user , password):
    add_admin_history(send=f'New admin login: {user}')

    def exit_admin():
        admin_root.destroy()
        add_admin_history(send=f'{user} has logged out')
        main()

    def admin_read_history():
        admin_root.destroy()
        history = os.path.join(database , "history.txt")

        def exit_history():
            check_history_root.destroy()
            admin_user(user , password)
            return
        
        def set_text():
            with open(history , "r") as f:
                insert = f.read()
            return insert

        check_history_root = Tk()
        check_history_root.geometry("400x400+475+150")
        check_history_root.resizable(False , False)
        check_history_root.title("Checking history")

        margin1 = Label(check_history_root , text="")
        margin1.grid(column=0 , row=0)

        show_text = Text(check_history_root , state=NORMAL)
        show_text.grid(column=1 , row=0)
        show_text.insert("1.0" , set_text())
        show_text.config(state="disabled")

        margin2 = Label(check_history_root , text="")
        margin2.grid(column=3 , row=0)

        exit_button = Button(check_history_root , width=20 , pady=10 , text="Exit" , command=exit_history)
        exit_button.grid(column=1 , row=1)

        check_history_root.geometry("")
        return
        return
    
    def admin_delete_user():
        return
    
    def create_admin():

        def create_admin_info(send):
            info_label.config(text=send)

        def exit_create_account():
            create_admin_root.destroy()

        def confirm_create_admin():
            user = user_entry2.get().strip()
            password = password_entry2.get().strip()
            password_confirm = password_confirm_entry.get().strip()
            
            if user == "":
                create_admin_info(send="Please indicate your username")
                return
            if (user in get_admin_list()) or (user in get_users_list()):
                create_admin_info(send="Username not disponile")
                return
            if (" " in user):
                create_admin_info(send="Username cannot contain spaces")
                return
            if (password == "") or (password_confirm == ""):
                create_admin_info(send="Indicate your password in both spaces")
                return
            if (" " in password):
                create_admin_info(send="Password cannot contain spaces")
                return
            if password != password_confirm:
                create_admin_info(send="Passwords must match")
                return #ULTIMA VERIFICACION
            add_admin(user , password)
            user_entry2.delete(0 , END)
            password_entry2.delete(0 , END)
            password_confirm_entry.delete(0 , END)
            create_admin_info(send="User created succesfully")

            
        create_admin_root = Tk() 
        create_admin_root.geometry("300x150+500+250")
        create_admin_root.title("Create an account")
        create_admin_root.config(width=13 , height=1)
        create_admin_root.resizable(False , False)

        new_title = Label(create_admin_root , text="Create an account" , font=("Arial" , 30))
        new_title.grid(column=0 , row=0 , columnspan=2)

        user_label2 = Label(create_admin_root , text="User name" , font=("Arial" , 20))
        user_label2.grid(column=0 , row=1)

        user_entry2 = Entry(create_admin_root)
        user_entry2.grid(column=1 , row=1)

        password_label2 = Label(create_admin_root , text="Passoword" , font=("Arial" , 20))
        password_label2.grid(column=0 , row=2)

        password_entry2 = Entry(create_admin_root , show="*")
        password_entry2.grid(column=1 , row=2)

        password_confirm_label = Label(create_admin_root , text="Confirm your password" , font=("Arial" , 20))
        password_confirm_label.grid(column=0 , row=3)

        password_confirm_entry = Entry(create_admin_root , show="*")
        password_confirm_entry.grid(column=1 , row=3)

        confirm2 = Button(create_admin_root , text="Create account" , command=confirm_create_admin , padx=13 , pady=8)
        confirm2.grid(column=0 , row=4 , columnspan=2)

        info_label = Label(create_admin_root , font=("Arial" , 17))
        info_label.grid(column=0 , row=5 , columnspan=2)

        exit_button = Button(create_admin_root , text="Exit" , width=12 , height=1 , command=exit_create_account , padx=13 , pady=8)
        exit_button.grid(column=0 , columnspan=2 , row=6)

        create_admin_root.geometry("")
 
    def clean_database():
        return

    admin_root = Tk()
    admin_root.geometry("300x150+500+250")
    admin_title = Label(admin_root , text="Welcome admin" , font=("Arial" , 35) , padx=10 , pady=10)
    admin_title.grid(column=0 , columnspan=2 , row=0)
    admin_root.resizable(False , False)
    
    admin_subtitle = Label(admin_root , text="Choose an option" , font=("Arial" , 25))
    admin_subtitle.grid(column=0 , columnspan=2 , row=1)

    admin_history = Button(admin_root , text="Read history" , width=20 , pady=10 , command=admin_read_history)
    admin_history.grid(column=0 , row=2)

    admin_delete = Button(admin_root , text="Delete an user" , width=20 , pady=10, command=admin_delete_user)
    admin_delete.grid(column=1 , row=2)

    create_admin_button = Button(admin_root , text="Create admin" , width=20 , pady=10 , command=create_admin)
    create_admin_button.grid(column=0 , row=3)

    clean_database_button = Button(admin_root , text="Clean database" , width=20 , pady=10 , command=clean_database)
    clean_database_button.grid(column=1 , row=3)

    exit_button = Button(admin_root , text="Exit" , width=20 , pady=10 , command=exit_admin)
    exit_button.grid(column=0 , columnspan=2 , row=4)

    admin_root.geometry("")
    admin_root.mainloop()

def main_root():
    global root , login_info

    def login(): #estudiar si se puede incorporar dentro de special

        def refresh(send): #actualiza la vetana principal
            global login_info
            login_info.config(text=send)

        try:
            user = user_entry.get().strip()
            password = password_entry.get().strip()
            if ((user == "aaa") and (password == "aaa")):
                root.destroy()
                admin_user(user , password)
                return
            if user == "":
                refresh(send="Please, indicate your username")
                return
            with open(admins_file , "r") as f:
                for line in f.readlines():
                    credential = line.split()
                    if (credential[0] == user):
                        if password == "":
                            refresh(send="Please indicate your password")
                            return
                        if (encrypt(credential[1] , -4) == password):
                            root.destroy()
                            admin_user(user , password)
                            return
                        else:
                            refresh(send="Incorrect password")
                            return
            with open(users_file , "r") as f:
                for line in f.readlines():
                    credentials = line.split()
                    if (credentials[0] == user):
                        if password == "":
                            refresh(send="Please indicate your password")
                            return
                        if (encrypt(credentials[1] , -4) == password):
                            add_general_history(send=f'New login: {user}')
                            add_user_history(send="New login" , user=user)
                            root.destroy()
                            user_interface(user , password=encrypt(password , 4))
                            return
                        else:
                            refresh(send="Incorrect password")
                        return
                refresh(send="Not user found")#se ejecuta cuando el bucle no encuentra ninguna salida
        except FileNotFoundError:
            check() #se pone aqui por si el archivo se elimina durante la ejecucion
            login()

    def create_account():
        global user_entry2 , password_entry2 , password_confirm_entry , info_label
        user_entry.delete(0 , END)
        password_entry.delete(0 , END)

        def info(send): #se envía antes de los return cuando ocurre un error en la creacion de una contraseña
            info_label.config(text=send)

        def add_user():
            user = user_entry2.get().strip()
            password = password_entry2.get().strip()
            password_confirm = password_confirm_entry.get().strip()
            try:
                def check_user():
                    if user == "":
                        info(send="Indicate your username") #el checkeo de contraseñas debe ser después de si se repite un usuario
                        return
                    if " " in user: #evita que haya espacios en los nombres de usuario para evitar errores en la lectura de la base de datos
                        info(send="Username cannot contain spaces")
                        return
                    if (len(user) > 12):
                        print(len(user))
                        info(send="Username cannot have more 12 characters")
                        return
                    if user in get_users_list():
                        info(send="Username not disponible")
                        return
                    if user in get_admin_list() or user == "aaa":
                        info(send="Username not disponible")
                        return
                    if (password == ""): # la condicion se separa para un buen eso de la funcion security_check
                        info(send="Indicate your password in both spaces")
                        return
                    #if not security_check(password): #SE OMITE PARA HACER PRUEBAS MAS RAPIDO
                        #info(send="Password must contain 6 characters 1 nomber and 1 spcial character")
                        #return
                    if (password_confirm == ""):
                        info(send="Indicate your password in both spaces")
                        return
                    if (" " in password) or (" " in password_confirm):
                        info(send="Password cannot contain spaces")
                        return
                    if password != password_confirm:
                        info(send="Passwords must match")
                        return
                    return True
                
                if check_user():
                    create_user(user , password)
                    user_entry2.delete(0, END)
                    password_entry2.delete(0 , END)
                    password_confirm_entry.delete(0 , END)
                    add_general_history(send=f'New account created: {user}')
                    info(send="Account created succesfully")
                else:
                    return
            except FileNotFoundError:
                check() #se pone aqui por si el archivo se elimina durante la ejecucion
                add_user()

        def exit_create_account():
                create_account_root.destroy()
                root.destroy()
                main()
   
        create_account_root = Toplevel(root) #crea una ventana secundaria dependiente de la primera
        create_account_root.geometry("300x150+500+250")
        create_account_root.title("Create an account")
        create_account_root.config(width=13 , height=1)
        create_account_root.resizable(False , False)
        create_account_root.transient(root)
        create_account_root.grab_set()

        new_title = Label(create_account_root , text="Create an account" , font=("Arial" , 30))
        new_title.grid(column=0 , row=0 , columnspan=2)

        user_label2 = Label(create_account_root , text="User name" , font=("Arial" , 20))
        user_label2.grid(column=0 , row=1)

        user_entry2 = Entry(create_account_root)
        user_entry2.grid(column=1 , row=1)

        password_label2 = Label(create_account_root , text="Passoword" , font=("Arial" , 20))
        password_label2.grid(column=0 , row=2)

        password_entry2 = Entry(create_account_root , show="*")
        password_entry2.grid(column=1 , row=2)

        password_confirm_label = Label(create_account_root , text="Confirm your password" , font=("Arial" , 20))
        password_confirm_label.grid(column=0 , row=3)
        password_confirm_entry = Entry(create_account_root , show="*")
        password_confirm_entry.grid(column=1 , row=3)

        confirm_button = Button(create_account_root , text="Create account" , command=add_user , pady=8 , padx=13)
        confirm_button.grid(column=0 , row=4 , columnspan=2)

        info_label = Label(create_account_root , font=("Arial" , 20))
        info_label.grid(column=0 , row=5 , columnspan=2)

        exit_button = Button(create_account_root , text="Exit" , width=12 , height=1 , command=exit_create_account , pady=8 , padx=13 , font=("Arial" , 10))
        exit_button.grid(column=0 , columnspan=2 , row=6)

        create_account_root.geometry("")

    def exit_main_root():
        root.destroy()
    
    def set_user_entry():
        user_entry.focus_set()
        return

    def set_password_entry():
        password_entry.focus_set()
        return

    root = Tk()
    root.title("Log in")
    root.resizable(False, False)
    root.geometry("300x150+500+250")

    title = Label(text="Welcome" , font=("Arial" , 30))
    title.grid(column=0 , row=0 , columnspan=2)
    title.config(width=13 , height=1)

    user_label = Label(text="User" , font=("Arial" , 20) , width=5 , height=2)
    user_label.grid(column=0 , row=1)
    user_label.bind("<Button-1>" , lambda event: set_user_entry())

    user_entry = Entry()
    user_entry.grid(column=1 , row=1)

    password_label = Label(text="Password" , font=("Arial" , 20))
    password_label.grid(column=0 , row=2)
    password_label.bind("<Button-1>" , lambda event: set_password_entry())

    password_entry = Entry(show="*")
    password_entry.grid(column=1 , row=2)

    login_confirm = Button(text="Log in" , width=15 , command=login , pady=6)
    login_confirm.grid(column=0 , row=3 , columnspan=2)

    login_info = Label(text="" , font=("Arial" , 15))
    login_info.grid(column=0 , row=4 , columnspan=2)

    info = Label(text="Aren't you a registered? Create an account!" , font=("Arial" , 15) , pady=5)
    info.grid(column=0 , row=5 , columnspan=2)

    create_account_button = Button(text="Create account" , command=create_account, width=15 , pady=6)
    create_account_button.grid(column=0 , row=6 , columnspan=2)
    check() #comprobar la existencia de una base de datos

    exit_button = Button(root , text="Exit", width=15 , command=exit_main_root , pady=5)
    exit_button.grid(column=0 , columnspan=2 , row=8)

    
    root.geometry("")
    root.mainloop()

def main():
    global directory , database , admins , admins_file , users , users_file , history_file
    directory = os.path.dirname(os.path.abspath(__file__))
    database = os.path.join(directory , "DataBase")
    admins = os.path.join(database , "Admins")
    admins_file = os.path.join(database , "admins.txt")
    users = os.path.join(database , "Users")
    users_file = os.path.join(database , "users.txt")
    history_file = os.path.join(database , "history.txt")#crea el archivo para el historial
    check()
    add_general_history(send="Program started")
    main_root()

main()