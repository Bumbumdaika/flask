
import ttkbootstrap as ttk
from tkinter import *
import pandas as pd
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import pymysql
import requests
from config import host, user, password, db_name, res



class Welcom(ttk.Window):
    def __init__(self):
        super().__init__()

        self.geometry("600x400")

        def registration():
            rg = Registration()
            self.destroy

        def signIn():
            rg = SignIn()
            self.destroy

        title = ttk.Label(self, text="Добро Пожаловать!\n Выберите действие:")
        btn1=ttk.Button(self, text="Зарегистрироваться", command=registration)
        btn2=ttk.Button(self, text="Войти", command=signIn)

        title.pack(pady=30)
        btn1.pack(pady=10)
        btn2.pack(pady=10)
        self.resizable(False, False)
        self.mainloop()


class Registration(ttk.Window):
    def __init__(self):
        super().__init__()

        self.geometry("600x400")

        def insert_user():
            login=text_box_login.get()
            pwd=text_box_pwd.get()
        # insert data  - добавление данный в таблицу
            with connection.cursor() as cursor:
                insert_querry=f"INSERT INTO `user`(login, pwd) VALUES ('{login}','{pwd}')"
                cursor.execute(insert_querry)
                connection.commit()
            mw=MainWindow()

        frame = ttk.Frame(self)
        frame.pack(pady=50)
        title = ttk.Label(frame, text="Регистрация")
        label_registration = ttk.Label(frame, text="Логин")
        text_box_login = ttk.Entry(frame)
        label_pwd = ttk.Label(frame, text="Пароль")
        text_box_pwd = ttk.Entry(frame)

        btn1=ttk.Button(frame, text="Закрыть", command=self.destroy)
        btn2=ttk.Button(frame, text="Войти", command=insert_user)

        title.grid(column=3, row=1)
        label_registration.grid(column=3, row=3)
        text_box_login.grid(column=3, row=5)
        label_pwd.grid(column=3, row=7)
        text_box_pwd.grid(column=3, row=9)
        btn1.grid(column=1, row=11)
        btn2.grid(column=5, row=11)

        self.resizable(False, False)
        self.mainloop()


class SignIn(ttk.Window):
    def __init__(self):
        super().__init__()

        self.geometry("600x400")

        def signIn():
            try:
                login=text_box_login.get()
                pwd=text_box_pwd.get()
                #select data - выборка данных из таблицы
                with connection.cursor() as cursor:
                    select_all_rows="select * from `user`"
                    cursor.execute(select_all_rows)
                    rows = cursor.fetchall()
                    for row in rows:
                        if row['login']==login and row['pwd']==pwd:  
                            mw=MainWindow()
                        else:
                            title.config(text="не правильный логин или пароль")
            except:
                title.config(text="что-то пошло не так:(")


        frame = ttk.Frame(self)
        frame.pack(pady=50)
        title = ttk.Label(frame, text="Вход")
        label_registration = ttk.Label(frame, text="Логин")
        text_box_login = ttk.Entry(frame)
        label_pwd = ttk.Label(frame, text="Пароль")
        text_box_pwd = ttk.Entry(frame)
        btn1=ttk.Button(frame, text="Закрыть", command=self.destroy)
        btn2=ttk.Button(frame, text="Войти", command=signIn)

        title.grid(column=3, row=1)
        label_registration.grid(column=3, row=3)
        text_box_login.grid(column=3, row=5)
        label_pwd.grid(column=3, row=7)
        text_box_pwd.grid(column=3, row=9)
        btn1.grid(column=1, row=11)
        btn2.grid(column=5, row=11)

        self.resizable(False, False)
        self.mainloop()

