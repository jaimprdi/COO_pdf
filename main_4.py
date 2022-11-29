import pandas as pd 
import sys 
import matplotlib.pyplot as plt 
import seaborn as sns
from fpdf import FPDF


sns.set_style("whitegrid")


def salida_controlada():

    print('\nFinalizando programa\nmaven_pizzas ')
    print('\nPrograma finalizado')
    sys.exit()

def extract():
    ordersdetails = pd.read_csv('order_details_2016.csv', sep=';')                   
    ingredients = pd.read_csv('pizza_types.csv', encoding='latin1')    
    pizza_price = pd.read_csv('pizzas.csv')           
    orders=pd.read_csv('orders_2016.csv', sep=';')  

    return [ingredients , orders , pizza_price , ordersdetails]


def tablas(fichero, fichero_2, details):    
    # tabla de los ingredientes.
    fig = plt.figure(figsize=(20,25))
    sns.barplot(x='Ingredientes_necesarios', y='Cantidad a comprar por semana', data=fichero,
                palette=sns.color_palette("Greens_d", len(fichero)))
    plt.xlabel('Ingredientes')
    plt.ylabel('Cantidad')
    plt.xticks(rotation=45)
    plt.title("Ingredientes mas usados")
    plt.savefig("Ingredientes_semanales.jpg")
    
    # tabla de las pizzas mas caras y baratas  y sus precios respectivos. 
    fig = plt.figure (figsize=(12, 10))
    fichero_22 = fichero_2.groupby(by='pizza_id')['price'].sum().sort_values(ascending=False)[:5]
    #5 mas baratas :
    fichero_23=fichero_2.groupby(by='pizza_id')['price'].sum().sort_values(ascending=True)[:5]
    sns.barplot(y=['the greek xxl','the greek xl','brie_carre_s','ital veggie l','bbq chicken l'] ,x=fichero_22, data=fichero_22 , palette=sns.color_palette("Blues_d", len(fichero_22)),orient='horizontal')
    plt.xlabel("Identificador pizza")
    plt.title("Precios de las pizzas")
    plt.xticks(rotation=45)
    plt.savefig ("Preciosdelaspizzas.jpg")
  
    fig=plt.figure(figsize=(12,10))
    sns.barplot(y=['pepperoni s','hawaian s','pep msh pep s','four cheese s','mediterraneo s'] ,x=fichero_23, data=fichero_23 , palette=sns.color_palette("Purples_d", len(fichero_23)),orient='horizontal')
    plt.xlabel("Identificador pizza")
    plt.title("Precios de las pizzas")
    plt.xticks(rotation=45)
    plt.savefig ("Preciosdelaspizzas_baratas.jpg")



    # grafica de las 5 pizzas mas pedidas. 
    quantity_pizzas = details.groupby(by='pizza_id')['quantity'].sum().sort_values(ascending=False)
    quant_5=quantity_pizzas[:5]
    fig=plt.figure (figsize=(10,10))
    sns.barplot(x=['big meat s','five cheese large','thai chicken l ','four cheese l','classic dxl medium'], y=[1544,1142,1104,1036,934], data=quant_5, palette=sns.color_palette("Reds_d", len(quant_5)))
    plt.xlabel('Identificador pizza')
    plt.ylabel('Cantidad de pedidos ')
    plt.title(" Cinco pizzas mas pedidas")
    plt.xticks(rotation=45)
    plt.savefig ("cinco_pizzas.jpg")

    #hacer ahora las 5 pizzas menos pedidas 
    quantity_pizzas = details.groupby(by='pizza_id')['quantity'].sum().sort_values(ascending=True)
    quantity_5=quantity_pizzas[:5]
    fig=plt.figure (figsize=(10,10))
    sns.barplot(x=['the greek xxl','chicken alfredo s','green garden l ','calabrese l','mexicana s'], y=[22,78,79,81,133], data=quantity_5, palette=sns.color_palette("Blues_d", len(quant_5)))
    plt.xlabel('Identificador pizza')
    plt.ylabel('Cantidad de pedidos ')
    plt.title(" Cinco pizzas menos pedidas")
    plt.xticks(rotation=45)
    plt.savefig ("cinco_pizzas_menos.jpg")

    #hacer las mas caras y las mas baratas , tratar de hacerlo en una grafica. 

    return


