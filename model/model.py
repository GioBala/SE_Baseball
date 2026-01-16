import copy

import networkx as nx
from database.dao import DAO


class Model:
    def __init__(self):
        self.G=nx.Graph()
        self.teams={}
        self.nodi=[]
        self.percorso_migliore=[]
        self.peso_massimo=0

    def get_anni(self):
        #print(DAO.get_anni())
        return DAO.get_anni()

    def get_teams(self):
        self.teams={}
        teams=DAO.get_teams()
        for team in teams:
            self.teams[team.id]=team
        #print(self.teams)

    def riempi_lista(self,anno):
        self.nodi=DAO.get_team_by_year(anno)
        self.get_teams()
        #print(self.nodi)
        return self.nodi

    def crea_grafo(self):
        self.G=nx.Graph()
        for i in self.nodi:
            for j in self.nodi:
                if i!=j and (i,j) not in list(self.G.edges):
                    self.G.add_edge(i,j,weight=i.salario+j.salario)
        #print(list(self.G.edges))
        print(self.G)
        print("Grafo creato")

    def get_vicini(self,team):
        n=list(self.G.neighbors(self.teams[team]))
        s=""
        for i in sorted(n,key=lambda x:x.salario,reverse=True):
            p=self.G.get_edge_data(i,self.teams[team],"weight")
            peso=p["weight"]
            s=s+f"{i} - peso: {peso}\n"
        return s

    def percorso(self,id):
        self.percorso_migliore=[]
        self.peso_massimo=0
        team=self.teams[id]
        percorso=[]
        percorso.append(team)
        peso=team.salario
        h0=list(self.G.neighbors(team))
        h1=max(h0,key=lambda x:x.salario)
        p=self.G.get_edge_data(team,h1,"weight")
        peso=p["weight"]
        #pesi=[]
        #pesi.append(peso)
        self.ricorsione(h1,percorso,peso)
        #print("...")
        s=""
        for i in range(len(self.percorso_migliore)-1):
            p=self.G.get_edge_data(self.percorso_migliore[i+1],self.percorso_migliore[i],"weight")
            peso=p["weight"]
            s=s+f"{self.percorso_migliore[i]} --> {self.percorso_migliore[i+1]} (peso: {peso})\n"
        s=s+f"Peso totale: {self.peso_massimo}"
        return s

    def ricorsione(self,team,percorso,peso):
        print("...")
        n=sorted(list(self.G.neighbors(team)),key=lambda x:x.salario,reverse=True)
        if team not in percorso:
            percorso.append(team)
        if self.peso_massimo<peso:
            self.peso_massimo=peso
            self.percorso_migliore=copy.deepcopy(percorso)
        k=0
        #print(percorso(-2))
        for i in n:
            p1=self.G.get_edge_data(percorso[-2],team,"weight")
            pe1=p1["weight"]
            p2=self.G.get_edge_data(team,i,"weight")
            pe2=p2["weight"]
            if i not in percorso and pe2<pe1:
                self.ricorsione(i,percorso,peso=peso+pe2)
                percorso.pop()
                k = k + 1
            if k==3:
                return