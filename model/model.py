import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph=nx.Graph()
        self._airports=DAO.getAllAirports()
        self._idMapAirports={}
        for a in self._airports:
            self._idMapAirports[a.ID] = a
        self._bestCammino = []
        self._bestScore = 0

    def getCamminoOttimo(self, v0, v1,t):
        self._bestCammino=[]
        self._bestScore=0
        #soluzione parziale
        parziale=[v0]
        self._ricorsione(parziale,v1,t)
        return self._bestCammino, self._bestScore

    def _ricorsione(self, parziale, v1,t):
        #verifico se parziale è una soluzione valida ed in caso la salvo
        if parziale[-1]==v1: #potenzialmente questa è una soluz accettabile
            if self._getScore(parziale)>self._bestScore:
                #aggiorno le variabili di classe
                self._bestCammino = copy.deepcopy(parziale)
                self._bestScore = self._getScore(parziale)

        #verifico se ha senso continuare ad aggiungere elementi in parziale, oppure esco
        if len(parziale)==t+1: #allora parziale ha già raggiunto il num max di tratte e INTERROMPO
            return
        #espando parziale e faccio la ricorsione con backtracking
        for n in self._graph.neighbors(parziale[-1]):
            if n not in parziale:
                parziale.append(n)
                self._ricorsione(parziale, v1,t)
                parziale.pop()


    def _getScore(self, parziale):
        #deve sommare i pesi degli archi
        sumPesi=0
        for i in range(0,len(parziale)-1):
            sumPesi+=self._graph[parziale[i]][parziale[i+1]]['weight']
        return sumPesi

    def buildGraph(self, nMin):
        nodes=DAO.getAllNodes(nMin, self._idMapAirports)

        #AGGIUNGO I NODI AL GRAFICO
        self._graph.add_nodes_from(nodes)
        print(f"N nodi:{len(self._graph.nodes)} num archi: {len(self._graph.edges)}")
        self.addEdges()
        print(f"N nodi:{ len(self._graph.nodes)} num archi: {len(self._graph.edges)}")

        #svuoto gli archi
        self._graph.clear_edges()
        self.addEdgesV2()
        print(f"N nodi:{len(self._graph.nodes)} num archi: {len(self._graph.edges)}")

    def addEdges(self):
        allTratte=DAO.getAllEdgesV1(self._idMapAirports)
        #Queste tratte hann 2 problemi:
        #1) HO ARCHI DIRETTI E INVERSI E QUINDI DOVRò FARE LA SOMMA
        #2) HO ARCHI FRA AEROPORTI CHE HO FILTRATO

        #POSSO ciclare sulle tratte
        for t in allTratte:
            if t.aereoportoP in self._graph and t.aereoportoA in self._graph:
                #allora posso aggiungerlo
                if self._graph.has_edge(t.aereoportoP, t.aereoportoP): #se già presente
                    self._graph[t.aereoportoP][t.aereoportoP]["weight"]+=t.peso #incremento peso
                else:
                    self._graph.add_edge(t.aereoportoP, t.aereoportoA, weight=t.peso)

    def addEdgesV2(self):
        allTratte = DAO.getAllEdgesV1(self._idMapAirports)
        for t in allTratte:
            if t.aereoportoP in self._graph and t.aereoportoA in self._graph:
               self._graph.add_edge(t.aereoportoP, t.aereoportoA, weight=t.peso)
                #USANDO LA QUERY PIù LUNGA RISPARMIO UN IF

    def getViciniOrdinati(self,source):
        #Restituisce tutti i vicini si source, ordinati per peso dell'arco che collega source al vicino
        vicini= self._graph.neighbors(source)
        viciniT=[]
        for v in vicini:
            viciniT.append((v,self._graph[source][v]["weight"])) #nodo di partenza | nodo di arrivo |peso

        viciniT.sort(key=lambda x:x[1], reverse=True) #ordino andando a guardare il secondo elemento= quello in posizione 1
        #REVERSE TRUE le stamoa in senso decrescente
        return viciniT

    def hasPath(self, v0, v1):
        #Restituisce true se un qualche cammino esiste, altrimenti restisuisce False
        return v1 in nx.node_connected_component( self._graph,v0)

    def getPath(self, v0, v1):
       #1)
        #dictOfPredecessors=dict(nx.bfs_predecessors(self._graph,v0) )#passo il grafo e nodo di partenza
        #path=[v1] #un percorso tra vo e v1
        #while path[0] !=v0:
         #   path.insert( dictOfPredecessors[path[0]])
        #2)
        #POTEVO USARE ANCHE dfs - ma avrei avuto un cammimo più lungo
        #dictOfPredecessors = dict(nx.dfs_predecessors(self._graph, v0))  # passo il grafo e nodo di partenza
        #path = [v1]  # un percorso tra vo e v1
       # while path[0] != v0:
         #   path.insert(dictOfPredecessors[path[0]])

        #3)
        #path=nx.shortest_path(v0, v1)

        #4)
        path=nx.dijkstra_path(self._graph,v0,v1, weight=None)
       # 5)
        #path = nx.dijkstra_path(self._graph, v0, v1) #così avro cammini più lunghi
        return path



    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def getAllNodes(self):
        nodes= list(self._graph.nodes)
        nodes.sort(key=lambda x:x.IATA_CODE)
        return nodes


