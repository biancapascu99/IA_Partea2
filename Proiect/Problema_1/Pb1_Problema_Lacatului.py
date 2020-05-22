""" definirea problemei """
"""Problema blocurilor"""

import time

euristica = 1


# numar de incuietori
# N = 2

# config_initiala = [('i',1),('d',0)]
#
# config_scop= [('i',2),('d',0)]
# N=7
# config_initiala = [('i',1),('i',1),('i',1),('i',1),('i',1),('i',1),('i',1)]
# config_scop = [('d',0),('d',0),('d',0),('d',0),('d',0),('d',0),('d',0)]
# # # config_scop = [('d',0),('d',0),('d',0),('d',0),('d',0),('d',0),('d',0)]
# # # config_initiala = [('i',3),('i',4),('i',2),('i',1),('d',0),('d',0),('d',0)]
# chei = ["ddddgii","dddddid","didddii","dddgiig","dgggiid","didiigg","gigddgg","gdggggg","gggiggd","dgggddg"]

def citire(fisier):
    f = open(fisier, 'r')
    N = int(f.readline())
    conf_initiala = []
    conf_scop = []
    for i in range(N):
        stare = []
        linie = f.readline()
        linie_split = linie.split()
        stare = (str(linie_split[0]), int(linie_split[1]))
        # stare.append(str(linie_split[0]))
        # stare.append(int(linie_split[1]))
        conf_initiala.append(stare)

    for i in range(N):
        stare = []
        linie = f.readline()
        linie_split = linie.split()
        stare = (str(linie_split[0]), int(linie_split[1]))
        # stare.append(str(linie_split[0]))
        # stare.append(int(linie_split[1]))
        conf_scop.append(stare)

    chei = []
    linie = f.readline()
    while linie != 'final_fisier':
        chei.append(str(linie.split()[0]))
        linie = f.readline()

    return N, conf_initiala, conf_scop, chei


class Nod:
    # nr de descuieri ramase
    def euristica_1(self, lacat):
        s = 0
        for i in lacat:
            if i[0] == 'i':
                s += i[1]
        return s

    # nr de incuietori ramase inchise
    def euristica_2(self, lacat):
        list = []
        for i in lacat:
            if i[0] == 'i':
                list.append(i[1])
        if not list:
            return 0
        return max(list)

    #
    def euristica_3(self, lacat):
        count = 0
        for i in lacat:
            if i[0] == 'i':
                count += 1;
        return count

    def __init__(self, lacat):
        self.info = lacat

        # aici schimbam tipul de euristica
        if euristica == 1:
            self.h = self.euristica_1(lacat)
        elif euristica == 2:
            # print(self.euristica_2(lacat))
            self.h = self.euristica_2(lacat)
        else:
            self.h = self.euristica_3(lacat)


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

    def __init__(self, nod_graf, parinte=None, g=0, f=None, cheie=None):
        self.nod_graf = nod_graf  # obiect de tip Nod
        self.parinte = parinte  # obiect de tip NodParcurgere
        self.g = g  # costul drumului de la radacina pana la nodul curent
        self.cheie = cheie

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
        nod_c = self
        while nod_c is not None:
            if nod.info == nod_c.nod_graf.info:
                return True
            nod_c = nod_c.parinte
        return False

    # se modifica in functie de problema
    def expandeaza(self):
        """Pentru nodul curent (self) parinte, trebuie sa gasiti toti succesorii (fiii)
       si sa returnati o lista de tupluri (nod_fiu, cost_muchie_tata_fiu),
       sau lista vida, daca nu exista niciunul.
       (Fiecare tuplu contine un obiect de tip Nod si un numar.)
       """
        # print(N)
        lacat = self.nod_graf.info
        fiii = []
        # generam toate posibilitatiile de avansare folosing toate cheile
        for cheie in chei:
            mutare = []
            for incuietoare in range(N):
                if cheie[incuietoare] == 'd':
                    # daca cheia are simbolul pt descuiat si intalneste o incuietoare deschisa atunci o lasa deschisa
                    if lacat[incuietoare][0] == 'd':
                        mutare.append(('d', 0))
                    # daca cheia are simbolul pt descuiat si intalneste o incuietoare inchisa o data atunci o transforma in (d,0)
                    elif lacat[incuietoare][1] == 1:
                        mutare.append(('d', 0))
                    else:
                        # daca cheia are simbolul pt descuiat si intalneste o incuietoare inchisa de mai multe ori o deschide o data
                        mutare.append(('i', lacat[incuietoare][1] - 1))

                if cheie[incuietoare] == 'i':
                    # daca cheia are simbolul pt incuiat si intalneste o incuietoare deschisa atunci o incuie
                    # print(lacat)
                    if lacat[incuietoare][0] == 'd':
                        mutare.append(('i', 1))
                    else:
                        # daca cheia are simbolul pt incuiat si intalneste o incuietoare incuiata atunci o mai incuie inca o data
                        mutare.append(('i', lacat[incuietoare][1] + 1))

                # daca cheia are simbolul pt gol nu se produce nicio modificare
                if cheie[incuietoare] == 'g':
                    mutare.append((lacat[incuietoare][0], lacat[incuietoare][1]))

            # verific daca am mai avut aceasta configurație
            fiu = problema.cauta_nod_nume(mutare)

            if not fiu:
                nod_nou = Nod(mutare)
                problema.noduri.append(nod_nou)
                fiu = nod_nou

            cost = 1  # toate mutarile au costul 1
            fiii.append((fiu, cost, cheie))

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
    pas = 0
    sir = "\n"
    afisare = []
    for x in l:
        afisare.append(x.nod_graf.info)
        if pas == 0:
            sir += "Initial: " + str(afisare[pas]) + '\n'
            pas += 1
        if x.cheie != None:
            sir += str(pas) + ") "
            sir += "Incuietori: " + str(afisare[pas - 1]) + "\n"
            sir += "Folosim cheia: [" + str(x.cheie) + "] pentru a ajunge la " + str(x.nod_graf.info) + '\n'
            pas += 1
        if x.nod_graf.info == config_scop:
            sir += "Incuietori(stare scop): " + str(config_scop) + "\n"
            sir += "S-au realizat " + str(pas - 1) + " operatii" + "\n";
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


