""" definirea problemei """

import copy
import time
# configurația inițială

config_initiala = [[4, 0, 3], [2, 1, 5], [7, 8, 6]]

# configurația scop
config_scop = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]


# determinarea pozitiilor pieselor pe tabla
def pozitii_8_puzzle(puzzle):
    pozitii_piese = {}
    for i, linie in enumerate(puzzle):
        for j, piesa in enumerate(linie):
            pozitii_piese[piesa] = (i, j)
    return pozitii_piese


# pozitiile pieselor pe tabla finala
pozitii_config_finala = pozitii_8_puzzle(config_scop)


class Nod:
    # distanta manhattan intre pozitia placutei si pozitia ei din scop
    def euristica_1(self, puzzle):
        pozitii_config_curenta = pozitii_8_puzzle(puzzle)
        count = 0
        for piesa in range(len(puzzle) * len(puzzle)):
            if piesa == 0:
                continue
            if pozitii_config_curenta[piesa] == pozitii_config_finala[piesa]:
                count += abs(pozitii_config_curenta[piesa][0] - pozitii_config_finala[piesa][0]) + abs(
                    pozitii_config_curenta[piesa][1] - pozitii_config_finala[piesa][1])
        return count

    # numarul de placute care nu se afla pe pozitia corect in scop
    def euristica_2(self, puzzle):
        count = 0
        pozitii_config_curenta = pozitii_8_puzzle(puzzle)

        for piesa in range(len(puzzle) * len(puzzle)):
            if piesa == 0:
                continue
            if pozitii_config_curenta[piesa] != pozitii_config_finala[piesa]:
                count += 1
        return count

    def __init__(self, puzzle):
        self.info = puzzle

        # aici schimbam tipul de euristica

        self.h = self.euristica_2(puzzle)

    def __str__(self):
        return "({}, h={})".format(self.info, self.h)

    def __repr__(self):
        return f"({self.info}, h={self.h})"


class Arc:
    def __init__(self, capat, varf):
        self.capat = capat  # de unde pleaca muchia
        self.varf = varf  # unde ajunge muchia
        self.cost = 1  # costul g al muchiei este 1


class Problema:
    def __init__(self):
        self.noduri = [Nod(config_initiala)]
        self.arce = []
        self.nod_start = self.noduri[0]  # de tip Nod
        self.nod_scop = config_scop  # doar info (fara h)

    def cauta_nod_nume(self, info):
        """Stiind doar informatia "info" a unui nod,
        trebuie sa returnati fie obiectul de tip Nod care are acea informatie,
        fie None, daca nu exista niciun nod cu acea informatie."""
        for nod in self.noduri:
            if nod.info == info:
                return nod

        return None


""" Sfarsit definire problema """

""" Clase folosite in algoritmul A* """


class NodParcurgere:
    """O clasa care cuprinde informatiile asociate unui nod din listele open/closed
        Cuprinde o referinta catre nodul in sine (din graf)
        dar are ca proprietati si valorile specifice algoritmului A* (f si g).
        Se presupune ca h este proprietate a nodului din graf
    """

    problema = None  # atribut al clasei (se suprascrie jos in __main__)

    def __init__(self, nod_graf, parinte=None, g=0, f=None):
        self.nod_graf = nod_graf  # obiect de tip Nod
        self.parinte = parinte  # obiect de tip NodParcurgere
        self.g = g  # costul drumului de la radacina pana la nodul curent
        if f is None:
            self.f = self.g + self.nod_graf.h
        else:
            self.f = f

    def drum_arbore(self):
        """
            Functie care calculeaza drumul asociat unui nod din arborele de cautare.
            Functia merge din parinte in parinte pana ajunge la radacina
        """
        nod_c = self
        drum = [nod_c]
        while nod_c.parinte is not None:
            drum = [nod_c.parinte] + drum
            nod_c = nod_c.parinte
        return drum

    def contine_in_drum(self, nod):
        """
            Functie care verifica daca nodul "nod" se afla in drumul dintre radacina si nodul curent (self).
            Verificarea se face mergand din parinte in parinte pana la radacina
            Se compara doar informatiile nodurilor (proprietatea info)
            Returnati True sau False.

            "nod" este obiect de tip Nod (are atributul "nod.info")
            "self" este obiect de tip NodParcurgere (are "self.nod_graf.info")
        """
        nod_curent = self
        while nod_curent is not None:
            if nod_curent.nod_graf.info == nod.info:
                return True
            nod_curent = nod_curent.parinte
        return False

    # se modifica in functie de problema
    def expandeaza(self):
        """Pentru nodul curent (self) parinte, trebuie sa gasiti toti succesorii (fiii)
        si sa returnati o lista de tupluri (nod_fiu, cost_muchie_tata_fiu),
        sau lista vida, daca nu exista niciunul.
        (Fiecare tuplu contine un obiect de tip Nod si un numar.)
        """
        puzzle = self.nod_graf.info
        fiii = []

        # cautam piesa cu valoarea 0 si facem toate cele 4 mutari posibile

        for i, linie in enumerate(puzzle):
            for j, piesa in enumerate(linie):
                if piesa == 0:
                    for (rand, col) in [[-1, 0], [0, -1], [1, 0], [0, 1]]:
                        # verificam sa nu iesm din suprafata puzzelului
                        if (i + rand) < 0 or (i + rand) >= len(puzzle) or (j + col) < 0 or (j + col) >= len(puzzle):
                            continue

                        copie_puzzle = copy.deepcopy(self.nod_graf.info)
                        # mutam piesa cu valoarea 0
                        copie_puzzle[i][j] = copie_puzzle[i + rand][j + col]
                        copie_puzzle[i + rand][j + col] = 0
                        # adaugam nodul

                        nod_nou = Nod(copie_puzzle)
                        problema.noduri.append(nod_nou)
                        fiu = nod_nou

                        cost = 1  # toate mutarile au costul 1
                        fiii.append((fiu, cost))
        return fiii

    # se modifica in functie de problema
    def test_scop(self):
        return self.nod_graf.info == self.problema.nod_scop

    def __str__(self):
        parinte = self.parinte if self.parinte is None else self.parinte.nod_graf.info
        return f"({self.nod_graf}, parinte={parinte}, f={self.f}, g={self.g})"


