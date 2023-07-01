'''
PARTE I
La gerente de una mueblería nos pide desarrollar una app para su negocio, para ello debemos informatizar los tres segmentos de este: la administración, el departamento de ventas y la gerencia.
Vista administración:
Esta parte de la debemos desarrollar un programa que pueda:
a. cargar los productos de ofertas ofrecidos (id, designación, precio unitario, stock)
b. editar las cargas
c. mostrar todas las cargas realizadas (ordenadas por nombre, ordenadas por precio)
d. buscar una carga específica (por nombre o por código) o por rango de precios
e. eliminar una carga.

Agregado: (esto de momento no)
Tenemos que poder dar de alta, baja, modificar o mostrar a los  empleados:
número_legajo, nombre, apellido, comisiones.

PARTE II
Vista Vendedor:
Desarrollaremos el módulo venta:
Ofreceremos todos los muebles cargados en la vista administración y los clientes podrán comprar los muebles que quieran, cuantas veces quieran.
Nos piden generar un ticket para cada cliente indicando:
El nombre del producto seleccionado, las cantidades compradas, el subtotal por producto, el nombre del vendedor y el total por producto.

Parte 3 Vista Gerencia.
Mostrar las cantidades vendidas por producto (ordenadas de mayor a menor)
Mostrar el stock de productos resultantes del día:
Mostrar la recaudación total obtenida.
Mostrar un ranking de clientes que más compraron.
Mostrar un ranking de comisiones pagadas.
'''

import mysql.connector;

base_datos = mysql.connector.connect(
  host="localhost",
  user="root",
  password="barTT3nd3rNO.04"
)
# mi_cursor es la representación de la base de datos en python
mi_cursor = base_datos.cursor()
mi_cursor.execute("SHOW DATABASES")
bds = mi_cursor.fetchall()

if ('muebleria0000',) not in bds:
    mi_cursor.execute("CREATE DATABASE muebleria0000")
    mi_cursor.execute("use muebleria0000")
    print('BD "muebleria0000" creada y designada.')

    mi_cursor.execute("CREATE TABLE muebles (id int primary key auto_increment, designacion VARCHAR(50), precio_unitario int, stock int)")

    insertar_datos = "INSERT INTO muebles (designacion, precio_unitario, stock) VALUES (%s, %s, %s)" #agregar descripcion
    valores = [
    ('banqueta_individual', 110, 0),
    ('esquinero', 130, 0),
    ('banqueta_doble', 170, 0),
    ('mesa_ratona_grande_1.00x1.00', 200, 0),
    ('mesa_ratona_chica0.70x0.70', 170, 0),
    ('silla_cocina-comedor', 110, 0),
    ('silla_con_apoyabrazos', 150, 0),
    ('mesa_de_cocina-comedor', 330, 0),
    ('mesa_de_cocina-comedor_con_detalles', 400, 0),
    ('camastro_de_descanso_de_1.30m', 570, 0),
    ('camastro_de_descanso_con_almohadones', 650, 0),
    ('gazebo_simple', 1000, 0),
    ('gazebo_doble', 1700, 0)
    ]
    mi_cursor.executemany(insertar_datos, valores)
    print(mi_cursor.rowcount, "registros insertados en la tabla 'muebles'.")

    mi_cursor.execute("CREATE TABLE clientes (id INT PRIMARY KEY AUTO_INCREMENT, nombre VARCHAR(50), apellido VARCHAR(50))")

    mi_cursor.execute("CREATE TABLE ventas (id INT PRIMARY KEY AUTO_INCREMENT, id_cliente INT, total FLOAT, fecha DATE, FOREIGN KEY (id_cliente) REFERENCES clientes(id))")

    mi_cursor.execute("CREATE TABLE detalles_ventas (id INT PRIMARY KEY AUTO_INCREMENT, id_venta INT, id_mueble INT, FOREIGN KEY (id_mueble) REFERENCES muebles(id), FOREIGN KEY (id_venta) REFERENCES ventas(id))")

    base_datos.commit()
else:
    mi_cursor.execute("use muebleria0000")
    print("BD 'muebleria0000' designada.")

#alter table change campoviejo camponuevo varchar(50) --> para modificar creo
#clases: interfaz para hacer mas manejable el programa, no pasa naranja si no tenes un __init__

from abc import ABC, abstractmethod

