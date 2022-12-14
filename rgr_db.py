#!/usr/local/bin/python3
# Библиотеки
import fdb
from datetime import timedelta, datetime
import easygui
import pandas as pd
import tkinter as tk
import tkinter.ttk as ttk
import sys
from tkinter import *
import time

ShipAttrs = ['regnum','shipname','motherport','capacity','shipprice','shipdate']
ShipAttrsUser = ['regnum','shipname','motherport']
GoodsAttrs = ['goodsreg','gname','costs','weight']
RouteAttrs = ['rnum','placefrom','placeto','toport','fromport']
RouteAttrsUser = ['rnum','toport','fromport']
RentAttrs = ['contract','shipnum','goodsnum','routenum','price','starts','ends']
RentAttrsUser = ['contract','shipnum','price','starts','ends']

# Класс таблицы
class Table(tk.Frame):
    def __init__(self, parent=None, headings=tuple(), rows=tuple(), buttons=1, role='user'):
        super().__init__(parent)

        table = ttk.Treeview(self, show="headings", selectmode="browse")
        table["columns"]=headings
        table["displaycolumns"]=headings

        for head in headings:
            table.heading(head, text=head, anchor=tk.CENTER)
            table.column(head, anchor=tk.CENTER)

        for row in rows:
            table.insert('', tk.END, values=tuple(row))

        scrolltable = tk.Scrollbar(self, command=table.yview)
        table.configure(yscrollcommand=scrolltable.set)
        scrolltable.pack(side=tk.RIGHT, fill=tk.Y)
        table.pack(expand=tk.YES, fill=tk.BOTH)
        
        if (buttons == 1):
            if (role == 'admin'):
                Del = Button(root, bg="gray", text=u"Удалить", command=self.DelForm)
                Del.pack(side=BOTTOM, fill='x')
                Sort = Button(root, bg="gray", text=u"Сортировать", command=self.SortForm)
                Sort.pack(side=BOTTOM, fill='x')
                Search = Button(root, bg="gray", text=u"Искать", command=self.SearchForm)
                Search.pack(side=BOTTOM, fill='x')
                Edit = Button(root, bg="gray", text=u"Редактировать", command=self.EditForm)
                Edit.pack(side=BOTTOM, fill='x')
                Add = Button(root, bg="gray", text=u"Добавить", command=self.AddForm)
                Add.pack(side=BOTTOM, fill='x')
            elif (role == 'user'):
                Sort = Button(root, bg="gray", text=u"Сортировать", command=self.SortForm)
                Sort.pack(side=BOTTOM, fill='x')
                Search = Button(root, bg="gray", text=u"Искать", command=self.SearchForm)
                Search.pack(side=BOTTOM, fill='x')
                
