
# Para ler aquivos TSV, CSV (tudo a mesma coisa, só muda se é separado por tab ou ; , etc)
# O nome é csv pois o separado por , (comma) é o mais comum (padrão excel, por assim dizer)
import csv
# Para dar parse já que a linha é codificada em url (quando tem algum caractere especial
# tipo em Zürich, vai estar codificado como Z%C3%BCrich)
import urllib.parse
import time
import random

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

    def add_in_name(self, nome):
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

    def buscalarg(self, start, end):
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

    def calculaDistancia(self, origem, destino):
        v1, v2 = None, None
        for i, j in zip(self.arrayNome, self.newvtx):
            if i == origem:
                v1 = j
            elif i == destino:
                v2 = j
        if v1 != None and v2 != None:
            start_time = time.time()
            distancia = self.buscalarg(v1, v2)
            if distancia != None:
                print('\nA busca entre {} e {} tem distancia {}'.format(
                    origem, destino, self.buscalarg(v1, v2)))
            else:
                print('\nO vertice {} não alcança o vertice {}'.format(
                    origem, destino))
            print("--- {} Segundos para executar a busca ---".format(time.time() - start_time))
        else:
            print('Erro: Vertices invalidos')

    def wikiVertices(self):
        arq = open('VerticeNome.txt', 'w')
        for i in self.arrayNome:
            arq.write(i+'\n')
        arq.close()

    def wikiAdj(self):
        arq = open('VerticeAdjacencia.txt', 'w')
        for i in self.newvtx:
            if len(i.adj) > 0:
                arq.write("Saindo de [%s]->" % i.valor)
                for j in i.adj:
                    arq.write(" [%s]" % j.valor)
                arq.write('\n')
        arq.close()
    
    def populate(self,arquivo):
        print('\nAguarde, estamos computando os vertices e arestas')
        start_time = time.time()
        with open(arquivo+'.tsv', encoding='ascii') as arquivo:
            leitor = csv.reader(arquivo)
            partida = None
            chegada = None
            for linha in leitor:
                v1 = urllib.parse.unquote(linha[0].split()[0])
                if v1 not in self.arrayNome:
                    partida = Vtx(v1)
                    self.add_in_name(v1)
                    self.addvtx(partida)
                else:
                    partida = self.newvtx[self.arrayNome.index(v1)]
    
                v2 = urllib.parse.unquote(linha[0].split()[1])
                if v2 not in self.arrayNome:
                    chegada = Vtx(v2)
                    self.addvtx(chegada)
                    self.add_in_name(v2)
                else:
                    chegada = self.newvtx[self.arrayNome.index(v2)]
    
                if type(chegada) is Vtx and type(partida) is Vtx:
                    self.createAresta(partida, chegada)
                    
        print("--- {} Segundos para carregar o grafo ---".format(time.time() - start_time))

dictTsv = {
    0: ['1k','1k'],
    1: ['10k','10k'],
    2: ['20k','20k'],
    3: ['30k','30k'],
    4: ['40k','40k'],
    5: ['50k','50k'],
    6: ['120k','adjacencia']
}

def selectFile():
    print('Selecione um dos arquivos para ser usado como grafo:\n')
    for i in range(0, len(dictTsv)):
        print('Opção {}: {} linhas de ligações'.format(i,dictTsv[i][0]))
    print('\nOpção desejada: ', end='')
    selecionado = int(input())
    return dictTsv[selecionado][1]
    

if __name__ == "__main__":
    arquivo = selectFile()    

    grafo = Grafo()
    grafo.populate(arquivo)
    grafo.wikiAdj()
    grafo.wikiVertices()
    print('\nOs nomes do vertices existentes estão disponiveis em {} e as arestas existentes estão em {}'.format('VerticeNome.txt', 'VerticeAdjacencia.txt'))
    
    option = 1

    while(option != 0):
        print('\nDigite 2 para vértices aleatórios, 1 para inserir nomes de vertices ou 0 para sair: ', end='')
        option = int(input())
        if option == 1:
            print('\nDigite o vertice de origem: ', end='')
            origem = input()
            print('Digite o vertice de destino: ', end='')
            destino = input()
            grafo.calculaDistancia(origem, destino)
        elif option == 2:
            origem = random.choice(grafo.newvtx)
            destino = random.choice(grafo.newvtx)
            grafo.calculaDistancia(origem.valor, destino.valor)