def crear_pdf():

    pdf=PDF('P', 'mm', 'Letter')
    # limite del pdf : 
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font('times','B',11)
    # add text : 
    pdf.cell(30,5,'Informe Para el COO de Maven Pizzas', ln=True)
    pdf.cell(30,10, '        ' ,ln=True)
    pdf.cell(30,5,' Trataremos varios aspectos de los pedidos de pizzas') 
    pdf.cell(30,10,'           ',ln=True)
    pdf.cell(20,5,'En las graficas podran comparar precios, pedidos, cantidades del año 2016',ln=True)
    pdf.image('icai.jpg',10,90,200)

    pdf.add_page()
    pdf.cell(10,5,'           Las cinco pizzas mas  y menos caras para el año 2016 ')
    pdf.image('Preciosdelaspizzas.jpg',40,55,100)
    pdf.image('Preciosdelaspizzas_baratas.jpg',40,150,100)
    pdf.add_page()
    pdf.cell(10,5,'                Cantidad de ingredientes empleados por semana en 2016 ')
    pdf.image('Ingredientes_semanales.jpg',10,50,170)
    pdf.add_page()
    pdf.cell(10,5,'           Las cinco pizzas mas  y menos pedidas para el año 2016 ')
    pdf.image("cinco_pizzas.jpg",41,50,100)
    pdf.image('cinco_pizzas_menos.jpg',41,147,100)

    pdf.output('maven_pdf.pdf')

    return 

class PDF(FPDF):
    def header(self):
        #coger logo 
        self.image('logo.jpg',12,10,25)
        self.set_font('helvetica', 'B', 15)
        self.cell(0,10,'                      Informe para el COO de maven Pizzas', border=False, ln=1)
        self.ln(20)
    
    def footer(self):
        self.set_y(-20)
        self.set_font('helvetica', 'I', 10)


def main():

    dfs=extract()
    # este fichero de resultados se obtiene ejecutando el obtencion_fichero_resultados.py (el main de la practica 2) adjunto en el repo
    # se trata de una lectura de un fichero sucio. 
    fichero=pd.read_csv('resultado_pizzas_2.csv',sep=',')

    #limpio el fichero de order details : 
    orderdetails_= dfs[3]
    for i in range(len(orderdetails_['pizza_id'])):
        if orderdetails_['quantity'][i] == None:
            orderdetails_.iloc[i]
    orderdetails_=orderdetails_[orderdetails_['pizza_id'].notna()] #quita filas de nans
    orderdetails_=orderdetails_[orderdetails_['quantity'].notna()] #quita filas de Nan ya que no podemos dar un valor, no hay pistas 
    identifier = []
    identifier_2 = []
    # diccionario con claves erroneas que vamos a sustituir por aquellos valores correctos
    # a los que nos queremos referir.
    diccionario = { '@':'a','3':'e',
                 '0':'o',' ':'_',
                 '-':'_' }

    diccionario1 = { '@':'a','3':'e',
                 'One':'1','one':'1',
                 'two':'2','Two':'2',
                 '0':'o',' ':'_',
                 '-':'_','O': 'o','_1':'1', '_2':'2',
                 'e':'3'}

    for id in orderdetails_['pizza_id']:
        for key in diccionario:
            pizza = id.replace(key,diccionario[key])
            id=pizza
        identifier.append(id)

    for cuanta_final in orderdetails_['quantity']:
        cuanta_final=str(cuanta_final)
        for key in diccionario1:
            cuentas = cuanta_final.replace(key,diccionario1[key])
            cuanta_final = cuentas
        identifier_2.append(int(cuanta_final))
    lista_1=identifier
    lista_2=identifier_2

    orderdetails_['pizza_id'] = lista_1
    # Reescribimos las dos columnas del dataframe que acabamos de procesar
    orderdetails_['quantity'] = lista_2
    detalles_final = orderdetails_
    detalles_final.reset_index(drop=True, inplace=True)
    print(detalles_final) # imprimimos el dataset de 2016 limpio. 
    tablas(fichero,dfs[2], detalles_final)
    crear_pdf()
    # fichero con la informacion de los ingredientes necesarios por semana 
    # guardarlo en el csv designado en la fucnion load 
    salida_controlada()
    
    
if __name__  ==  '__main__' :
    main()