class ShipTable(Table):
    def AddForm(self):
        AddValues = easygui.multenterbox('Заполните поля для добавления записи', title, ShipHeadings)
        notify = ''
        Wrong = [0] * 6
        
        #Проверка regnum
        try:
            AddValues[0] = int(AddValues[0])
        except:
            notify += 'Неверный тип поля ' + ShipHeadings[0]
            Wrong[0] = 1
        if (len(str(AddValues[0])) != 7):
            notify += '\nДлина поля ' + ShipHeadings[0] + ' должна составлять 7 цифр' 
            Wrong[0] = 1
        dt = (datetime.now() - timedelta(minutes=30)).replace(microsecond=0)
        cur.execute("select regnum from ship")
        AddArr = cur.fetchall()
        ArrRegnums = [0] * len(AddArr)
        for i in range(len(AddArr)): 
            ArrRegnums[i] = int(AddArr[i][0])
        for i in range(len(ArrRegnums)):
            if (ArrRegnums[i] == AddValues[0]):
                notify += '\nПоле ' + ShipHeadings[0] + ' должно быть уникальным'
                Wrong[0] = 1
                break
            
        #Проверка shipname
        try:
            AddValues[1] = str(AddValues[1])
        except:
            notify += '\nНеверный тип поля ' + ShipHeadings[1]
            Wrong[1] = 1
        if (len(str(AddValues[1])) > 20 or len(str(AddValues[1])) == 0):
            notify += '\nДлина поля ' + ShipHeadings[1] + ' должна составлять не более 20 символов'
            Wrong[1] = 1
        if (AddValues[1] == ''):
            notify += '\nПоле ' + ShipHeadings[1] + ' не должно быть пустым'
            Wrong[1] = 1
            
        #Проверка motherport
        try:
            AddValues[2] = str(AddValues[2])
        except:
            notify += '\nНеверный тип поля ' + ShipHeadings[2]
            Wrong[2] = 1
        if (len(str(AddValues[2])) > 20 or len(str(AddValues[2])) == 0):
            notify += '\nДлина поля ' + ShipHeadings[2] + ' должна составлять не более 20 символов'
            Wrong[2] = 1
        if (AddValues[2] == ''):
            notify += '\nПоле ' + ShipHeadings[2] + ' не должно быть пустым'
            Wrong[2] = 1
            
        #Проверка capacity
        try:
            AddValues[3] = int(AddValues[3])
        except:
            notify += '\nНеверный тип поля ' + ShipHeadings[3]
            Wrong[3] = 1
            
        #Проверка shipprice
        try:
            AddValues[4] = int(AddValues[4])
        except:
            notify += '\nНеверный тип поля ' + ShipHeadings[4]
            Wrong[4] = 1
            
        #Проверка shipdate
        try:
            AddValues[5] = str(AddValues[5])
        except:
            notify += '\nНеверный тип поля ' + ShipHeadings[5]
            Wrong[5] = 1
        if (len(str(AddValues[5])) != 10 or AddValues[5] == ''):
            notify += '\nДлина поля ' + ShipHeadings[5] + ' должна составлять 10 символов'
            Wrong[5] = 1
        if (AddValues[5] != '' and len(str(AddValues[5])) == 10):
            if (AddValues[5][4] != '-' or AddValues[5][7] != '-'):
                notify += '\nПоле ' + ShipHeadings[5] + ' должно быть в формате ГГГГ-ММ-ДД'
                Wrong[5] = 1
                
        AddFlag = 1
        if (any(el == 1 for el in Wrong)):
            easygui.msgbox(notify, title)
            AddFlag = 0
        
        if (AddValues != None and AddFlag == 1):
            dt = (datetime.now() - timedelta(minutes=30)).replace(microsecond=0)
            cur.execute("insert into ship (regnum,shipname,motherport,capacity,shipprice,shipdate) values (?,?,?,?,?,?)",
                        (AddValues[0], AddValues[1], AddValues[2], AddValues[3], AddValues[4], AddValues[5]))
            con.commit();
    def DelForm(self):
        regnum = easygui.enterbox('Введите Рег_ном удаляемой записи', title)
        try:
            regnum = int(regnum)
        except:
            easygui.msgbox('Неверный тип поля', title)
            regnum = None
        if (regnum != None):
            dt = (datetime.now() - timedelta(minutes=30)).replace(microsecond=0)
            cur.execute("select regnum from ship")
            ArrRegnums = cur.fetchall()
            DelFlag = 0
            for i in range(len(ArrRegnums)):
                if (ArrRegnums[i][0] == int(regnum)):
                    DelFlag = 1
                    break
            if (DelFlag == 1):
                dt = (datetime.now() - timedelta(minutes=30)).replace(microsecond=0)
                cur.execute("delete from ship where regnum="+str(regnum))
                con.commit()
            else:
                easygui.msgbox('Такой записи нет в базе данных', title)
    def EditForm(self):
        regnum = easygui.enterbox('Введите Рег_ном редактируемой записи', title)
        try:
            regnum = int(regnum)
        except:
            easygui.msgbox('Неверный тип поля', title)
            regnum = None
        if (regnum != None):
            dt = (datetime.now() - timedelta(minutes=30)).replace(microsecond=0)
            cur.execute("select regnum from ship")
            ArrRegnums = cur.fetchall()
            EditFlag = 0
            for i in range(len(ArrRegnums)):
                if (ArrRegnums[i][0] == int(regnum)):
                    EditFlag = 1
                    break
            if (EditFlag == 1):
                var = easygui.indexbox('Выберите поле для редактирования', title, ShipHeadings)
                if (var != None):
                    newvar = easygui.enterbox('Введите новое значения поля', title)
                    if (newvar != None):
                        dt = (datetime.now() - timedelta(minutes=30)).replace(microsecond=0)
                        Wrong = 0
                        if (var == 0):
                            notify = ''
                            Wrong = 0
                            try:
                                newvar = int(newvar)
                            except:
                                notify = 'Неверный тип поля ' + ShipHeadings[0]
                                Wrong = 1
                            if (len(str(newvar)) != 7):
                                notify += '\nДлина поля ' + ShipHeadings[0] + ' должна составлять 7 цифр'
                                Wrong = 1
                            dt = (datetime.now() - timedelta(minutes=30)).replace(microsecond=0)
                            cur.execute("select regnum from ship")
                            ArrRegnums = cur.fetchall()
                            for i in range(len(ArrRegnums)):
                                if (ArrRegnums[i][0] == int(newvar)):
                                    notify += '\nПоле ' + ShipHeadings[0] + ' должно быть уникальным'
                                    Wrong = 1
                                    break
                            if (Wrong == 1):
                                easygui.msgbox(notify, title)
                            else:
                                cur.execute("update ship set regnum="+str(newvar)+"where regnum="+str(regnum))
                        if (var == 1):
                            notify = ''
                            Wrong = 0
                            if (len(newvar) > 20 or len(newvar) == 0):
                                notify += '\nДлина поля ' + ShipHeadings[1] + ' должна составлять от 1 до 20 символов'
                                Wrong = 1
                            elif (newvar == ''):
                                notify += '\nПоле ' + ShipHeadings[1] + ' не должно быть пустым'
                                Wrong = 1
                            if (Wrong == 1):
                                easygui.msgbox(notify, title)
                            else:
                                cur.execute("update ship set shipname='"+newvar+"' where regnum="+str(regnum))
                        if (var == 2):
                            notify = ''
                            Wrong = 0
                            if (len(newvar) > 20 or len(newvar) == 0):
                                notify += '\nДлина поля ' + ShipHeadings[2] + ' должна составлять от 1 до 20 символов'
                                Wrong = 1
                            if (newvar == ''):
                                notify += '\nПоле ' + ShipHeadings[2] + ' не должно быть пустым'
                                Wrong = 1
                            if (Wrong == 1):
                                easygui.msgbox(notify, title)
                            else:
                                cur.execute("update ship set motherport='"+newvar+"' where regnum="+str(regnum))
                        if (var == 3):
                            Wrong = 0
                            try:
                                newvar = int(newvar)
                            except:
                                easygui.msgbox('Неверный тип поля ' + ShipHeadings[3], title)
                                Wrong = 1
                            if (Wrong == 0):
                                cur.execute("update ship set capacity="+str(newvar)+"where regnum="+str(regnum))
                        if (var == 4):
                            Wrong = 0
                            try:
                                newvar = int(newvar)
                            except:
                                easygui.msgbox('Неверный тип поля ' + ShipHeadings[4], title)
                                Wrong = 1
                            if (Wrong == 0):
                                cur.execute("update ship set shipprice="+str(newvar)+"where regnum="+str(regnum))
                        if (var == 5):
                            notify = ''
                            Wrong = 0
                            if (len(newvar) != 10 or newvar == ''):
                                notify += '\nДлина поля ' + ShipHeadings[5] + ' должна составлять 10 символов'
                                Wrong = 1
                            if (newvar != '' and len(newvar) == 10):
                                if (newvar[4] != '-' or newvar[7] != '-'):
                                    notify += '\nПоле ' + ShipHeadings[5] + ' должно быть в формате ГГГГ-ММ-ДД'
                                    Wrong = 1
                            if (Wrong == 1):
                                easygui.msgbox(notify, title)
                            else:
                                cur.execute("update ship set shipdate='"+newvar+"' where regnum="+str(regnum))
                        con.commit()
            else:
                easygui.msgbox('Такой записи нет в базе данных', title)
    def SearchForm(self):
        searchby = easygui.indexbox('Выберите поле для поиска', title, ShipHeadings)
        srch = easygui.enterbox('Введите значение поля ' + ShipHeadings[searchby] + ' для поиска')  
        if (searchby == 0):
            self.root = tk.Tk()
            dt = (datetime.now() - timedelta(minutes=30)).replace(microsecond=0)
            if (RoleIs == 'admin'):
                cur.execute('select * from ship where regnum=' + srch)
            elif (RoleIs == 'user'):
                cur.execute('select regnum,shipname,motherport from ship where regnum=' + srch)
            table = ShipTable(self.root, headings=ShipHeadings, rows=cur.fetchall(), buttons=0, role=RoleIs)
            table.pack(expand=tk.YES, fill=tk.BOTH)
            if (RoleIs == 'admin'):
                Del = Button(self.root, bg="gray", text=u"Удалить", command=self.DelForm)
                Del.pack(side=BOTTOM, fill='x')
                Sort = Button(self.root, bg="gray", text=u"Сортировать", command=self.SortForm)
                Sort.pack(side=BOTTOM, fill='x')
                Search = Button(self.root, bg="gray", text=u"Искать", command=self.SearchForm)
                Search.pack(side=BOTTOM, fill='x')
                Edit = Button(self.root, bg="gray", text=u"Редактировать", command=self.EditForm)
                Edit.pack(side=BOTTOM, fill='x')
                Add = Button(self.root, bg="gray", text=u"Добавить", command=self.AddForm)
                Add.pack(side=BOTTOM, fill='x')
            elif (RoleIs == 'user'):
                Sort = Button(self.root, bg="gray", text=u"Сортировать", command=self.SortForm)
                Sort.pack(side=BOTTOM, fill='x')
                Search = Button(self.root, bg="gray", text=u"Искать", command=self.SearchForm)
                Search.pack(side=BOTTOM, fill='x')
            self.root.mainloop()
        if (searchby == 1):
            self.root = tk.Tk()
            dt = (datetime.now() - timedelta(minutes=30)).replace(microsecond=0)
            if (RoleIs == 'admin'):
                cur.execute("select * from ship where shipname='" + srch + "'")
            elif (RoleIs == 'user'):
                cur.execute("select regnum,shipname,motherport from ship where shipname='" + srch + "'")
            table = ShipTable(self.root, headings=ShipHeadings, rows=cur.fetchall(), buttons=0, role=RoleIs)
            table.pack(expand=tk.YES, fill=tk.BOTH)
            if (RoleIs == 'admin'):
                Del = Button(self.root, bg="gray", text=u"Удалить", command=self.DelForm)
                Del.pack(side=BOTTOM, fill='x')
                Sort = Button(self.root, bg="gray", text=u"Сортировать", command=self.SortForm)
                Sort.pack(side=BOTTOM, fill='x')
                Search = Button(self.root, bg="gray", text=u"Искать", command=self.SearchForm)
                Search.pack(side=BOTTOM, fill='x')
                Edit = Button(self.root, bg="gray", text=u"Редактировать", command=self.EditForm)
                Edit.pack(side=BOTTOM, fill='x')
                Add = Button(self.root, bg="gray", text=u"Добавить", command=self.AddForm)
                Add.pack(side=BOTTOM, fill='x')
            elif (RoleIs == 'user'):
                Sort = Button(self.root, bg="gray", text=u"Сортировать", command=self.SortForm)
                Sort.pack(side=BOTTOM, fill='x')
                Search = Button(self.root, bg="gray", text=u"Искать", command=self.SearchForm)
                Search.pack(side=BOTTOM, fill='x')
            self.root.mainloop()
        if (searchby == 2):
            self.root = tk.Tk()
            dt = (datetime.now() - timedelta(minutes=30)).replace(microsecond=0)
            if (RoleIs == 'admin'):
                cur.execute("select * from ship where motherport='" + srch + "'")
            elif (RoleIs == 'user'):
                cur.execute("select regnum,shipname,motherport from ship where motherport='" + srch + "'")
            table = ShipTable(self.root, headings=ShipHeadings, rows=cur.fetchall(), buttons=0, role=RoleIs)
            table.pack(expand=tk.YES, fill=tk.BOTH)
            if (RoleIs == 'admin'):
                Del = Button(self.root, bg="gray", text=u"Удалить", command=self.DelForm)
                Del.pack(side=BOTTOM, fill='x')
                Sort = Button(self.root, bg="gray", text=u"Сортировать", command=self.SortForm)
                Sort.pack(side=BOTTOM, fill='x')
                Search = Button(self.root, bg="gray", text=u"Искать", command=self.SearchForm)
                Search.pack(side=BOTTOM, fill='x')
                Edit = Button(self.root, bg="gray", text=u"Редактировать", command=self.EditForm)
                Edit.pack(side=BOTTOM, fill='x')
                Add = Button(self.root, bg="gray", text=u"Добавить", command=self.AddForm)
                Add.pack(side=BOTTOM, fill='x')
            elif (RoleIs == 'user'):
                Sort = Button(self.root, bg="gray", text=u"Сортировать", command=self.SortForm)
                Sort.pack(side=BOTTOM, fill='x')
                Search = Button(self.root, bg="gray", text=u"Искать", command=self.SearchForm)
                Search.pack(side=BOTTOM, fill='x')
            self.root.mainloop()
        if (searchby == 3):
            self.root = tk.Tk()
            dt = (datetime.now() - timedelta(minutes=30)).replace(microsecond=0)
            cur.execute('select * from ship where capacity=' + srch)
            table = ShipTable(self.root, headings=ShipHeadings, rows=cur.fetchall(), buttons=0, role=RoleIs)
            table.pack(expand=tk.YES, fill=tk.BOTH)
            if (RoleIs == 'admin'):
                Del = Button(self.root, bg="gray", text=u"Удалить", command=self.DelForm)
                Del.pack(side=BOTTOM, fill='x')
                Sort = Button(self.root, bg="gray", text=u"Сортировать", command=self.SortForm)
                Sort.pack(side=BOTTOM, fill='x')
                Search = Button(self.root, bg="gray", text=u"Искать", command=self.SearchForm)
                Search.pack(side=BOTTOM, fill='x')
                Edit = Button(self.root, bg="gray", text=u"Редактировать", command=self.EditForm)
                Edit.pack(side=BOTTOM, fill='x')
                Add = Button(self.root, bg="gray", text=u"Добавить", command=self.AddForm)
                Add.pack(side=BOTTOM, fill='x')
            elif (RoleIs == 'user'):
                Sort = Button(self.root, bg="gray", text=u"Сортировать", command=self.SortForm)
                Sort.pack(side=BOTTOM, fill='x')
                Search = Button(self.root, bg="gray", text=u"Искать", command=self.SearchForm)
                Search.pack(side=BOTTOM, fill='x')
            self.root.mainloop()
        if (searchby == 4):
            self.root = tk.Tk()
            dt = (datetime.now() - timedelta(minutes=30)).replace(microsecond=0)
            cur.execute('select * from ship where shipprice=' + srch)
            table = ShipTable(self.root, headings=ShipHeadings, rows=cur.fetchall(), buttons=0, role=RoleIs)
            table.pack(expand=tk.YES, fill=tk.BOTH)
            if (RoleIs == 'admin'):
                Del = Button(self.root, bg="gray", text=u"Удалить", command=self.DelForm)
                Del.pack(side=BOTTOM, fill='x')
                Sort = Button(self.root, bg="gray", text=u"Сортировать", command=self.SortForm)
                Sort.pack(side=BOTTOM, fill='x')
                Search = Button(self.root, bg="gray", text=u"Искать", command=self.SearchForm)
                Search.pack(side=BOTTOM, fill='x')
                Edit = Button(self.root, bg="gray", text=u"Редактировать", command=self.EditForm)
                Edit.pack(side=BOTTOM, fill='x')
                Add = Button(self.root, bg="gray", text=u"Добавить", command=self.AddForm)
                Add.pack(side=BOTTOM, fill='x')
            elif (RoleIs == 'user'):
                Sort = Button(self.root, bg="gray", text=u"Сортировать", command=self.SortForm)
                Sort.pack(side=BOTTOM, fill='x')
                Search = Button(self.root, bg="gray", text=u"Искать", command=self.SearchForm)
                Search.pack(side=BOTTOM, fill='x')
            self.root.mainloop()
        if (searchby == 5):
            self.root = tk.Tk()
            dt = (datetime.now() - timedelta(minutes=30)).replace(microsecond=0)
            cur.execute("select * from ship where shipdate='" + srch + "'")
            table = ShipTable(self.root, headings=ShipHeadings, rows=cur.fetchall(), buttons=0, role=RoleIs)
            table.pack(expand=tk.YES, fill=tk.BOTH)
            if (RoleIs == 'admin'):
                Del = Button(self.root, bg="gray", text=u"Удалить", command=self.DelForm)
                Del.pack(side=BOTTOM, fill='x')
                Sort = Button(self.root, bg="gray", text=u"Сортировать", command=self.SortForm)
                Sort.pack(side=BOTTOM, fill='x')
                Search = Button(self.root, bg="gray", text=u"Искать", command=self.SearchForm)
                Search.pack(side=BOTTOM, fill='x')
                Edit = Button(self.root, bg="gray", text=u"Редактировать", command=self.EditForm)
                Edit.pack(side=BOTTOM, fill='x')
                Add = Button(self.root, bg="gray", text=u"Добавить", command=self.AddForm)
                Add.pack(side=BOTTOM, fill='x')
            elif (RoleIs == 'user'):
                Sort = Button(self.root, bg="gray", text=u"Сортировать", command=self.SortForm)
                Sort.pack(side=BOTTOM, fill='x')
                Search = Button(self.root, bg="gray", text=u"Искать", command=self.SearchForm)
                Search.pack(side=BOTTOM, fill='x')
            self.root.mainloop()
    def SortForm(self):
        sortby = easygui.indexbox('Выберите поле для сортировки', title, ShipHeadings)
        orderby = easygui.indexbox('Выберите направление сортировки', title, ('По убыванию','По возрастанию'))
        order, attr = '',''
        if (orderby == 0):
            order = 'desc'
        elif (orderby == 1):
            order = 'asc'
        if (RoleIs == 'admin'):
            for i in range(len(ShipAttrs)):
                if (sortby == i):
                    attr = ShipAttrs[i]
        elif (RoleIs == 'user'):
            for i in range(len(ShipAttrsUser)):
                if (sortby == i):
                    attr = ShipAttrsUser[i]
        self.root = tk.Tk()
        dt = (datetime.now() - timedelta(minutes=30)).replace(microsecond=0)
        if (RoleIs == 'admin'):
            cur.execute("select * from ship order by "+attr+" "+order)
        elif (RoleIs == 'user'):
            cur.execute("select regnum,shipname,motherport from ship order by "+attr+" "+order)
        table = ShipTable(self.root, headings=ShipHeadings, rows=cur.fetchall(), buttons=0, role=RoleIs)
        table.pack(expand=tk.YES, fill=tk.BOTH)
        if (RoleIs == 'admin'):
            Del = Button(self.root, bg="gray", text=u"Удалить", command=self.DelForm)
            Del.pack(side=BOTTOM, fill='x')
            Sort = Button(self.root, bg="gray", text=u"Сортировать", command=self.SortForm)
            Sort.pack(side=BOTTOM, fill='x')
            Search = Button(self.root, bg="gray", text=u"Искать", command=self.SearchForm)
            Search.pack(side=BOTTOM, fill='x')
            Edit = Button(self.root, bg="gray", text=u"Редактировать", command=self.EditForm)
            Edit.pack(side=BOTTOM, fill='x')
            Add = Button(self.root, bg="gray", text=u"Добавить", command=self.AddForm)
            Add.pack(side=BOTTOM, fill='x')
        elif (RoleIs == 'user'):
            Sort = Button(self.root, bg="gray", text=u"Сортировать", command=self.SortForm)
            Sort.pack(side=BOTTOM, fill='x')
            Search = Button(self.root, bg="gray", text=u"Искать", command=self.SearchForm)
            Search.pack(side=BOTTOM, fill='x')
        self.root.mainloop()
