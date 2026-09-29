import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import mysql.connector
from mysql.connector import Error
from datetime import datetime
import csv

# ============================================================
# CLASE LOGIN
# ============================================================
class Login:
    def __init__(self, root, conexion):
        self.root = root
        self.conexion = conexion
        self.autenticado = False
        self.usuario_actual = None
        self.root.title("Iniciar Sesión - Tienda Genérica")
        self.root.geometry("450x400")
        self.root.resizable(False, False)
        self.root.eval('tk::PlaceWindow . center')
        self.intentos = 0
        self.max_intentos = 3
        self.crear_interfaz()

    def crear_interfaz(self):
        main_frame = tk.Frame(self.root, bg="#34495e", padx=30, pady=20)
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)

        tk.Label(main_frame, text="TIENDA GENÉRICA",
                 font=("Arial", 18, "bold"),
                 bg="#34495e", fg="#ecf0f1").pack(pady=(0, 5))
        tk.Label(main_frame, text="Inicio de Sesión",
                 font=("Arial", 12),
                 bg="#34495e", fg="#bdc3c7").pack(pady=(0, 20))

        # Usuario
        frame_user = tk.Frame(main_frame, bg="#34495e")
        frame_user.pack(fill='x', pady=8)
        tk.Label(frame_user, text="Usuario:",
                 font=("Arial", 10), bg="#34495e", fg="#ecf0f1", anchor='w').pack(fill='x')
        self.entry_usuario = tk.Entry(frame_user, font=("Arial", 11),
                                      relief="flat", bg="#ecf0f1", bd=5)
        self.entry_usuario.pack(fill='x', pady=(3, 0))
        self.entry_usuario.focus()
        self.entry_usuario.bind('<Return>', lambda e: self.entry_password.focus())

        # Contraseña
        frame_pass = tk.Frame(main_frame, bg="#34495e")
        frame_pass.pack(fill='x', pady=8)
        tk.Label(frame_pass, text="Contraseña:",
                 font=("Arial", 10), bg="#34495e", fg="#ecf0f1", anchor='w').pack(fill='x')
        self.entry_password = tk.Entry(frame_pass, font=("Arial", 11),
                                       show="*", relief="flat", bg="#ecf0f1", bd=5)
        self.entry_password.pack(fill='x', pady=(3, 0))
        self.entry_password.bind('<Return>', lambda e: self.validar_login())

        self.label_estado = tk.Label(main_frame, text="",
                                     font=("Arial", 9),
                                     bg="#34495e", fg="#e74c3c")
        self.label_estado.pack(pady=5)

        btn_login = tk.Button(main_frame, text="INICIAR SESIÓN",
                              font=("Arial", 11, "bold"),
                              bg="#27ae60", fg="white",
                              activebackground="#229954",
                              relief="flat", cursor="hand2",
                              command=self.validar_login)
        btn_login.pack(fill='x', pady=(15, 5), ipady=8)

        btn_salir = tk.Button(main_frame, text="Salir",
                              font=("Arial", 9),
                              bg="#95a5a6", fg="white",
                              relief="flat", cursor="hand2",
                              command=self.root.destroy)
        btn_salir.pack(fill='x', ipady=3)

        tk.Label(main_frame, text="Usuario demo: admininicial / admin123456",
                 font=("Arial", 8, "italic"),
                 bg="#34495e", fg="#7f8c8d").pack(pady=(10, 0))

    def validar_login(self):
        usuario = self.entry_usuario.get().strip()
        password = self.entry_password.get().strip()
        if not usuario or not password:
            self.label_estado.config(text="Complete todos los campos")
            return
        try:
            cursor = self.conexion.cursor(dictionary=True)
            query = """SELECT cedula, usuario, nombre_completo, correo
                       FROM usuarios
                       WHERE usuario = %s AND password = %s AND activo = 1"""
            cursor.execute(query, (usuario, password))
            resultado = cursor.fetchone()
            if resultado:
                self.autenticado = True
                self.usuario_actual = resultado
                messagebox.showinfo("Bienvenido",
                                    f"Hola {resultado['nombre_completo']}!")
                self.root.destroy()
            else:
                self.intentos += 1
                intentos_restantes = self.max_intentos - self.intentos
                if intentos_restantes > 0:
                    self.label_estado.config(
                        text=f"Credenciales incorrectas. Intentos: {intentos_restantes}")
                    self.entry_password.delete(0, tk.END)
                else:
                    messagebox.showerror("Bloqueado",
                                         "Demasiados intentos fallidos.")
                    self.root.destroy()
        except Error as e:
            messagebox.showerror("Error", f"Error al validar: {e}")


