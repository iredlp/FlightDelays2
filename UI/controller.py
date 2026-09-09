import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._choicePartenza=None
        self._choiceArrivo=None

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
        self._fillDropdown(allNodes)

        self._view._txtResults.controls.clear()
        self._view._txtResults.controls.append(
            ft.Text("GRafo correttamente creato!", color="green"))
        self._view._txtResults.controls.append(
            ft.Text(f" Il GRafo contiene {nNodes} nodi e {nEdges} archi!", color="green"))
        self._view.update_page()
        return




    def handleConnessi(self,e):
        pass

    def handleCerca(self,e):
        pass

    def fillDropdown(self,allNodes):
        for n in allNodes:
            self._view._ddAeroportoP.options.append(
                ft.dropdown.Option(data=n, key=n.IATA_CODE, on_click=self._choiceDDPartenza))

            self._view._ddAeroportoA.options.append(
                ft.dropdown.Option(data=n, key=n.IATA_CODE, on_click=self._choiceDDArrivo))

    def choiceDDPartenza(self,e):
        self._choicePartenza=e.control.data
        print(f"Hai selezionato come aereoporto di partenza {self._choicePartenza}")

    def choiceDDArrivo(self,e):
        self._choiceArrivo = e.control.data
        print(f"Hai selezionato come aereoporto di arrivo {self._choiceArrivo}")