class GoodsTable(Table):
    def AddForm(self):
        AddValues = easygui.multenterbox('Заполните поля для добавления записи', title, GoodsHeadings)
        notify = ''
        Wrong = [0] * 4
        
        #Проверка goodsreg
        try:
            AddValues[0] = int(AddValues[0])
        except:
            notify += 'Неверный тип поля ' + GoodsHeadings[0]
            Wrong[0] = 1
        if (len(str(AddValues[0])) != 5):
            notify += '\nДлина поля ' + GoodsHeadings[0] + ' должна составлять 5 цифр' 
            Wrong[0] = 1
        dt = (datetime.now() - timedelta(minutes=30)).replace(microsecond=0)
        cur.execute("select goodsreg from goods")
        AddArr = cur.fetchall()
        ArrGoodsregs = [0] * len(AddArr)
        for i in range(len(AddArr)): 
            ArrGoodsregs[i] = int(AddArr[i][0])
        for i in range(len(ArrGoodsregs)):
            if (ArrGoodsregs[i] == AddValues[0]):
                notify += '\nПоле ' + GoodsHeadings[0] + ' должно быть уникальным'
                Wrong[0] = 1
                break
            
        #Проверка gname
        try:
            AddValues[1] = str(AddValues[1])
        except:
            notify += '\nНеверный тип поля ' + GoodsHeadings[1]
            Wrong[1] = 1
        if (len(str(AddValues[1])) > 20 or len(str(AddValues[1])) == 0):
            notify += '\nДлина поля ' + GoodsHeadings[1] + ' должна составлять не более 20 символов'
            Wrong[1] = 1
        if (AddValues[1] == ''):
            notify += '\nПоле ' + GoodsHeadings[1] + ' не должно быть пустым'
            Wrong[1] = 1
            
        #Проверка costs
        try:
            AddValues[2] = int(AddValues[2])
        except:
            notify += '\nНеверный тип поля ' + GoodsHeadings[2]
            Wrong[2] = 1
            
        #Проверка weight
        try:
            AddValues[3] = int(AddValues[3])
        except:
            notify += '\nНеверный тип поля ' + GoodsHeadings[3]
            Wrong[3] = 1
                
        AddFlag = 1
        if (any(el == 1 for el in Wrong)):
            easygui.msgbox(notify, title)
            AddFlag = 0
        
        if (AddValues != None and AddFlag == 1):
            dt = (datetime.now() - timedelta(minutes=30)).replace(microsecond=0)
            cur.execute("insert into goods (goodsreg,gname,costs,weight) values (?,?,?,?)",
                        (AddValues[0], AddValues[1], AddValues[2], AddValues[3]))
            con.commit(); 
    def DelForm(self):
        goodsreg = easygui.enterbox('Введите Рег_ном удаляемого груза', title)
        try:
            goodsreg = int(goodsreg)
        except:
            easygui.msgbox('Неверный тип поля', title)
            goodsreg = None
        if (goodsreg != None):
            dt = (datetime.now() - timedelta(minutes=30)).replace(microsecond=0)
            cur.execute("select goodsreg from goods")
            ArrGoodsregs = cur.fetchall()
            DelFlag = 0
            for i in range(len(ArrGoodsregs)):
                if (ArrGoodsregs[i][0] == int(goodsreg)):
                    DelFlag = 1
                    break
            if (DelFlag == 1):
                dt = (datetime.now() - timedelta(minutes=30)).replace(microsecond=0)
                cur.execute("delete from goods where goodsreg="+str(goodsreg))
                con.commit()
            else:
                easygui.msgbox('Такой записи нет в базе данных', title)
    def EditForm(self):
        goodsreg = easygui.enterbox('Введите Рег_ном редактируемого груза', title)
        try:
            goodsreg = int(goodsreg)
        except:
            easygui.msgbox('Неверный тип поля', title)
            goodsreg = None
        if (goodsreg != None):
            dt = (datetime.now() - timedelta(minutes=30)).replace(microsecond=0)
            cur.execute("select goodsreg from goods")
            ArrGoodsregs = cur.fetchall()
            EditFlag = 0
            for i in range(len(ArrGoodsregs)):
                if (ArrGoodsregs[i][0] == int(goodsreg)):
                    EditFlag = 1
                    break
            if (EditFlag == 1):
                var = easygui.indexbox('Выберите поле для редактирования', title, GoodsHeadings)
                if (var != None):
                    newvar = easygui.enterbox('Введите новое значения поля', title)
                    if (newvar != None):
                        dt = (datetime.now() - timedelta(minutes=30)).replace(microsecond=0)
                        Wrong = 0
                        if (var == 0):
                            notify = ''
                            Wrong = 0
                            try:
                                newvar = int(newvar)
                            except:
                                notify = 'Неверный тип поля ' + GoodsHeadings[0]
                                Wrong = 1
                            if (len(str(newvar)) != 5):
                                notify += '\nДлина поля ' + GoodsHeadings[0] + ' должна составлять 5 цифр'
                                Wrong = 1
                            dt = (datetime.now() - timedelta(minutes=30)).replace(microsecond=0)
                            cur.execute("select goodsreg from goods")
                            ArrGoodsregs = cur.fetchall()
                            for i in range(len(ArrGoodsregs)):
                                if (ArrGoodsregs[i][0] == int(newvar)):
                                    notify += '\nПоле ' + GoodsHeadings[0] + ' должно быть уникальным'
                                    Wrong = 1
                                    break
                            if (Wrong == 1):
                                easygui.msgbox(notify, title)
                            else:
                                cur.execute("update goods set goodsreg="+str(newvar)+"where goodsreg="+str(goodsreg))
                        if (var == 1):
                            notify = ''
                            Wrong = 0
                            if (len(newvar) > 20 or len(newvar) == 0):
                                notify += '\nДлина поля ' + GoodsHeadings[1] + ' должна составлять от 1 до 20 символов'
                                Wrong = 1
                            elif (newvar == ''):
                                notify += '\nПоле ' + GoodsHeadings[1] + ' не должно быть пустым'
                                Wrong = 1
                            if (Wrong == 1):
                                easygui.msgbox(notify, title)
                            else:
                                cur.execute("update goods set gname='"+newvar+"' where goodsreg="+str(goodsreg))
                        if (var == 2):
                            notify = ''
                            Wrong = 0
                            try:
                                newvar = int(newvar)
                            except:
                                notify = 'Неверный тип поля ' + GoodsHeadings[2]
                                Wrong = 1
                            if (Wrong == 1):
                                easygui.msgbox(notify, title)
                            else:
                                cur.execute("update goods set costs="+str(newvar)+"where goodsreg="+str(goodsreg))
                        if (var == 3):
                            Wrong = 0
                            try:
                                newvar = int(newvar)
                            except:
                                easygui.msgbox('Неверный тип поля ' + GoodsHeadings[3], title)
                                Wrong = 1
                            if (Wrong == 0):
                                cur.execute("update goods set weight="+str(newvar)+"where goodsreg="+str(goodsreg))
                        con.commit()
            else:
                easygui.msgbox('Такой записи нет в базе данных', title)
    def SearchForm(self):
        searchby = easygui.indexbox('Выберите поле для поиска', title, GoodsHeadings)
        srch = easygui.enterbox('Введите значение поля ' + GoodsHeadings[searchby] + ' для поиска')  
        if (searchby == 0):
            self.root = tk.Tk()
            dt = (datetime.now() - timedelta(minutes=30)).replace(microsecond=0)
            cur.execute('select * from goods where goodsreg=' + srch)
            table = GoodsTable(self.root, headings=GoodsHeadings, rows=cur.fetchall(), buttons=0, role=RoleIs)
            table.pack(expand=tk.YES, fill=tk.BOTH)
            if (RoleIs == 'admin'):
                Del = Button(self.root, bg="gray", text=u"Удалить", command=self.DelForm)
                Del.pack(side=BOTTOM, fill='x')
                Sort = Button(self.root, bg="gray", text=u"Сортировать", command=self.SortForm)
                Sort.pack(side=BOTTOM, fill='x')
                Search = Button(self.root, bg="gray", text=u"Искать", command=self.SearchForm)
                Search.pack(side=BOTTOM, fill='x')
                Edit = Button(self.root, bg="gray", text=u"Редактировать", command=self.EditForm)
                Edit.pack(side=BOTTOM, fill='x')
                Add = Button(self.root, bg="gray", text=u"Добавить", command=self.AddForm)
                Add.pack(side=BOTTOM, fill='x')
            elif (RoleIs == 'user'):
                Sort = Button(self.root, bg="gray", text=u"Сортировать", command=self.SortForm)
                Sort.pack(side=BOTTOM, fill='x')
                Search = Button(self.root, bg="gray", text=u"Искать", command=self.SearchForm)
                Search.pack(side=BOTTOM, fill='x')
            self.root.mainloop()
        if (searchby == 1):
            self.root = tk.Tk()
            dt = (datetime.now() - timedelta(minutes=30)).replace(microsecond=0)
            cur.execute("select * from goods where gname='" + srch + "'")
            table = GoodsTable(self.root, headings=GoodsHeadings, rows=cur.fetchall(), buttons=0, role=RoleIs)
            table.pack(expand=tk.YES, fill=tk.BOTH)
            if (RoleIs == 'admin'):
                Del = Button(self.root, bg="gray", text=u"Удалить", command=self.DelForm)
                Del.pack(side=BOTTOM, fill='x')
                Sort = Button(self.root, bg="gray", text=u"Сортировать", command=self.SortForm)
                Sort.pack(side=BOTTOM, fill='x')
                Search = Button(self.root, bg="gray", text=u"Искать", command=self.SearchForm)
                Search.pack(side=BOTTOM, fill='x')
                Edit = Button(self.root, bg="gray", text=u"Редактировать", command=self.EditForm)
                Edit.pack(side=BOTTOM, fill='x')
                Add = Button(self.root, bg="gray", text=u"Добавить", command=self.AddForm)
                Add.pack(side=BOTTOM, fill='x')
            elif (RoleIs == 'user'):
                Sort = Button(self.root, bg="gray", text=u"Сортировать", command=self.SortForm)
                Sort.pack(side=BOTTOM, fill='x')
                Search = Button(self.root, bg="gray", text=u"Искать", command=self.SearchForm)
                Search.pack(side=BOTTOM, fill='x')
            self.root.mainloop()
        if (searchby == 2):
            self.root = tk.Tk()
            dt = (datetime.now() - timedelta(minutes=30)).replace(microsecond=0)
            cur.execute("select * from goods where costs=" + srch)
            table = GoodsTable(self.root, headings=GoodsHeadings, rows=cur.fetchall(), buttons=0, role=RoleIs)
            table.pack(expand=tk.YES, fill=tk.BOTH)
            if (RoleIs == 'admin'):
                Del = Button(self.root, bg="gray", text=u"Удалить", command=self.DelForm)
                Del.pack(side=BOTTOM, fill='x')
                Sort = Button(self.root, bg="gray", text=u"Сортировать", command=self.SortForm)
                Sort.pack(side=BOTTOM, fill='x')
                Search = Button(self.root, bg="gray", text=u"Искать", command=self.SearchForm)
                Search.pack(side=BOTTOM, fill='x')
                Edit = Button(self.root, bg="gray", text=u"Редактировать", command=self.EditForm)
                Edit.pack(side=BOTTOM, fill='x')
                Add = Button(self.root, bg="gray", text=u"Добавить", command=self.AddForm)
                Add.pack(side=BOTTOM, fill='x')
            elif (RoleIs == 'user'):
                Sort = Button(self.root, bg="gray", text=u"Сортировать", command=self.SortForm)
                Sort.pack(side=BOTTOM, fill='x')
                Search = Button(self.root, bg="gray", text=u"Искать", command=self.SearchForm)
                Search.pack(side=BOTTOM, fill='x')
            self.root.mainloop()
        if (searchby == 3):
            self.root = tk.Tk()
            dt = (datetime.now() - timedelta(minutes=30)).replace(microsecond=0)
            cur.execute('select * from goods where weight=' + srch)
            table = GoodsTable(self.root, headings=GoodsHeadings, rows=cur.fetchall(), buttons=0, role=RoleIs)
            table.pack(expand=tk.YES, fill=tk.BOTH)
            if (RoleIs == 'admin'):
                Del = Button(self.root, bg="gray", text=u"Удалить", command=self.DelForm)
                Del.pack(side=BOTTOM, fill='x')
                Sort = Button(self.root, bg="gray", text=u"Сортировать", command=self.SortForm)
                Sort.pack(side=BOTTOM, fill='x')
                Search = Button(self.root, bg="gray", text=u"Искать", command=self.SearchForm)
                Search.pack(side=BOTTOM, fill='x')
                Edit = Button(self.root, bg="gray", text=u"Редактировать", command=self.EditForm)
                Edit.pack(side=BOTTOM, fill='x')
                Add = Button(self.root, bg="gray", text=u"Добавить", command=self.AddForm)
                Add.pack(side=BOTTOM, fill='x')
            elif (RoleIs == 'user'):
                Sort = Button(self.root, bg="gray", text=u"Сортировать", command=self.SortForm)
                Sort.pack(side=BOTTOM, fill='x')
                Search = Button(self.root, bg="gray", text=u"Искать", command=self.SearchForm)
                Search.pack(side=BOTTOM, fill='x')
            self.root.mainloop()
    def SortForm(self):
        sortby = easygui.indexbox('Выберите поле для сортировки', title, GoodsHeadings)
        orderby = easygui.indexbox('Выберите направление сортировки', title, ('По убыванию','По возрастанию'))
        order, attr = '',''
        if (orderby == 0):
            order = 'desc'
        elif (orderby == 1):
            order = 'asc'
        for i in range(len(GoodsAttrs)):
            if (sortby == i):
                attr = GoodsAttrs[i]
        self.root = tk.Tk()
        dt = (datetime.now() - timedelta(minutes=30)).replace(microsecond=0)
        cur.execute("select * from goods order by "+attr+" "+order)
        table = GoodsTable(self.root, headings=GoodsHeadings, rows=cur.fetchall(), buttons=0, role=RoleIs)
        table.pack(expand=tk.YES, fill=tk.BOTH)
        if (RoleIs == 'admin'):
            Del = Button(self.root, bg="gray", text=u"Удалить", command=self.DelForm)
            Del.pack(side=BOTTOM, fill='x')
            Sort = Button(self.root, bg="gray", text=u"Сортировать", command=self.SortForm)
            Sort.pack(side=BOTTOM, fill='x')
            Search = Button(self.root, bg="gray", text=u"Искать", command=self.SearchForm)
            Search.pack(side=BOTTOM, fill='x')
            Edit = Button(self.root, bg="gray", text=u"Редактировать", command=self.EditForm)
            Edit.pack(side=BOTTOM, fill='x')
            Add = Button(self.root, bg="gray", text=u"Добавить", command=self.AddForm)
            Add.pack(side=BOTTOM, fill='x')
        elif (RoleIs == 'user'):
            Sort = Button(self.root, bg="gray", text=u"Сортировать", command=self.SortForm)
            Sort.pack(side=BOTTOM, fill='x')
            Search = Button(self.root, bg="gray", text=u"Искать", command=self.SearchForm)
            Search.pack(side=BOTTOM, fill='x')
        self.root.mainloop()