class MainWindow(ttk.Window):
    def __init__(self):
        super().__init__()

        self.geometry("1000x600")
        frame_table=ttk.Frame(self)
        frame_duwn = ttk.Frame(self)
        frame_filters = ttk.Frame(frame_duwn)
        frame_insert = ttk.Frame(frame_duwn)
        frame_function=ttk.Frame(frame_duwn)
        
        def clear():
            for col in tree['columns']:
                tree.heading(col, text='')
            tree.delete(*tree.get_children())
            for c in columns:
                tree.heading(c,text=c)

        def char():
            a=res.json()
            dates=a[0]
            d1=dates.split('"ip"')
            d=d1[1:]
            row = []
            #  [71:195]- деталь,[28:55] data, [3:16]вычленить ip, [:203]убрать номер
            for l in d: 
                ip=l[3:16]
                row.append(ip)
                date=l[28:55]
                row.append(date)
                detail=l[71:195]
                row.append(detail)
                # with connection.cursor() as cursor:
                #     insert_querry=f"INSERT INTO `mydb`.`logs`(ip, time, another) VALUES ('{row[0]}','{row[1]}','{row[2]}')"
                #     cursor.execute(insert_querry)
                #     connection.commit()
                tree.insert('',END,values=row)
                row = []
            # for re in res:
            #     tree.insert('',END,values=re)

        def filter():
            for col in tree['columns']:
                tree.heading(col, text='')
            tree.delete(*tree.get_children())
            for c in columns:
                tree.heading(c,text=c)
            a=res.json()
            dates=a[0]
            d1=dates.split('"ip"')
            d=d1[1:]
            row = []
            #  [71:195]- деталь,[28:55] data, [3:16]вычленить ip, [:203]убрать номер
            for l in d: 
                ip=l[3:16]
                date=l[28:55]
                detail=l[71:195]
                if ip in text_ips_filter.get() or date in text_tim_filter.get():
                    row.append(ip)
                    row.append(date)
                    row.append(detail)
                tree.insert('',END,values=row)
                row = []

        
        def insert():
            row = []
            ip=text_ips_insert.get()
            date=text_tim_insert.get()
            detail=text_detail_insert.get()
            row.append(ip)
            row.append(date)
            row.append(detail)
            with connection.cursor() as cursor:
                    insert_querry=f"INSERT INTO `mydb`.`logs`(ip, time, another) VALUES ('{row[0]}','{row[1]}','{row[2]}')"
                    cursor.execute(insert_querry)
                    connection.commit()
            res = requests.post("http://127.0.0.1:3000/api/main/", {"ip":f"{row[0]}", "time":f"{row[1]}", "another":f"{row[2]}" })
            tree.insert('',END,values=row)
            row=[]


        frame_table.grid(column=5, row = 1)
        frame_duwn.grid(column=5, row=2)
        frame_table['borderwidth'] = 5
        frame_table['relief'] = 'sunken'
        frame_duwn['borderwidth'] = 5
        frame_duwn['relief'] = 'sunken'
        frame_filters.grid(column=3, row=1)
        frame_function.grid(column=5, row=1)
        frame_insert.grid(column=8, row=1)

        title_insert=ttk.Label(frame_insert, text="Вставить")
        title_ip_insert=ttk.Label(frame_insert, text="ip")
        text_ips_insert=ttk.Entry(frame_insert)
        title_time_insert=ttk.Label(frame_insert, text="time")
        text_tim_insert=ttk.Entry(frame_insert)
        title_detail_insert=ttk.Label(frame_insert, text="detail")
        text_detail_insert=ttk.Entry(frame_insert)
        btn_exec_insert = ttk.Button(frame_insert, text='выдолнить', command=insert)

        title_insert.pack(pady=10)
        title_ip_insert.pack(pady=10)
        text_ips_insert.pack(pady=10)
        title_time_insert.pack(pady=10)
        text_tim_insert.pack(pady=10)
        title_detail_insert.pack(pady=10)
        text_detail_insert.pack(pady=10)
        btn_exec_insert.pack(pady=10)

        title_filter=ttk.Label(frame_filters, text="Фильтрация")
        title_ip_filter=ttk.Label(frame_filters, text="ip")
        text_ips_filter=ttk.Entry(frame_filters)
        title_time_filter=ttk.Label(frame_filters, text="time")
        text_tim_filter=ttk.Entry(frame_filters)
        btn_exec_filter = ttk.Button(frame_filters, text='выдолнить', command=filter)

        title_filter.pack(pady=10)
        title_ip_filter.pack(pady=10)
        text_ips_filter.pack(pady=10)
        title_time_filter.pack(pady=10)
        text_tim_filter.pack(pady=10)
        btn_exec_filter.pack(pady=10)

        columns = ('ip','time','detail')
        tree = ttk.Treeview(frame_table,bootstyle="success",columns=columns,show='headings')
        tree.pack(pady=30, fill=X)

        for c in columns:
            tree.heading(c,text=c)


        btn_logs=ttk.Button(frame_function, text='Просмотреть логи', command=char)
        btn_clear=ttk.Button(frame_function, text='очистить', command=clear)
        btn_close=ttk.Button(frame_function, text='закрыть')

        btn_clear.pack(pady=10)
        btn_logs.pack(pady=10)
        btn_close.pack(pady=10)

        #пример значений
        # def char():
        #     values = (("Большой куш","Гай Ричи",10),("Начало","Кристофер Нолан",10),("Джентльмены","Гай Ричи",9))
        #     for value in values:
        #         tree.insert('',END,values=value)

        self.resizable(True, True)
        self.mainloop()



try:
    connection = pymysql.connect(
        host=host,
        port=3306,
        user=user,
        password = password,
        database=db_name,
        cursorclass=pymysql.cursors.DictCursor

    )
    nw = Welcom()
    print("succses connection")

except Exception as ex:
    print("Connextion refused...")
    print(ex)