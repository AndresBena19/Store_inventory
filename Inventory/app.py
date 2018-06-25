import sqlalchemy

from flask import Flask
from flask import request
from flask import render_template
from flask import flash
from flask import url_for


import forms


from collections import OrderedDict
from config import DBconfig

from models import *

app = Flask(__name__)
app.config.from_object(DBconfig)
db.init_app(app)

def Get_products():
    Temp = {}
    for key,name in db.session.query(Products.Identifier,Products.Description):
        Temp[key]=name

    Product = list(Temp.items())
    Product.sort(key=lambda x: x[1])

    return Product

def All_Products():
    final = {}

    for Product in db.session.query(Products):
        Temp,Pro= {},{}
        Temp['Tickets_now'] = Product.Tickets_now
        Temp['Units'] =Product.Units
        Temp['Departures_now'] = Product.Departures_now
        Temp['balance_now'] = Product.balance_now
        Pro[Product.Identifier] = Temp
        final[Product.Description]= Pro


    print(dict(OrderedDict(sorted(final.items(), key=lambda t: t[0]))))
    return dict(OrderedDict(sorted(final.items(), key=lambda t: t[0])))

def Get_provider():
    Temp = {}

    for key, name in db.session.query(Provider.Identifier, Provider.Name):

        Temp[key]=name
    Provide = list(Temp.items())
    Provide.sort(key=lambda x: x[1])

    return Provide

@app.route('/')
@app.route('/Products', methods=['GET','POST'])
def Products_table():
    del_P = forms.Delete(request.form)

    if request.method == 'POST':

            PDU = Products.query.filter_by(Identifier =del_P.Delete_P.data).first()
            if PDU != None:
                Products.query.filter(Products.Identifier==del_P.Delete_P.data).delete()
                db.session.commit()
                flash("Producto " + PDU.Description + " Ha sido borrado exitosamente")
            else:
                flash("No existen valores para  borrar")

    return render_template('Products.html', Inventory = All_Products(), form =del_P)



@app.route('/Create_product', methods=['GET', 'POST'])
def Product_work():

    loginform = forms.formlogin(request.form)


    if request.method == 'POST' and loginform.validate():
        try:
            Product = Products( Identifier=loginform.Identifier.data, Description= loginform.Description.data, Units= loginform.Units.data)
            db.session.add(Product)
            db.session.commit()
            flash("Creacion exitosa de " + loginform.Description.data)
        except sqlalchemy.exc.IntegrityError:

            flash("La clave de producto ya existe")



    return render_template('Make_product.html', login=loginform)


@app.route('/Provider', methods=['GET','POST'])
def Provider_table():

    del_Pro = forms.Delete(request.form)
    if(request.method == 'POST'):


            PRO = Provider.query.filter_by(Identifier =del_Pro.Delete_Pro.data).first()
            if PRO != None:
                Provider.query.filter(Provider.Identifier==del_Pro.Delete_Pro.data).delete()
                db.session.commit()
                flash("Producto " + PRO.Name + " Ha sido borrado exitosamente")
            else:
                flash("No existen valores para  borrar")


    Provider_data = {}
    for ID,Name,Ced,Address in  db.session.query(Provider.Identifier,Provider.Name,Provider.Ced,Provider.Address):
            Temp = {}
            Temp['ID'] = ID
            Temp['Name'] = Name
            Temp['Ced'] = Ced
            Temp['Address'] = Address

            Provider_data[ID] = Temp

    return render_template('Provider.html', Inventory = Provider_data, form=del_Pro )



@app.route('/Create_Provider', methods=['GET', 'POST'])
def Provider_work():

    Prividerform = forms.Provider(request.form)

    if request.method == 'POST' and Prividerform.validate():
        try:
            print (Prividerform.Name.data)
            Provider_new = Provider(Identifier=Prividerform.Identifier.data, Name=Prividerform.Name.data, Ced= Prividerform.Ced.data, Address= Prividerform.Address.data)
            db.session.add(Provider_new)
            db.session.commit()
            flash("Creacion exitosa de " + Prividerform.Name.data)
        except sqlalchemy.exc.IntegrityError:
            flash("La clave de producto ya existe")



    return render_template('Make_provider.html', Inventory=Prividerform)



