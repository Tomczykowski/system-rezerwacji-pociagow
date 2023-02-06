from osoba import Osoba
from funkcje_operacji_na_plikach import (
    pobieranie_z_pliku_pociagi,
    nadpisywanie_pociagi
)
from wyjatki import (
    BladKolejnosciPrzystankow, BladKoniecNieJestPrzystankiemTrasyPociagu,
    BladMiejsceZajete, BladNieIstniejeTakiRzad,
    BladOsobaNieMaBiletow, BladPoczatekNieJestPrzystankiemTrasyPociagu,
    BladWybranoTakiSamPoczatekIKoniec, BladNieZdefiniowanaOsoba,
    BladPodanaOsobaNieMaTakiegoBiletu
)
import copy


def zmiana_na_zajete(id_poczatku, id_konca, miejsca, trasa, rzad, id_miejsca):
    """
    Zmienia wartosci w slowniku na taka ktora oznacza zajete miejsce.
    Zwraca blad jesli wybrane miejsce jest zajete.
    """
    for i in range(id_poczatku, id_konca):
        if miejsca[trasa[i]][rzad-1][id_miejsca] == "O":
            miejsca[trasa[i]][rzad-1][id_miejsca] = "X"
        else:
            raise BladMiejsceZajete
    return miejsca


def zmiana_na_wolne(id_poczatku, id_konca, slownik, trasa,
                    rzad, dane, nazwa, id_miejsca):
    """
    Zmienia wartosc w slowniku na taka ktora oznacza wolne miejsce.
    Zmienia slownik w pliku pociagi.json.
    """
    for i in range(id_poczatku, id_konca):
        slownik[trasa[i]][rzad-1][id_miejsca] = "O"
    dane[nazwa]['slownik'] = slownik
    nadpisywanie_pociagi(dane)


