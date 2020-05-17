import copy
import time


# derectiile in care poate sa mearga o piesa
directii = [[-1, 0], [-1, 1], [0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1]]


# functie pentru inlocuitul pieselor dintre doua piese de acelasi tip
def schimba_culoare(matr, pozitie, directii, jucator):
    for directie in directii:
        i, j = pozitie[0], pozitie[1]
        matr[i][j] = jucator
        i -= directie[0]
        j -= directie[1]

        while matr[i][j] != jucator:
            matr[i][j] = jucator
            i -= directie[0]
            j -= directie[1]

class Joc:
    """
    Clasa care defineste jocul. Se va schimba de la un joc la altul.
    """
    NR_COLOANE = 8
    NR_LINII = 8
    SIMBOLURI_JUC = ['a', 'n']  # ['G', 'R'] sau ['X', '0']
    JMIN = None  # 'R'
    JMAX = None  # 'G'
    GOL = '#'


    def __init__(self, tabla=None):
        if tabla is not None:
            self.matr = tabla
        else:
            self.matr = [ ['#' for i in range (self.NR_COLOANE)] for j in range(self.NR_LINII) ]
            self.matr[self.NR_LINII//2 -1][self.NR_COLOANE//2 -1] = 'a'
            self.matr[self.NR_LINII // 2 ][self.NR_COLOANE // 2] = 'a'
            self.matr[self.NR_LINII // 2 - 1][self.NR_COLOANE // 2] = 'n'
            self.matr[self.NR_LINII // 2][self.NR_COLOANE // 2 - 1] = 'n'
    def variante(self, jucator):

        # construin un dictionar format din pozitie si directii
        jucator_opus = self.JMAX if jucator == self.JMIN else self.JMIN
        posibilitati = {}

        for i in range(len(self.matr)):
            for j in range(len(self.matr[i])):
                if self.matr[i][j] == jucator:
                    for directie in directii:
                        # coordonatele vecinilor
                        i_vecin, j_vecin = i + directie[0], j + directie[1]
                        if i_vecin not in range(self.NR_LINII) or j_vecin not in range(self.NR_COLOANE) or \
                                self.matr[i_vecin][j_vecin] != jucator_opus:
                            continue  # trebuie sa treaca peste cel putin o piesa de cealalta culoare

                        gasit = True
                        # merg pana la prima pozitie libera gasita
                        while self.matr[i_vecin][j_vecin] == jucator_opus:
                            i_vecin += directie[0]
                            j_vecin += directie[1]
                            if i_vecin not in range(self.NR_LINII) or j_vecin not in range(self.NR_COLOANE):
                                gasit = False
                                break
                        # adaugam in dictionar
                        if gasit:
                            if (i_vecin, j_vecin) not in posibilitati.keys():
                                posibilitati[(i_vecin, j_vecin)] = [directie]
                            else:
                                posibilitati[(i_vecin, j_vecin)].append(directie)

        return posibilitati

    def nr_piese(self, jucator):
        nr = 0
        for line in self.matr:
            nr += line.count(jucator)
        return nr

    def final(self,jucator):
        # returnam simbolul jucatorului castigator daca are 4 piese adiacente
        #	pe linie, coloana, diagonala \ sau diagonala /
        # sau returnam 'remiza'
        # sau 'False' daca nu s-a terminat jocul
        rez = False

        pos = self.variante(jucator)
        if len(pos) == 0:
            scor_jmin = self.nr_piese(self.JMIN)  # trebuie calculate ambele pentru ca jocul se poate termina
            scor_jmax = self.nr_piese(self.JMAX)  # si inainte sa se umple tabla
            if scor_jmax > scor_jmin:
                return self.JMAX
            elif scor_jmax == scor_jmin:
                return 'remiza'
            else:
                return self.JMIN



    def mutari_joc(self, jucator_opus):
        l_mutari = []

        posibilitati = self.variante(jucator_opus)

        for pozitie, directie in posibilitati.items():
            matr_noua = copy.deepcopy(self.matr)
            schimba_culoare(matr_noua, pozitie, directie, jucator_opus)
            l_mutari.append(Joc(matr_noua))

        return l_mutari

    def fct_euristica(self):
        # diferenta dintre nr de piese ale fiecarui jucator

        nr_max = 0
        nr_min = 0
        for line in self.matr:
            nr_max += line.count(Joc.JMAX)
            nr_min += line.count(Joc.JMIN)
        return nr_max - nr_min

    def estimeaza_scor(self, adancime, jucator):
         t_final = self.final(jucator)
         if t_final == Joc.JMAX:
             return 999 + adancime
         elif t_final == Joc.JMIN:
             return -999 - adancime
         elif t_final == 'remiza':
             return 0
         else:
             return self.fct_euristica()

    def __str__(self):
        sir = '  '
        for nr_col in range(self.NR_COLOANE):
            sir += str(nr_col) + ' '
        sir += '\n'

        for lin in range(self.NR_LINII):
            sir += (str(lin) + ' ' + " ".join([str(x) for x in self.matr[lin]]) + "\n")
        return sir


class Stare:
    """
    Clasa folosita de algoritmii minimax si alpha-beta
    Are ca proprietate tabla de joc
    Functioneaza cu conditia ca in cadrul clasei Joc sa fie definiti JMIN si JMAX (cei doi jucatori posibili)
    De asemenea cere ca in clasa Joc sa fie definita si o metoda numita mutari() care ofera lista cu
    configuratiile posibile in urma mutarii unui jucator
    """

    ADANCIME_MAX = None

    def __init__(self, tabla_joc, j_curent, adancime, parinte=None, scor=None):
        self.tabla_joc = tabla_joc
        self.j_curent = j_curent

        # adancimea in arborele de stari
        self.adancime = adancime

        # scorul starii (daca e finala) sau al celei mai bune stari-fiice (pentru jucatorul curent)
        self.scor = scor

        # lista de mutari posibile din starea curenta
        self.mutari_posibile = []

        # cea mai buna mutare din lista de mutari posibile pentru jucatorul curent
        self.stare_aleasa = None

    def jucator_opus(self):
        if self.j_curent == Joc.JMIN:
            return Joc.JMAX
        else:
            return Joc.JMIN

    def mutari(self):
        l_mutari = self.tabla_joc.mutari_joc(self.j_curent)
        juc_opus = self.jucator_opus()
        l_stari_mutari = [Stare(mutare, juc_opus, self.adancime - 1, parinte=self) for mutare in l_mutari]

        return l_stari_mutari

    def __str__(self):
        sir = str(self.tabla_joc) + "(Juc curent: " + self.j_curent + ")\n"
        return sir


""" Algoritmul MinMax """


def min_max(stare):
    if stare.adancime == 0 or stare.tabla_joc.final(stare.j_curent):
        stare.scor = stare.tabla_joc.estimeaza_scor(stare.adancime, stare.j_curent)
        return stare

    # calculez toate mutarile posibile din starea curenta
    stare.mutari_posibile = stare.mutari()

    # aplic algoritmul minimax pe toate mutarile posibile (calculand astfel subarborii lor)
    mutari_scor = [min_max(mutare) for mutare in stare.mutari_posibile]

    if stare.j_curent == Joc.JMAX:
        # daca jucatorul e JMAX aleg starea-fiica cu scorul maxim
        stare.stare_aleasa = max(mutari_scor, key=lambda x: x.scor)
    else:
        # daca jucatorul e JMIN aleg starea-fiica cu scorul minim
        stare.stare_aleasa = min(mutari_scor, key=lambda x: x.scor)

    stare.scor = stare.stare_aleasa.scor
    return stare


def alpha_beta(alpha, beta, stare):
    if stare.adancime == 0 or stare.tabla_joc.final(stare.j_curent):
        stare.scor = stare.tabla_joc.estimeaza_scor(stare.adancime, stare.j_curent)
        return stare

    if alpha >= beta:
        return stare  # este intr-un interval invalid deci nu o mai procesez

    stare.mutari_posibile = stare.mutari()

    if stare.j_curent == Joc.JMAX:
        scor_curent = float('-inf')

        for mutare in stare.mutari_posibile:
            # calculeaza scorul
            stare_noua = alpha_beta(alpha, beta, mutare)

            if scor_curent < stare_noua.scor:
                stare.stare_aleasa = stare_noua
                scor_curent = stare_noua.scor
            if alpha < stare_noua.scor:
                alpha = stare_noua.scor
                if alpha >= beta:
                    break

    elif stare.j_curent == Joc.JMIN:
        scor_curent = float('inf')

        for mutare in stare.mutari_posibile:
            stare_noua = alpha_beta(alpha, beta, mutare)

            if scor_curent > stare_noua.scor:
                stare.stare_aleasa = stare_noua
                scor_curent = stare_noua.scor

            if beta > stare_noua.scor:
                beta = stare_noua.scor
                if alpha >= beta:
                    break

    stare.scor = stare.stare_aleasa.scor

    return stare


def afis_daca_final(stare_curenta, jucator):
    final = stare_curenta.tabla_joc.final(jucator)
    if final:
        if final == "remiza":
            print("Remiza!")
        else:
            print("A castigat " + final)

        return True

    return False


def main():
    # initializare algoritm
    raspuns_valid = False
    while not raspuns_valid:
        tip_algoritm = input("Algorimul folosit? (raspundeti cu 1 sau 2)\n 1.Minimax\n 2.Alpha-beta\n ")
        if tip_algoritm in ['1', '2']:
            raspuns_valid = True
        else:
            print("Nu ati ales o varianta corecta.")

    # initializare ADANCIME_MAX
    raspuns_valid = False
    while not raspuns_valid:
        n = input("Adancime maxima a arborelui: ")
        if n.isdigit():
            Stare.ADANCIME_MAX = int(n)
            raspuns_valid = True
        else:
            print("Trebuie sa introduceti un numar natural nenul.")

    # initializare jucatori
    [s1, s2] = Joc.SIMBOLURI_JUC.copy()  # lista de simboluri posibile
    raspuns_valid = False
    while not raspuns_valid:
        Joc.JMIN = str(input("Doriti sa jucati cu {} sau cu {}? ".format(s1, s2)))
        if Joc.JMIN in Joc.SIMBOLURI_JUC:
            raspuns_valid = True
        else:
            print("Raspunsul trebuie sa fie {} sau {}.".format(s1, s2))
    Joc.JMAX = s1 if Joc.JMIN == s2 else s2

    # initializare tabla
    tabla_curenta = Joc()
    print("Tabla initiala")
    print(str(tabla_curenta))

    # creare stare initiala
    stare_curenta = Stare(tabla_curenta, Joc.SIMBOLURI_JUC[0], Stare.ADANCIME_MAX)

    linie = -1
    coloana = -1
    while True:
        if stare_curenta.j_curent == Joc.JMIN:
            # testez daca jocul a ajuns intr-o stare finala
            # si afisez un mesaj corespunzator in caz ca da
            if afis_daca_final(stare_curenta, Joc.JMIN):
                break

            # muta jucatorul
            raspuns_valid = False
            while not raspuns_valid:
                try:
                    pos = stare_curenta.tabla_joc.variante(Joc.JMIN)
                    print("Pozitii posibile: ")
                    for p in pos.keys():
                        print(p, end=' ')
                    print()

                    linie = int(input("linie = "))
                    coloana = int(input("coloana = "))

                    if (linie, coloana) in pos.keys():
                        raspuns_valid = True
                    else:
                        print("Pozitie invalida. Pozitii posibile: ")
                        for p in pos.keys():
                            print(p, end=' ')
                        print()

                except ValueError:
                    print("Coloana trebuie sa fie un numar intreg.")

            # datele sunt corecte
            dirs = pos[(linie, coloana)]
            schimba_culoare(stare_curenta.tabla_joc.matr, (linie, coloana), dirs, Joc.JMIN)

            # afisarea starii jocului in urma mutarii utilizatorului
            print("\nTabla dupa mutarea jucatorului")
            print(str(stare_curenta))

            # S-a realizat o mutare. Schimb jucatorul cu cel opus
            stare_curenta.j_curent = stare_curenta.jucator_opus()

        # --------------------------------
        else:  # jucatorul e JMAX (calculatorul)

            if afis_daca_final(stare_curenta, Joc.JMAX):
                break

            # preiau timpul in milisecunde de dinainte de mutare
            t_inainte = int(round(time.time() * 1000))
            if tip_algoritm == '1':
                stare_actualizata = min_max(stare_curenta)
            else:
                stare_actualizata = alpha_beta(-5000, 5000, stare_curenta)
            stare_curenta.tabla_joc = stare_actualizata.stare_aleasa.tabla_joc
            print("Tabla dupa mutarea calculatorului")
            print(str(stare_curenta))

            # preiau timpul in milisecunde de dupa mutare
            t_dupa = int(round(time.time() * 1000))
            print("Calculatorul a \"gandit\" timp de " + str(t_dupa - t_inainte) + " milisecunde.")

            # S-a realizat o mutare. Schimb jucatorul cu cel opus
            stare_curenta.j_curent = stare_curenta.jucator_opus()


if __name__ == "__main__":
    main()