""" Algoritmul A* """


def str_info_noduri(l):
    """
        o functie folosita strict in afisari - poate fi modificata in functie de problema
    """
    pas=0
    sir = "\n"
    for x in l:
        sir += "\nPas " + str(pas) + ":\n"
        pas +=1
        sir += str(x.nod_graf.info[0]) + "  \n" + str(x.nod_graf.info[1]) + "  \n"+str(x.nod_graf.info[2]) + "  \n"
        sir += "\n"

    return sir


def afis_succesori_cost(l):
    """
        o functie folosita strict in afisari - poate fi modificata in functie de problema
    """
    sir = ""
    for (x, cost) in l:
        sir += "\nnod: " + str(x) + ", cost arc:" + str(cost)

    return sir


def in_lista(l, nod):
    """
    lista "l" contine obiecte de tip NodParcurgere
    "nod" este de tip Nod
    """
    for i in range(len(l)):
        if l[i].nod_graf.info == nod.info:
            return l[i]
    return None


def a_star():
    rad_arbore = NodParcurgere(NodParcurgere.problema.nod_start)
    open = [rad_arbore]  # open va contine elemente de tip NodParcurgere
    closed = []  # closed va contine elemente de tip NodParcurgere

    while open:  # cat timp open nu e vida

        nod_curent = open.pop(0)  # extragem primul nod din open si il punem in variabila nod_curent

        closed.append(nod_curent)  # adaugam nodul curent in closed

        if nod_curent.test_scop():  # daca nod_curent indeplineste conditia scop:
            break  # oprim cautarea

        expandare = nod_curent.expandeaza()  # expandez nod_curent
        for (succesor, cost) in expandare:
            nod_nou = None

            if nod_curent.contine_in_drum(succesor):  # daca succesor nu apartine drumului lui nod_curent
                continue

            node_in_open = in_lista(open, succesor)
            node_in_closed = in_lista(closed, succesor)

            if node_in_open:  # daca succesor e in open

                if node_in_open.g > nod_curent.g + cost + succesor.h:  # daca f-ul nodului din open e mai mare decat f-ul gasit pentru succesor
                    open.remove(node_in_open)  # scoatem nodul din open

            elif node_in_closed:  # daca succesor e in closed
                if node_in_closed.f > nod_curent.g + cost + succesor.h:  # daca f-ul nodului din closed e mai mare decat f-ul gasit pentru succesor
                    closed.remove(node_in_closed)  # scoatem nodul din closed

            # seteam pentru succesor parintele, g-ul si f-ul si il adaugam in open
            nod_nou = NodParcurgere(succesor, nod_curent, nod_curent.g + cost, nod_curent.g + cost + succesor.h)
            open.append(nod_nou)

        # sortam crescator dupa f, apoi descrescator dupa g
        open.sort(key=lambda x: (x.f, -x.g))

    print("\n------------------ Concluzie -----------------------")
    if (len(open) == 0):
        print("Lista open e vida, nu avem drum de la nodul start la nodul scop")
    else:
        print("Drum de cost minim: " + str_info_noduri(nod_curent.drum_arbore()))


if __name__ == "__main__":
    problema = Problema()
    NodParcurgere.problema = problema
    a_star()
