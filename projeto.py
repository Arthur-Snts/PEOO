from tkinter import *
import imdb
import pickle
import sqlite3

class Main():
    def __init__(self):
        self.janela = Tk()
        self.largura = self.janela.winfo_screenwidth()
        self.altura = self.janela.winfo_screenheight()
        self.janela.geometry("%dx%d" % (self.largura, self.altura))
        self.janela.title("AMA Filmes")

        # Cria o canvas principal
        self.canva1 = Canvas(self.janela, bg="#5CE1E6", width=self.largura, height=self.altura)
        self.canva1.place(x=0, y=0)

        # Cria o canvas do cabeçalho
        self.canvas3 = Canvas(self.canva1, bg="#37C9E4", width=self.largura, height=123)
        self.canvas3.place(x=0, y=0)

        # Cria o canvas do lado esquerdo
        self.canvas2 = Canvas(self.canva1, bg="#37C9E4", width=330, height=self.altura)
        self.canvas2.place(x=0, y=0)

        self.logo = PhotoImage(file="logo.png") 

        self.coord = self.largura/1.05
        self.canvas3.create_image(self.coord, 60, image=self.logo) 
      
    
        self.butao1 = Button(self.canvas2, text="Alugar",fg="white",bg="#0097B2", relief="raised", borderwidth=2, font=("Arial", 13), width=21, command = self.aluga)
        self.butao1.place(x=69, y=230)
        self.butao2 = Button(self.canvas2, text="Devolver", fg="white",bg="#0097B2", relief="raised", borderwidth=2, font=("Arial", 13),  width=21, command= self.devolve)
        self.butao2.place(x=69, y=310)
        self.butao3 = Button(self.canvas2, text="Meus Filmes", fg="white", bg="#0097B2", relief="raised", borderwidth=2, font=("Arial", 13),width=21, command= self.consulta)
        self.butao3.place(x=69, y= 400)
        self.butao3 = Button(self.canvas2, text="Pesquisar", fg="white", bg="#0097B2", relief="raised", borderwidth=2, font=("Arial", 13),width=21, command = self.pesquisa)
        self.butao3.place(x=69, y=480)
        # ... (cria outros botões)

        # Cria a entrada
        self.entrada = Entry(self.canva1, width=70, bg="#FCF6DB")
        self.entrada.place(x=420, y=170, height=37)  # Posiciona a entrada mais à esquerda
        self.entrada.insert(0,"Nome pessoal")

        self.entrada2 = Entry(self.canva1, width=70, bg="#FCF6DB")
        self.entrada2.place(x=420, y=220, height=37)  # Posiciona a entrada mais à esquerda
        self.entrada2.insert(0,"Nome do Filme desejado (Em inglês)")

        # Cria o label com dimensões e posição especificadas
        self.label_final = Label(self.canva1, text="", bg="#E2E2E2", font=("Arial"), width=153, height=35)
        self.label_final.place(x=420, y=350)  # Posiciona o Label no final da tela

        self.filmes_totais = imdb.IMDb()

        self.loterica = {}
        self.pagadores = {}

        self.con = sqlite3.connect('banco.db')
        self.sql = self.con.cursor()

        self.desserializando()
        self.janela.mainloop()

    def serializando(self):
        arq = open("dados da loterica.bin","wb")
        #pickle.dump(self.loterica,arq)
        #arq.close()
        self.con.commit()
        self.con.close()


    def desserializando(self):
        arq = open("dados da loterica.bin","rb")
        #self.loterica = pickle.load(arq)
        arq.close()
        self.sql.execute("SELECT * FROM pagadores")
        registros = self.sql.fetchall()
        cont = len(registros)
        cont2 = 0
        for reg in registros:
            self.pagadores.update({reg[1]:reg[2]})

    def pesquisa(self):
        self.label_final["text"] = ""
        self.busca = self.filmes_totais.search_movie(self.entrada2.get())
        cont = 0
        for i in self.busca:
            self.label_final["text"] += str(i) + "    |    "
            cont += 1
            if cont%3 == 0:
                self.label_final["text"] += "\n"
        

    def aluga(self):
        self.label_final["text"] = ""
        self.pesquisa()
        filme = self.busca[0]
        pessoa = self.entrada.get()
        if filme["title"] in self.loterica.keys():
            self.loterica.update({filme["title"] : (self.loterica.get(filme["title"])-1)})
        else: 
            self.loterica.update({filme["title"] : 3})
        if pessoa in self.pagadores.keys():
            lista = self.pagadores.get(pessoa)
            lista.append(filme["title"])
            self.pagadores.update({pessoa : lista})
            self.sql.execute(f"UPDATE pagadores SET filmes = {lista} WHERE nome = {pessoa}")
        else:
            lista = []
            lista.append(filme["title"])
            self.pagadores.update({pessoa : lista})
            self.sql.execute(f"INSERT INTO pagadores (nome,filmes) VALUES ({pessoa},{lista})")
        self.serializando()
    
    def devolve(self):
        self.label_final["text"] = ""
        filme = self.busca[0]
        pessoa = self.entrada.get()
        try:
            if filme["title"] in self.loterica.keys():
                self.loterica.update({filme["title"] : (self.loterica.get(filme["title"])+1)})
            else:
                raise Exception("Esse filme não existe")
        except Exception as error:
            self.label_final["text"] = error
        try:
            if pessoa in self.pagadores.keys():
                lista = self.pagadores.get(pessoa)
                lista.remove(filme["title"])
                self.pagadores.update({pessoa : lista})
                self.sql.execute(f"UPDATE pagadores SET filmes = {lista} WHERE nome = {pessoa}")
            else:
                raise Exception("O Senhor(a) não tem filmes à devolver")
        except Exception as error:
            self.label_final["text"] = error
        self.serializando()
    
    def consulta(self):
        self.label_final["text"] = ""
        filme = self.busca[0]
        pessoa = self.entrada.get()
        self.label_final["text"] = f"{self.loterica}"
        try:
            if pessoa in self.pagadores.keys():
                self.label_final["text"] = f"{self.pagadores[pessoa]}"
            else:
                raise Exception("O Senhor(a) não tem filmes à devolver")
        except Exception as error:
            self.label_final["text"] = error

App = Main()

        
        
        
        