@app.route('/Tickets', methods=['GET','POST'])
def Tickets_table():
    search = forms.Search(request.form)
    Del_form = forms.Search(request.form)

    if request.method == 'POST':

            if (len(search.Remision.data) > 0):
                Remision_s = {}
                Remisi = Tickets.query.filter_by(Number_remision=search.Remision.data).all()
                print(Remisi)
                for R in Remisi:
                    Provider_v = Provider.query.filter_by(Identifier=R.Provider_id).first()
                    Product = Products.query.filter_by(Identifier=R.Products_id).first()
                    Order = Buy_order.query.filter_by(N_compra=R.N_compra).all()

                    for O in Order:
                        if (O.Products_id == Product.Identifier):
                            Requisi_s = Requisition.query.filter_by(N_Requisition=O.Requisition).all()
                            for Rq in Requisi_s:
                                Temp = {}
                                Temp['id'] = R.id
                                Temp['Solicitud'] = Rq.Solicitud_name
                                Temp['Ced'] = Rq.Ced
                                Temp['Provider'] = Provider_v.Name

                                Temp['Date_stored'] = R.Date_stored

                                Temp['Ident'] = Product.Identifier
                                Temp['Description'] = Product.Description
                                Temp['Amount'] = R.amount
                                Temp['Units'] = Product.Units
                                Temp['Number_Solicitud'] = Rq.Solicitud_P


                                Temp['Number_Requisition'] = Rq.N_Requisition
                                Temp['Purchase_number'] = O.N_compra
                                Temp['Number_remision'] = str(R.Number_remision).split(
                                    '+') if R.Number_remision != "" else "Ninguna Remision"

                                Temp['Tickets'] = Product.Tickets_now
                                Temp['Balance'] = Product.balance_now

                                Remision_s[R.id] = Temp
                print(Remision_s)
                return render_template('Tickets.html', Inventory=Remision_s, form = Del_form , form2=search)

            if(len(Del_form.Delete_En.data)>0):

                    Entrada = Tickets.query.filter_by(id=Del_form.Delete_En.data).first()
                    if Entrada != None:
                        Product = Products.query.filter_by(Identifier=Entrada.Products_id).first()
                        print("fuck",Entrada.N_Requisition)

                        Order = Buy_order.query.filter(Buy_order.N_compra==Entrada.N_compra).filter(Buy_order.Requisition == Entrada.N_Requisition).all()

                        Products.query.filter(Products.Identifier==Entrada.Products_id).update({"Tickets_now": Product.Tickets_now - Entrada.amount,"balance_now":Product.balance_now - Entrada.amount })


                        for O in Order:

                            try:
                                if(O.Products_id==Entrada.Products_id):

                                    R = Requisition.query.filter_by(N_Requisition=O.Requisition,Products_id=O.Products_id).first()


                                    if(O.State == "Recibido"):

                                        if((R.amount - Entrada.amount) == 0):
                                            O.State = "No Recibido"
                                        else:
                                            print("Cambiando orden")
                                            O.State = R.amount - Entrada.amount

                                    elif(type(O.State) == str):


                                            print("1")
                                            if(int(O.State) == Entrada.amount ):
                                                O.State = "No Recibido"
                                            elif(int(O.State) - Entrada.amount > 0):
                                                    Value = int(O.State) + Entrada.amount

                                                    print("cumpliendo condicion")
                                                    if (R.amount == Value):
                                                        O.State = "No Recibido"
                                                    else:
                                                        O.State = O.State - Entrada.amount

                                    REMI = R.Remision.split('+')
                                    Result = []

                                    for i in REMI:
                                        try:
                                            Result.append(int(i))
                                        except Exception:
                                            pass


                                    if Entrada.Number_remision in Result :
                                            print("rem")
                                            Result.remove(Entrada.Number_remision)


                                    Resultb = [str(i) for i in Result ]

                                    R.Remision = '+'.join(Resultb)

                            except Exception as e:
                                print(e)



                        Tickets.query.filter(Tickets.id==Del_form.Delete_En.data).delete()

                        db.session.commit()
                        flash("Entrada # " +Del_form.Delete_En.data + " Ha sido borrado exitosamente")
                    else:
                        flash("No existen valores para  borrar")


    Tickets_inventory = {}
    for ID,date_stored,Amount,Number_remision,N_compra,Product_id,Provider_id in  db.session.query(Tickets.id,
                                                                                                                        Tickets.Date_stored,
                                                                                                                        Tickets.amount,
                                                                                                                        Tickets.Number_remision,
                                                                                                                        Tickets.N_compra,
                                                                                                                        Tickets.Products_id,
                                                                                                                        Tickets.Provider_id):

                Provider_v = Provider.query.filter_by(Identifier=Provider_id).first()
                Product = Products.query.filter_by(Identifier=Product_id).first()

                Temp = {}
                Temp['id']= ID
                Temp['Ident'] = Product.Identifier

                Temp['Provider'] = Provider_v.Name
                Temp['Ced'] = Provider_v.Ced

                Temp['Description'] = Product.Description
                Temp['Units'] = Product.Units

                Temp['Date_stored'] = date_stored

                Temp['Amount'] = Amount

                Temp['Number_remision'] = Number_remision
                Temp['Purchase_number'] = N_compra

                Temp['Tickets'] = Product.Tickets_now
                Temp['Balance'] = Product.balance_now


                Tickets_inventory[ID] = Temp

    return render_template('Tickets.html', Inventory=Tickets_inventory , form = Del_form , form2=search)