class RouteTable(Table):        
    def AddForm(self):
        AddValues = easygui.multenterbox('Заполните поля для добавления записи', title, RouteHeadings)
        notify = ''
        Wrong = [0] * 5
        
        #Проверка rnum
        try:
            AddValues[0] = int(AddValues[0])
        except:
            notify += 'Неверный тип поля ' + RouteHeadings[0]
            Wrong[0] = 1
        if (len(str(AddValues[0])) != 3):
            notify += '\nДлина поля ' + RouteHeadings[0] + ' должна составлять 3 цифры' 
            Wrong[0] = 1
        dt = (datetime.now() - timedelta(minutes=30)).replace(microsecond=0)
        cur.execute("select rnum from route")
        AddArr = cur.fetchall()
        ArrRnums = [0] * len(AddArr)
        for i in range(len(AddArr)): 
            ArrRnums[i] = int(AddArr[i][0])
        for i in range(len(ArrRnums)):
            if (ArrRnums[i] == AddValues[0]):
                notify += '\nПоле ' + RouteHeadings[0] + ' должно быть уникальным'
                Wrong[0] = 1
                break
            
        #Проверка placefrom
        try:
            AddValues[1] = str(AddValues[1])
        except:
            notify += '\nНеверный тип поля ' + RouteHeadings[1]
            Wrong[1] = 1
        if (len(str(AddValues[1])) > 20 or len(str(AddValues[1])) == 0):
            notify += '\nДлина поля ' + RouteHeadings[1] + ' должна составлять не более 20 символов'
            Wrong[1] = 1
        if (AddValues[1] == ''):
            notify += '\nПоле ' + RouteHeadings[1] + ' не должно быть пустым'
            Wrong[1] = 1
            
        #Проверка placeto
        try:
            AddValues[2] = str(AddValues[2])
        except:
            notify += '\nНеверный тип поля ' + RouteHeadings[2]
            Wrong[2] = 1
        if (len(str(AddValues[2])) > 20 or len(str(AddValues[2])) == 0):
            notify += '\nДлина поля ' + RouteHeadings[2] + ' должна составлять не более 20 символов'
            Wrong[2] = 1
        if (AddValues[2] == ''):
            notify += '\nПоле ' + RouteHeadings[2] + ' не должно быть пустым'
            Wrong[2] = 1
            
        #Проверка toport
        try:
            AddValues[3] = str(AddValues[3])
        except:
            notify += '\nНеверный тип поля ' + RouteHeadings[3]
            Wrong[3] = 1
        if (len(str(AddValues[3])) != 10 or AddValues[3] == ''):
            notify += '\nДлина поля ' + RouteHeadings[3] + ' должна составлять 10 символов'
            Wrong[3] = 1
        if (AddValues[3] != '' and len(str(AddValues[3])) == 10):
            if (AddValues[3][4] != '-' or AddValues[3][7] != '-'):
                notify += '\nПоле ' + RouteHeadings[3] + ' должно быть в формате ГГГГ-ММ-ДД'
                Wrong[3] = 1
                
        #Проверка fromport
        try:
            AddValues[4] = str(AddValues[4])
        except:
            notify += '\nНеверный тип поля ' + RouteHeadings[4]
            Wrong[4] = 1
        if (len(str(AddValues[4])) != 10 or AddValues[4] == ''):
            notify += '\nДлина поля ' + RouteHeadings[4] + ' должна составлять 10 символов'
            Wrong[4] = 1
        if (AddValues[4] != '' and len(str(AddValues[4])) == 10):
            if (AddValues[4][4] != '-' or AddValues[4][7] != '-'):
                notify += '\nПоле ' + RouteHeadings[4] + ' должно быть в формате ГГГГ-ММ-ДД'
                Wrong[4] = 1
                
        AddFlag = 1
        if (any(el == 1 for el in Wrong)):
            easygui.msgbox(notify, title)
            AddFlag = 0
        
        if (AddValues != None and AddFlag == 1):
            dt = (datetime.now() - timedelta(minutes=30)).replace(microsecond=0)
            cur.execute("insert into route (rnum,placefrom,placeto,toport,fromport) values (?,?,?,?,?)",
                        (AddValues[0], AddValues[1], AddValues[2], AddValues[3], AddValues[4]))
            con.commit();
    def DelForm(self):
        rnum = easygui.enterbox('Введите номер удаляемой записи', title)
        try:
            rnum = int(rnum)
        except:
            easygui.msgbox('Неверный тип поля', title)
            rnum = None
        if (rnum != None):
            dt = (datetime.now() - timedelta(minutes=30)).replace(microsecond=0)
            cur.execute("select rnum from route")
            ArrRnums = cur.fetchall()
            DelFlag = 0
            for i in range(len(ArrRnums)):
                if (ArrRnums[i][0] == int(rnum)):
                    DelFlag = 1
                    break
            if (DelFlag == 1):
                dt = (datetime.now() - timedelta(minutes=30)).replace(microsecond=0)
                cur.execute("delete from route where rnum="+str(rnum))
                con.commit()
            else:
                easygui.msgbox('Такой записи нет в базе данных', title)
    def EditForm(self):
        rnum = easygui.enterbox('Введите номер редактируемой записи', title)
        try:
            rnum = int(rnum)
        except:
            easygui.msgbox('Неверный тип поля', title)
            rnum = None
        if (rnum != None):
            dt = (datetime.now() - timedelta(minutes=30)).replace(microsecond=0)
            cur.execute("select rnum from route")
            ArrRnums = cur.fetchall()
            EditFlag = 0
            for i in range(len(ArrRnums)):
                if (ArrRnums[i][0] == int(rnum)):
                    EditFlag = 1
                    break
            if (EditFlag == 1):
                var = easygui.indexbox('Выберите поле для редактирования', title, RouteHeadings)
                if (var != None):
                    newvar = easygui.enterbox('Введите новое значения поля', title)
                    if (newvar != None):
                        dt = (datetime.now() - timedelta(minutes=30)).replace(microsecond=0)
                        Wrong = 0
                        if (var == 0):
                            notify = ''
                            Wrong = 0
                            try:
                                newvar = int(newvar)
                            except:
                                notify = 'Неверный тип поля ' + RouteHeadings[0]
                                Wrong = 1
                            if (len(str(newvar)) != 3):
                                notify += '\nДлина поля ' + RouteHeadings[0] + ' должна составлять 3 цифры'
                                Wrong = 1
                            dt = (datetime.now() - timedelta(minutes=30)).replace(microsecond=0)
                            cur.execute("select rnum from route")
                            ArrRnums = cur.fetchall()
                            for i in range(len(ArrRnums)):
                                if (ArrRnums[i][0] == int(newvar)):
                                    notify += '\nПоле ' + RouteHeadings[0] + ' должно быть уникальным'
                                    Wrong = 1
                                    break
                            if (Wrong == 1):
                                easygui.msgbox(notify, title)
                            else:
                                cur.execute("update route set rnum="+str(newvar)+"where rnum="+str(rnum))
                        if (var == 1):
                            notify = ''
                            Wrong = 0
                            if (len(newvar) > 20 or len(newvar) == 0):
                                notify += '\nДлина поля ' + RouteHeadings[1] + ' должна составлять от 1 до 20 символов'
                                Wrong = 1
                            elif (newvar == ''):
                                notify += '\nПоле ' + RouteHeadings[1] + ' не должно быть пустым'
                                Wrong = 1
                            if (Wrong == 1):
                                easygui.msgbox(notify, title)
                            else:
                                cur.execute("update route set placefrom='"+newvar+"' where rnum="+str(rnum))
                        if (var == 2):
                            notify = ''
                            Wrong = 0
                            if (len(newvar) > 20 or len(newvar) == 0):
                                notify += '\nДлина поля ' + RouteHeadings[2] + ' должна составлять от 1 до 20 символов'
                                Wrong = 1
                            if (newvar == ''):
                                notify += '\nПоле ' + RouteHeadings[2] + ' не должно быть пустым'
                                Wrong = 1
                            if (Wrong == 1):
                                easygui.msgbox(notify, title)
                            else:
                                cur.execute("update route set placeto='"+newvar+"' where rnum="+str(rnum))
                        if (var == 3):
                            notify = ''
                            Wrong = 0
                            if (len(newvar) != 10 or newvar == ''):
                                notify += '\nДлина поля ' + RouteHeadings[3] + ' должна составлять 10 символов'
                                Wrong = 1
                            if (newvar != '' and len(newvar) == 10):
                                if (newvar[4] != '-' or newvar[7] != '-'):
                                    notify += '\nПоле ' + RouteHeadings[3] + ' должно быть в формате ГГГГ-ММ-ДД'
                                    Wrong = 1
                            if (Wrong == 1):
                                easygui.msgbox(notify, title)
                            else:
                                cur.execute("update route set toport='"+newvar+"' where rnum="+str(rnum))
                        if (var == 4):
                            notify = ''
                            Wrong = 0
                            if (len(newvar) != 10 or newvar == ''):
                                notify += '\nДлина поля ' + RouteHeadings[4] + ' должна составлять 10 символов'
                                Wrong = 1
                            if (newvar != '' and len(newvar) == 10):
                                if (newvar[4] != '-' or newvar[7] != '-'):
                                    notify += '\nПоле ' + RouteHeadings[4] + ' должно быть в формате ГГГГ-ММ-ДД'
                                    Wrong = 1
                            if (Wrong == 1):
                                easygui.msgbox(notify, title)
                            else:
                                cur.execute("update route set fromport='"+newvar+"' where rnum="+str(rnum))
                        con.commit()
            else:
                easygui.msgbox('Такой записи нет в базе данных', title)
    def SearchForm(self):
        searchby = easygui.indexbox('Выберите поле для поиска', title, RouteHeadings)
        srch = easygui.enterbox('Введите значение поля ' + RouteHeadings[searchby] + ' для поиска')  
        if (searchby == 0):
            self.root = tk.Tk()
            dt = (datetime.now() - timedelta(minutes=30)).replace(microsecond=0)
            if (RoleIs == 'admin'):
                cur.execute('select * from route where rnum=' + srch)
            elif (RoleIs == 'user'):
                cur.execute('select rnum,toport,fromport from route where rnum=' + srch)
            table = RouteTable(self.root, headings=RouteHeadings, rows=cur.fetchall(), buttons=0, role=RoleIs)
            table.pack(expand=tk.YES, fill=tk.BOTH)
            if (RoleIs == 'admin'):
                Del = Button(self.root, bg="gray", text=u"Удалить", command=self.DelForm)
                Del.pack(side=BOTTOM, fill='x')
                Sort = Button(self.root, bg="gray", text=u"Сортировать", command=self.SortForm)
                Sort.pack(side=BOTTOM, fill='x')
                Search = Button(self.root, bg="gray", text=u"Искать", command=self.SearchForm)
                Search.pack(side=BOTTOM, fill='x')
                Edit = Button(self.root, bg="gray", text=u"Редактировать", command=self.EditForm)
                Edit.pack(side=BOTTOM, fill='x')
                Add = Button(self.root, bg="gray", text=u"Добавить", command=self.AddForm)
                Add.pack(side=BOTTOM, fill='x')
            elif (RoleIs == 'user'):
                Sort = Button(self.root, bg="gray", text=u"Сортировать", command=self.SortForm)
                Sort.pack(side=BOTTOM, fill='x')
                Search = Button(self.root, bg="gray", text=u"Искать", command=self.SearchForm)
                Search.pack(side=BOTTOM, fill='x')
            self.root.mainloop()
        if (searchby == 1):
            self.root = tk.Tk()
            dt = (datetime.now() - timedelta(minutes=30)).replace(microsecond=0)
            if (RoleIs == 'admin'):
                cur.execute("select * from route where placefrom='" + srch + "'")
            elif (RoleIs == 'user'):
                cur.execute("select rnum,toport,fromport from route where toport='" + srch + "'")
            table = RouteTable(self.root, headings=RouteHeadings, rows=cur.fetchall(), buttons=0, role=RoleIs)
            table.pack(expand=tk.YES, fill=tk.BOTH)
            if (RoleIs == 'admin'):
                Del = Button(self.root, bg="gray", text=u"Удалить", command=self.DelForm)
                Del.pack(side=BOTTOM, fill='x')
                Sort = Button(self.root, bg="gray", text=u"Сортировать", command=self.SortForm)
                Sort.pack(side=BOTTOM, fill='x')
                Search = Button(self.root, bg="gray", text=u"Искать", command=self.SearchForm)
                Search.pack(side=BOTTOM, fill='x')
                Edit = Button(self.root, bg="gray", text=u"Редактировать", command=self.EditForm)
                Edit.pack(side=BOTTOM, fill='x')
                Add = Button(self.root, bg="gray", text=u"Добавить", command=self.AddForm)
                Add.pack(side=BOTTOM, fill='x')
            elif (RoleIs == 'user'):
                Sort = Button(self.root, bg="gray", text=u"Сортировать", command=self.SortForm)
                Sort.pack(side=BOTTOM, fill='x')
                Search = Button(self.root, bg="gray", text=u"Искать", command=self.SearchForm)
                Search.pack(side=BOTTOM, fill='x')
            self.root.mainloop()
        if (searchby == 2):
            self.root = tk.Tk()
            dt = (datetime.now() - timedelta(minutes=30)).replace(microsecond=0)
            if (RoleIs == 'admin'):
                cur.execute("select * from route where placeto='" + srch + "'")
            elif (RoleIs == 'user'):
                cur.execute("select rnum,toport,fromport from route where fromport='" + srch + "'")
            table = RouteTable(self.root, headings=RouteHeadings, rows=cur.fetchall(), buttons=0, role=RoleIs)
            table.pack(expand=tk.YES, fill=tk.BOTH)
            if (RoleIs == 'admin'):
                Del = Button(self.root, bg="gray", text=u"Удалить", command=self.DelForm)
                Del.pack(side=BOTTOM, fill='x')
                Sort = Button(self.root, bg="gray", text=u"Сортировать", command=self.SortForm)
                Sort.pack(side=BOTTOM, fill='x')
                Search = Button(self.root, bg="gray", text=u"Искать", command=self.SearchForm)
                Search.pack(side=BOTTOM, fill='x')
                Edit = Button(self.root, bg="gray", text=u"Редактировать", command=self.EditForm)
                Edit.pack(side=BOTTOM, fill='x')
                Add = Button(self.root, bg="gray", text=u"Добавить", command=self.AddForm)
                Add.pack(side=BOTTOM, fill='x')
            elif (RoleIs == 'user'):
                Sort = Button(self.root, bg="gray", text=u"Сортировать", command=self.SortForm)
                Sort.pack(side=BOTTOM, fill='x')
                Search = Button(self.root, bg="gray", text=u"Искать", command=self.SearchForm)
                Search.pack(side=BOTTOM, fill='x')
            self.root.mainloop()
        if (searchby == 3):
            self.root = tk.Tk()
            dt = (datetime.now() - timedelta(minutes=30)).replace(microsecond=0)
            cur.execute("select * from route where toport='" + srch + "'")
            table = RouteTable(self.root, headings=RouteHeadings, rows=cur.fetchall(), buttons=0, role=RoleIs)
            table.pack(expand=tk.YES, fill=tk.BOTH)
            if (RoleIs == 'admin'):
                Del = Button(self.root, bg="gray", text=u"Удалить", command=self.DelForm)
                Del.pack(side=BOTTOM, fill='x')
                Sort = Button(self.root, bg="gray", text=u"Сортировать", command=self.SortForm)
                Sort.pack(side=BOTTOM, fill='x')
                Search = Button(self.root, bg="gray", text=u"Искать", command=self.SearchForm)
                Search.pack(side=BOTTOM, fill='x')
                Edit = Button(self.root, bg="gray", text=u"Редактировать", command=self.EditForm)
                Edit.pack(side=BOTTOM, fill='x')
                Add = Button(self.root, bg="gray", text=u"Добавить", command=self.AddForm)
                Add.pack(side=BOTTOM, fill='x')
            elif (RoleIs == 'user'):
                Sort = Button(self.root, bg="gray", text=u"Сортировать", command=self.SortForm)
                Sort.pack(side=BOTTOM, fill='x')
                Search = Button(self.root, bg="gray", text=u"Искать", command=self.SearchForm)
                Search.pack(side=BOTTOM, fill='x')
            self.root.mainloop()
        if (searchby == 4):
            self.root = tk.Tk()
            dt = (datetime.now() - timedelta(minutes=30)).replace(microsecond=0)
            cur.execute("select * from route where fromport='" + srch + "'")
            table = RouteTable(self.root, headings=RouteHeadings, rows=cur.fetchall(), buttons=0, role=RoleIs)
            table.pack(expand=tk.YES, fill=tk.BOTH)
            if (RoleIs == 'admin'):
                Del = Button(self.root, bg="gray", text=u"Удалить", command=self.DelForm)
                Del.pack(side=BOTTOM, fill='x')
                Sort = Button(self.root, bg="gray", text=u"Сортировать", command=self.SortForm)
                Sort.pack(side=BOTTOM, fill='x')
                Search = Button(self.root, bg="gray", text=u"Искать", command=self.SearchForm)
                Search.pack(side=BOTTOM, fill='x')
                Edit = Button(self.root, bg="gray", text=u"Редактировать", command=self.EditForm)
                Edit.pack(side=BOTTOM, fill='x')
                Add = Button(self.root, bg="gray", text=u"Добавить", command=self.AddForm)
                Add.pack(side=BOTTOM, fill='x')
            elif (RoleIs == 'user'):
                Sort = Button(self.root, bg="gray", text=u"Сортировать", command=self.SortForm)
                Sort.pack(side=BOTTOM, fill='x')
                Search = Button(self.root, bg="gray", text=u"Искать", command=self.SearchForm)
                Search.pack(side=BOTTOM, fill='x')
            self.root.mainloop()
    def SortForm(self):
        sortby = easygui.indexbox('Выберите поле для сортировки', title, RouteHeadings)
        orderby = easygui.indexbox('Выберите направление сортировки', title, ('По убыванию','По возрастанию'))
        order, attr = '',''
        if (orderby == 0):
            order = 'desc'
        elif (orderby == 1):
            order = 'asc'
        if (RoleIs == 'admin'):
            for i in range(len(RouteAttrs)):
                if (sortby == i):
                    attr = RouteAttrs[i]
        elif (RoleIs == 'user'):
            for i in range(len(RouteAttrsUser)):
                if (sortby == i):
                    attr = RouteAttrsUser[i]
        self.root = tk.Tk()
        dt = (datetime.now() - timedelta(minutes=30)).replace(microsecond=0)
        if (RoleIs == 'admin'):
            cur.execute("select * from route order by "+attr+" "+order)
        elif (RoleIs == 'user'):
            cur.execute("select rnum,toport,fromport from route order by "+attr+" "+order)
        table = RouteTable(self.root, headings=RouteHeadings, rows=cur.fetchall(), buttons=0, role=RoleIs)
        table.pack(expand=tk.YES, fill=tk.BOTH)
        if (RoleIs == 'admin'):
            Del = Button(self.root, bg="gray", text=u"Удалить", command=self.DelForm)
            Del.pack(side=BOTTOM, fill='x')
            Sort = Button(self.root, bg="gray", text=u"Сортировать", command=self.SortForm)
            Sort.pack(side=BOTTOM, fill='x')
            Search = Button(self.root, bg="gray", text=u"Искать", command=self.SearchForm)
            Search.pack(side=BOTTOM, fill='x')
            Edit = Button(self.root, bg="gray", text=u"Редактировать", command=self.EditForm)
            Edit.pack(side=BOTTOM, fill='x')
            Add = Button(self.root, bg="gray", text=u"Добавить", command=self.AddForm)
            Add.pack(side=BOTTOM, fill='x')
        elif (RoleIs == 'user'):
            Sort = Button(self.root, bg="gray", text=u"Сортировать", command=self.SortForm)
            Sort.pack(side=BOTTOM, fill='x')
            Search = Button(self.root, bg="gray", text=u"Искать", command=self.SearchForm)
            Search.pack(side=BOTTOM, fill='x')
        self.root.mainloop()
