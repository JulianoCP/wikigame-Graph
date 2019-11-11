# Wiki-Game

## Arquivos

Cada arquivo .tsv contém uma certa quantidade de vértices e arestas de um grafo representado nele, por exemplo, o arquivo 1k.tsv contém 1000 arestas, 10k.tsv contém 10 mil e assim por diante.

O arquivo adjacencia.tsv contém o conjunto completo de vértices e arestas, sendo 4604 vértices e 119882.

[Site original onde os dados foram retirados, aqui](http://snap.stanford.edu/data/wikispeedia.html)


### Créditos para:
* Robert West and Jure Leskovec: [Human Wayfinding in Information Networks.](http://infolab.stanford.edu/~west1/pubs/West-Leskovec_WWW-12.pdf) 21st International World Wide Web Conference (WWW), 2012.
* Robert West, Joelle Pineau, and Doina Precup: [Wikispeedia: An Online Game for Inferring Semantic Distances between Concepts.](http://infolab.stanford.edu/~west1/pubs/West-Pineau-Precup_IJCAI-09.pdf) 21st International Joint Conference on Artificial Intelligence (IJCAI), 2009.


## Wiki-Game ##

O projeto é uma implemnetação de um Wiki-Game, um jogo solenamente consistente de navegação entre hiperlinks dentro de um artigo aleatório do Wikipedia(dentro de nosso dataset, tal artigo inicial seria um dos vértices), e a partir desse artigo inicial, deve-se chegar em uma quantidade definida de passos a um artigo alvo, tal artigo esse que também é definido aleartoriamente, o jogo será executado automaticamente, sem necessidade de intervenção humana.

Após a definição do artigo inicial e o alvo, é aplicado um algoritimo dentro desse grafo, algoritimo esse ainda a ser definido (provavelmente uma busca em largura ou distância entre dois pontos), e então é mostrada a distância entre esses dois pontos, e computado o tempo necessário tanto para carregar o grafo, quanto para executar o algoritimo, o tempo será utilizado na escrita de nosso artigo.