@app.route('/Create_Tickets', methods=['GET','POST'])
def Tickets_work():
    Ticketform = forms.Make_ticket(request.form)

    Ticketform.Identifier_P.choices=Get_products()
    Ticketform.Identifier_Pro.choices = Get_provider()

    if request.method == 'POST' and Ticketform.validate():

        flag =False

        Ticket = Tickets(Date_stored=Ticketform.Date_stored.data,
                         amount=Ticketform.amount.data,
                         Number_remision=Ticketform.Number_remision.data,
                         N_compra=Ticketform.N_Orde_Comprar.data,
                         Products_id=Ticketform.Identifier_P.data,
                         N_Requisition = Ticketform.Number_Requisition.data,
                         Provider_id=Ticketform.Identifier_Pro.data)
        db.session.add(Ticket)


        Product_now = Products.query.filter_by(Identifier= Ticketform.Identifier_P.data).first()
        Provider_now = Products.query.filter_by(Identifier= Ticketform.Identifier_Pro.data).first()

        Order_new = Buy_order.query.filter(Buy_order.N_compra == Ticketform.N_Orde_Comprar.data).filter(Buy_order.Requisition == Ticketform.Number_Requisition.data).all()

        if(len(Order_new) == 0):
            flag = True
            flash("No existe orden de compra " + Ticketform.N_Orde_Comprar.data )

        if (not flag):
            for Order in Order_new:
                if(Order.Products_id == Ticketform.Identifier_P.data):
                    Buy=Order
                    print("Producto coincide")


            Requisi_new = Requisition.query.filter(Requisition.N_compra==Ticketform.N_Orde_Comprar.data).filter(Requisition.N_Requisition==Ticketform.Number_Requisition.data).all()
            print(Requisi_new)
            for Req in Requisi_new:

                if(Req.Products_id == Ticketform.Identifier_P.data ):
                    Requisi = Req

            print("here")
            try:
                flagtwo = False

                if(str(Buy.State) == "No Recibido"):

                    Total = int(Requisi.amount) - int(Ticketform.amount.data)

                    if(Total < 0):
                        flagtwo =True
                        flash("Esta recibiendo mas unidades de las presentes en al orden")
                        return render_template('Make_ticket.html',Tick=Ticketform)
                else:
                    try:

                        Valor_reserva = int(Buy.State)
                        Total = Valor_reserva - int(Ticketform.amount.data)

                        if(Total < 0):
                          flagtwo =True
                          flash("Esta recibiendo mas unidades de las presentes en al orden")
                          return render_template('Make_ticket.html',Tick=Ticketform)

                    except ValueError :
                        print("ERRORRR")
                if(str(Buy.State) == "Recibido"):
                    flagtwo =True
                    flash("Ya se recibio el pedido completamente")
                    return render_template('Make_ticket.html',Tick=Ticketform)

                if (int(Ticketform.amount.data) == Requisi.amount and (Ticketform.Identifier_P.data ==  Buy.Products_id) ):

                    Buy_order.query.filter(Buy_order.N_compra == Ticketform.N_Orde_Comprar.data).filter(Buy_order.Requisition ==Ticketform.Number_Requisition.data).filter(Buy_order.Products_id==Ticketform.Identifier_P.data).update({"State": "Recibido"})
                    db.session.commit()

                elif(int(Ticketform.amount.data) < Requisi.amount  and (Ticketform.Identifier_P.data ==  Buy.Products_id) and (str(Buy.State) == "No Recibido")):

                    Buy_order.query.filter(Buy_order.N_compra == Ticketform.N_Orde_Comprar.data).filter(Buy_order.Requisition ==Ticketform.Number_Requisition.data).filter(Buy_order.Products_id==Ticketform.Identifier_P.data).update({"State": str(int(Requisi.amount) - int(Ticketform.amount.data))})
                    db.session.commit()

                elif(str(Buy.State) != "Recibido" and str(Buy.State) != "No Recibido"):
                    Buy_order.query.filter(Buy_order.N_compra == Ticketform.N_Orde_Comprar.data).filter(Buy_order.Requisition ==Ticketform.Number_Requisition.data).filter(Buy_order.Products_id==Ticketform.Identifier_P.data).update({"State": str(int(Buy.State) - int(Ticketform.amount.data))})
                    db.session.commit()

                    if(int(Buy.State)== 0):
                            Buy_order.query.filter(Buy_order.N_compra == Ticketform.N_Orde_Comprar.data).filter(Buy_order.Requisition ==Ticketform.Number_Requisition.data).filter(Buy_order.Products_id==Ticketform.Identifier_P.data).update({"State": "Recibido"})
                            db.session.commit()

                if(not flagtwo):

                    Products.query.filter(Products.Identifier == Ticketform.Identifier_P.data).update({"Tickets_now":(Product_now.Tickets_now + int(Ticketform.amount.data))})
                    Products.query.filter(Products.Identifier == Ticketform.Identifier_P.data).update({"balance_now":(Product_now.balance_now + int(Ticketform.amount.data))})
                    print("Modificando Requisicion")
                    print(Ticketform.Identifier_P.data ,Ticketform.N_Orde_Comprar.data,Ticketform.Number_Requisition.data)
                    print(type(Ticketform.Number_Requisition.data))
                    Requisition.query.filter(Requisition.id == Requisi.id).update({"Remision":Requisi.Remision + "+"+ Ticketform.Number_remision.data})

                    db.session.commit()
            except Exception as e :
                print(e)
                P = Products.query.filter_by(Identifier= Ticketform.Identifier_P.data).first()

                flash("El producto " + P.Description+ " No pertenece a la orden de compra " + Ticketform.N_Orde_Comprar.data )


    return render_template('Make_ticket.html',Tick=Ticketform)

