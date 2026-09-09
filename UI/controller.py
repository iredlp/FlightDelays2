import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._choiceDDPartenza=None
        self._choiceDDArrivo=None

    def handleAnalizza(self, e):
        #self._view.txt_result.controls.append(ft.Text(f"Hello, !"))
        #self._view.update_page()
        cMinTxT=self._view._txtInCMin.value
        if cMinTxT==" ":
            self._view._txtResults.controls.clear()
            self._view._txtResults.controls.append(ft.Text("Per favore inserire un valore numerico per numero minimo compagnie", color="red"))
            return

        try:
            cMin=int(cMinTxT)
        except ValueError:
            self._view._txtResults.controls.clear()
            self._view._txtResults.controls.append(ft.Text("inserire un valore numerico per numero minimo compagnie", color="red"))
            self._view.update_page()
            return

        if cMin<=0:
            self._view._txtResults.controls.clear()
            self._view._txtResults.controls.append(
                ft.Text("Il filtro sul numero di compagnie deve essere un intero positivo", color="red"))
            self._view.update_page()
            return

        self._model.buildGraph(cMin)
        nNodes,nEdges=self._model.getGraphDetails()

        allNodes=self._model.getAllNodes()
        self.fillDropdown(allNodes)

        self._view._txtResults.controls.clear()
        self._view._txtResults.controls.append(
            ft.Text("GRafo correttamente creato!", color="green"))
        self._view._txtResults.controls.append(
            ft.Text(f" Il GRafo contiene {nNodes} nodi e {nEdges} archi!", color="green"))
        self._view.update_page()
        return

    def handleConnessi(self,e):
        if self._choiceDDPartenza is None:
            self._view._txtResults.controls.clear()
            self._view._txtResults.controls.append(ft.Text("Attenzione per usare questo metodo occorre selezionare un aeroporto di partenza"))
            self._view.update_page()
            return

        viciniT=self._model.getViciniOrdinati(self._choiceDDPartenza)
        #self._view._txtResults.controls.clear()
        for v in viciniT:
            self._view._txtResults.controls.append(ft.Text(f"{v[0]}-{v[1]}"))
        self._view.update_page()




    def handleTestConnessione(self, e):
        if self._choiceDDPartenza is None:
            self._view._txtResults.controls.clear()
            self._view._txtResults.controls.append(ft.Text("Attenzione per usare questo metodo occorre selezionare un aeroporto di partenza", color="red"))
            self._view.update_page()
            return

        if self._choiceDDArrivo is None:
            self._view._txtResults.controls.clear()
            self._view._txtResults.controls.append(
                ft.Text("Attenzione per usare questo metodo occorre selezionare un aeroporto di arrivo", color="red"))
            self._view.update_page()
            return

        if not self._model.hasPath(self._choiceDDPartenza, self._choiceDDArrivo):
            self._view._txtResults.controls.clear()
            self._view._txtResults.controls.append(
                ft.Text(f"Non ho trovato un cammino tra{self._choiceDDArrivo}-{self._choiceDDPartenza}",color="orange"))
            self._view.update_page()
            return
        self._view._txtResults.controls.clear()
        self._view._txtResults.controls.append(
            ft.Text(f"Ho trovato un cammino fra {self._choiceDDPartenza} - {self._choiceDDArrivo}!"
                    f" Di seguito i nodi che lo compongono:",color="green"))
        path=self._model.getPath(self._choiceDDPartenza, self._choiceDDArrivo)

        for v in path:
            self._view._txtResults.controls.append(ft.Text(f"{v}"))
        self._view.update_page()


    def handleCerca(self,e):
        pass

    def fillDropdown(self,allNodes):
        for n in allNodes:
            self._view._ddAeroportoP.options.append(
                ft.dropdown.Option(data=n, key=n.IATA_CODE, on_click=self.choiceDDPartenza))

            self._view._ddAeroportoA.options.append(
                ft.dropdown.Option(data=n, key=n.IATA_CODE, on_click=self.choiceDDArrivo))


        self._view.update_page()

    def choiceDDPartenza(self,e):
        self._choiceDDPartenza=e.control.data
        print(f"Hai selezionato come aereoporto di partenza {self._choiceDDPartenza}")

    def choiceDDArrivo(self,e):
        self._choiceDDArrivo = e.control.data
        print(f"Hai selezionato come aereoporto di arrivo {self._choiceDDArrivo}")
