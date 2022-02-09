# -*- coding: utf-8 -*-
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox
import sqlite3
database_connect = sqlite3.connect('data.db')
database_cursor = database_connect.cursor()
data_sheet = ''
combobox1_get = ''
def database_connect_function():
    def handle_sheet():
        global data_sheet
        data_sheet = combobox1.get()
        try:
            database_cursor.execute('select * from ' + data_sheet).fetchall()
        except:
            tk.messagebox.showerror('连接失败！','连接失败！')
        else:
            tk.messagebox.showinfo('连接成功！','连接成功')
            root_connect_to_database.destroy()
            edit_database_function()
    def create_sheet():
        def create_sheet_function():
            table_name = entry1.get()
            table_attribute_num = entry2.get()
            table_attribute_len = entry3.get()
            if int(table_attribute_num) >=8:
                table_attribute_num = 7
                tk.messagebox.showerror('属性个数错误','属性个数太多，已自动修改为7！')
            sql_sentence = 'create table ' + table_name + '(id int(10) primary key,'
            for i in range(int(table_attribute_num)):
                sql_sentence += 'name' + str(i + 1) + ' str(' + str(table_attribute_len) + '),'
            sql_sentence = sql_sentence[0:-1] + ')'
            database_cursor.execute(sql_sentence)
            root_database_connect_function_create_database.destroy()
            root_connect_to_database.destroy()
            database_connect_function()
        root_database_connect_function_create_database = tk.Tk()
        root_database_connect_function_create_database.geometry('400x250')
        label2 = tk.Label(root_database_connect_function_create_database,text = '创建数据表').pack()
        label3 = tk.Label(root_database_connect_function_create_database,text = '表名：').place(x = 50,y = 50)
        label4 = tk.Label(root_database_connect_function_create_database,text = '数据属性个数：').place(x = 50,y = 100)
        label5 = tk.Label(root_database_connect_function_create_database,text = '属性长度：').place(x = 50,y = 150)
        entry1 = tk.Entry(root_database_connect_function_create_database)
        entry1.place(x = 150,y = 50)
        entry2 = tk.Entry(root_database_connect_function_create_database)
        entry2.place(x = 150,y = 100)
        entry3 = tk.Entry(root_database_connect_function_create_database)
        entry3.place(x = 150,y = 150)
        button3 = tk.Button(root_database_connect_function_create_database,text = '创建',command = create_sheet_function).place(x = 175,y = 200)
        root_database_connect_function_create_database.mainloop()
    table_name_tuple1 = database_cursor.execute("select name from sqlite_master where type = 'table' order by name").fetchall()
    table_name_tuple2 = []
    for i in table_name_tuple1:
        table_name_tuple2.append(i[0])
    root_connect_to_database = tk.Tk()
    root_connect_to_database.geometry('300x150')
    label1 = tk.Label(root_connect_to_database,text = '选择数据表').place(x = 125,y = 10)
    str_var = tk.StringVar()
    combobox1 = ttk.Combobox(root_connect_to_database,textvariable = str_var)
    combobox1.place(x = 65,y = 50)
    button1 = tk.Button(root_connect_to_database,text = '连接',command = handle_sheet,fg = 'red').place(x = 75,y = 90)
    button2 = tk.Button(root_connect_to_database,text = '创建',command = create_sheet,fg = 'red').place(x = 195,y = 90)
    combobox1['value'] = tuple(table_name_tuple2)
    root_connect_to_database.mainloop()