@app.route('/Despartures', methods=['GET','POST'])
def Despartures_table():
    search = forms.Search(request.form)
    Del_Sa = forms.Delete(request.form)
    if request.method == 'POST':
        if(len(Del_Sa.Delete_Sa.data) != 0):

            Sali = Departures.query.filter_by(id = Del_Sa.Delete_Sa.data ).first()
            if Sali != None:
                P= Products.query.filter_by(Identifier =Sali.Products_id ).first()

                Departures.query.filter(Departures.id==Del_Sa.Delete_Sa.data).delete()
                Products.query.filter(Products.Identifier==Sali.Products_id).update({"Departures_now" : P.Departures_now - Sali.amount , "balance_now": P.balance_now +  Sali.amount  })

                db.session.commit()
                flash("Producto " + Del_Sa.Delete_Sa.data + " Ha sido borrado exitosamente")
            else:
                flash("No existen valores para  borrar")

        if(len(search.Contratista.data) !=0):
            print(search.Contratista.data)
            Contra = Departures.query.filter_by(builder=search.Contratista.data).all()
            print(Contra)
            if(len(Contra)!=0):
                    Depart_inventory = {}
                    print("aaa")
                    for Co in Contra:

                        Product = Products.query.filter_by(Identifier=Co.Products_id).first()

                        Temp = {}
                        Temp['ID'] = Co.id
                        Temp['ident'] = Product.Identifier
                        Temp['Description'] = Product.Description
                        Temp['Units'] = Product.Units
                        Temp['Date'] = Co.date
                        Temp['Amount'] = Co.amount
                        Temp['Number_vale'] = Co.Number_vale
                        Temp['builder'] = Co.builder
                        Temp['Destine'] = Co.Dest
                        Temp['Solicitud'] = Co.N_Solicitud

                        Temp['Departures'] = Product.Departures_now
                        Temp['Balance'] = Product.balance_now

                        Depart_inventory[Co.id] = Temp
                    return render_template('Despartures.html', Inventory= Depart_inventory, form = Del_Sa, form2 = search)
            else:
                flash("No existe el contratista")

    Depart_inventory = {}
    for ID,date,amount,Number_vale,builder,Dest,Solicitud, Product_id in  db.session.query(Departures.id,
                                                                                                    Departures.date,
                                                                                                    Departures.amount,
                                                                                                    Departures.Number_vale,
                                                                                                    Departures.builder,
                                                                                                    Departures.Dest,
                                                                                                    Departures.N_Solicitud,
                                                                                                    Departures.Products_id):
                Product = Products.query.filter_by(Identifier= Product_id).first()

                Temp = {}
                Temp['ID'] = ID
                Temp['ident'] = Product.Identifier
                Temp['Description'] = Product.Description
                Temp['Units'] = Product.Units
                Temp['Date'] = date
                Temp['Amount'] = amount
                Temp['Number_vale'] = Number_vale
                Temp['builder'] = builder
                Temp['Destine'] = Dest
                Temp['Solicitud'] = Solicitud

                Temp['Departures'] = Product.Departures_now
                Temp['Balance'] = Product.balance_now

                Depart_inventory[ID] = Temp


    return render_template('Despartures.html', Inventory= Depart_inventory, form = Del_Sa, form2 = search)