class Persona(ABC):
    def __init__(self):
        self.nombre= ""
        self.apellido= ""
    
    @abstractmethod
    def set_nombre(self):
        pass

    def get_nombre(self):
        return self.nombre

    def set_apellido(self,apellido):
        self.apellido= apellido

    def get_apellido(self):
        return self.apellido

class Cliente(Persona):
    def __init__(self,nombre,apellido):
        super().__init__(nombre,apellido)
        self.id= 0

    def set_nombre(self,nombre):
        self.nombre= nombre

    def set_id(self,id):
        self.id= id

    def get_id(self):
        return self.id

class Empleado(Persona):
    def __init__(self,nombre,apellido):
        super().__init__(nombre,apellido)
        self.legajo= 0
        self.comision= 0
    
    def set_nombre(self,nombre):
        self.nombre= nombre

    def set_legajo(self,legajo):
        self.legajo= legajo

    def get_legajo(self):
        return self.legajo

    def set_comision(self,comision):
        self.comision= comision

    def get_comision(self):
        return self.comision
        
class Muebleria:
    def mostrar_menu_administracion(self):
        menu=int(input('''
------------------------------
     VISTA ADMINISTRACIÓN
1. Cargar nuevo mueble
2. Editar mueble
3. Mostrar muebles registrados
4. Buscar un mueble
5. Eliminar un mueble
------------------------------
Ingrese opción elegida: '''))
        return menu
    
    def registrar_nuevo_mueble(self):
        insertar_datos = "INSERT INTO muebles (designacion, precio_unitario, stock) VALUES (%s, %s, %s)"
        designacion= input("Designación: ")
        precio_uni= int(input("Precio unitario: $"))
        stock= int(input("Stock: "))
        registro = (designacion, precio_uni, stock)
        mi_cursor.execute(insertar_datos, registro)
        base_datos.commit()
        print("Registro insertado.")
    
    def editar_mueble(self):
        id= int(input("Ingresar el ID del mueble a editar: "))
        dato_a_editar= int(input("Datos a editar:\n1. Designación\n2. Precio unitario\n3. Stock\nIngrese el número de opción: "))
        if dato_a_editar == 1:
            designacion= input("Ingrese la nueva designacion de mueble: ")
            editar_mueble= "UPDATE muebles SET designacion = %s WHERE id = %s"
            valores= (designacion,id)
            mi_cursor.execute(editar_mueble, valores)
            base_datos.commit()
            print("Designación editada.")
        if dato_a_editar == 2:
            precio= int(input("Ingrese el nuevo precio del producto: "))
            editar_mueble= "UPDATE muebles SET precio = %s WHERE id = %s"
            valores= (precio, id)
            mi_cursor.execute(editar_mueble, valores)
            base_datos.commit()
            print("Precio unitario editado.")
        if dato_a_editar == 3:
            stock= int(input("Ingrese el stock actual de producto: "))
            mi_cursor.execute("UPDATE muebles SET stock = %s WHERE id = %s", (stock, id)) #cambia esto despues
            base_datos.commit()
            print("Stock actualizado.")
    
    def mostrar_muebles(self):
        opc= int(input("Mostrar muebles por\n1. Nombre\n2. Precio\nIngresar número de opción elegida:"))
        if opc == 1:
            self.mostrar_muebles_x_nombre()
        if opc == 2:
            self.mostrar_muebles_x_precio()

    def mostrar_muebles_x_nombre(self):
        consulta= "SELECT * FROM muebles ORDER BY designacion"
        mi_cursor.execute(consulta)
        muebles_x_nombre= mi_cursor.fetchall()
        print("------------------------------")
        for mueble in muebles_x_nombre:
            print("ID:", mueble[0])
            print("Designación: ", mueble[1])
            print("Precio: $"+ str(mueble[2]))
            print("Stock: ",mueble[3])
            print("------------------------------")

    def mostrar_muebles_x_precio(self):
        consulta= "SELECT * FROM muebles ORDER BY precio_unitario"
        mi_cursor.execute(consulta)
        muebles_x_precio= mi_cursor.fetchall()
        print("------------------------------")
        for mueble in muebles_x_precio:
            print("ID:", mueble[0])
            print("Designación: ", mueble[1])
            print("Precio: $"+ str(mueble[2]))
            print("Stock: ",mueble[3])
            print("------------------------------")

    def buscar_mueble(self):
        q= int(input("Buscar mueble por...\n1. Nombre\n2. ID\n3. Rango de precios\nIngrese la opción deseada:"))
        if q == 1:
            self.buscar_mueble_x_nombre()
        if q == 2:
            self.buscar_mueble_x_ID()
        if q == 3:
            self.buscar_mueble_x_rango()

    def buscar_mueble_x_nombre(self):
        nombre_buscado= input("Ingresar el nombre buscado: ")
        consulta= "SELECT * FROM muebles WHERE designacion LIKE CONCAT('%',%s,'%') LIMIT 10" #limit 10 me trae los primeros 10 registros que encuentra - aca formateo el string de la query (????????????????????)
        mi_cursor.execute(consulta, (nombre_buscado,))
        muebles_encontrados= mi_cursor.fetchall()
        print("------------------------------")
        for mueble in muebles_encontrados:
            print("ID:", mueble[0])
            print("Designación:", mueble[1])
            print("Precio: $"+ str(mueble[2]))
            print("Stock:",mueble[3])
            print("------------------------------")

    def buscar_mueble_x_ID(self):
        id_buscado= int(input("Ingresar el ID buscado: "))
        consulta= "SELECT * FROM muebles WHERE id = %s"
        mi_cursor.execute(consulta, (id_buscado,))
        muebles_encontrados= mi_cursor.fetchall()
        print("------------------------------")
        for mueble in muebles_encontrados:
            print("ID:", mueble[0])
            print("Designación:", mueble[1])
            print("Precio: $"+ str(mueble[2]))
            print("Stock:",mueble[3])
            print("------------------------------")

    def buscar_mueble_x_rango(self):
        precio1= int(input("Ingresar el precio más bajo buscado: "))
        precio2= int(input("Ingresar el precio más alto buscado: "))
        consulta= "SELECT * FROM muebles WHERE precio_unitario > %s AND precio_unitario < %s"
        mi_cursor.execute(consulta, (precio1,precio2))
        muebles_encontrados= mi_cursor.fetchall()
        print("------------------------------")
        for mueble in muebles_encontrados:
            print("ID:", mueble[0])
            print("Designación:", mueble[1])
            print("Precio: $"+ str(mueble[2]))
            print("Stock:",mueble[3])
            print("------------------------------")

    def eliminar_mueble(self):
        id= int(input("Ingresar el ID del mueble que desea eliminar: "))
        mi_cursor.execute("SELECT designacion FROM muebles WHERE id = %s", (id,))
        designacion= str(mi_cursor.fetchone())
        nombre_del_mueble=  designacion.strip("'(),")
        print("¿Borrar permanentemente el registro",nombre_del_mueble,"?")
        borrar= input("(s/n): ").lower()
        if borrar == "s":
            mi_cursor.execute("DELETE FROM muebles WHERE id = %s", (id,))
            base_datos.commit()
            print("Registro borrado exitosamente.")
        else:
            print("Operación cancelada.")

    def realizar_otra_operacion(self):
        q= input("¿Realizar otra operación? s/n: ").lower()
        if q == "s":
            return True
        else:
            return False

