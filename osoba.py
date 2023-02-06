from funkcje_operacji_na_plikach import (
    pobieranie_z_pliku_osoby,
    nadpisywanie_osoby
)


class Osoba:
    """
    Class Osoba. Zawiera atrybuty:
    :param imie: przechowuje imie osoby.
    :typ imie: str.
    :param nazwisko: przechowuje nazwisko osoby.
    :typ nazwisko: str.
    :param zapis: przechowuje wartosc bool.
    :typ zapis: bool.
    """
    def __init__(self, imie, nazwisko, zapis=False) -> None:
        """
        Tworzy instancje klasy Osoba.
        Tworzy pusta liste biletow w ktorej przechowywane
        beda kupione bilety przez obiekt klasy.
        Zglasza blad jesli imie lub nazwisko nie jest ciagiem znakow.
        Jezeli podczas wywaloania zapis ma wartosc True,
        nadpisuje plik osoby.json dodajac do niego osobe.
        """
        if not isinstance(imie, str):
            raise ValueError("Imie musi byc tekstem.")
        if not isinstance(nazwisko, str):
            raise ValueError("Nazwisko musi byc tekstem.")
        self.imie = imie
        self.nazwisko = nazwisko
        self.bilety = []
        self.id = self.imie + self.nazwisko
        if zapis is True:
            dane = pobieranie_z_pliku_osoby()
            klucze = dane.keys()
            if self.id not in klucze:
                dane[self.id] = {
                        'imie': self.imie,
                        'nazwisko': self.nazwisko,
                        'bilety': self.bilety
                    }
                nadpisywanie_osoby(dane)

    def dodaj_bilet(self, bilet):
        """
        Pobiera dane z pliku osoby.json.
        Dodaje bilet do listy biletow obiektu klasy.
        Nadpisuje plik osoby.json dodajac do osoby bilet.
        """
        osoby = pobieranie_z_pliku_osoby()
        self.bilety = osoby[self.id]['bilety']
        osoby[self.id]['bilety'].append(bilet)
        nadpisywanie_osoby(osoby)
        return True

    def usun_bilet(self, index_biletu):
        """
        Pobiera dane z pliku osoby.json.
        Usuwa bilet z listy biletow obiektu klasy.
        Nadpisuje plik osoby.json usuwajac osobie bilet.
        """
        osoby = pobieranie_z_pliku_osoby()
        self.bilety = osoby[self.id]['bilety']
        del self.bilety[index_biletu]
        osoby[self.id]['bilety'] = self.bilety
        nadpisywanie_osoby(osoby)
        return True