def edit_database_function():
    def create():
        def handle():
            data_list = []
            for i in obj_list:
                data_list.append(i.get())
            handle_str = 'insert into ' + data_sheet + '('
            for i in name:
                handle_str += i + ','
            handle_str = handle_str[:-1] + ") values (" + str(len(table_info_get) + 1) + ",'"
            for i in data_list:
                handle_str += i + "','"
            handle_str = handle_str[:-2] + ")"
            try:
                database_cursor.execute(handle_str)
            except:
                tk.messagebox.showerror('插入失败','插入失败')
            else:
                tk.messagebox.showinfo('插入成功','插入成功')
                database_connect.commit()
            root_edit_database_create.destroy()
            root_edit_database.destroy()
            edit_database_function()
        root_edit_database_create = tk.Tk()
        name = []
        for i in table_heads:
            name.append(i[1])
        obj_list = []
        for i in name[1:]:
            tk.Label(root_edit_database_create,text = i + ':').pack()
            obj_list.append(tk.Entry(root_edit_database_create))
            obj_list[int(i[4:]) - 1].pack()
        button4 = tk.Button(root_edit_database_create,text = '插入',command = handle).pack()
        root_edit_database_create.mainloop()
    def update():
        def handle():
            global find_data_num
            try:
                find_data_num = int(entry1.get())
            except:
                tk.messagebox.showerror('输入id错误！','输入id错误！')
            data_list = []
            for i in obj_list:
                data_list.append(i.get())
            handle_str = 'update ' + data_sheet + ' set '
            count = 1
            for i in data_list:
                handle_str += 'name' + str(count) + " = '" + i + "',"
                count += 1
            handle_str = handle_str[:-1] + ' where id = ' + str(find_data_num)
            try:
                database_cursor.execute(handle_str)
            except:
                tk.messagebox.showerror('修改失败','修改失败')
            else:
                tk.messagebox.showinfo('修改成功', '修改成功')
            database_connect.commit()
            root_edit_database_update.destroy()
            root_edit_database.destroy()
            edit_database_function()
        root_edit_database_update = tk.Tk()
        tk.Label(root_edit_database_update, text = 'id：').pack()
        entry1 = tk.Entry(root_edit_database_update)
        entry1.pack()
        name = []
        for i in table_heads:
            name.append(i[1])
        obj_list = []
        for i in name[1:]:
            tk.Label(root_edit_database_update, text=i + ':').pack()
            obj_list.append(tk.Entry(root_edit_database_update))
            obj_list[int(i[4:]) - 1].pack()
        button5 = tk.Button(root_edit_database_update, text='修改', command=handle).pack()
        root_edit_database_update.mainloop()
    def delete():
        def handle():
            handle_str = 'delete from ' + data_sheet + ' where id = ' + entry2.get()
            try:
                database_cursor.execute(handle_str)
            except:
                tk.messagebox.showerror('删除失败','删除失败')
            else:
                tk.messagebox.showinfo('删除成功', '删除成功')
            database_connect.commit()
            root_edit_database_delete.destroy()
            root_edit_database.destroy()
            edit_database_function()
        root_edit_database_delete = tk.Tk()
        label2 = tk.Label(root_edit_database_delete,text = 'id：').pack()
        entry2 = tk.Entry(root_edit_database_delete)
        entry2.pack()
        button6 = tk.Button(root_edit_database_delete,text = '删除',command = handle).pack()
        root_edit_database_delete.mainloop()
    global data_sheet
    root_edit_database = tk.Tk()
    root_edit_database.geometry('1920x1080')
    menu = tk.Menu(root_edit_database)
    menu_edit = tk.Menu(menu,tearoff = True)
    menu.add_cascade(label = '编辑',menu = menu_edit)
    menu_edit.add_command(label = '插入',command = create)
    menu_edit.add_command(label = '修改',command = update)
    menu_edit.add_command(label = '删除',command = delete)
    root_edit_database.config(menu = menu)
    table_heads = database_cursor.execute('PRAGMA table_info(' + data_sheet + ')').fetchall()
    table_heads_list = []
    table_info_get = database_cursor.execute('select * from ' + data_sheet).fetchall()
    for head in table_heads:
        table_heads_list.append(head[1])
    treeview = ttk.Treeview(root_edit_database,columns = tuple(table_heads_list[1:]))
    for head in table_heads:
        treeview.heading('#' + str(head[0]),text = head[1])
    for info in table_info_get:
        treeview.insert('',index = tk.END,text = info[0],values = info[1:])
    scrollbar = ttk.Scrollbar(root_edit_database,orient = 'vertical',command = treeview.yview)
    scrollbar.pack(side = tk.RIGHT,fill = tk.Y)
    treeview.pack()
    treeview.configure(yscrollcommand = scrollbar.set)
    root_edit_database.mainloop()
database_connect_function()
database_cursor.close()
database_connect.commit()
database_connect.close()