def a_star(f_output):
    """
           Functia care implementeaza algoritmul A-star
       """
    ### TO DO ... DONE

    rad_arbore = NodParcurgere(NodParcurgere.problema.nod_start)
    _open = [rad_arbore]  # open va contine elemente de tip NodParcurgere
    closed = []  # closed va contine elemente de tip NodParcurgere
    pas = 0
    while len(_open) > 0:
        # print(str_info_noduri(open))  # afisam lista open
        nod_curent = _open[0]  # scoatem primul element din lista open
        pas += 1
        closed.append(nod_curent)  # si il adaugam la finalul listei closed

        # testez daca nodul extras din lista open este nod scop (si daca da, ies din bucla while)
        if nod_curent.test_scop():
            break
        _open.remove(nod_curent)

        l_succesori = nod_curent.expandeaza()  # contine tupluri de tip (Nod, numar)
        for (nod_succesor, cost_succesor, cheie) in l_succesori:
            # "nod_curent" este tatal, "nod_succesor" este fiul curent

            # daca fiul nu e in drumul dintre radacina si tatal sau (adica nu se creeaza un circuit)
            if (not nod_curent.contine_in_drum(nod_succesor)):

                # calculez valorile g si f pentru "nod_succesor" (fiul)
                g_succesor = nod_curent.g + cost_succesor  # g-ul tatalui + cost muchie(tata, fiu)
                f_succesor = g_succesor + nod_succesor.h  # g-ul fiului + h-ul fiului

                # verific daca "nod_succesor" se afla in closed
                # (si il si sterg, returnand nodul sters in nod_parcg_vechi
                nod_parcg_vechi = in_lista(closed, nod_succesor)

                if nod_parcg_vechi is not None:  # "nod_succesor" e in closed
                    # daca f-ul calculat pentru drumul actual este mai bun (mai mic) decat
                    #      f-ul pentru drumul gasit anterior (f-ul nodului aflat in lista closed)
                    # atunci actualizez parintele, g si f
                    # si apoi voi adauga "nod_nou" in lista open
                    if (f_succesor < nod_parcg_vechi.f):
                        closed.remove(nod_parcg_vechi)  # scot nodul din lista closed
                        nod_parcg_vechi.parinte = nod_curent  # actualizez parintele
                        nod_parcg_vechi.g = g_succesor  # actualizez g
                        nod_parcg_vechi.f = f_succesor  # actualizez f
                        nod_nou = nod_parcg_vechi  # setez "nod_nou", care va fi adaugat apoi in open

                else:
                    # daca nu e in closed, verific daca "nod_succesor" se afla in open
                    nod_parcg_vechi = in_lista(_open, nod_succesor)

                    if nod_parcg_vechi is not None:  # "nod_succesor" e in open
                        # daca f-ul calculat pentru drumul actual este mai bun (mai mic) decat
                        #      f-ul pentru drumul gasit anterior (f-ul nodului aflat in lista open)
                        # atunci scot nodul din lista open
                        #       (pentru ca modificarea valorilor f si g imi va strica sortarea listei open)
                        # actualizez parintele, g si f
                        # si apoi voi adauga "nod_nou" in lista open (la noua pozitie corecta in sortare)
                        if (f_succesor < nod_parcg_vechi.f):
                            _open.remove(nod_parcg_vechi)
                            nod_parcg_vechi.parinte = nod_curent
                            nod_parcg_vechi.g = g_succesor
                            nod_parcg_vechi.f = f_succesor
                            nod_nou = nod_parcg_vechi

                    else:  # cand "nod_succesor" nu e nici in closed, nici in open
                        nod_nou = NodParcurgere(nod_graf=nod_succesor, parinte=nod_curent, g=g_succesor, cheie=cheie)
                    # se calculeaza f automat in constructor

                if nod_nou:
                    # inserare in lista sortata crescator dupa f
                    # (si pentru f-uri egale descrescator dupa g)
                    i = 0
                    while i < len(_open):
                        if _open[i].f < nod_nou.f:
                            i += 1
                        else:
                            while i < len(_open) and _open[i].f == nod_nou.f and _open[i].g > nod_nou.g:
                                i += 1
                            break

                    _open.insert(i, nod_nou)

    fisier = open(f_output, 'a')
    fisier.write("\n------------- Fisier input" + str(f_output) + " -----------------\n")
    if len(_open) == 0:
        fisier.write("Lista open e vida, nu avem drum de la nodul start la nodul scop\n")
    else:
        print(str_info_noduri(nod_curent.drum_arbore()))
        fisier.write("Drum de cost minim: " + str_info_noduri(nod_curent.drum_arbore()))
        if euristica == 1:
            fisier.write("euristica 1 ")
            fisier.write(str(time.perf_counter()))
            fisier.write("\npasi: ")
            fisier.write(str(pas))
        elif euristica == 2:
            fisier.write("euristica 2 ")
            fisier.write(str(time.perf_counter()))
            fisier.write("\npasi: ")
            fisier.write(str(pas))
        else:
            fisier.write("euristica 3 ")
            fisier.write(str(time.perf_counter()))
            fisier.write("\npasi: ")
            fisier.write(str(pas))


if __name__ == "__main__":
    date_intrare = ['input1.txt', 'input2.txt', 'input3.txt', 'input4.txt']
    date_iesire = ['output1.txt', 'output2.txt', 'output3.txt', 'output4.txt']

    for i in range(len(date_intrare)):
        f = open(date_iesire[i], "w")
        f.close()
        N, config_initiala, config_scop, chei = citire(date_intrare[i])
        now = time.perf_counter()
        euristica = 1
        problema = Problema()
        NodParcurgere.problema = problema
        a_star(date_iesire[i])

        now = time.perf_counter()
        euristica = 2
        problema = Problema()
        NodParcurgere.problema = problema
        a_star(date_iesire[i])

        # now = time.perf_counter()
        # euristica = 3
        # problema = Problema()
        # NodParcurgere.problema = problema
        # a_star()
