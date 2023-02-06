from pociag import (
    Pociag, BladPoczatekNieJestPrzystankiemTrasyPociagu,
    BladKoniecNieJestPrzystankiemTrasyPociagu, BladKolejnosciPrzystankow,
    BladNieIstniejeTakiRzad, BladMiejsceZajete,
    BladWybranoTakiSamPoczatekIKoniec, BladOsobaNieMaBiletow,
    BladPodanaOsobaNieMaTakiegoBiletu,)
from osoba import Osoba
from funkcje_operacji_na_plikach import (
    pobieranie_z_pliku_osoby,
    pobieranie_z_pliku_pociagi,
    nadpisywanie_osoby,
    nadpisywanie_pociagi
)


def menu():
    """
    Menu wyboru wypisujace komunikat w koncoli w ktorym opisane jest
    co uzytkownik moze zrobic za pomoca programu.
    """
    print("Wybierz co chcesz zrobic:")
    print("1 - kup bilet")
    print("2 - anuluj bilet")
    print("3 - wyswietl stan rezerwacji")
    print("9 - zakoncz")
    wybor = input()
    return wybor


def pobieranie_danych_trasy():
    """
    Inputy z wypisaniami w konsoli pozwalajacymi pobrac
    od uzytkownika danych trasy.
    """
    print("Podaj nazwe pociagu:")
    nazwa = input()
    print("Podaj stacje poczatkowa:")
    poczatek = input()
    print("podaj stacje koncowa:")
    koniec = input()
    return nazwa, poczatek, koniec


def naprawianie_plikow(dane_pociagi, dane_osoby):
    """
    Funkcja naprawiajaca plik w jakby podczas dzialania programu wystapil
    wyjatek, dzieki czemu pliki przechowujace dane nie zostana uszkodzone.
    """
    nadpisywanie_pociagi(dane_pociagi)
    nadpisywanie_osoby(dane_osoby)


def pobieranie_wartosci():
    """
    Funkcja pobierajaca od uzytkowanika dane potrzebne
    do dzialania programu przyjmuje rzad i typ tak dluga
    az uzytkownik poda poprawne dane.
    """
    print("Podaj nr rzedu miejsca:")
    rzad = input()
    while not rzad.isdigit():
        print("Podana wartosc nie jest liczba! Podaj ja ponownie:")
        rzad = input()
    rzad = int(rzad)
    print("Podaj typ miejsca:")
    typ = input()
    while typ not in ['A', 'B', 'C']:
        print("Podany typ nie wystepuje w pociagu. Podaj go ponownie:")
        typ = input()
    print("Podaj imie:")
    imie = input()
    print("Podaj nazwisko:")
    nazisko = input()
    id = imie + nazisko
    return rzad, typ, imie, nazisko, id


wybor = menu()

while wybor != '9':
    dane_pociagi = pobieranie_z_pliku_pociagi()
    dane_osoby = pobieranie_z_pliku_osoby()
    if wybor == '1':
        nazwa, poczatek, koniec = pobieranie_danych_trasy()
        rzad, typ, imie, nazisko, id = pobieranie_wartosci()
        osoby = pobieranie_z_pliku_osoby()
        if id not in osoby.keys():
            Osoba(imie, nazisko, True)
        dane = pobieranie_z_pliku_pociagi()
        klucze = dane.keys()
        if nazwa in klucze:
            trasa = dane[nazwa]['trasa']
            ilosc_rzedow = dane[nazwa]['ilosc_rzedow']
            pociag = Pociag(nazwa, trasa, ilosc_rzedow)
            osoba = Osoba(imie, nazisko)
            try:
                pociag.kup(poczatek, koniec, rzad, typ, osoba)
            except BladNieIstniejeTakiRzad:
                naprawianie_plikow(dane_pociagi, dane_osoby)
                print("\nNie ma takiego rzedu w pociagu.\n")
            except BladPoczatekNieJestPrzystankiemTrasyPociagu:
                naprawianie_plikow(dane_pociagi, dane_osoby)
                print("\nPodana stacja poczatkowa nie jest stacja trasy\
 pociagu")
            except BladKoniecNieJestPrzystankiemTrasyPociagu:
                naprawianie_plikow(dane_pociagi, dane_osoby)
                print("\nPodana stacja koncowa nie jest stacja trasy\
 pociagu.")
            except BladMiejsceZajete:
                naprawianie_plikow(dane_pociagi, dane_osoby)
                print("\nWybrano zajete miejsce.\n")
            except BladWybranoTakiSamPoczatekIKoniec:
                naprawianie_plikow(dane_pociagi, dane_osoby)
                print("\nPodano taka sama nazwe stacji poczatkowej i\
 koncowej.")
            except BladKolejnosciPrzystankow:
                naprawianie_plikow(dane_pociagi, dane_osoby)
                print("\nPodany przystanek poczatkowy wystepuje po przystanku\
 koncowym na trasie pociagu")
            except ValueError:
                naprawianie_plikow(dane_pociagi, dane_osoby)
        else:
            print("Nie ma pociagu o takiej nazwie")
        wybor = menu()

    elif wybor == '2':
        nazwa, poczatek, koniec = pobieranie_danych_trasy()
        rzad, typ, imie, nazisko, id = pobieranie_wartosci()
        osoby = pobieranie_z_pliku_osoby()
        if id not in osoby.keys():
            print("Podana osoba nie istnieje")
            wybor = menu()
            continue
        else:
            osoba = Osoba(imie, nazisko)
            osoba.bilety = osoby[id]['bilety']
        dane = pobieranie_z_pliku_pociagi()
        nazwy = dane.keys()
        if nazwa in nazwy:
            trasa = dane[nazwa]['trasa']
            ilosc_rzedow = dane[nazwa]['ilosc_rzedow']
            pociag = Pociag(nazwa, trasa, ilosc_rzedow)
            pociag.slownik = dane[nazwa]['slownik']
            try:
                pociag.anuluj(poczatek, koniec, rzad, typ, osoba)
            except BladOsobaNieMaBiletow:
                naprawianie_plikow(dane_pociagi, dane_osoby)
                print("Podana osoba nie ma biletow.")
            except BladPodanaOsobaNieMaTakiegoBiletu:
                print("Podana osoba nie posiada rezerwacji z podanymi danymi.")
        else:
            print("Nie ma pociagu o takiej nazwie")

        wybor = menu()

    elif wybor == '3':
        nazwa, poczatek, koniec = pobieranie_danych_trasy()
        dane = pobieranie_z_pliku_pociagi()
        klucze = dane.keys()
        if nazwa in klucze:
            trasa = dane[nazwa]['trasa']
            ilosc_rzedow = dane[nazwa]['ilosc_rzedow']
            pociag = Pociag(nazwa, trasa, ilosc_rzedow)
        else:
            print("Nie ma pociagu o takiej nazwie")
        try:
            pociag.wyswietl(poczatek, koniec)
        except BladPoczatekNieJestPrzystankiemTrasyPociagu:
            print("Podana stacja poczatkowa jest nieprawidlowa.")
        except BladKoniecNieJestPrzystankiemTrasyPociagu:
            print("Podana stacja koncowa jest nieprawidlowa.")
        except BladKolejnosciPrzystankow:
            print("Podano przystanki w zlej kolejnosci.")
        wybor = menu()
    else:
        print("\nNieobslugiwany znak!")
        wybor = menu()
