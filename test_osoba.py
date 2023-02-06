from osoba import Osoba
from pociag import Pociag
from funkcje_operacji_na_plikach import (
    pobieranie_z_pliku_pociagi,
    pobieranie_z_pliku_osoby,
    nadpisywanie_osoby,
    nadpisywanie_pociagi
)
import pytest


def test_init():
    osoba = Osoba("Jacek", "Placek")
    assert osoba.imie == "Jacek"
    assert osoba.nazwisko == "Placek"
    assert osoba.bilety == []


def test_imie__valueError():
    with pytest.raises(ValueError):
        Osoba(123, "Placek")


def test_nazwisko__valueError():
    with pytest.raises(ValueError):
        Osoba("Jacek", 123)


def test_dodaj_bilet():
    plik_pociagi = pobieranie_z_pliku_pociagi()
    plik_osoby = pobieranie_z_pliku_osoby()
    trasa = ["Wschodnia", "Stadion", "Powisle"]
    osoba = Osoba("test", "testowy", True)
    pociag = Pociag("pociag_testowy", trasa, 2, True)
    bilet = ["Wschodnia", "Powisle", 1, "B", pociag.nazwa]
    osoba.dodaj_bilet(bilet)
    assert osoba.bilety == [bilet]
    nadpisywanie_pociagi(plik_pociagi)
    nadpisywanie_osoby(plik_osoby)


def test_usun_bilet():
    plik_pociagi = pobieranie_z_pliku_pociagi()
    plik_osoby = pobieranie_z_pliku_osoby()
    trasa = ["Wschodnia", "Stadion", "Powisle"]
    osoba = Osoba("test", "testowy", True)
    pociag = Pociag("pociag_testowy", trasa, 2, True)
    bilet = ["Wschodnia", "Powisle", 1, "B", pociag.nazwa]
    bilet1 = ["Wschodnia", "Powisle", 1, "A", pociag.nazwa]
    osoba.dodaj_bilet(bilet)
    osoba.dodaj_bilet(bilet1)
    osoba.usun_bilet(0)
    assert osoba.bilety == [bilet1]
    nadpisywanie_pociagi(plik_pociagi)
    nadpisywanie_osoby(plik_osoby)
