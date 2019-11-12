
# Para ler aquivos TSV, CSV (tudo a mesma coisa, só muda se é separado por tab ou ; , etc)
# O nome é csv pois o separado por , (comma) é o mais comum (padrão excel, por assim dizer)
import csv
# Para dar parse já que a linha é codificada em url (quando tem algum caractere especial
# tipo em Zürich, vai estar codificado como Z%C3%BCrich)
import urllib.parse
import time

cont = 0


class Vtx:
    def __init__(self, valor):
        self.valor = valor
        self.adj = list()
        self.incd = list()
        self.grau_entry = 0
        global cont
        self.numero = cont
        cont = cont + 1

    def listadj(self):
        for i in self.adj:
            print(' - ', i.valor, end="")
        print()


class Aresta:
    def __init__(self, vtx, vtx2):
        self.origem = vtx
        self.destino = vtx2


class Grafo:
    def __init__(self):
        self.arrayNome = list()
        self.newvtx = list()
        self.arrst = list()
        self.tempo = 0

    def add_in_nome(self,nome):
        self.arrayNome.append(nome)
    
    def printGrafo(self):
        for i in self.newvtx:
            print(i.valor)

    def addvtx(self, vtx):
        self.newvtx.append(vtx)

    def createAresta(self, vtx1, vtx2):
        self.arrst.append(Aresta(vtx1, vtx2))
        vtx1.adj.append(vtx2)
        vtx2.incd.append(vtx1)
        vtx2.grau_entry += 1
      

    def printAdj(self):
        for i in self.newvtx:
            print("Saindo de [%s]->" % i.valor, end="")
            for j in i.adj:
                print(" [%s]" % j.valor, end="")
            print()
            print()

    def printIncd(self):
        for i in self.newvtx:
            print("chegando em [%s]->" % i.valor, end="")
            for j in i.incd:
                print(" [%s]" % j.valor, end="")
            print()

    def printAresta(self):
        for i in self.arrst:
            print('de', i.origem.valor, 'para', i.destino.valor)

    def buscalarg(self, start,end):
        s = start
        queue = list()
        pai = [None] * len(self.newvtx)
        cor = [None] * len(self.newvtx)
        distancia = [None] * len(self.newvtx)

        for i in self.newvtx:
            if i != s:
                cor[i.numero] = "branco"
                distancia[i.numero] = None
                pai[i.numero] = None

        cor[s.numero] = "cinza"
        distancia[s.numero] = 0
        pai[s.numero] = None
        queue.append(s)

        while len(queue):
            j = queue.pop()
            for i in j.adj:
                if cor[i.numero] == "branco":
                    cor[i.numero] = "cinza"
                    distancia[i.numero] = distancia[j.numero] + 1
                    pai[i.numero] = j.valor
                    queue.append(i)
                cor[j.numero] = "preto"

        return distancia[end.numero]


def calculaDistancia(origem,destino,grafo):
    n1,n2 = None,None
    for i,j in zip(grafo.arrayNome, grafo.newvtx):
        if i == origem:
            n1 = j
        if i == destino:
            n2 = j
    print('a busca entre {} e {} tem distancia {}'.format(origem,destino,grafo.buscalarg(n1,n2)))

if __name__ == "__main__":
    grafo = Grafo()

    # Plano de acão:
    # Ler diretamente de adjacencia já que tem o ponto de partida e o de chegada
    # Guarda o nome do vertice, caso for diferente do anterior (começa em nulo)...
    # ...cria um vértice novo, e então checa se o ponto de chegada já existe...
    # ...se não existe, é criado um novo ponto de chegada e colocado na lista
    #
    #
    # PROBLEMAS:
    # Poderia ser um pouco mais rápido, porém tá daora por enquanto
    #
    #
    # Solução:
    # Threads
    # Computador mais rápido
    # Rezar?
    #

    start_time = time.time()

    with open('1k.tsv', encoding='ascii') as arquivo:
        leitor = csv.reader(arquivo)
        vertice = ""
        contador =0
        partida = None
        chegada = None 
        for linha in leitor:
            v1 = urllib.parse.unquote(linha[0].split()[0])
            if v1 not in grafo.arrayNome:
                partida = Vtx(v1)
                grafo.add_in_nome(v1)
                grafo.addvtx(partida)
            else:
                for i,j in zip(grafo.arrayNome, grafo.newvtx):
                    if i == v1:
                        partida = j

            v2 = urllib.parse.unquote(linha[0].split()[1])
            if v2 not in grafo.arrayNome:
                chegada = Vtx(v2)
                grafo.addvtx(chegada)
                grafo.add_in_nome(v2)
            else:
                for i,j in zip(grafo.arrayNome, grafo.newvtx):
                    if i == v2:
                        chegada = j
          
            if type(chegada) is Vtx and type(partida) is Vtx:
                grafo.createAresta(partida,chegada)

    grafo.printGrafo()
    grafo.printAdj()
    calculaDistancia('Áedán_mac_Gabráin','kkk',grafo)