class Venta:
    def __init__(self):
        self.id_producto= 0 #id del producto seleccionado
        self.designacion= ""
        self.cantidad= 0 #cantidad que va a comprar el cliente
        self.stock= 0 #stock actual del producto_seleccionado
        self.subtotal= 0 
        self.total= 0
        self.vendedor= ""

    def set_id_producto(self,id_producto):
        self.id_producto= id_producto

    def get_id_producto(self):
        return self.id_producto

    def set_cantidad(self,cantidad):
        self.cantidad= cantidad

    def get_cantidad(self):
        return self.cantidad
    
    def set_stock(self,stock):
        self.stock= stock

    def get_stock(self):
        return self.stock

    def set_subtotal(self,subtotal):
        self.subtotal= subtotal

    def get_subtotal(self):
        return self.subtotal

    def set_total(self,total):
        self.total= total

    def get_total(self):
        return self.total

    def set_vendedor(self,vendedor):
        self.vendedor= vendedor

    def get_vendedor(self):
        return self.vendedor

    def mostrar_muebles(self):
        print("-----------------------------------------------\n              MUEBLES DISPONIBLES")
        mi_cursor.execute("SELECT * FROM muebles ORDER BY designacion")
        muebles= mi_cursor.fetchall()
        for mueble in muebles:
            if len(str(mueble[2])) > 3 and len(str(mueble[0])) > 1:
                print("ID:",mueble[0],"| $"+str(mueble[2]), "| ",mueble[1])
            elif len(str(mueble[2])) > 3:
                print("ID:",mueble[0]," | $"+str(mueble[2]), "| ",mueble[1])
            elif len(str(mueble[0])) > 1:
                print("ID:",mueble[0],"| $"+str(mueble[2]), " | ",mueble[1])
            else:
                print("ID:",mueble[0]," | $"+str(mueble[2]), " | ",mueble[1])
        print("---------------------------------------------")


    '''
    def elegir_mueble(self):
        mueble_a_comprar= int(input("Ingrese el ID del mueble que desea comprar: "))
        self.set_producto_seleccionado(mueble_a_comprar) #id
    
    def elegir_cantidad(self):
        query= "SELECT designacion FROM muebles WHERE id = %s"
        valor= self.get_id_producto()
        mi_cursor.execute(query,(valor,))
        mueble_elegido= mi_cursor.fetchone()
        print("Mueble seleccionado: "+str(mueble_elegido).strip("',()").replace("_"," "))
        cantidad= int(input("Ingrese la cantidad que desea comprar: "))
        self.set_cantidad(cantidad)
    '''

    def elegir_mueble(self):
        mueble_a_comprar= int(input("Ingrese el ID del mueble que desea comprar: ")) #o que el cliente desea comprar
        self.id_producto(mueble_a_comprar)

    def elegir_cantidad(self):
        """Me muestra la designacion del mueble elegido, y me pide la cantidad que quiero comprar del mismo.
        Ademas me trae el stock del producto solicitado."""
        query1= "SELECT designacion FROM muebles WHERE id = %s"
        id_mueble= self.get_id_producto()
        mi_cursor.execute(query1,(id_mueble,))      
        mueble_elegido= mi_cursor.fetchone()
        print("Mueble seleccionado: "+str(mueble_elegido).strip("',()").replace("_"," "))

        query2= "SELECT precio_unitario FROM muebles WHERE id = %s"
        mi_cursor.execute(query2, (id_mueble,))
        stock_mueble_elegido= mi_cursor.fetchone
        self.set_stock(stock_mueble_elegido)

        if stock_mueble_elegido > 0:
            cantidad= int(input("Ingrese la cantidad que desea comprar: "))
            self.set_cantidad(cantidad)
        else:
            print("No existe esa cantidad de",mueble_elegido,"en stock actualmente.")

    def calcular_precio(self):
        pass

    def descontar_stock(self):
        """Descuenta el atributo 'cantidad' del stock del producto cuyo id se ingreso en el atributo 'producto_seleccionado'."""
        pass

    def procesar_compra(self):
        self.elegir_cantidad()
        self.descontar_stock()


    def prueba(self):
        print(self.get_producto_seleccionado())
        print(self.get_cantidad())
        print(self.get_subtotal())
        print(self.get_total())
        print(self.get_vendedor())
      

    

    def comprar_muebles(self): #PRUEBA
        self.mostrar_muebles()
        self.elegir_mueble()
        self.elegir_cantidad()
