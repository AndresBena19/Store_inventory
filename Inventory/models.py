from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()



class Products(db.Model):
    __tablename__="Products"
    Identifier = db.Column(db.String(100), primary_key=True)
    Description = db.Column(db.String(100))
    Units= db.Column(db.String(100))
    Tickets_now = db.Column(db.Integer, default = 0)
    Departures_now = db.Column(db.Integer, default = 0)
    balance_now  = db.Column(db.Integer, default = 0)

    Ticket = db.relationship('Tickets', backref='Products')
    Departures = db.relationship('Departures', backref='Products')
    Requisition = db.relationship('Requisition', backref='Products')
    Buy_order = db.relationship('Buy_order', backref='Products')


class Provider(db.Model):
    __tablename__="Provider"
    Identifier = db.Column(db.String(100), primary_key=True)

    Name = db.Column(db.String(100))
    Ced = db.Column(db.String(100))
    Address = db.Column(db.String(100))


    Buy_Order= db.relationship('Buy_order', backref='Provider')

    Entrada = db.relationship('Tickets')



class Buy_order(db.Model):
    __tablename__="Buy_order"
    id= db.Column(db.Integer, autoincrement=True,primary_key=True)

    date = db.Column(db.String(100))
    Value_U = db.Column(db.Integer)

    Value_T = db.Column(db.Integer)
    Value_T_Iva = db.Column(db.Float)

    N_compra = db.Column(db.String(100))

    State = db.Column(db.String(100), default = "No recibida")

    Products_id = db.Column(db.String(255), db.ForeignKey('Products.Identifier'))
    Provider_id = db.Column(db.String(255), db.ForeignKey('Provider.Identifier'))

    Requisition = db.Column(db.String(255), db.ForeignKey('Requisition.N_Requisition'))



class Requisition(db.Model):
    __tablename__="Requisition"
    id = db.Column(db.Integer, autoincrement=True,primary_key=True)

    N_Requisition = db.Column(db.String(100))
    Solicitud_name= db.Column(db.String(100))
    Ced = db.Column(db.String(100))

    Destine = db.Column(db.String(100))
    Date =  db.Column(db.String(100))

    amount =  db.Column(db.Integer)
    N_compra = db.Column(db.String(100), default=" ")
    Remision =  db.Column(db.String(100), default=" ")
    Products_id= db.Column(db.String(255), db.ForeignKey('Products.Identifier'))
    Solicitud_P = db.Column(db.String(100))

    Buy_Order = db.relationship('Buy_order')



class Tickets(db.Model):
    __tablename__="Tickets"
    id = db.Column(db.Integer, autoincrement=True,primary_key=True)

    Date_stored = db.Column(db.String(100))
    amount = db.Column(db.Integer)

    Number_remision = db.Column(db.Integer)
    N_compra= db.Column(db.Integer)

    Products_id= db.Column(db.String(255), db.ForeignKey('Products.Identifier'))
    Provider_id= db.Column(db.String(255), db.ForeignKey('Provider.Identifier'))


class Departures(db.Model):
    __tablename__="Departures"
    id = db.Column(db.Integer, autoincrement=True,primary_key=True)

    date = db.Column(db.String(100))
    amount = db.Column(db.Integer)
    Number_vale = db.Column(db.Integer)
    builder = db.Column(db.String(100))
    Dest = db.Column(db.String(100))

    Products_id= db.Column(db.String(255), db.ForeignKey('Products.Identifier'))
