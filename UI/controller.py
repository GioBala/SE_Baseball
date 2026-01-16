import flet as ft
from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def handle_crea_grafo(self, e):
        """ Handler per gestire creazione del grafo """""
        # TODO
        self._model.crea_grafo()

    def handle_dettagli(self, e):
        """ Handler per gestire i dettagli """""
        # TODO
        try:
            team=int(self._view.dd_squadra.value)
            vicini=self._model.get_vicini(team)
            self._view.txt_risultato.controls.clear()
            self._view.txt_risultato.controls.append(ft.Text(f"{vicini}"))
            self._view.update()
        except Exception:
            self._view.show_alert("Inserisci una squadra")


    def handle_percorso(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del percorso """""
        # TODO
        try:
            team = int(self._view.dd_squadra.value)
            per= self._model.percorso(team)
            self._view.txt_risultato.controls.clear()
            self._view.txt_risultato.controls.append(ft.Text(f"{per}"))
            self._view.update()
        except Exception:
            self._view.show_alert("Inserisci una squadra")

    """ Altri possibili metodi per gestire di dd_anno """""
    # TODO
    def anni(self):
         return self._model.get_anni()

    def aggiorna_dd(self,e):
        anno=self._view.dd_anno.value
        team=self._model.riempi_lista(int(anno))
        self._view.txt_out_squadre.controls.clear()
        self._view.txt_out_squadre.controls.append(ft.Text(f"Numero di squadre: {len(team)}"))
        if len(team)==0:
            self._view.show_alert("Nessuna squadra trovata")
            self._view.dd_squadra.options=[ft.dropdown.Option("Nessuna")]
        else:
            for i in  team:
                #print(i)
                self._view.txt_out_squadre.controls.append(ft.Text(i))

            self._view.dd_squadra.options.clear()
            self._view.dd_squadra.options=[ft.dropdown.Option(key=i.id, text=i) for i in team]

            self._view.update()