#main
muebleriaPOO= Muebleria()
venta0000= Venta()
print('¡Bienvenido a Muebleria POO!')
menu= int(input('-------------------\nVistas:\n1. Administración\n2. Ventas\n3. Gerencia\n-------------------\nIngrese el número de vista que desea consultar: '))
if menu == 1:
    on= True
    while on == True:
        opc= muebleriaPOO.mostrar_menu_administracion()
        if opc == 1:
            muebleriaPOO.registrar_nuevo_mueble()
        if opc == 2:
            muebleriaPOO.editar_mueble()
        if opc == 3:
            muebleriaPOO.mostrar_muebles()
        if opc == 4:
            muebleriaPOO.buscar_mueble()
        if opc == 5:
            muebleriaPOO.eliminar_mueble()
        on= muebleriaPOO.realizar_otra_operacion()

if menu == 2:
    on= True
    while on == True:
        print("Vista Ventas")
        venta0000.comprar_muebles()
        venta0000.prueba()
        on= muebleriaPOO.realizar_otra_operacion()

if menu == 3:
    print("Vista Gerencia")
print("¡Gracias por utilizar el software!")

'''
Vista Vendedor:
Desarrollaremos el módulo venta:
Ofreceremos todos los muebles cargados en la vista administración y los clientes podrán comprar los muebles que quieran, cuantas veces quieran.
Nos piden generar un ticket para cada cliente indicando:
El nombre del producto seleccionado, las cantidades compradas, el subtotal por producto, el nombre del vendedor y el total por producto.
'''