# ============================================================
# CLASE PRINCIPAL - SISTEMA TIENDA GENÉRICA
# ============================================================
class TiendaGenerica:
    def __init__(self, root, conexion, usuario_actual):
        self.root = root
        self.conexion = conexion
        self.usuario_actual = usuario_actual
        self.root.title(f"SISTEMA TIENDA GENÉRICA - Usuario: {usuario_actual['usuario']}")
        self.root.geometry("1280x800")

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # Crear pestañas según los módulos del proyecto
        self.crear_pestana_usuarios()
        self.crear_pestana_clientes()
        self.crear_pestana_proveedores()
        self.crear_pestana_productos()
        self.crear_pestana_ventas()
        self.crear_pestana_reportes()

    # ============================================================
    # MÓDULO USUARIOS (Sprint 1)
    # ============================================================
    def crear_pestana_usuarios(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Usuarios")

        form_frame = ttk.LabelFrame(frame, text="Datos del Usuario")
        form_frame.pack(fill='x', padx=10, pady=5)

        campos = [("Cédula:", "entry_ced_usu"), ("Nombre Completo:", "entry_nom_usu"),
                  ("Correo:", "entry_cor_usu"), ("Usuario:", "entry_usr_usu"),
                  ("Contraseña:", "entry_pas_usu")]
        for texto, var in campos:
            row = ttk.Frame(form_frame)
            row.pack(fill='x', padx=5, pady=3)
            ttk.Label(row, text=texto, width=15).pack(side='left')
            entry = ttk.Entry(row)
            entry.pack(side='left', expand=True, fill='x')
            setattr(self, var, entry)

        btn_frame = ttk.Frame(form_frame)
        btn_frame.pack(fill='x', pady=10)
        ttk.Button(btn_frame, text="Crear/Actualizar", command=self.guardar_usuario).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Consultar", command=self.consultar_usuario).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Eliminar", command=self.eliminar_usuario).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Limpiar", command=self.limpiar_usuarios).pack(side='left', padx=5)

        table_frame = ttk.Frame(frame)
        table_frame.pack(fill='both', expand=True, padx=10, pady=5)
        cols = ('cedula', 'nombre', 'correo', 'usuario', 'password')
        self.tree_usuarios = ttk.Treeview(table_frame, columns=cols, show='headings')
        for c, t, w in zip(cols, ['Cédula', 'Nombre', 'Correo', 'Usuario', 'Password'], [100, 200, 200, 120, 120]):
            self.tree_usuarios.heading(c, text=t)
            self.tree_usuarios.column(c, width=w)
        self.tree_usuarios.pack(fill='both', expand=True)
        self.tree_usuarios.bind('<<TreeviewSelect>>', self.cargar_usuario_sel)
        self.actualizar_lista_usuarios()

    def actualizar_lista_usuarios(self):
        try:
            cursor = self.conexion.cursor(dictionary=True)
            cursor.execute("SELECT * FROM usuarios WHERE usuario != 'admininicial'")
            for i in self.tree_usuarios.get_children():
                self.tree_usuarios.delete(i)
            for u in cursor:
                self.tree_usuarios.insert('', 'end', values=(
                    u['cedula'], u['nombre_completo'], u['correo'], u['usuario'], u['password']))
        except Error as e:
            messagebox.showerror("Error", f"Error al cargar usuarios: {e}")

    def cargar_usuario_sel(self, event):
        sel = self.tree_usuarios.selection()
        if sel:
            v = self.tree_usuarios.item(sel[0])['values']
            self.limpiar_usuarios()
            self.entry_ced_usu.insert(0, v[0])
            self.entry_nom_usu.insert(0, v[1])
            self.entry_cor_usu.insert(0, v[2])
            self.entry_usr_usu.insert(0, v[3])
            self.entry_pas_usu.insert(0, v[4])

    def guardar_usuario(self):
        cedula = self.entry_ced_usu.get().strip()
        nombre = self.entry_nom_usu.get().strip()
        correo = self.entry_cor_usu.get().strip()
        usuario = self.entry_usr_usu.get().strip()
        password = self.entry_pas_usu.get().strip()
        if not all([cedula, nombre, correo, usuario, password]):
            messagebox.showwarning("Advertencia", "Faltan datos del usuario")
            return
        try:
            cursor = self.conexion.cursor()
            cursor.execute("SELECT cedula FROM usuarios WHERE cedula = %s", (cedula,))
            existe = cursor.fetchone()
            if existe:
                cursor.execute("""UPDATE usuarios SET nombre_completo=%s, correo=%s,
                                  usuario=%s, password=%s WHERE cedula=%s""",
                               (nombre, correo, usuario, password, cedula))
                messagebox.showinfo("Éxito", "Datos del Usuario Actualizados")
            else:
                cursor.execute("""INSERT INTO usuarios (cedula, nombre_completo, correo, usuario, password)
                                  VALUES (%s,%s,%s,%s,%s)""",
                               (cedula, nombre, correo, usuario, password))
                messagebox.showinfo("Éxito", "Usuario Creado")
            self.conexion.commit()
            self.actualizar_lista_usuarios()
            self.limpiar_usuarios()
        except Error as e:
            messagebox.showerror("Error", f"Error al guardar: {e}")

    def consultar_usuario(self):
        cedula = simpledialog.askstring("Consultar", "Ingrese la cédula del usuario:")
        if not cedula:
            return
        try:
            cursor = self.conexion.cursor(dictionary=True)
            cursor.execute("SELECT * FROM usuarios WHERE cedula = %s", (cedula,))
            r = cursor.fetchone()
            if r:
                self.limpiar_usuarios()
                self.entry_ced_usu.insert(0, r['cedula'])
                self.entry_nom_usu.insert(0, r['nombre_completo'])
                self.entry_cor_usu.insert(0, r['correo'])
                self.entry_usr_usu.insert(0, r['usuario'])
                self.entry_pas_usu.insert(0, r['password'])
            else:
                messagebox.showerror("Error", "Usuario Inexistente")
        except Error as e:
            messagebox.showerror("Error", str(e))

    def eliminar_usuario(self):
        cedula = self.entry_ced_usu.get().strip()
        if not cedula:
            messagebox.showwarning("Advertencia", "Cédula Errada")
            return
        if messagebox.askyesno("Confirmar", "¿Eliminar este usuario?"):
            try:
                cursor = self.conexion.cursor()
                cursor.execute("DELETE FROM usuarios WHERE cedula = %s", (cedula,))
                self.conexion.commit()
                messagebox.showinfo("Éxito", "Datos del Usuario Borrados")
                self.actualizar_lista_usuarios()
                self.limpiar_usuarios()
            except Error as e:
                messagebox.showerror("Error", str(e))

    def limpiar_usuarios(self):
        for e in [self.entry_ced_usu, self.entry_nom_usu, self.entry_cor_usu,
                  self.entry_usr_usu, self.entry_pas_usu]:
            e.delete(0, tk.END)

    # ============================================================
    # MÓDULO CLIENTES (Sprint 2)
    # ============================================================
    def crear_pestana_clientes(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Clientes")

        form_frame = ttk.LabelFrame(frame, text="Datos del Cliente")
        form_frame.pack(fill='x', padx=10, pady=5)

        campos = [("Cédula:", "entry_ced_cli"), ("Nombre Completo:", "entry_nom_cli"),
                  ("Dirección:", "entry_dir_cli"), ("Teléfono:", "entry_tel_cli"),
                  ("Correo:", "entry_cor_cli")]
        for texto, var in campos:
            row = ttk.Frame(form_frame)
            row.pack(fill='x', padx=5, pady=3)
            ttk.Label(row, text=texto, width=15).pack(side='left')
            entry = ttk.Entry(row)
            entry.pack(side='left', expand=True, fill='x')
            setattr(self, var, entry)

        btn_frame = ttk.Frame(form_frame)
        btn_frame.pack(fill='x', pady=10)
        ttk.Button(btn_frame, text="Crear/Actualizar", command=self.guardar_cliente).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Consultar", command=self.consultar_cliente).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Eliminar", command=self.eliminar_cliente).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Limpiar", command=self.limpiar_clientes).pack(side='left', padx=5)

        table_frame = ttk.Frame(frame)
        table_frame.pack(fill='both', expand=True, padx=10, pady=5)
        cols = ('cedula', 'nombre', 'direccion', 'telefono', 'correo')
        self.tree_clientes = ttk.Treeview(table_frame, columns=cols, show='headings')
        for c, t, w in zip(cols, ['Cédula', 'Nombre', 'Dirección', 'Teléfono', 'Correo'], [100, 200, 200, 120, 200]):
            self.tree_clientes.heading(c, text=t)
            self.tree_clientes.column(c, width=w)
        self.tree_clientes.pack(fill='both', expand=True)
        self.tree_clientes.bind('<<TreeviewSelect>>', self.cargar_cliente_sel)
        self.actualizar_lista_clientes()

    def actualizar_lista_clientes(self):
        try:
            cursor = self.conexion.cursor(dictionary=True)
            cursor.execute("SELECT * FROM clientes")
            for i in self.tree_clientes.get_children():
                self.tree_clientes.delete(i)
            for c in cursor:
                self.tree_clientes.insert('', 'end', values=(
                    c['cedula'], c['nombre_completo'], c['direccion'],
                    c['telefono'], c['correo']))
        except Error as e:
            messagebox.showerror("Error", str(e))

    def cargar_cliente_sel(self, event):
        sel = self.tree_clientes.selection()
        if sel:
            v = self.tree_clientes.item(sel[0])['values']
            self.limpiar_clientes()
            self.entry_ced_cli.insert(0, v[0])
            self.entry_nom_cli.insert(0, v[1])
            self.entry_dir_cli.insert(0, v[2])
            self.entry_tel_cli.insert(0, v[3])
            self.entry_cor_cli.insert(0, v[4])

    def guardar_cliente(self):
        cedula = self.entry_ced_cli.get().strip()
        nombre = self.entry_nom_cli.get().strip()
        direccion = self.entry_dir_cli.get().strip()
        telefono = self.entry_tel_cli.get().strip()
        correo = self.entry_cor_cli.get().strip()
        if not all([cedula, nombre, direccion, telefono, correo]):
            messagebox.showwarning("Advertencia", "Faltan datos del cliente")
            return
        try:
            cursor = self.conexion.cursor()
            cursor.execute("SELECT cedula FROM clientes WHERE cedula = %s", (cedula,))
            if cursor.fetchone():
                cursor.execute("""UPDATE clientes SET nombre_completo=%s, direccion=%s,
                                  telefono=%s, correo=%s WHERE cedula=%s""",
                               (nombre, direccion, telefono, correo, cedula))
                messagebox.showinfo("Éxito", "Datos del Cliente Actualizados")
            else:
                cursor.execute("""INSERT INTO clientes (cedula, nombre_completo, direccion, telefono, correo)
                                  VALUES (%s,%s,%s,%s,%s)""",
                               (cedula, nombre, direccion, telefono, correo))
                messagebox.showinfo("Éxito", "Cliente Creado")
            self.conexion.commit()
            self.actualizar_lista_clientes()
            self.limpiar_clientes()
        except Error as e:
            messagebox.showerror("Error", str(e))

    def consultar_cliente(self):
        cedula = simpledialog.askstring("Consultar", "Ingrese la cédula del cliente:")
        if not cedula:
            return
        try:
            cursor = self.conexion.cursor(dictionary=True)
            cursor.execute("SELECT * FROM clientes WHERE cedula = %s", (cedula,))
            r = cursor.fetchone()
            if r:
                self.limpiar_clientes()
                self.entry_ced_cli.insert(0, r['cedula'])
                self.entry_nom_cli.insert(0, r['nombre_completo'])
                self.entry_dir_cli.insert(0, r['direccion'])
                self.entry_tel_cli.insert(0, r['telefono'])
                self.entry_cor_cli.insert(0, r['correo'])
            else:
                messagebox.showerror("Error", "Cliente Inexistente")
        except Error as e:
            messagebox.showerror("Error", str(e))

    def eliminar_cliente(self):
        cedula = self.entry_ced_cli.get().strip()
        if not cedula:
            messagebox.showwarning("Advertencia", "Cédula Errada")
            return
        if messagebox.askyesno("Confirmar", "¿Eliminar este cliente?"):
            try:
                cursor = self.conexion.cursor()
                cursor.execute("DELETE FROM clientes WHERE cedula = %s", (cedula,))
                self.conexion.commit()
                messagebox.showinfo("Éxito", "Datos del Cliente Borrados")
                self.actualizar_lista_clientes()
                self.limpiar_clientes()
            except Error as e:
                messagebox.showerror("Error", str(e))

    def limpiar_clientes(self):
        for e in [self.entry_ced_cli, self.entry_nom_cli, self.entry_dir_cli,
                  self.entry_tel_cli, self.entry_cor_cli]:
            e.delete(0, tk.END)

    # ============================================================
    # MÓDULO PROVEEDORES (Sprint 2)
    # ============================================================
    def crear_pestana_proveedores(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Proveedores")

        form_frame = ttk.LabelFrame(frame, text="Datos del Proveedor")
        form_frame.pack(fill='x', padx=10, pady=5)

        campos = [("NIT:", "entry_nit_pro"), ("Nombre Proveedor:", "entry_nom_pro"),
                  ("Dirección:", "entry_dir_pro"), ("Teléfono:", "entry_tel_pro"),
                  ("Ciudad:", "entry_ciu_pro")]
        for texto, var in campos:
            row = ttk.Frame(form_frame)
            row.pack(fill='x', padx=5, pady=3)
            ttk.Label(row, text=texto, width=15).pack(side='left')
            entry = ttk.Entry(row)
            entry.pack(side='left', expand=True, fill='x')
            setattr(self, var, entry)

        btn_frame = ttk.Frame(form_frame)
        btn_frame.pack(fill='x', pady=10)
        ttk.Button(btn_frame, text="Crear/Actualizar", command=self.guardar_proveedor).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Consultar", command=self.consultar_proveedor).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Eliminar", command=self.eliminar_proveedor).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Limpiar", command=self.limpiar_proveedores).pack(side='left', padx=5)

        table_frame = ttk.Frame(frame)
        table_frame.pack(fill='both', expand=True, padx=10, pady=5)
        cols = ('nit', 'nombre', 'direccion', 'telefono', 'ciudad')
        self.tree_proveedores = ttk.Treeview(table_frame, columns=cols, show='headings')
        for c, t, w in zip(cols, ['NIT', 'Nombre', 'Dirección', 'Teléfono', 'Ciudad'], [100, 200, 200, 120, 120]):
            self.tree_proveedores.heading(c, text=t)
            self.tree_proveedores.column(c, width=w)
        self.tree_proveedores.pack(fill='both', expand=True)
        self.tree_proveedores.bind('<<TreeviewSelect>>', self.cargar_proveedor_sel)
        self.actualizar_lista_proveedores()

    def actualizar_lista_proveedores(self):
        try:
            cursor = self.conexion.cursor(dictionary=True)
            cursor.execute("SELECT * FROM proveedores")
            for i in self.tree_proveedores.get_children():
                self.tree_proveedores.delete(i)
            for p in cursor:
                self.tree_proveedores.insert('', 'end', values=(
                    p['nit'], p['nombre_proveedor'], p['direccion'],
                    p['telefono'], p['ciudad']))
        except Error as e:
            messagebox.showerror("Error", str(e))

    def cargar_proveedor_sel(self, event):
        sel = self.tree_proveedores.selection()
        if sel:
            v = self.tree_proveedores.item(sel[0])['values']
            self.limpiar_proveedores()
            self.entry_nit_pro.insert(0, v[0])
            self.entry_nom_pro.insert(0, v[1])
            self.entry_dir_pro.insert(0, v[2])
            self.entry_tel_pro.insert(0, v[3])
            self.entry_ciu_pro.insert(0, v[4])

    def guardar_proveedor(self):
        nit = self.entry_nit_pro.get().strip()
        nombre = self.entry_nom_pro.get().strip()
        direccion = self.entry_dir_pro.get().strip()
        telefono = self.entry_tel_pro.get().strip()
        ciudad = self.entry_ciu_pro.get().strip()
        if not all([nit, nombre, direccion, telefono, ciudad]):
            messagebox.showwarning("Advertencia", "Faltan datos del proveedor")
            return
        try:
            nit_int = int(nit)
            cursor = self.conexion.cursor()
            cursor.execute("SELECT nit FROM proveedores WHERE nit = %s", (nit_int,))
            if cursor.fetchone():
                cursor.execute("""UPDATE proveedores SET nombre_proveedor=%s, direccion=%s,
                                  telefono=%s, ciudad=%s WHERE nit=%s""",
                               (nombre, direccion, telefono, ciudad, nit_int))
                messagebox.showinfo("Éxito", "Datos del Proveedor Actualizados")
            else:
                cursor.execute("""INSERT INTO proveedores (nit, nombre_proveedor, direccion, telefono, ciudad)
                                  VALUES (%s,%s,%s,%s,%s)""",
                               (nit_int, nombre, direccion, telefono, ciudad))
                messagebox.showinfo("Éxito", "Proveedor Creado")
            self.conexion.commit()
            self.actualizar_lista_proveedores()
            self.limpiar_proveedores()
        except ValueError:
            messagebox.showerror("Error", "El NIT debe ser un número")
        except Error as e:
            messagebox.showerror("Error", str(e))

    def consultar_proveedor(self):
        nit = simpledialog.askstring("Consultar", "Ingrese el NIT del proveedor:")
        if not nit:
            return
        try:
            cursor = self.conexion.cursor(dictionary=True)
            cursor.execute("SELECT * FROM proveedores WHERE nit = %s", (int(nit),))
            r = cursor.fetchone()
            if r:
                self.limpiar_proveedores()
                self.entry_nit_pro.insert(0, r['nit'])
                self.entry_nom_pro.insert(0, r['nombre_proveedor'])
                self.entry_dir_pro.insert(0, r['direccion'])
                self.entry_tel_pro.insert(0, r['telefono'])
                self.entry_ciu_pro.insert(0, r['ciudad'])
            else:
                messagebox.showerror("Error", "Proveedor Inexistente")
        except Error as e:
            messagebox.showerror("Error", str(e))

    def eliminar_proveedor(self):
        nit = self.entry_nit_pro.get().strip()
        if not nit:
            messagebox.showwarning("Advertencia", "NIT Errado")
            return
        if messagebox.askyesno("Confirmar", "¿Eliminar este proveedor?"):
            try:
                cursor = self.conexion.cursor()
                cursor.execute("DELETE FROM proveedores WHERE nit = %s", (int(nit),))
                self.conexion.commit()
                messagebox.showinfo("Éxito", "Datos del Proveedor Borrados")
                self.actualizar_lista_proveedores()
                self.limpiar_proveedores()
            except Error as e:
                messagebox.showerror("Error", str(e))

    def limpiar_proveedores(self):
        for e in [self.entry_nit_pro, self.entry_nom_pro, self.entry_dir_pro,
                  self.entry_tel_pro, self.entry_ciu_pro]:
            e.delete(0, tk.END)

    # ============================================================
    # MÓDULO PRODUCTOS - CARGA CSV (Sprint 3)
    # ============================================================
    def crear_pestana_productos(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Productos")

        info_frame = ttk.LabelFrame(frame, text="Carga de Productos desde CSV")
        info_frame.pack(fill='x', padx=10, pady=10)

        tk.Label(info_frame,
                 text="Formato CSV: codigo_producto,nombre_producto,nitproveedor,precio_compra,ivacompra,precio_venta",
                 font=("Arial", 9)).pack(padx=10, pady=5, anchor='w')

        btn_frame = ttk.Frame(info_frame)
        btn_frame.pack(fill='x', padx=10, pady=10)
        ttk.Button(btn_frame, text="Examinar y Cargar CSV", command=self.cargar_csv_productos).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Refrescar Lista", command=self.actualizar_lista_productos).pack(side='left', padx=5)

        table_frame = ttk.Frame(frame)
        table_frame.pack(fill='both', expand=True, padx=10, pady=5)
        cols = ('codigo', 'nombre', 'nit', 'p_compra', 'iva', 'p_venta')
        self.tree_productos = ttk.Treeview(table_frame, columns=cols, show='headings')
        for c, t, w in zip(cols, ['Código', 'Nombre', 'NIT Proveedor', 'P. Compra', 'IVA', 'P. Venta'],
                           [100, 200, 120, 120, 100, 120]):
            self.tree_productos.heading(c, text=t)
            self.tree_productos.column(c, width=w)
        self.tree_productos.pack(fill='both', expand=True)
        self.actualizar_lista_productos()

    def cargar_csv_productos(self):
        archivo = filedialog.askopenfilename(
            title="Seleccionar archivo CSV de productos",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if not archivo:
            messagebox.showerror("Error", "Error: no se seleccionó archivo para cargar")
            return

        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                filas = list(reader)

            if not filas:
                messagebox.showerror("Error", "Error: formato de archivo inválido")
                return

            # Validar y procesar cada fila
            productos_validos = []
            cursor = self.conexion.cursor()

            for i, fila in enumerate(filas, 1):
                if len(fila) != 6:
                    messagebox.showerror("Error", f"Error: datos leídos inválidos en fila {i}")
                    return
                try:
                    codigo = int(fila[0])
                    nombre = fila[1].strip()
                    nit = int(fila[2])
                    p_compra = float(fila[3])
                    iva = float(fila[4])
                    p_venta = float(fila[5])

                    # Validar que el NIT exista
                    cursor.execute("SELECT nit FROM proveedores WHERE nit = %s", (nit,))
                    if not cursor.fetchone():
                        messagebox.showerror("Error",
                                             f"Error: datos leídos inválidos\nFila {i}: NIT {nit} no existe en proveedores")
                        return

                    productos_validos.append((codigo, nombre, nit, p_compra, iva, p_venta))
                except ValueError:
                    messagebox.showerror("Error", f"Error: datos leídos inválidos en fila {i}")
                    return

            # Borrar productos anteriores e insertar los nuevos
            cursor.execute("DELETE FROM productos")
            for p in productos_validos:
                cursor.execute("""INSERT INTO productos
                                  (codigo_producto, nombre_producto, nitproveedor,
                                   precio_compra, ivacompra, precio_venta)
                                  VALUES (%s,%s,%s,%s,%s,%s)""", p)
            self.conexion.commit()
            messagebox.showinfo("Éxito", "Archivo Cargado Exitosamente")
            self.actualizar_lista_productos()

        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar archivo: {e}")

    def actualizar_lista_productos(self):
        try:
            cursor = self.conexion.cursor(dictionary=True)
            cursor.execute("SELECT * FROM productos")
            for i in self.tree_productos.get_children():
                self.tree_productos.delete(i)
            for p in cursor:
                self.tree_productos.insert('', 'end', values=(
                    p['codigo_producto'], p['nombre_producto'], p['nitproveedor'],
                    p['precio_compra'], p['ivacompra'], p['precio_venta']))
        except Error as e:
            messagebox.showerror("Error", str(e))

    # ============================================================
    # MÓDULO VENTAS (Sprint 4)
    # ============================================================
    def crear_pestana_ventas(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Ventas")

        # Datos del cliente
        cli_frame = ttk.LabelFrame(frame, text="Datos del Cliente")
        cli_frame.pack(fill='x', padx=10, pady=5)

        row_cli = ttk.Frame(cli_frame)
        row_cli.pack(fill='x', padx=5, pady=5)
        ttk.Label(row_cli, text="Cédula Cliente:", width=15).pack(side='left')
        self.entry_ced_cli_ven = ttk.Entry(row_cli, width=20)
        self.entry_ced_cli_ven.pack(side='left', padx=5)
        ttk.Button(row_cli, text="Consultar", command=self.consultar_cliente_venta).pack(side='left', padx=5)

        ttk.Label(row_cli, text="Nombre:", width=10).pack(side='left', padx=(20, 0))
        self.lbl_nom_cli_ven = ttk.Label(row_cli, text="", width=40, relief='sunken')
        self.lbl_nom_cli_ven.pack(side='left', padx=5)

        # Carrito de productos (hasta 3)
        prod_frame = ttk.LabelFrame(frame, text="Productos (máximo 3)")
        prod_frame.pack(fill='x', padx=10, pady=5)

        row_prod = ttk.Frame(prod_frame)
        row_prod.pack(fill='x', padx=5, pady=5)
        ttk.Label(row_prod, text="Código Producto:", width=15).pack(side='left')
        self.entry_cod_prod_ven = ttk.Entry(row_prod, width=15)
        self.entry_cod_prod_ven.pack(side='left', padx=5)
        ttk.Button(row_prod, text="Consultar", command=self.consultar_producto_venta).pack(side='left', padx=5)

        ttk.Label(row_prod, text="Nombre:", width=10).pack(side='left', padx=(10, 0))
        self.lbl_nom_prod_ven = ttk.Label(row_prod, text="", width=25, relief='sunken')
        self.lbl_nom_prod_ven.pack(side='left', padx=5)

        ttk.Label(row_prod, text="Cant.:", width=5).pack(side='left', padx=(10, 0))
        self.entry_cant_ven = ttk.Entry(row_prod, width=8)
        self.entry_cant_ven.pack(side='left', padx=5)
        ttk.Button(row_prod, text="Agregar", command=self.agregar_producto_venta).pack(side='left', padx=5)

        # Tabla detalle de venta
        det_frame = ttk.Frame(frame)
        det_frame.pack(fill='x', padx=10, pady=5)
        cols = ('codigo', 'nombre', 'cantidad', 'v_unitario', 'v_total')
        self.tree_detalle = ttk.Treeview(det_frame, columns=cols, show='headings', height=5)
        for c, t, w in zip(cols, ['Código', 'Nombre', 'Cantidad', 'V. Unitario', 'V. Total'],
                           [100, 200, 80, 120, 120]):
            self.tree_detalle.heading(c, text=t)
            self.tree_detalle.column(c, width=w)
        self.tree_detalle.pack(fill='x')

        # Totales
        tot_frame = ttk.LabelFrame(frame, text="Totales")
        tot_frame.pack(fill='x', padx=10, pady=5)

        row_tot = ttk.Frame(tot_frame)
        row_tot.pack(fill='x', padx=10, pady=10)

        ttk.Label(row_tot, text="Total Venta:", font=("Arial", 11, "bold")).pack(side='left')
        self.lbl_total_venta = ttk.Label(row_tot, text="$ 0.00", width=15,
                                         font=("Arial", 11, "bold"), relief='sunken')
        self.lbl_total_venta.pack(side='left', padx=(5, 20))

        ttk.Label(row_tot, text="Total IVA:", font=("Arial", 11, "bold")).pack(side='left')
        self.lbl_total_iva = ttk.Label(row_tot, text="$ 0.00", width=15,
                                       font=("Arial", 11, "bold"), relief='sunken')
        self.lbl_total_iva.pack(side='left', padx=(5, 20))

        ttk.Label(row_tot, text="Total con IVA:", font=("Arial", 11, "bold")).pack(side='left')
        self.lbl_total_con_iva = ttk.Label(row_tot, text="$ 0.00", width=15,
                                           font=("Arial", 11, "bold"), relief='sunken', foreground='green')
        self.lbl_total_con_iva.pack(side='left', padx=5)

        # Botones finales
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill='x', padx=10, pady=10)
        ttk.Button(btn_frame, text="Totalizar y Confirmar Venta",
                   command=self.confirmar_venta).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Limpiar Venta",
                   command=self.limpiar_venta).pack(side='left', padx=5)

        self.detalle_venta_actual = []  # Lista temporal de productos en la venta

    def consultar_cliente_venta(self):
        cedula = self.entry_ced_cli_ven.get().strip()
        if not cedula:
            messagebox.showwarning("Advertencia", "Ingrese una cédula")
            return
        try:
            cursor = self.conexion.cursor(dictionary=True)
            cursor.execute("SELECT * FROM clientes WHERE cedula = %s", (cedula,))
            r = cursor.fetchone()
            if r:
                self.lbl_nom_cli_ven.config(text=r['nombre_completo'])
                self.cliente_venta_actual = r
            else:
                messagebox.showerror("Error", "Cédula no se encuentra registrada en la base de datos")
                self.lbl_nom_cli_ven.config(text="")
        except Error as e:
            messagebox.showerror("Error", str(e))

    def consultar_producto_venta(self):
        codigo = self.entry_cod_prod_ven.get().strip()
        if not codigo:
            messagebox.showwarning("Advertencia", "Ingrese un código")
            return
        try:
            cursor = self.conexion.cursor(dictionary=True)
            cursor.execute("SELECT * FROM productos WHERE codigo_producto = %s", (int(codigo),))
            r = cursor.fetchone()
            if r:
                self.lbl_nom_prod_ven.config(text=r['nombre_producto'])
                self.producto_venta_actual = r
            else:
                messagebox.showerror("Error", "Código de producto no se encuentra en la base de datos")
                self.lbl_nom_prod_ven.config(text="")
        except Error as e:
            messagebox.showerror("Error", str(e))

    def agregar_producto_venta(self):
        if not hasattr(self, 'producto_venta_actual') or not self.producto_venta_actual:
            messagebox.showwarning("Advertencia", "Consulte primero un producto")
            return
        cantidad = self.entry_cant_ven.get().strip()
        if not cantidad:
            messagebox.showwarning("Advertencia", "Ingrese una cantidad")
            return
        try:
            cant = int(cantidad)
            if cant <= 0:
                messagebox.showerror("Error", "El valor de cantidad es incorrecto")
                return
        except ValueError:
            messagebox.showerror("Error", "Cantidad debe ser un número entero")
            return

        if len(self.detalle_venta_actual) >= 3:
            messagebox.showwarning("Advertencia", "Solo se permiten 3 productos por venta")
            return

        prod = self.producto_venta_actual
        valor_unitario = prod['precio_venta']
        valor_total = cant * valor_unitario

        self.detalle_venta_actual.append({
            'codigo': prod['codigo_producto'],
            'nombre': prod['nombre_producto'],
            'cantidad': cant,
            'valor_unitario': valor_unitario,
            'valor_total': valor_total,
            'iva': prod['ivacompra']
        })

        self.tree_detalle.insert('', 'end', values=(
            prod['codigo_producto'], prod['nombre_producto'],
            cant, valor_unitario, valor_total))

        # Limpiar campos de producto
        self.entry_cod_prod_ven.delete(0, tk.END)
        self.entry_cant_ven.delete(0, tk.END)
        self.lbl_nom_prod_ven.config(text="")
        self.producto_venta_actual = None

        self.calcular_totales()

    def calcular_totales(self):
        total_venta = sum(p['valor_total'] for p in self.detalle_venta_actual)
        total_iva = sum(p['valor_total'] * (p['iva'] / 100.0) for p in self.detalle_venta_actual)
        total_con_iva = total_venta + total_iva

        self.lbl_total_venta.config(text=f"$ {total_venta:,.2f}")
        self.lbl_total_iva.config(text=f"$ {total_iva:,.2f}")
        self.lbl_total_con_iva.config(text=f"$ {total_con_iva:,.2f}")

    def confirmar_venta(self):
        if not hasattr(self, 'cliente_venta_actual') or not self.cliente_venta_actual:
            messagebox.showwarning("Advertencia", "Consulte primero un cliente")
            return
        if not self.detalle_venta_actual:
            messagebox.showwarning("Advertencia", "Agregue al menos un producto")
            return

        try:
            cursor = self.conexion.cursor()
            total_venta = sum(p['valor_total'] for p in self.detalle_venta_actual)
            total_iva = sum(p['valor_total'] * (p['iva'] / 100.0) for p in self.detalle_venta_actual)
            total_con_iva = total_venta + total_iva

            # Insertar venta (consecutivo automático)
            cursor.execute("""INSERT INTO ventas (cedula_cliente, cedula_usuario,
                             valor_total, valor_iva, valor_total_con_iva)
                             VALUES (%s, %s, %s, %s, %s)""",
                           (self.cliente_venta_actual['cedula'],
                            self.usuario_actual['cedula'],
                            total_venta, total_iva, total_con_iva))
            codigo_venta = cursor.lastrowid

            # Insertar detalle de venta
            for p in self.detalle_venta_actual:
                cursor.execute("""INSERT INTO detalleVentas
                                  (codigo_venta, codigo_producto, cantidad, valor_unitario, valor_total)
                                  VALUES (%s, %s, %s, %s, %s)""",
                               (codigo_venta, p['codigo'], p['cantidad'],
                                p['valor_unitario'], p['valor_total']))

            self.conexion.commit()
            messagebox.showinfo("Éxito",
                                f"Venta registrada correctamente\n"
                                f"Código de venta: {codigo_venta}\n"
                                f"Total con IVA: $ {total_con_iva:,.2f}")
            self.limpiar_venta()
        except Error as e:
            self.conexion.rollback()
            messagebox.showerror("Error", f"No se pudo registrar la venta: {e}")

    def limpiar_venta(self):
        self.entry_ced_cli_ven.delete(0, tk.END)
        self.entry_cod_prod_ven.delete(0, tk.END)
        self.entry_cant_ven.delete(0, tk.END)
        self.lbl_nom_cli_ven.config(text="")
        self.lbl_nom_prod_ven.config(text="")
        self.lbl_total_venta.config(text="$ 0.00")
        self.lbl_total_iva.config(text="$ 0.00")
        self.lbl_total_con_iva.config(text="$ 0.00")
        for i in self.tree_detalle.get_children():
            self.tree_detalle.delete(i)
        self.detalle_venta_actual = []
        self.cliente_venta_actual = None
        self.producto_venta_actual = None

    # ============================================================
    # MÓDULO CONSULTAS Y REPORTES (Sprint 5)
    # ============================================================
    def crear_pestana_reportes(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Consultas y Reportes")

        btn_frame = ttk.LabelFrame(frame, text="Seleccione un reporte")
        btn_frame.pack(fill='x', padx=10, pady=10)

        ttk.Button(btn_frame, text="Listado de Usuarios",
                   command=self.reporte_usuarios, width=30).pack(side='left', padx=10, pady=10)
        ttk.Button(btn_frame, text="Listado de Clientes",
                   command=self.reporte_clientes, width=30).pack(side='left', padx=10, pady=10)
        ttk.Button(btn_frame, text="Total Ventas por Cliente",
                   command=self.reporte_ventas_cliente, width=30).pack(side='left', padx=10, pady=10)

        # Área de resultado
        self.text_reporte = tk.Text(frame, height=25, font=("Courier", 10))
        self.text_reporte.pack(fill='both', expand=True, padx=10, pady=10)

    def reporte_usuarios(self):
        self.text_reporte.delete(1.0, tk.END)
        try:
            cursor = self.conexion.cursor(dictionary=True)
            cursor.execute("SELECT * FROM usuarios WHERE usuario != 'admininicial'")
            usuarios = cursor.fetchall()
            if not usuarios:
                self.text_reporte.insert(tk.END, "No existen usuarios registrados.\n")
                return
            self.text_reporte.insert(tk.END, "=" * 90 + "\n")
            self.text_reporte.insert(tk.END, "LISTADO DE USUARIOS\n")
            self.text_reporte.insert(tk.END, "=" * 90 + "\n")
            self.text_reporte.insert(tk.END, f"{'Cédula':<15}{'Nombre':<30}{'Email':<30}{'Usuario':<15}\n")
            self.text_reporte.insert(tk.END, "-" * 90 + "\n")
            for u in usuarios:
                self.text_reporte.insert(tk.END,
                    f"{u['cedula']:<15}{u['nombre_completo']:<30}{u['correo']:<30}{u['usuario']:<15}\n")
        except Error as e:
            self.text_reporte.insert(tk.END, f"Error: {e}\n")

    def reporte_clientes(self):
        self.text_reporte.delete(1.0, tk.END)
        try:
            cursor = self.conexion.cursor(dictionary=True)
            cursor.execute("SELECT * FROM clientes")
            clientes = cursor.fetchall()
            if not clientes:
                self.text_reporte.insert(tk.END, "No existen clientes registrados.\n")
                return
            self.text_reporte.insert(tk.END, "=" * 100 + "\n")
            self.text_reporte.insert(tk.END, "LISTADO DE CLIENTES\n")
            self.text_reporte.insert(tk.END, "=" * 100 + "\n")
            self.text_reporte.insert(tk.END,
                f"{'Cédula':<15}{'Nombre':<25}{'Email':<30}{'Dirección':<25}{'Teléfono':<15}\n")
            self.text_reporte.insert(tk.END, "-" * 100 + "\n")
            for c in clientes:
                self.text_reporte.insert(tk.END,
                    f"{c['cedula']:<15}{c['nombre_completo']:<25}{c['correo']:<30}{c['direccion']:<25}{c['telefono']:<15}\n")
        except Error as e:
            self.text_reporte.insert(tk.END, f"Error: {e}\n")

    def reporte_ventas_cliente(self):
        self.text_reporte.delete(1.0, tk.END)
        try:
            cursor = self.conexion.cursor(dictionary=True)
            cursor.execute("""
                SELECT c.cedula, c.nombre_completo,
                       COALESCE(SUM(v.valor_total_con_iva), 0) as total_ventas
                FROM clientes c
                LEFT JOIN ventas v ON c.cedula = v.cedula_cliente
                GROUP BY c.cedula, c.nombre_completo
                ORDER BY c.nombre_completo
            """)
            resultados = cursor.fetchall()
            if not resultados:
                self.text_reporte.insert(tk.END, "No existen clientes registrados.\n")
                return
            self.text_reporte.insert(tk.END, "=" * 70 + "\n")
            self.text_reporte.insert(tk.END, "TOTAL DE VENTAS POR CLIENTE\n")
            self.text_reporte.insert(tk.END, "=" * 70 + "\n")
            self.text_reporte.insert(tk.END,
                f"{'Cédula':<15}{'Nombre del Cliente':<35}{'Total Ventas':>20}\n")
            self.text_reporte.insert(tk.END, "-" * 70 + "\n")
            total_consolidado = 0
            for r in resultados:
                self.text_reporte.insert(tk.END,
                    f"{r['cedula']:<15}{r['nombre_completo']:<35}$ {r['total_ventas']:>15,.2f}\n")
                total_consolidado += r['total_ventas']
            self.text_reporte.insert(tk.END, "=" * 70 + "\n")
            self.text_reporte.insert(tk.END,
                f"{'TOTAL CONSOLIDADO':<51}$ {total_consolidado:>15,.2f}\n")
        except Error as e:
            self.text_reporte.insert(tk.END, f"Error: {e}\n")


# ============================================================
# MAIN
# ============================================================
if __name__ == "__main__":
    # 1. Conexión a la base de datos
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="mariajose",
            database="tienda_generica"
        )
    except Error as e:
        messagebox.showerror("Error", f"No se pudo conectar a MySQL: {e}")
        exit()

    # 2. Ventana de Login
    root_login = tk.Tk()
    app_login = Login(root_login, conexion)
    root_login.mainloop()

    # 3. Si se autenticó, abrir sistema principal
    if app_login.autenticado:
        root_main = tk.Tk()
        app = TiendaGenerica(root_main, conexion, app_login.usuario_actual)
        root_main.mainloop()

    # 4. Cerrar conexión
    if conexion.is_connected():
        conexion.close()