class RentTable(Table):
    def AddForm(self):
        AddValues = easygui.multenterbox('Заполните поля для добавления записи', title, RentHeadings)
        notify = ''
        Wrong = [0] * 7
        
        #Проверка contract
        try:
            AddValues[0] = int(AddValues[0])
        except:
            notify += 'Неверный тип поля ' + RentHeadings[0]
            Wrong[0] = 1
        if (len(str(AddValues[0])) != 8):
            notify += '\nДлина поля ' + RentHeadings[0] + ' должна составлять 8 цифр' 
            Wrong[0] = 1
        dt = (datetime.now() - timedelta(minutes=30)).replace(microsecond=0)
        cur.execute("select contract from rent")
        AddArr = cur.fetchall()
        ArrContracts = [0] * len(AddArr)
        for i in range(len(AddArr)): 
            ArrContracts[i] = int(AddArr[i][0])
        for i in range(len(ArrContracts)):
            if (ArrContracts[i] == AddValues[0]):
                notify += '\nПоле ' + RentHeadings[0] + ' должно быть уникальным'
                Wrong[0] = 1
                break
            
        #Проверка shipnum
        try:
            AddValues[1] = int(AddValues[1])
        except:
            notify += '\nНеверный тип поля ' + RentHeadings[1]
            Wrong[1] = 1
        if (len(str(AddValues[1])) != 7):
            notify += '\nДлина поля ' + RentHeadings[1] + ' должна составлять 7 цифр' 
            Wrong[1] = 1
        dt = (datetime.now() - timedelta(minutes=30)).replace(microsecond=0)
        cur.execute("select shipnum from rent")
        AddArr = cur.fetchall()
        ArrShipnums = [0] * len(AddArr)
        for i in range(len(AddArr)): 
            ArrShipnums[i] = int(AddArr[i][0])
        for i in range(len(ArrShipnums)):
            if (ArrShipnums[i] == AddValues[1]):
                notify += '\nПоле ' + RentHeadings[1] + ' должно быть уникальным'
                Wrong[1] = 1
                break
        dt = (datetime.now() - timedelta(minutes=30)).replace(microsecond=0)
        cur.execute("select regnum from ship")
        AddArr = cur.fetchall()
        ArrRegnums = [0] * len(AddArr)
        for i in range(len(AddArr)): 
            ArrRegnums[i] = int(AddArr[i][0])
        IsInShip = 1
        for i in range(len(ArrRegnums)):
            if (ArrRegnums[i] == AddValues[1]):
                IsInShip = 1
                break
            IsInShip = 0
        if (IsInShip == 0):
            notify += '\nПоле ' + RentHeadings[1] + ' должно быть в таблице Корабль'
            Wrong[1] = 1
            
        #Проверка goodsnum
        try:
            AddValues[2] = int(AddValues[2])
        except:
            notify += '\nНеверный тип поля ' + RentHeadings[2]
            Wrong[2] = 1
        if (len(str(AddValues[2])) != 5):
            notify += '\nДлина поля ' + RentHeadings[2] + ' должна составлять 5 цифр' 
            Wrong[2] = 1
        dt = (datetime.now() - timedelta(minutes=30)).replace(microsecond=0)
        cur.execute("select goodsnum from rent")
        AddArr = cur.fetchall()
        AddGoodsnums = [0] * len(AddArr)
        for i in range(len(AddArr)): 
            AddGoodsnums[i] = int(AddArr[i][0])
        for i in range(len(AddGoodsnums)):
            if (AddGoodsnums[i] == AddValues[2]):
                notify += '\nПоле ' + RentHeadings[2] + ' должно быть уникальным'
                Wrong[2] = 1
                break
        dt = (datetime.now() - timedelta(minutes=30)).replace(microsecond=0)
        cur.execute("select goodsreg from goods")
        AddArr = cur.fetchall()
        ArrGoodsregs = [0] * len(AddArr)
        for i in range(len(AddArr)): 
            ArrGoodsregs[i] = int(AddArr[i][0])
        IsInGoods = 1
        for i in range(len(ArrGoodsregs)):
            if (ArrGoodsregs[i] == AddValues[2]):
                IsInGoods = 1
                break
            IsInGoods = 0
        if (IsInGoods == 0):
            notify += '\nПоле ' + RentHeadings[2] + ' должно быть в таблице Груз'
            Wrong[2] = 1
            
        #Проверка routenum
        try:
            AddValues[3] = int(AddValues[3])
        except:
            notify += '\nНеверный тип поля ' + RentHeadings[3]
            Wrong[3] = 1
        if (len(str(AddValues[3])) != 3):
            notify += '\nДлина поля ' + RentHeadings[3] + ' должна составлять 3 цифры' 
            Wrong[3] = 1
        dt = (datetime.now() - timedelta(minutes=30)).replace(microsecond=0)
        cur.execute("select routenum from rent")
        AddArr = cur.fetchall()
        AddRoutenums = [0] * len(AddArr)
        for i in range(len(AddArr)): 
            AddRoutenums[i] = int(AddArr[i][0])
        for i in range(len(AddRoutenums)):
            if (AddRoutenums[i] == AddValues[3]):
                notify += '\nПоле ' + RentHeadings[3] + ' должно быть уникальным'
                Wrong[3] = 1
                break
        dt = (datetime.now() - timedelta(minutes=30)).replace(microsecond=0)
        cur.execute("select rnum from route")
        AddArr = cur.fetchall()
        ArrRnums = [0] * len(AddArr)
        for i in range(len(AddArr)): 
            ArrRnums[i] = int(AddArr[i][0])
        IsInRoute = 1
        for i in range(len(ArrRnums)):
            if (ArrRnums[i] == AddValues[3]):
                IsInRoute = 1
                break
            IsInRoute = 0
        if (IsInRoute == 0):
            notify += '\nПоле ' + RentHeadings[3] + ' должно быть в таблице Маршрут'
            Wrong[3] = 1
                
        #Проверка price
        try:
            AddValues[4] = str(AddValues[4])
        except:
            notify += '\nНеверный тип поля ' + RouteHeadings[4]
            Wrong[4] = 1
            
        #Проверка starts
        try:
            AddValues[5] = str(AddValues[5])
        except:
            notify += '\nНеверный тип поля ' + RentHeadings[5]
            Wrong[5] = 1
        if (len(str(AddValues[5])) != 10 or AddValues[5] == ''):
            notify += '\nДлина поля ' + RentHeadings[5] + ' должна составлять 10 символов'
            Wrong[5] = 1
        if (AddValues[4] != '' and len(str(AddValues[5])) == 10):
            if (AddValues[5][4] != '-' or AddValues[5][7] != '-'):
                notify += '\nПоле ' + RentHeadings[5] + ' должно быть в формате ГГГГ-ММ-ДД'
                Wrong[5] = 1
                
        #Проверка starts
        try:
            AddValues[6] = str(AddValues[6])
        except:
            notify += '\nНеверный тип поля ' + RentHeadings[6]
            Wrong[6] = 1
        if (len(str(AddValues[6])) != 10 or AddValues[6] == ''):
            notify += '\nДлина поля ' + RentHeadings[6] + ' должна составлять 10 символов'
            Wrong[6] = 1
        if (AddValues[4] != '' and len(str(AddValues[6])) == 10):
            if (AddValues[6][4] != '-' or AddValues[6][7] != '-'):
                notify += '\nПоле ' + RentHeadings[6] + ' должно быть в формате ГГГГ-ММ-ДД'
                Wrong[6] = 1
                
        AddFlag = 1
        if (any(el == 1 for el in Wrong)):
            easygui.msgbox(notify, title)
            AddFlag = 0
        
        if (AddValues != None and AddFlag == 1):
            dt = (datetime.now() - timedelta(minutes=30)).replace(microsecond=0)
            cur.execute("insert into rent (contract,shipnum,goodsnum,routenum,price,starts,ends) values (?,?,?,?,?,?,?)",
                        (AddValues[0], AddValues[1], AddValues[2], AddValues[3], AddValues[4], AddValues[5], AddValues[6]))
            con.commit();
    def DelForm(self):
        contract = easygui.enterbox('Введите номер удаляемой записи', title)
        try:
            contract = int(contract)
        except:
            easygui.msgbox('Неверный тип поля', title)
            contract = None
        if (contract != None):
            dt = (datetime.now() - timedelta(minutes=30)).replace(microsecond=0)
            cur.execute("select contract from rent")
            ArrContracts = cur.fetchall()
            DelFlag = 0
            for i in range(len(ArrContracts)):
                if (ArrContracts[i][0] == int(contract)):
                    DelFlag = 1
                    break
            if (DelFlag == 1):
                dt = (datetime.now() - timedelta(minutes=30)).replace(microsecond=0)
                cur.execute("select shipnum from rent where contract="+str(contract))
                RegnumDel = cur.fetchall()
                
                dt = (datetime.now() - timedelta(minutes=30)).replace(microsecond=0)
                cur.execute("select goodsnum from rent where contract="+str(contract))
                GoodsnumDel = cur.fetchall()
                
                dt = (datetime.now() - timedelta(minutes=30)).replace(microsecond=0)
                cur.execute("select routenum from rent where contract="+str(contract))
                RoutenumDel = cur.fetchall()
                
                print(RegnumDel[0][0], GoodsnumDel[0][0], RoutenumDel[0][0])
                dt = (datetime.now() - timedelta(minutes=30)).replace(microsecond=0)
                cur.execute("delete from ship where regnum="+str(RegnumDel[0][0]))
                cur.execute("delete from goods where goodsreg="+str(GoodsnumDel[0][0]))
                cur.execute("delete from route where rnum="+str(RoutenumDel[0][0]))
                cur.execute("delete from rent where contract="+str(contract))
                con.commit()
            else:
                easygui.msgbox('Такой записи нет в базе данных', title)
    def EditForm(self):
        contract = easygui.enterbox('Введите номер редактируемого маршрута', title)
        try:
            contract = int(contract)
        except:
            easygui.msgbox('Неверный тип поля', title)
            contract = None
        if (contract != None):
            dt = (datetime.now() - timedelta(minutes=30)).replace(microsecond=0)
            cur.execute("select contract from rent")
            ArrContracts = cur.fetchall()
            EditFlag = 0
            for i in range(len(ArrContracts)):
                if (ArrContracts[i][0] == int(contract)):
                    EditFlag = 1
                    break
            if (EditFlag == 1):
                var = easygui.indexbox('Выберите поле для редактирования', title, RentHeadings)
                if (var != None):
                    newvar = easygui.enterbox('Введите новое значения поля', title)
                    if (newvar != None):
                        dt = (datetime.now() - timedelta(minutes=30)).replace(microsecond=0)
                        Wrong = 0
                        if (var == 0):
                            notify = ''
                            Wrong = 0
                            WrongType = 0
                            try:
                                newvar = int(newvar)
                            except:
                                notify = 'Неверный тип поля ' + RentHeadings[0]
                                Wrong = 1
                                WrongType = 1
                            if (WrongType == 0):
                                if (len(str(newvar)) != 8):
                                    notify += '\nДлина поля ' + ShipHeadings[0] + ' должна составлять 8 цифр'
                                    Wrong = 1
                                dt = (datetime.now() - timedelta(minutes=30)).replace(microsecond=0)
                                cur.execute("select contract from rent")
                                ArrContracts = cur.fetchall()
                                for i in range(len(ArrContracts)):
                                    if (ArrContracts[i][0] == newvar):
                                        notify += '\nПоле ' + RentHeadings[0] + ' должно быть уникальным'
                                        Wrong = 1
                                        break
                                if (Wrong == 1):
                                    easygui.msgbox(notify, title)
                                else:
                                    cur.execute("update rent set contract="+str(newvar)+"where contract="+str(contract))
                        if (var == 1):
                            notify = ''
                            Wrong = 0
                            WrongType = 0
                            try:
                                newvar = int(newvar)
                            except:
                                notify = 'Неверный тип поля ' + RentHeadings[1]
                                easygui.msgbox(notify, title)
                                print(1)
                                Wrong = 1
                                WrongType = 1
                            if (WrongType == 0):
                                if (len(str(newvar)) != 7):
                                    notify += '\nДлина поля ' + RentHeadings[1] + ' должна составлять 7 цифр'
                                    Wrong = 1
                                dt = (datetime.now() - timedelta(minutes=30)).replace(microsecond=0)
                                cur.execute("select shipnum from rent")
                                ArrShipnums = cur.fetchall()
                                print(ArrShipnums)
                                for i in range(len(ArrShipnums)):
                                    if (ArrShipnums[i][0] == newvar):
                                        notify += '\nПоле ' + RentHeadings[1] + ' должно быть уникальным'
                                        Wrong = 1
                                        break
                                dt = (datetime.now() - timedelta(minutes=30)).replace(microsecond=0)
                                cur.execute("select regnum from ship")
                                AddArr = cur.fetchall()
                                ArrRegnums = [0] * len(AddArr)
                                for i in range(len(AddArr)): 
                                    ArrRegnums[i] = int(AddArr[i][0])
                                IsInShip = 1
                                for i in range(len(ArrRegnums)):
                                    if (ArrRegnums[i] == newvar):
                                        IsInShip = 1
                                        break
                                    IsInShip = 0
                                if (IsInShip == 0):
                                    notify += '\nПоле ' + RentHeadings[1] + ' должно быть в таблице Корабль'
                                    Wrong = 1
                                if (Wrong == 1):
                                    easygui.msgbox(notify, title)
                                else:
                                    cur.execute("update rent set shipnum="+str(newvar)+"where contract="+str(contract))
                        if (var == 2):
                            notify = ''
                            Wrong = 0
                            WrongType = 0
                            try:
                                newvar = int(newvar)
                            except:
                                notify = 'Неверный тип поля ' + RentHeadings[2]
                                easygui.msgbox(notify, title)
                                Wrong = 1
                                WrongType = 1
                            if (WrongType == 0):
                                if (len(str(newvar)) != 5):
                                    notify += '\nДлина поля ' + RentHeadings[2] + ' должна составлять 5 цифр'
                                    Wrong = 1
                                dt = (datetime.now() - timedelta(minutes=30)).replace(microsecond=0)
                                cur.execute("select goodsnum from rent")
                                ArrGoodsnums = cur.fetchall()
                                for i in range(len(ArrGoodsnums)):
                                    if (ArrGoodsnums[i][0] == newvar):
                                        notify += '\nПоле ' + RentHeadings[2] + ' должно быть уникальным'
                                        Wrong = 1
                                        break
                                dt = (datetime.now() - timedelta(minutes=30)).replace(microsecond=0)
                                cur.execute("select goodsreg from goods")
                                AddArr = cur.fetchall()
                                ArrGoodsregs = [0] * len(AddArr)
                                for i in range(len(AddArr)): 
                                    ArrGoodsregs[i] = int(AddArr[i][0])
                                IsInGoods = 1
                                for i in range(len(ArrGoodsregs)):
                                    if (ArrGoodsregs[i] == newvar):
                                        IsInGoods = 1
                                        break
                                    IsInGoods = 0
                                if (IsInGoods == 0):
                                    notify += '\nПоле ' + RentHeadings[2] + ' должно быть в таблице Груз'
                                    Wrong = 1
                                if (Wrong == 1):
                                    easygui.msgbox(notify, title)
                                else:
                                    cur.execute("update rent set goodsnum="+str(newvar)+"where contract="+str(contract))
                        if (var == 3):
                            notify = ''
                            Wrong = 0
                            WrongType = 0
                            try:
                                newvar = int(newvar)
                            except:
                                notify = 'Неверный тип поля ' + RentHeadings[3]
                                easygui.msgbox(notify, title)
                                Wrong = 1
                                WrongType = 1
                            if (WrongType == 0):
                                if (len(str(newvar)) != 3):
                                    notify += '\nДлина поля ' + RentHeadings[3] + ' должна составлять 3 цифры'
                                    Wrong = 1
                                dt = (datetime.now() - timedelta(minutes=30)).replace(microsecond=0)
                                cur.execute("select routenum from rent")
                                ArrRoutenums = cur.fetchall()
                                for i in range(len(ArrRoutenums)):
                                    if (ArrRoutenums[i][0] == int(newvar)):
                                        notify += '\nПоле ' + RentHeadings[3] + ' должно быть уникальным'
                                        Wrong = 1
                                        break
                                dt = (datetime.now() - timedelta(minutes=30)).replace(microsecond=0)
                                cur.execute("select routenum from route")
                                AddArr = cur.fetchall()
                                ArrRoutenums = [0] * len(AddArr)
                                for i in range(len(AddArr)): 
                                    ArrRoutenums[i] = int(AddArr[i][0])
                                IsInRoute = 1
                                for i in range(len(ArrRoutenums)):
                                    if (ArrRoutenums[i] == newvar):
                                        IsInRoute = 1
                                        break
                                    IsInRoute = 0
                                if (IsInRoute == 0):
                                    notify += '\nПоле ' + RentHeadings[3] + ' должно быть в таблице Маршрут'
                                    Wrong = 1
                                if (Wrong == 1):
                                    easygui.msgbox(notify, title)
                                else:
                                    cur.execute("update rent set routenum="+str(newvar)+"where contract="+str(contract))
                        if (var == 4):
                            notify = ''
                            Wrong = 0
                            WrongType = 0
                            try:
                                newvar = int(newvar)
                            except:
                                notify = 'Неверный тип поля ' + RentHeadings[4]
                                easygui.msgbox(notify, title)
                                Wrong = 1
                                WrongType  =1
                            if (WrongType == 0):
                                if (len(newvar) != 3):
                                    notify += '\nДлина поля ' + RentHeadings[4] + ' должна составлять 3 цифры'
                                    Wrong = 1
    
                                if (Wrong == 1):
                                    easygui.msgbox(notify, title)
                                else:
                                    cur.execute("update rent set price="+str(newvar)+"where contract="+str(contract))
                            #else:
                        if (var == 5):
                            notify = ''
                            Wrong = 0
                            if (len(newvar) != 10 or newvar == ''):
                                notify += '\nДлина поля ' + RentHeadings[5] + ' должна составлять 10 символов'
                                Wrong = 1
                            if (newvar != '' and len(newvar) == 10):
                                if (newvar[4] != '-' or newvar[7] != '-'):
                                    notify += '\nПоле ' + RentHeadings[5] + ' должно быть в формате ГГГГ-ММ-ДД'
                                    Wrong = 1
                            if (Wrong == 1):
                                easygui.msgbox(notify, title)
                            else:
                                cur.execute("update ship set starts='"+newvar+"' where contract="+str(contract))
                        if (var == 6):
                            notify = ''
                            Wrong = 0
                            if (len(newvar) != 10 or newvar == ''):
                                notify += '\nДлина поля ' + RentHeadings[6] + ' должна составлять 10 символов'
                                Wrong = 1
                            if (newvar != '' and len(newvar) == 10):
                                if (newvar[4] != '-' or newvar[7] != '-'):
                                    notify += '\nПоле ' + RentHeadings[6] + ' должно быть в формате ГГГГ-ММ-ДД'
                                    Wrong = 1
                            if (Wrong == 1):
                                easygui.msgbox(notify, title)
                            else:
                                cur.execute("update ship set ends='"+newvar+"' where contract="+str(contract))
                        con.commit()
            else:
                easygui.msgbox('Такой записи нет в базе данных', title)
    def SearchForm(self):
        searchby = easygui.indexbox('Выберите поле для поиска', title, RentHeadings)
        srch = easygui.enterbox('Введите значение поля ' + RentHeadings[searchby] + ' для поиска')  
        if (searchby == 0):
            self.root = tk.Tk()
            dt = (datetime.now() - timedelta(minutes=30)).replace(microsecond=0)
            if (RoleIs == 'admin'):
                cur.execute('select * from rent where contract=' + srch)
            elif (RoleIs == 'user'):
                cur.execute('select contract,shipnum,price,starts,ends from rent where contract=' + srch)
            table = RentTable(self.root, headings=RentHeadings, rows=cur.fetchall(), buttons=0, role=RoleIs)
            table.pack(expand=tk.YES, fill=tk.BOTH)
            if (RoleIs == 'admin'):
                Del = Button(self.root, bg="gray", text=u"Удалить", command=self.DelForm)
                Del.pack(side=BOTTOM, fill='x')
                Sort = Button(self.root, bg="gray", text=u"Сортировать", command=self.SortForm)
                Sort.pack(side=BOTTOM, fill='x')
                Search = Button(self.root, bg="gray", text=u"Искать", command=self.SearchForm)
                Search.pack(side=BOTTOM, fill='x')
                Edit = Button(self.root, bg="gray", text=u"Редактировать", command=self.EditForm)
                Edit.pack(side=BOTTOM, fill='x')
                Add = Button(self.root, bg="gray", text=u"Добавить", command=self.AddForm)
                Add.pack(side=BOTTOM, fill='x')
            elif (RoleIs == 'user'):
                Sort = Button(self.root, bg="gray", text=u"Сортировать", command=self.SortForm)
                Sort.pack(side=BOTTOM, fill='x')
                Search = Button(self.root, bg="gray", text=u"Искать", command=self.SearchForm)
                Search.pack(side=BOTTOM, fill='x')
            self.root.mainloop()
        if (searchby == 1):
            self.root = tk.Tk()
            dt = (datetime.now() - timedelta(minutes=30)).replace(microsecond=0)
            if (RoleIs == 'admin'):
                cur.execute("select * from rent where shipnum=" + srch)
            elif (RoleIs == 'user'):
                cur.execute("select contract,shipnum,price,starts,ends from rent where shipnum=" + srch)
            table = RentTable(self.root, headings=RentHeadings, rows=cur.fetchall(), buttons=0, role=RoleIs)
            table.pack(expand=tk.YES, fill=tk.BOTH)
            if (RoleIs == 'admin'):
                Del = Button(self.root, bg="gray", text=u"Удалить", command=self.DelForm)
                Del.pack(side=BOTTOM, fill='x')
                Sort = Button(self.root, bg="gray", text=u"Сортировать", command=self.SortForm)
                Sort.pack(side=BOTTOM, fill='x')
                Search = Button(self.root, bg="gray", text=u"Искать", command=self.SearchForm)
                Search.pack(side=BOTTOM, fill='x')
                Edit = Button(self.root, bg="gray", text=u"Редактировать", command=self.EditForm)
                Edit.pack(side=BOTTOM, fill='x')
                Add = Button(self.root, bg="gray", text=u"Добавить", command=self.AddForm)
                Add.pack(side=BOTTOM, fill='x')
            elif (RoleIs == 'user'):
                Sort = Button(self.root, bg="gray", text=u"Сортировать", command=self.SortForm)
                Sort.pack(side=BOTTOM, fill='x')
                Search = Button(self.root, bg="gray", text=u"Искать", command=self.SearchForm)
                Search.pack(side=BOTTOM, fill='x')
            self.root.mainloop()
        if (searchby == 2):
            self.root = tk.Tk()
            dt = (datetime.now() - timedelta(minutes=30)).replace(microsecond=0)
            if (RoleIs == 'admin'):
                cur.execute("select * from rent where goodsnum=" + srch)
            elif (RoleIs == 'user'):
                cur.execute("select contract,shipnum,price,starts,ends from rent where price=" + srch)
            table = RentTable(self.root, headings=RentHeadings, rows=cur.fetchall(), buttons=0, role=RoleIs)
            table.pack(expand=tk.YES, fill=tk.BOTH)
            if (RoleIs == 'admin'):
                Del = Button(self.root, bg="gray", text=u"Удалить", command=self.DelForm)
                Del.pack(side=BOTTOM, fill='x')
                Sort = Button(self.root, bg="gray", text=u"Сортировать", command=self.SortForm)
                Sort.pack(side=BOTTOM, fill='x')
                Search = Button(self.root, bg="gray", text=u"Искать", command=self.SearchForm)
                Search.pack(side=BOTTOM, fill='x')
                Edit = Button(self.root, bg="gray", text=u"Редактировать", command=self.EditForm)
                Edit.pack(side=BOTTOM, fill='x')
                Add = Button(self.root, bg="gray", text=u"Добавить", command=self.AddForm)
                Add.pack(side=BOTTOM, fill='x')
            elif (RoleIs == 'user'):
                Sort = Button(self.root, bg="gray", text=u"Сортировать", command=self.SortForm)
                Sort.pack(side=BOTTOM, fill='x')
                Search = Button(self.root, bg="gray", text=u"Искать", command=self.SearchForm)
                Search.pack(side=BOTTOM, fill='x')
            self.root.mainloop()
        if (searchby == 3):
            self.root = tk.Tk()
            dt = (datetime.now() - timedelta(minutes=30)).replace(microsecond=0)
            if (RoleIs == 'admin'):
                cur.execute("select * from rent where routenum=" + srch)
            elif (RoleIs == 'user'):
                cur.execute("select contract,shipnum,price,starts,ends from rent where starts='" + srch + "'")
            table = RentTable(self.root, headings=RentHeadings, rows=cur.fetchall(), buttons=0, role=RoleIs)
            table.pack(expand=tk.YES, fill=tk.BOTH)
            if (RoleIs == 'admin'):
                Del = Button(self.root, bg="gray", text=u"Удалить", command=self.DelForm)
                Del.pack(side=BOTTOM, fill='x')
                Sort = Button(self.root, bg="gray", text=u"Сортировать", command=self.SortForm)
                Sort.pack(side=BOTTOM, fill='x')
                Search = Button(self.root, bg="gray", text=u"Искать", command=self.SearchForm)
                Search.pack(side=BOTTOM, fill='x')
                Edit = Button(self.root, bg="gray", text=u"Редактировать", command=self.EditForm)
                Edit.pack(side=BOTTOM, fill='x')
                Add = Button(self.root, bg="gray", text=u"Добавить", command=self.AddForm)
                Add.pack(side=BOTTOM, fill='x')
            elif (RoleIs == 'user'):
                Sort = Button(self.root, bg="gray", text=u"Сортировать", command=self.SortForm)
                Sort.pack(side=BOTTOM, fill='x')
                Search = Button(self.root, bg="gray", text=u"Искать", command=self.SearchForm)
                Search.pack(side=BOTTOM, fill='x')
            self.root.mainloop()
        if (searchby == 4):
            self.root = tk.Tk()
            dt = (datetime.now() - timedelta(minutes=30)).replace(microsecond=0)
            if (RoleIs == 'admin'):
                cur.execute("select * from rent where price=" + src)
            elif (RoleIs == 'user'):
                cur.execute("select contract,shipnum,price,starts,ends from rent where ends='" + srch + "'")
            table = RentTable(self.root, headings=RentHeadings, rows=cur.fetchall(), buttons=0, role=RoleIs)
            table.pack(expand=tk.YES, fill=tk.BOTH)
            if (RoleIs == 'admin'):
                Del = Button(self.root, bg="gray", text=u"Удалить", command=self.DelForm)
                Del.pack(side=BOTTOM, fill='x')
                Sort = Button(self.root, bg="gray", text=u"Сортировать", command=self.SortForm)
                Sort.pack(side=BOTTOM, fill='x')
                Search = Button(self.root, bg="gray", text=u"Искать", command=self.SearchForm)
                Search.pack(side=BOTTOM, fill='x')
                Edit = Button(self.root, bg="gray", text=u"Редактировать", command=self.EditForm)
                Edit.pack(side=BOTTOM, fill='x')
                Add = Button(self.root, bg="gray", text=u"Добавить", command=self.AddForm)
                Add.pack(side=BOTTOM, fill='x')
            elif (RoleIs == 'user'):
                Sort = Button(self.root, bg="gray", text=u"Сортировать", command=self.SortForm)
                Sort.pack(side=BOTTOM, fill='x')
                Search = Button(self.root, bg="gray", text=u"Искать", command=self.SearchForm)
                Search.pack(side=BOTTOM, fill='x')
            self.root.mainloop()
        if (searchby == 5):
            self.root = tk.Tk()
            dt = (datetime.now() - timedelta(minutes=30)).replace(microsecond=0)
            cur.execute("select * from rent where starts='" + src + "'")
            table = RentTable(self.root, headings=RentHeadings, rows=cur.fetchall(), buttons=0, role=RoleIs)
            table.pack(expand=tk.YES, fill=tk.BOTH)
            if (RoleIs == 'admin'):
                Del = Button(self.root, bg="gray", text=u"Удалить", command=self.DelForm)
                Del.pack(side=BOTTOM, fill='x')
                Sort = Button(self.root, bg="gray", text=u"Сортировать", command=self.SortForm)
                Sort.pack(side=BOTTOM, fill='x')
                Search = Button(self.root, bg="gray", text=u"Искать", command=self.SearchForm)
                Search.pack(side=BOTTOM, fill='x')
                Edit = Button(self.root, bg="gray", text=u"Редактировать", command=self.EditForm)
                Edit.pack(side=BOTTOM, fill='x')
                Add = Button(self.root, bg="gray", text=u"Добавить", command=self.AddForm)
                Add.pack(side=BOTTOM, fill='x')
            elif (RoleIs == 'user'):
                Sort = Button(self.root, bg="gray", text=u"Сортировать", command=self.SortForm)
                Sort.pack(side=BOTTOM, fill='x')
                Search = Button(self.root, bg="gray", text=u"Искать", command=self.SearchForm)
                Search.pack(side=BOTTOM, fill='x')
            self.root.mainloop()
        if (searchby == 6):
            self.root = tk.Tk()
            dt = (datetime.now() - timedelta(minutes=30)).replace(microsecond=0)
            cur.execute("select * from rent where ends='" + src + "'")
            table = RentTable(self.root, headings=RentHeadings, rows=cur.fetchall(), buttons=0, role=RoleIs)
            table.pack(expand=tk.YES, fill=tk.BOTH)
            if (RoleIs == 'admin'):
                Del = Button(self.root, bg="gray", text=u"Удалить", command=self.DelForm)
                Del.pack(side=BOTTOM, fill='x')
                Sort = Button(self.root, bg="gray", text=u"Сортировать", command=self.SortForm)
                Sort.pack(side=BOTTOM, fill='x')
                Search = Button(self.root, bg="gray", text=u"Искать", command=self.SearchForm)
                Search.pack(side=BOTTOM, fill='x')
                Edit = Button(self.root, bg="gray", text=u"Редактировать", command=self.EditForm)
                Edit.pack(side=BOTTOM, fill='x')
                Add = Button(self.root, bg="gray", text=u"Добавить", command=self.AddForm)
                Add.pack(side=BOTTOM, fill='x')
            elif (RoleIs == 'user'):
                Sort = Button(self.root, bg="gray", text=u"Сортировать", command=self.SortForm)
                Sort.pack(side=BOTTOM, fill='x')
                Search = Button(self.root, bg="gray", text=u"Искать", command=self.SearchForm)
                Search.pack(side=BOTTOM, fill='x')
            self.root.mainloop()
    def SortForm(self):
        sortby = easygui.indexbox('Выберите поле для сортировки', title, RentHeadings)
        orderby = easygui.indexbox('Выберите направление сортировки', title, ('По убыванию','По возрастанию'))
        order, attr = '',''
        if (orderby == 0):
            order = 'desc'
        elif (orderby == 1):
            order = 'asc'
        if (RoleIs == 'admin'):
            for i in range(len(RentAttrs)):
                if (sortby == i):
                    attr = RentAttrs[i]
        elif (RoleIs == 'user'):
            for i in range(len(RentAttrsUser)):
                if (sortby == i):
                    attr = RentAttrsUser[i]
        self.root = tk.Tk()
        dt = (datetime.now() - timedelta(minutes=30)).replace(microsecond=0)
        if (RoleIs == 'admin'):
            cur.execute("select * from rent order by "+attr+" "+order)
        elif (RoleIs == 'user'):
            cur.execute("select contract,shipnum,price,starts,ends from rent order by "+attr+" "+order)
        table = RentTable(self.root, headings=RentHeadings, rows=cur.fetchall(), buttons=0, role=RoleIs)
        table.pack(expand=tk.YES, fill=tk.BOTH)
        if (RoleIs == 'admin'):
            Del = Button(self.root, bg="gray", text=u"Удалить", command=self.DelForm)
            Del.pack(side=BOTTOM, fill='x')
            Sort = Button(self.root, bg="gray", text=u"Сортировать", command=self.SortForm)
            Sort.pack(side=BOTTOM, fill='x')
            Search = Button(self.root, bg="gray", text=u"Искать", command=self.SearchForm)
            Search.pack(side=BOTTOM, fill='x')
            Edit = Button(self.root, bg="gray", text=u"Редактировать", command=self.EditForm)
            Edit.pack(side=BOTTOM, fill='x')
            Add = Button(self.root, bg="gray", text=u"Добавить", command=self.AddForm)
            Add.pack(side=BOTTOM, fill='x')
        elif (RoleIs == 'user'):
            Sort = Button(self.root, bg="gray", text=u"Сортировать", command=self.SortForm)
            Sort.pack(side=BOTTOM, fill='x')
            Search = Button(self.root, bg="gray", text=u"Искать", command=self.SearchForm)
            Search.pack(side=BOTTOM, fill='x')
        self.root.mainloop()
