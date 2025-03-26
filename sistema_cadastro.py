from PyQt5 import uic, QtWidgets
import psycopg2
import tkinter as tk
from tkinter import messagebox
from reportlab.pdfgen import canvas

numero_id = 0

dbname = 'your_DB_name'
user = 'postgres'
password = 'your_DB_password'
host = 'localhost'
port = '5432'

conn = psycopg2.connect(
    dbname=dbname,
    user=user,
    password=password,
    host=host,
    port=port)

cur = conn.cursor()

def excluir_dados():
    linha = formulario2.tableWidget.currentRow()
    formulario2.tableWidget.removeRow(linha)

    cursor=conn.cursor()
    cursor.execute("SELECT id FROM produtos")
    dados_lidos=cursor.fetchall()
    valor_id=dados_lidos[linha][0] 
    cursor.execute("DELETE FROM produtos WHERE id="+ str(valor_id))
    conn.commit()

def editar_dados():
    global numero_id
    formulario3.show()
    linha = formulario2.tableWidget.currentRow()

    cursor=conn.cursor()
    cursor.execute("SELECT id FROM produtos")
    dados_lidos=cursor.fetchall()
    valor_id=dados_lidos[linha][0] 
    cursor.execute("SELECT * FROM produtos WHERE id="+ str(valor_id))
    produto = cursor.fetchall()
    numero_id = valor_id

    formulario3.lineEdit.setText(str(produto[0][0]))
    formulario3.lineEdit_2.setText(str(produto[0][1]))
    formulario3.lineEdit_3.setText(str(produto[0][2]))
    formulario3.lineEdit_4.setText(str(produto[0][3]))
    formulario3.lineEdit_5.setText(str(produto[0][4]))
    conn.commit()

def salvar_dados_editados():
    global numero_id
    codigo = formulario3.lineEdit_2.text()
    produto = formulario3.lineEdit_3.text()
    preco = formulario3.lineEdit_4.text()
    categoria = formulario3.lineEdit_5.text()
    cursor = conn.cursor()
    cursor.execute("UPDATE produtos SET codigo = '{}', produto = '{}', preco = '{}', categoria = '{}' WHERE id = {}".format(codigo,produto,preco,categoria,numero_id))
    conn.commit()
    formulario3.close()
    formulario2.close()
    chama_segunda_tela()

def gerar_pdf():
    cursor=conn.cursor()
    comando_SQL = "SELECT * FROM produtos"
    cursor.execute(comando_SQL)
    dados_lidos=cursor.fetchall()
    y=0
    pdf = canvas.Canvas("cadastro_produtos.pdf")
    pdf.setFont("Times-Bold",25)
    pdf.drawString(200,800, "Produtos cadastrados:")
    pdf.setFont("Times-Bold",18)
    pdf.drawString(10,750,"ID")
    pdf.drawString(110,750,"Código")
    pdf.drawString(210,750,"Produto")
    pdf.drawString(360,750,"Preço(R$)")
    pdf.drawString(460,750,"Categoria")

    for i in range (0,len(dados_lidos)):
        y = y + 50
        pdf.drawString(10,750 -y ,str(dados_lidos[i][0]))
        pdf.drawString(110,750 -y ,str(dados_lidos[i][1]))
        pdf.drawString(210,750 -y ,str(dados_lidos[i][2]))
        pdf.drawString(360,750 -y ,str(dados_lidos[i][3]))
        pdf.drawString(460,750 -y ,str(dados_lidos[i][4]))
    
    pdf.save()
    messagebox.showinfo("PDF gerado com sucesso!")
        
def funcao_principal():
    linha1 = formulario.lineEdit.text()
    print("Codigo",linha1)

    linha2 = formulario.lineEdit_2.text()
    print("Produto",linha2)    

    linha3 = formulario.lineEdit_3.text()
    print("Preço",linha3)

    categoria=""
    
    cur.execute("SELECT 1 FROM produtos WHERE codigo = %s", (linha1,))
    if cur.fetchone():
        messagebox.showerror(f"Erro: Código '{linha1}' já existe no banco de dados.")
        return

    if formulario.radioButton.isChecked():
        print("Selecionado: Eletronicos")
        categoria="Eletronicos"
    elif formulario.radioButton_2.isChecked():
        print("Selecionado: Mercado")
        categoria="Mercado"
    else: 
        print("Selecionado: Vestuario")
        categoria="Vestuario"

    cursor=conn.cursor()
    comando_SQL="INSERT INTO produtos (codigo,produto,preco,categoria) VALUES(%s,%s,%s,%s)"
    dados=(str(linha1),str(linha2),str(linha3),categoria)    
    cursor.execute(comando_SQL,dados)
    conn.commit()
    formulario.lineEdit.setText("")
    formulario.lineEdit_2.setText("")
    formulario.lineEdit_3.setText("")

def chama_segunda_tela():
    formulario2.show() 

    cursor=conn.cursor()
    comando_SQL = "SELECT * FROM produtos"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()

    formulario2.tableWidget.setRowCount(len(dados_lidos))
    formulario2.tableWidget.setColumnCount(5)

    for i in range(0, len(dados_lidos)):
        for j in range(0,5):
            formulario2.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))

app=QtWidgets.QApplication([])
formulario=uic.loadUi("first_window.ui")
formulario2=uic.loadUi("second_window.ui")
formulario3=uic.loadUi("third_window.ui")

formulario.pushButton.clicked.connect(funcao_principal)

formulario.pushButton_3.clicked.connect(chama_segunda_tela)

formulario2.pushButton.clicked.connect(gerar_pdf)

formulario2.pushButton_2.clicked.connect(excluir_dados)

formulario2.pushButton_3.clicked.connect(editar_dados)

formulario3.pushButton.clicked.connect(salvar_dados_editados)


formulario.show()
app.exec()