@app.route('/Create_Despartures', methods=['GET','POST'])
def Despartures_work():

    Departuresform = forms.Departures_ticket(request.form)

    Departuresform.Identifier_P.choices= Get_products()


    if request.method == 'POST' and Departuresform.validate():


        try:
            Product_now = Products.query.filter_by(Identifier= Departuresform.Identifier_P.data).first()

            print (Product_now)
            if (int(Product_now.balance_now) == 0):
                flash("Imposible, No hay puntillas en bodega")

            elif ((Product_now.balance_now - int(Departuresform.amount.data)) < 0 ):
                flash("Imposible, solo existen "  +str(Product_now.balance_now)+  " "+ Product_now.Description  + " En bodega")


            else:
                print("entr")
                Despartur = Departures(date= Departuresform.Date.data,amount = Departuresform.amount.data, Number_vale= Departuresform.N_vale.data,builder=Departuresform.builder.data.strip(),Dest=Departuresform.Destine.data,N_Solicitud = Departuresform.Solicitud.data,Products_id=Departuresform.Identifier_P.data)
                db.session.add(Despartur)
                db.session.commit()

                Products.query.filter(Products.Identifier == Departuresform.Identifier_P.data).update({"Departures_now":(Product_now.Departures_now + int(Departuresform.amount.data))})
                Products.query.filter(Products.Identifier == Departuresform.Identifier_P.data).update({"balance_now":(Product_now.balance_now - int(Departuresform.amount.data))})
                db.session.commit()
        except AttributeError as e:
            print(e)
            flash("Imposible, No existe el producto " + str(Departuresform.Identifier_P.data))

    return render_template('Make_Departure.html',Depart=Departuresform)