#easygui.egdemo()
title = 'База данных порта' # Заголовок

EnterFlag = 0
login = [0] * 2
RoleIs = ''
while (EnterFlag == 0 and login != None):
    login = easygui.multenterbox('Вход в базу данных порта', title, ['Имя пользователя', 'Пароль'])
    if (login == None):
        sys.exit(0)
    if (login == ['sysdba', 'masterkey'] or login == ['user', 'user']):
        # Соединение
        con = fdb.connect(dsn='C:/db_port', user='sysdba', password='masterkey')
        # Объект курсора
        cur = con.cursor()
        if (login == ['sysdba', 'masterkey']):
            RoleIs = 'admin'
        elif (login == ['user', 'user']):
            RoleIs = 'user'
        EnterFlag = 1
        easygui.msgbox('Вход выполнен успешно', title)
    else:
        easygui.msgbox('Неверное имя пользователя или пароль', title)
        EnterFlag = 0
        
# Атрибуты всех таблиц
if (RoleIs == 'admin'):
    ShipHeadings = ('Рег_ном', 'Название', 'Приписка', 'Грузоподъемность', 'Стоимость', 'Дата спуска')
    GoodsHeadings = ('Рег_ном', 'Наименование', 'Ценность', 'Вес')
    RouteHeadings = ('Номер', 'Откуда', 'Куда', 'Дата в порт', 'Дата из порта')
    RentHeadings = ('Договор', 'Ном_кор', 'Ном_гр', 'Ном_марш', 'Стоимость', 'Начало', 'Конец')
