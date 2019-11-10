
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

    def buscalarg(self, start):
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

        print("as cores", cor)
        print("as distancias", distancia)
        print('os pais', pai)
        print('fila atual', queue)

    def Dfs_Visit(self, start, cor, predecessor, f, d, pilha):

        self.tempo = self.tempo + 1
        d[start.numero] = self.tempo
        cor[start.numero] = "cinza"

        print("[", start.valor, ' ', end="")

        for i in start.adj:
            if cor[i.numero] == "branco":
                predecessor[i.numero] = start.valor
                self.Dfs_Visit(i, cor, predecessor, f, d, pilha)
        print(start.valor, "] ", end="")

        cor[start.numero] = "preto"
        self.tempo = self.tempo + 1
        f[start.numero] = self.tempo
        pilha.insert(0, start)

    def Dfs(self):
        f = [None] * len(self.newvtx)
        d = [None] * len(self.newvtx)
        cor = [None] * len(self.newvtx)
        predecessor = [None] * len(self.newvtx)
        pilha = list()
        for i in self.newvtx:
            cor[i.numero] = "branco"
            predecessor[i.numero] = None

        for i in self.newvtx:
            if cor[i.numero] == "branco":
                self.Dfs_Visit(i, cor, predecessor, f, d, pilha)

        print()
        print("momento descoberta", d)
        print("momento finalizacao", f)
        print("as cores", cor)
        print("papai", predecessor)
        self.tempo = 0
        return pilha

    def Dfs_Visit2(self, start, cor, predecessor, f, d, pilha, componente):

        self.tempo = self.tempo + 1
        d[start.numero] = self.tempo
        cor[start.numero] = "cinza"
        # print("[",start.valor,' ' , end="")

        if start.valor not in componente:
            componente.append(start.valor)

        for i in start.incd:
            if cor[i.numero] == "branco":
                if i not in componente:
                    componente.append(i.valor)
                predecessor[i.numero] = start.valor
                self.Dfs_Visit2(i, cor, predecessor, f, d, pilha, componente)
        # print(start.valor,"] " , end="")

        cor[start.numero] = "preto"
        self.tempo = self.tempo + 1
        f[start.numero] = self.tempo
        pilha.append(start)
        return componente.copy()

    def Dfs2(self, sequencia):
        f = [None] * len(self.newvtx)
        d = [None] * len(self.newvtx)
        cor = [None] * len(self.newvtx)
        predecessor = [None] * len(self.newvtx)
        pilha = list()
        for i in self.newvtx:
            cor[i.numero] = "branco"
            predecessor[i.numero] = None

        qntcomp = list()
        componente = list()

        for i in sequencia:
            if cor[i.numero] == "branco":
                qntcomp.append(self.Dfs_Visit2(
                    i, cor, predecessor, f, d, pilha, componente))
                componente.clear()

        print('\nvolta na transposta')
        print("momento descoberta", d)
        print("momento finalizacao", f)
        print("as cores", cor)
        print("papai", predecessor)
        print('componentes', qntcomp)

    def kahn(self):
        visitados = 0
        Qentrada = list()
        ordemSaida = list()
        for i in self.newvtx:
            if i.grau_entry == 0:
                Qentrada.append(i)
        while len(Qentrada):
            vert = Qentrada.pop(0)
            ordemSaida.append(vert.valor)
            visitados += 1
            for j in vert.adj:
                j.grau_entry -= 1
                if j.grau_entry == 0:
                    Qentrada.append(j)
        if visitados != len(self.newvtx):
            print('nao eh possivel')
        print('ordem', ordemSaida)

    def printgrau(self):
        for i in self.newvtx:
            print(i.grau_entry)

    def criaMatriz(self):
        matr = [[0 for i in range(len(self.newvtx))]
                for j in range(len(self.newvtx))]
        for i in self.arrst:
            matr[i.origem.numero][i.destino.numero] = 1

        for i in matr:
            for j in i:
                print(j, end=" ")
            print()
        print('\ntransposta')
        for i in range(len(matr)):
            for j in range(len(matr)):
                print(matr[j][i], end=" ")
            print()

    def kosajaru(self):
        print('grafo normal')
        self.Dfs2(self.Dfs())


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

    with open('30k.tsv', encoding='ascii') as arquivo:
        leitor = csv.reader(arquivo)
        vertice = ""
        for linha in leitor:
            if vertice != urllib.parse.unquote(linha[0].split()[0]):
                partida = Vtx(urllib.parse.unquote(linha[0].split()[0]))
                grafo.addvtx(partida)
                vertice = urllib.parse.unquote(linha[0].split()[0])

            vChegada = urllib.parse.unquote(linha[0].split()[1])
            for item in grafo.newvtx:
                if vChegada == item.valor:
                    chegada = item
                    grafo.createAresta(partida, chegada)
            try:
                chegada
            except NameError:
                chegada = Vtx(vChegada)
                grafo.addvtx(chegada)
                grafo.createAresta(partida, chegada)

    print('\n', "{0:#^50}".format(' mostrando grafo '))
    grafo.printGrafo()
    print('\n', "{0:#^50}".format(' lista adjacencia '))
    grafo.printAdj()

    print("--- %s Segundos ---" % (time.time() - start_time))

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