@app.route('/Create_Buy_Order', methods=['GET','POST'])
def Buy_Order_work():
    Buy_Orderform = forms.Buy_order(request.form)

    Buy_Orderform.Identifier_P.choices= Get_products()
    Buy_Orderform .Identifier_Pro.choices = Get_provider()

    if request.method == 'POST' and Buy_Orderform.validate():

        R_Q = Requisition.query.filter_by(N_Requisition= Buy_Orderform.N_Requisition.data).all()

        for Req in R_Q:
            if(Req.Products_id == Buy_Orderform.Identifier_P.data ):
                Requisit = Req

        try:
            Total = int(Buy_Orderform.Value_U.data)*int(Requisit.amount)
            Total_Iva = (int(Total)* 0.21) + Total

            Order = Buy_order(date=Buy_Orderform.Date.data,Value_U=int(Buy_Orderform.Value_U.data),Value_T=int(Total),Value_T_Iva=float(Total_Iva),N_compra=Buy_Orderform.N_Compra.data, Products_id=Buy_Orderform.Identifier_P.data,Provider_id=Buy_Orderform.Identifier_Pro.data,Requisition=Buy_Orderform.N_Requisition.data)
            db.session.add(Order)

            Requisition.query.filter(Requisition.N_Requisition == Buy_Orderform.N_Requisition.data).filter(Requisition.Products_id==Buy_Orderform.Identifier_P.data).update({"N_compra":Buy_Orderform.N_Compra.data})
            db.session.commit()
        except Exception:
                P = Products.query.filter_by(Identifier= Buy_Orderform.Identifier_P.data).first()

                flash("El producto " + P.Description+ " No pertenece a la requisicion " + Buy_Orderform.N_Requisition.data )

    return render_template('make_Buy_Order.html', Inventory=Buy_Orderform)


