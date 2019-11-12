
# Para ler aquivos TSV, CSV (tudo a mesma coisa, só muda se é separado por tab ou ; , etc)
# O nome é csv pois o separado por , (comma) é o mais comum (padrão excel, por assim dizer)
import csv
# Para dar parse já que a linha é codificada em url (quando tem algum caractere especial
# tipo em Zürich, vai estar codificado como Z%C3%BCrich)
import urllib.parse
import time

global cont
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
        self.newvtx = list()
        self.arrst = list()
        self.tempo = 0

    def printGrafo(self):
        for i in self.newvtx:
            print(i.valor)

    def addvtx(self, vtx):
        self.newvtx.append(vtx)

    def createAresta(self, vtx1, vtx2):
        '''comentarios para transformar em orientado'''
        self.arrst.append(Aresta(vtx1, vtx2))
        vtx1.adj.append(vtx2)
        vtx2.incd.append(vtx1)
        vtx2.grau_entry += 1
        # self.arrst.append(Aresta(vtx2,vtx1))
        # vtx2.adj.append(vtx1)
        # vtx1.incd.append(vtx2)

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
                if i == end:
                    return distancia[start.numero]
                if cor[i.numero] == "branco":
                    cor[i.numero] = "cinza"
                    distancia[i.numero] = distancia[j.numero] + 1
                    pai[i.numero] = j.valor
                    queue.append(i)
                cor[j.numero] = "preto"

        # print("as cores", cor)
        print("as distancias", distancia)
        # print('os pais', pai)
        # print('fila atual', queue)


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
    # Poderia ser um pouco mais rápido, porém ~34 segundos para...
    # ...4,604 vértices e 119,882 arestas parece razoável
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
        for linha in leitor:
            if vertice != urllib.parse.unquote(linha[0].split()[0]):
                partida = Vtx(urllib.parse.unquote(linha[0].split()[0]))
                # print('partida',partida.valor)
                grafo.addvtx(partida)
                vertice = urllib.parse.unquote(linha[0].split()[0])

            chegada = Vtx(urllib.parse.unquote(linha[0].split()[1]))
            # print(grafo.newvtx)
            #print('criando rota',vertice,vChegada)
            if chegada not in grafo.newvtx:
                grafo.addvtx(chegada)
            else:
                del chegada
            
            grafo.createAresta(partida,chegada)

    grafo.printGrafo()
    grafo.printAdj()
    print(grafo.buscalarg(grafo.newvtx[0],grafo.newvtx[1]))
    #print('\n', "{0:#^50}".format(' mostrando grafo '))
    #print('\n', "{0:#^50}".format(' lista adjacencia '))
    #grafo.printAdj()
    #print('tamanho->',len(grafo.newvtx))
    #print("--- %s Segundos ---" % (time.time() - start_time))

    # Coisas antigas
    # print('\n', "{0:#^50}".format(' Busca Largura '))
    # x.buscalarg(a)
    # print('\n', "{0:#^50}".format(' DFS '))
    # x.Dfs()
    # print('\n', "{0:#^50}".format(' lista incidencia '))
    # x.printIncd()
    # print('\n', "{0:#^50}".format(' arestas '))
    # x.printAresta()
    # print('\n', "{0:#^50}".format(' kahn '))
    # x.kahn()
    # print('\n', "{0:#^50}".format(' matriz adjacencia '))
    # x.criaMatriz()
    # print('\n', "{0:#^50}".format(' Kosajaru '))
    # x.kosajaru()
