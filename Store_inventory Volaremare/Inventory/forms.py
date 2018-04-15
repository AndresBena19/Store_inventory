from wtforms import Form
from wtforms import *

from models import *
from wtforms import validators






class  formlogin(Form):
    Identifier= StringField('Identificador', [validators.Required(message='falta campo'), validators.length(min=1, max=100)])
    Description= StringField('Descripcion', [validators.Required(message='falta campo'), validators.length(min=1, max=100)])
    Units= StringField('Units', [validators.Required(message='falta campo'), validators.length(min=1, max=100)])


class  Provider(Form):
    Identifier= StringField('Identifier', [validators.Required(message='falta campo'), validators.length(min=1, max=100)])
    Name= StringField('Nombre', [validators.Required(message='falta campo'), validators.length(min=1, max=100)])
    Ced= StringField('Cedula', [validators.Required(message='falta campo'), validators.length(min=1, max=100)])
    Address= StringField('Direccion', [validators.Required(message='falta campo'), validators.length(min=1, max=100)])


class  Make_ticket(Form):

    Identifier_P = SelectField('Identificador Producto')
    Identifier_Pro = SelectField('Identificador Proveedor')

    amount =StringField('Cantidad', [validators.Required(message='falta campo'), validators.length(min=1, max=100)])
    Date_stored  = DateField('Fecha ',format='%Y-%m-%d')
    Number_Requisition = StringField('Numero de Requision', [validators.Required(message='falta campo'), validators.length(min=1, max=100)])

    Number_remision = StringField('Numero de Remision', [validators.Required(message='falta campo'), validators.length(min=1, max=100)])
    N_Orde_Comprar = StringField('Orden de Compra', [validators.Required(message='falta campo'), validators.length(min=1, max=100)])


class  Departures_ticket(Form):
    Identifier_P = SelectField('Identificador Producto')

    amount =StringField('Cantidad', [validators.Required(message='falta campo'), validators.length(min=1, max=100)])
    Date  = DateField('Fecha Actual',format='%Y-%m-%d')
    N_vale = StringField('Numero de vale', [validators.Required(message='falta campo'), validators.length(min=1, max=100)])

    builder = StringField('Contratista', [validators.Required(message='falta campo'), validators.length(min=1, max=100)])
    Destine = StringField('Destino', [validators.Required(message='falta campo'), validators.length(min=1, max=100)])
    Solicitud = StringField('Numero de Solicitud', [validators.Required(message='falta campo'), validators.length(min=1, max=100)])






class Buy_order(Form):

    Identifier_P = SelectField('Identificador Producto')
    Identifier_Pro = SelectField('Identificador Proveedor')

    Date  = DateField('Fecha Actual',format='%Y-%m-%d')

    N_Compra = StringField('Numero de compra', [validators.Required(message='falta campo'), validators.length(min=1, max=100)])
    N_Requisition = StringField('Numero de Requisicion', [validators.Required(message='falta campo'), validators.length(min=1, max=100)])

    Value_U = StringField('Valor Unitario', [validators.Required(message='falta campo'), validators.length(min=1, max=100)])



class Requisition(Form):


    Solicitud_Name = StringField('Solicitado por', [validators.Required(message='falta campo'), validators.length(min=1, max=100)])
    Ced = StringField('Cedula', [validators.Required(message='falta campo'), validators.length(min=1, max=100)])

    N_Requisition = StringField('Numero Requisicion', [validators.Required(message='falta campo'), validators.length(min=1, max=100)])

    Destine = StringField('Destino', [validators.Required(message='falta campo'), validators.length(min=1, max=100)])
    Date  = DateField('Fecha Actual',format='%Y-%m-%d')

    Identifier_P = SelectField('Identificador Producto')

    N_Solicitud = StringField('Numero solicitud de pedido', [validators.Required(message='falta campo'), validators.length(min=1, max=100)])


    amount =StringField('Cantidad', [validators.Required(message='falta campo'), validators.length(min=1, max=100)])


class Search(Form):

    compra = StringField('Ingrese el numero de compra', [validators.Required(message='falta campo'), validators.length(min=1, max=100)])
    Remision = StringField('Ingrese el numero de remision', [validators.Required(message='falta campo'), validators.length(min=1, max=100)])
    Requisicion = StringField('Ingrese el numero de requisicion', [validators.Required(message='falta campo'), validators.length(min=1, max=100)])
    Contratista = StringField('Ingrese nombre del Contratista', [validators.Required(message='falta campo'), validators.length(min=1, max=100)])


    Delete_Re = StringField('Ingrese el ID de la requisicion', [validators.Required(message='falta campo'), validators.length(min=1, max=100)])
    Delete_Or= StringField('Ingrese el ID de Orden de compra', [validators.Required(message='falta campo'), validators.length(min=1, max=100)])
    Delete_En= StringField('Ingrese el ID de entrada', [validators.Required(message='falta campo'), validators.length(min=1, max=100)])
class Delete(Form):
    Delete_P = StringField('Ingrese el ID del producto', [validators.Required(message='falta campo'), validators.length(min=1, max=100)])
    Delete_Pro =  StringField('Ingrese el ID del Provedor', [validators.Required(message='falta campo'), validators.length(min=1, max=100)])
    Delete_Sa = StringField('Ingrese el ID de la salida', [validators.Required(message='falta campo'), validators.length(min=1, max=100)])