@app.route('/Buy_Order', methods=['GET','POST'])
def Buy_Order_table():

    search_form = forms.Search(request.form)
    if request.method == 'POST':


        if(len(search_form.compra.data)>0):
            Orders_two = {}

            Buy_orders = Buy_order.query.filter_by(N_compra=search_form.compra.data).all()

            for Order in Buy_orders:

                Provider_v = Provider.query.filter_by(Identifier=Order.Provider_id).first()
                Product = Products.query.filter_by(Identifier=Order.Products_id).first()
                New_Requisition= Requisition.query.filter_by(N_Requisition=Order.Requisition).all()

                for R in New_Requisition:
                    if(R.Products_id == Product.Identifier):

                        Temp = {}
                        Temp['ID'] = Order.id
                        Temp['Date'] = Order.date
                        Temp['Amount'] = R.amount
                        Temp['Number_Compra'] = Order.N_compra
                        Temp['Value_U'] = Order.Value_U
                        Temp['Value_T'] = Order.Value_T
                        Temp['Value_T_Iva'] = Order.Value_T_Iva
                        Temp['Requisition'] = R.N_Requisition

                        Temp['Ident'] = Product.Identifier
                        Temp['Name'] = Provider_v.Name
                        Temp['Ced'] = Provider_v.Ced
                        Temp['Address'] = Provider_v.Address
                        Temp['Units'] = Product.Units
                        Temp['Description'] = Product.Description

                        Temp['State'] = Order.State

                        Orders_two[Order.id] = Temp

            return render_template('Buy_Order.html',Inventory = Orders_two , form=search_form)

        if(len(search_form.Delete_Or.data)>0):

                Order = Buy_order.query.filter_by(id=search_form.Delete_Or.data).first()
                if Order != None:
                    Buy_order.query.filter(Buy_order.id==search_form.Delete_Or.data).delete()
                    Requisition.query.filter(Requisition.N_Requisition ==Order.Requisition).filter(Requisition.Products_id==Order.Products_id).update({"N_compra": " "})
                    flash("Orden " + Order.N_compra + " Ha sido borrado exitosamente")
                    db.session.commit()
                else:
                    flash("No existen valores para  borrar")


    Final = 0
    Final_Iva = 0

    Orders = {}
    for ID,date,N_Compra,Value_U,Value_T,Value_T_Iva,State,Product_id,Provider_id,Requisition_id in  db.session.query(Buy_order.id,
                                                                                                                Buy_order.date,
                                                                                                                Buy_order.N_compra,
                                                                                                                Buy_order.Value_U,
                                                                                                                Buy_order.Value_T,
                                                                                                                Buy_order.Value_T_Iva,
                                                                                                                Buy_order.State,
                                                                                                                Buy_order.Products_id,
                                                                                                                Buy_order.Provider_id,
                                                                                                                Buy_order.Requisition):


                New_Requisition= Requisition.query.filter_by(N_Requisition=Requisition_id).all()
                Product = Products.query.filter_by(Identifier=Product_id).first()
                Provider_v = Provider.query.filter_by(Identifier=Provider_id).first()



                for R in New_Requisition:
                    if(R.Products_id == Product.Identifier):
                        Temp = {}
                        Temp['ID'] = ID
                        Temp['Date'] = date
                        Temp['Amount'] = R.amount
                        Temp['Number_Compra'] = N_Compra
                        Temp['Value_U'] = Value_U
                        Temp['Value_T'] = Value_T
                        Temp['Value_T_Iva'] = Value_T_Iva
                        Temp['Requisition'] = Requisition_id

                        Temp['Ident'] = Product.Identifier
                        Temp['Name'] = Provider_v.Name
                        Temp['Ced'] = Provider_v.Ced
                        Temp['Address'] = Provider_v.Address
                        Temp['Units'] = Product.Units
                        Temp['Description'] = Product.Description

                        Temp['State'] = State
                        Final = Final + Value_T
                        Final_Iva = Final_Iva + Value_T_Iva

                        Orders[ID] = Temp
    return render_template('Buy_Order.html',Inventory = Orders, form=search_form, T = Final, T_iva = Final_Iva)




@app.route('/Create_Requisition', methods=['GET','POST'])
def Requisition_work():

    R_form = forms.Requisition(request.form)
    R_form.Identifier_P.choices= Get_products()


    if request.method == 'POST' and R_form.validate():
        R =Requisition.query.filter_by(N_Requisition=R_form.N_Requisition.data).all()
        Flag = False

        for Req in R:
            if(Req.Products_id==R_form.Identifier_P.data):

                Flag =True
                P = Products.query.filter_by(Identifier= R_form.Identifier_P.data).first()
                flash("Ya existe una requisicion con el producto " +P.Description)


        if(not Flag):
            New_Requisition = Requisition(Solicitud_name=R_form.Solicitud_Name.data,Ced=R_form.Ced.data,N_Requisition=R_form.N_Requisition.data,Destine=R_form.Destine.data,Date=R_form.Date.data,amount=R_form.amount.data,Products_id=R_form.Identifier_P.data,Solicitud_P=R_form.N_Solicitud.data)
            db.session.add(New_Requisition)
            db.session.commit()
            flash("Creacion exitosa")

    return render_template('make_Requisition.html', Inventory=R_form)



