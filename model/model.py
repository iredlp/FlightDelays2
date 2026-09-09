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

    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def getAllNodes(self):
        return list(self._graph.nodes)