elif (RoleIs == 'user'):
    ShipHeadings = ('Рег_ном', 'Название', 'Приписка')
    GoodsHeadings = ('Рег_ном', 'Наименование', 'Ценность', 'Вес')
    RouteHeadings = ('Номер', 'Дата в порт', 'Дата из порта')
    RentHeadings = ('Договор', 'Ном_кор', 'Стоимость', 'Начало', 'Конец')

tabchoice = 100
while (tabchoice != 4):
    tabchoice = easygui.indexbox('Выберите таблицу', title, ('Корабль', 'Груз', 'Маршрут', 'Аренда', 'Выход'))
    if (tabchoice == 0):
        root = tk.Tk()
        dt = (datetime.now() - timedelta(minutes=30)).replace(microsecond=0)
        if (RoleIs == 'admin'):
            cur.execute("select * from ship")
        elif (RoleIs == 'user'):
            cur.execute("select regnum,shipname,motherport from ship")
        table = ShipTable(root, headings=ShipHeadings, rows=cur.fetchall(), role=RoleIs)
        table.pack(expand=tk.YES, fill=tk.BOTH)
        root.mainloop()
    elif (tabchoice == 1):
        root = tk.Tk()
        dt = (datetime.now() - timedelta(minutes=30)).replace(microsecond=0)
        cur.execute("select * from goods")
        table = GoodsTable(root, headings=GoodsHeadings, rows=cur.fetchall(), role=RoleIs)
        table.pack(expand=tk.YES, fill=tk.BOTH)
        root.mainloop()
    elif (tabchoice == 2):
        root = tk.Tk()
        dt = (datetime.now() - timedelta(minutes=30)).replace(microsecond=0)
        if (RoleIs == 'admin'):
            cur.execute("select * from route")
        elif (RoleIs == 'user'):
            cur.execute("select rnum,toport,fromport from route")
        table = RouteTable(root, headings=RouteHeadings, rows=cur.fetchall(), role=RoleIs)
        table.pack(expand=tk.YES, fill=tk.BOTH)
        root.mainloop()
    elif (tabchoice == 3):
        root = tk.Tk()
        dt = (datetime.now() - timedelta(minutes=30)).replace(microsecond=0)
        if (RoleIs == 'admin'):
            cur.execute("select * from rent")
        elif (RoleIs == 'user'):
            cur.execute("select contract,shipnum,price,starts,ends from rent")
        table = RentTable(root, headings=RentHeadings, rows=cur.fetchall(), role=RoleIs)
        table.pack(expand=tk.YES, fill=tk.BOTH)
        root.mainloop()