@app.route('/Requisition', methods=['GET','POST'])
def Requisition_table():
    search_form = forms.Search(request.form)

    if request.method == 'POST':
        if(len(search_form.Remision.data)> 0):
            Remision_s = {}
            Remisi = Tickets.query.filter_by(Number_remision=search_form.Remision.data).all()

            for R in Remisi:
                Provider_v = Provider.query.filter_by(Identifier=R.Provider_id).first()
                Product = Products.query.filter_by(Identifier=R.Products_id).first()
                Order = Buy_order.query.filter_by(N_compra=R.N_compra).all()

                for O in Order:
                    if(O.Products_id==Product.Identifier):
                        Requisi_s = Requisition.query.filter_by(N_Requisition=O.Requisition).all()
                        for Rq in Requisi_s:

                            Temp = {}
                            Temp['ID'] = R.id
                            Temp['Solicitud']= Rq.Solicitud_name
                            Temp['Ced']= Rq.Ced

                            Temp['Date'] = R.Date_stored

                            Temp['Ident'] = Product.Identifier
                            Temp['Description'] = Product.Description
                            Temp['Amount'] = R.amount
                            Temp['Units'] = Product.Units
                            Temp['Number_Solicitud'] = Rq.Solicitud_P
                            Temp['Destine'] = Rq.Destine

                            Temp['Number_Requisition'] =Rq.N_Requisition
                            Temp['Number_Compra'] = O.N_compra
                            Temp['Remision'] = str(R.Number_remision).split('+') if R.Number_remision != "" else "Ninguna Remision"

                            Remision_s[R.id] = Temp
            return render_template('Requisition.html',Inventory = Remision_s , form=search_form )


        if(len(search_form.Requisicion.data)>0):

            Requisi_new = {}
            Requisi_s = Requisition.query.filter_by(N_Requisition=search_form.Requisicion.data).all()

            for R in Requisi_s:

                Product = Products.query.filter_by(Identifier=R.Products_id).first()

                Temp = {}
                Temp['ID'] = R.id
                Temp['Solicitud']= R.Solicitud_name
                Temp['Ced']= R.Ced

                Temp['Date'] = R.Date

                Temp['Ident'] = Product.Identifier
                Temp['Description'] = Product.Description
                Temp['Amount'] = R.amount
                Temp['Units'] = Product.Units
                Temp['Destine'] = R.Destine

                Temp['Number_Solicitud'] = R.Solicitud_P
                Temp['Number_Requisition'] = R.N_Requisition
                Temp['Number_Compra'] = R.N_compra
                Temp['Remision'] = str(R.Remision).split('+') if R.Remision != "" else " "

                Requisi_new[R.id] = Temp
            return render_template('Requisition.html',Inventory = Requisi_new , form=search_form )
        if(len(search_form.Delete_Re.data)>0):
                R = Requisition.query.filter_by(id = search_form.Delete_Re.data).first()
                if R != None:
                    Requisition.query.filter(Requisition.id==search_form.Delete_Re.data).delete()
                    db.session.commit()
                    flash("La requisicicon #  " + search_form.Delete_Re.data + " ")
                else:
                    flash("No existen valores para  borrar")

    Rquest = {}
    for ID,N_Requisition,Name_S,Ced,Destine,Date,amount,N_Compra,N_Remision,Product_id,N_Solicitud in  db.session.query(Requisition.id,Requisition.N_Requisition,Requisition.Solicitud_name,Requisition.Ced,Requisition.Destine,Requisition.Date,Requisition.amount,Requisition.N_compra,Requisition.Remision,Requisition.Products_id,Requisition.Solicitud_P):

                Product = Products.query.filter_by(Identifier=Product_id).first()

                Temp = {}
                Temp['ID'] = ID
                Temp['Solicitud']= Name_S
                Temp['Ced']= Ced

                Temp['Date'] = Date

                Temp['Ident'] = Product.Identifier
                Temp['Description'] = Product.Description
                Temp['Amount'] = amount
                Temp['Units'] = Product.Units
                Temp['Number_Solicitud'] = N_Solicitud
                Temp['Destine']= Destine

                Temp['Number_Requisition'] = N_Requisition
                Temp['Number_Compra'] = N_Compra
                Temp['Remision'] = str(N_Remision).split('+') if N_Remision != "" else " "

                Rquest[ID] = Temp

    return render_template('Requisition.html',Inventory = Rquest, form=search_form )




if __name__ == '__main__':


    with app.app_context():
        db.create_all()

    app.run(port=8888)