class Pociag:
    """
    Class Pociag. Zawiera atrybuty:
    :param nazwa: przechowuje nazwe pociagu.
    :typ nazwa: str.
    :param tasa: przechowuje liste nazw przystankow na trasie pociagu.
    :typ trasa: lista.
    :param ilosc_rzedow: przechwouje ilosc rzedow miejsc w pociagu.
    :typ ilosc_rzedow: int.
    :param zapis: przechowuje wartosc bool.
    :typ zapis: bool.
    """
    def __init__(self, nazwa, trasa, ilosc_rzedow, zapis=False) -> None:
        """
        Tworzy instancje klasy Pociag.
        Tworzy slownik kazdej stacji z trasy ktory przechowuje
        informacje ktore miejsca sa zajete.
        Zglasza blad jesli nazwa nie jest stringiem,
        trasa nie jest lista lub ilosc_rzedow nie jest liczba naturalna.
        Jezeli zapis przechowuje wartosc True, pociag jest dopisywany do
        pliku pociagi.json.
        """
        if not isinstance(nazwa, str):
            raise ValueError("Nazwa musi byc stringiem.")
        if (not isinstance(trasa, list)) or (len(trasa) < 2):
            raise ValueError("Trasa musi byc lista i musi miec min. 2 stacje.")
        if not isinstance(ilosc_rzedow, int) or ilosc_rzedow < 1:
            raise ValueError("Ilosc rzedow musi byc liczba calkowita.")
        self.nazwa = nazwa
        self.trasa = trasa
        self.ilosc_rzedow = ilosc_rzedow
        self.slownik = {}
        for stacja in trasa:
            self.lista = []
            for i in range(ilosc_rzedow):
                self.lista.append(["O", "O", "O"])
            self.slownik[stacja] = self.lista

        if zapis is True:
            dane = pobieranie_z_pliku_pociagi()
            klucze = dane.keys()
            if nazwa not in klucze:
                dane[self.nazwa] = {
                        'trasa': self.trasa,
                        'ilosc_rzedow': self.ilosc_rzedow,
                        'slownik': self.slownik
                    }
                nadpisywanie_pociagi(dane)

    def kup(self, poczatek, koniec, rzad, typ, osoba: Osoba):
        """
        Zmienia stan wolnego miejsca na zarezerwowany
        i zapisuje bilet w liscie biletow podanej osoby.
        Zwraca blad jesli poczatek lub koniec nie sa
        w spisie przystankow danego pociagu,
        koniec wystepuje w spisie przystankow wczesniej niz poczatek,
        poczatek jest taki sam jak koniec,
        rzad nie jest liczba wieksza z przedzialu 1 - ilosc rzedow pociagu,
        osoba nie jest obiektem klasy Osoba,
        typ nie jest rowny A, B lub C.
        Nadpisuje rezerwacje w pliku pociagi.json.
        """
        if poczatek not in self.trasa:
            raise BladPoczatekNieJestPrzystankiemTrasyPociagu
        if koniec not in self.trasa:
            raise BladKoniecNieJestPrzystankiemTrasyPociagu
        if (not isinstance(rzad, int) or
           rzad not in range(1, self.ilosc_rzedow + 1)):
            raise BladNieIstniejeTakiRzad
        if not isinstance(osoba, Osoba):
            raise BladNieZdefiniowanaOsoba
        index_poczatku = self.trasa.index(poczatek)
        index_konca = self.trasa.index(koniec)
        if index_poczatku > index_konca:
            raise BladKolejnosciPrzystankow
        if index_konca == index_poczatku:
            raise BladWybranoTakiSamPoczatekIKoniec
        dane = pobieranie_z_pliku_pociagi()
        slownik_miejsc = dane[self.nazwa]['slownik']

        if typ == "A":
            self.slownik = zmiana_na_zajete(index_poczatku, index_konca,
                                            slownik_miejsc, self.trasa,
                                            rzad, 0)
        elif typ == "B":
            self.slownik = zmiana_na_zajete(index_poczatku, index_konca,
                                            slownik_miejsc, self.trasa,
                                            rzad, 1)
        elif typ == "C":
            self.slownik = zmiana_na_zajete(index_poczatku, index_konca,
                                            slownik_miejsc, self.trasa,
                                            rzad, 2)
        else:
            raise ValueError("Typ musi byc rowny A lub B lub C.")
        osoba.dodaj_bilet([poczatek, koniec, rzad, typ, self.nazwa])
        dane = pobieranie_z_pliku_pociagi()
        dane[self.nazwa]['slownik'] = self.slownik
        nadpisywanie_pociagi(dane)
        return True

    def anuluj(self, poczatek, koniec, rzad, typ, osoba: Osoba):
        """
        Zmienia stan zajetego miejsca na wolny.
        Zwraca blad jesli osoba nie jest obiektem klasy Osoba lub
        jesli osoba nie ma biletow z podanymi wartosciami w
        swojej liscie kupionych biletow lub jesli
        dane biletu nie zgadzaja sie z danymi biletu wybranej osoby.
        Anuluje rezerwacje z pliku pociagi.json.
        """
        if not isinstance(osoba, Osoba):
            raise BladNieZdefiniowanaOsoba
        if len(osoba.bilety) == 0:
            raise BladOsobaNieMaBiletow

        dane = pobieranie_z_pliku_pociagi()
        poprawnosc = False
        index_biletu = 0
        for bilet in osoba.bilety:
            if (
                bilet[0] == poczatek and bilet[1] == koniec and
                bilet[2] == rzad and bilet[3] == typ and
                bilet[4] == self.nazwa
            ):
                poprawnosc = True
                osoba.usun_bilet(index_biletu)
                index_poczatku = self.trasa.index(poczatek)
                index_konca = self.trasa.index(koniec)
                if typ == "A":
                    zmiana_na_wolne(index_poczatku, index_konca, self.slownik,
                                    self.trasa, rzad, dane, self.nazwa, 0)
                elif typ == "B":
                    zmiana_na_wolne(index_poczatku, index_konca, self.slownik,
                                    self.trasa, rzad, dane, self.nazwa, 1)
                elif typ == "C":
                    zmiana_na_wolne(index_poczatku, index_konca, self.slownik,
                                    self.trasa, rzad, dane, self.nazwa, 2)
            index_biletu = index_biletu + 1
        if poprawnosc is False:
            raise BladPodanaOsobaNieMaTakiegoBiletu
        return True

    def wyswietl(self, poczatek, koniec) -> str:
        """
        Wyswietla miejsca w pociagu z informacja ktore sa wolne a ktore zajete.
        Zglasza wyjatek jesli poczatek lub koniec
        nie sa przystankami trasy pociagu,
        poczatek wystepuje po koncu na trasie pociagu
        """
        if poczatek not in self.trasa:
            raise BladPoczatekNieJestPrzystankiemTrasyPociagu
        if koniec not in self.trasa:
            raise BladKoniecNieJestPrzystankiemTrasyPociagu
        index_poczatku = self.trasa.index(poczatek)
        index_konca = self.trasa.index(koniec)
        if index_poczatku > index_konca:
            raise BladKolejnosciPrzystankow
        dane = pobieranie_z_pliku_pociagi()
        self.slownik = dane[self.nazwa]['slownik']
        spis = copy.deepcopy(self.slownik[poczatek])
        index_poczatku = self.trasa.index(poczatek)
        index_konca = self.trasa.index(koniec)
        for i in range(index_poczatku, index_konca):
            for j in range(0, self.ilosc_rzedow):
                for k in range(0, 3):
                    if self.slownik[self.trasa[i]][j][k] == "X":
                        spis[j][k] = "X"
        print(f"{poczatek}-{koniec}")
        print("   [A] [B] [C]")
        nr_rzad = 0
        for rzad in spis:
            nr_rzad += 1
            print(f"[{nr_rzad}]|{rzad[0]}| |{rzad[1]}| |{rzad[2]}|")
