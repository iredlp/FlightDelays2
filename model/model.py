import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph=nx.Graph()
        self._airports=DAO.getAllAirports()
        self._idMapAirports={}
        for a in self._airports:
            self._idMapAirports[a.ID] = a

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


