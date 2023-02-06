from pociag import (
    Pociag, BladKolejnosciPrzystankow,
    BladMiejsceZajete, BladWybranoTakiSamPoczatekIKoniec,
    BladOsobaNieMaBiletow, BladPoczatekNieJestPrzystankiemTrasyPociagu,
    BladKoniecNieJestPrzystankiemTrasyPociagu, BladNieIstniejeTakiRzad,
    BladNieZdefiniowanaOsoba, BladPodanaOsobaNieMaTakiegoBiletu,)
from funkcje_operacji_na_plikach import (
    pobieranie_z_pliku_osoby,
    pobieranie_z_pliku_pociagi,
    nadpisywanie_osoby,
    nadpisywanie_pociagi
)
from osoba import Osoba
import pytest


def test_init():
    trasa = ["Wschodnia", "Stadion"]
    pociag = Pociag("nazwa", trasa, 2)
    assert pociag.nazwa == "nazwa"
    assert pociag.trasa == trasa
    assert pociag.ilosc_rzedow == 2
    assert pociag.slownik == {'Wschodnia': [['O', 'O', 'O'], ['O', 'O', 'O']],
                              'Stadion': [['O', 'O', 'O'], ['O', 'O', 'O']]}


def test_nazwa_valueError():
    trasa = ["Wschodnia", "Stadion"]
    with pytest.raises(ValueError):
        Pociag(123, trasa, 3)


def test_trasa_valueError():
    with pytest.raises(ValueError):
        Pociag("R1", 123, 3)


def test_ilosc_rzedow_valueError():
    trasa = ["Wschodnia", "Stadion"]
    with pytest.raises(ValueError):
        Pociag("R1", trasa, "Blad")


def test_ilosc_rzedow_mniej_niz_1():
    trasa = ["Wschodnia", "Stadion"]
    with pytest.raises(ValueError):
        Pociag("R1", trasa, 0)


def test_kup():
    plik_pociagi = pobieranie_z_pliku_pociagi()
    plik_osoby = pobieranie_z_pliku_osoby()
    trasa = ["Wschodnia", "Stadion", "Powisle"]
    osoba = Osoba("test", "testowy", True)
    pociag = Pociag("pociag_testowy", trasa, 2, True)
    pociag.kup("Wschodnia", "Stadion", 2, "B", osoba)
    assert pociag.slownik["Wschodnia"] == [['O', 'O', 'O'], ['O', 'X', 'O']]
    nadpisywanie_pociagi(plik_pociagi)
    nadpisywanie_osoby(plik_osoby)


def test_kup_poczatek_BladPoczatekNieJestPrzystankiemTrasyPociagu():
    plik_pociagi = pobieranie_z_pliku_pociagi()
    plik_osoby = pobieranie_z_pliku_osoby()
    trasa = ["Wschodnia", "Stadion", "Powisle"]
    osoba = Osoba("test", "testowy", True)
    pociag = Pociag("pociag_testowy", trasa, 2, True)
    with pytest.raises(BladPoczatekNieJestPrzystankiemTrasyPociagu):
        pociag.kup("Blad", "Stadion", 2, "B", osoba)
    nadpisywanie_pociagi(plik_pociagi)
    nadpisywanie_osoby(plik_osoby)


def test_kup_koniec_BladKoniecNieJestPrzystankiemTrasyPociagu():
    plik_pociagi = pobieranie_z_pliku_pociagi()
    plik_osoby = pobieranie_z_pliku_osoby()
    trasa = ["Wschodnia", "Stadion", "Powisle"]
    osoba = Osoba("test", "testowy", True)
    pociag = Pociag("pociag_testowy", trasa, 2, True)
    with pytest.raises(BladKoniecNieJestPrzystankiemTrasyPociagu):
        pociag.kup("Wschodnia", "Blad", 2, "B", osoba)
    nadpisywanie_pociagi(plik_pociagi)
    nadpisywanie_osoby(plik_osoby)


def test_kup_rzad_BladNieIstniejeTakiRzad():
    plik_pociagi = pobieranie_z_pliku_pociagi()
    plik_osoby = pobieranie_z_pliku_osoby()
    trasa = ["Wschodnia", "Stadion", "Powisle"]
    osoba = Osoba("test", "testowy", True)
    pociag = Pociag("pociag_testowy", trasa, 2, True)
    with pytest.raises(BladNieIstniejeTakiRzad):
        pociag.kup("Wschodnia", "Stadion", "Blad", "B", osoba)
    nadpisywanie_pociagi(plik_pociagi)
    nadpisywanie_osoby(plik_osoby)


def test_kup_typ_valueError():
    plik_pociagi = pobieranie_z_pliku_pociagi()
    plik_osoby = pobieranie_z_pliku_osoby()
    trasa = ["Wschodnia", "Stadion", "Powisle"]
    osoba = Osoba("test", "testowy", True)
    pociag = Pociag("pociag_testowy", trasa, 2, True)
    with pytest.raises(ValueError):
        pociag.kup("Wschodnia", "Stadion", 2, 1, osoba)
    nadpisywanie_pociagi(plik_pociagi)
    nadpisywanie_osoby(plik_osoby)


def test_kup_osoba_BladNieIstniejeTakiRzad():
    plik_pociagi = pobieranie_z_pliku_pociagi()
    plik_osoby = pobieranie_z_pliku_osoby()
    trasa = ["Wschodnia", "Stadion", "Powisle"]
    osoba = Osoba("test", "testowy", True)
    pociag = Pociag("pociag_testowy", trasa, 2, True)
    with pytest.raises(BladNieIstniejeTakiRzad):
        pociag.kup("Wschodnia", "Stadion", "Blad", "B", osoba)
    nadpisywanie_pociagi(plik_pociagi)
    nadpisywanie_osoby(plik_osoby)


def test_kup_BladKolejnosciPrzystankow():
    plik_pociagi = pobieranie_z_pliku_pociagi()
    plik_osoby = pobieranie_z_pliku_osoby()
    trasa = ["Wschodnia", "Stadion", "Powisle"]
    osoba = Osoba("test", "testowy", True)
    pociag = Pociag("pociag_testowy", trasa, 2, True)
    with pytest.raises(BladKolejnosciPrzystankow):
        pociag.kup("Stadion", "Wschodnia", 2, "B", osoba)
    nadpisywanie_pociagi(plik_pociagi)
    nadpisywanie_osoby(plik_osoby)


def test_kup_BladMiejsceZajete_cala_trasa():
    plik_pociagi = pobieranie_z_pliku_pociagi()
    plik_osoby = pobieranie_z_pliku_osoby()
    trasa = ["Wschodnia", "Stadion", "Powisle"]
    osoba = Osoba("test", "testowy", True)
    pociag = Pociag("pociag_testowy", trasa, 2, True)
    pociag.kup("Wschodnia", "Stadion", 2, "B", osoba)
    with pytest.raises(BladMiejsceZajete):
        pociag.kup("Wschodnia", "Stadion", 2, "B", osoba)
    nadpisywanie_pociagi(plik_pociagi)
    nadpisywanie_osoby(plik_osoby)


def test_kupBladMiejsceZajete_czesc_trasy():
    plik_pociagi = pobieranie_z_pliku_pociagi()
    plik_osoby = pobieranie_z_pliku_osoby()
    trasa = ["Wschodnia", "Stadion", "Powisle"]
    osoba = Osoba("test", "testowy", True)
    pociag = Pociag("pociag_testowy", trasa, 2, True)
    pociag.kup("Wschodnia", "Powisle", 2, "B", osoba)
    with pytest.raises(BladMiejsceZajete):
        pociag.kup("Stadion", "Powisle", 2, "B", osoba)
    nadpisywanie_pociagi(plik_pociagi)
    nadpisywanie_osoby(plik_osoby)


def test_kup_ostatni_przystanek():
    plik_pociagi = pobieranie_z_pliku_pociagi()
    plik_osoby = pobieranie_z_pliku_osoby()
    trasa = ["Wschodnia", "Stadion", "Powisle", "Srodmiescie", "Ochota"]
    osoba = Osoba("test", "testowy", True)
    pociag = Pociag("pociag_testowy", trasa, 2, True)
    zbyszek = Osoba("Zbyszek", "Testowy", True)
    pociag.kup("Wschodnia", "Powisle", 2, "B", osoba)
    assert pociag.slownik["Wschodnia"][1][1] == "X"
    assert pociag.slownik["Wschodnia"][1][1] == "X"
    pociag.kup("Powisle", "Ochota", 2, "B", zbyszek)
    assert pociag.slownik["Powisle"][1][1] == "X"
    assert pociag.slownik["Srodmiescie"][1][1] == "X"
    nadpisywanie_pociagi(plik_pociagi)
    nadpisywanie_osoby(plik_osoby)


def test_kup_Poczatek_taki_jak_koniec():
    plik_pociagi = pobieranie_z_pliku_pociagi()
    plik_osoby = pobieranie_z_pliku_osoby()
    trasa = ["Wschodnia", "Stadion", "Powisle", "Srodmiescie", "Ochota"]
    osoba = Osoba("test", "testowy", True)
    pociag = Pociag("pociag_testowy", trasa, 2, True)
    with pytest.raises(BladWybranoTakiSamPoczatekIKoniec):
        pociag.kup("Wschodnia", "Wschodnia", 2, "B", osoba)
    nadpisywanie_pociagi(plik_pociagi)
    nadpisywanie_osoby(plik_osoby)


def test_kup_rozne_miejsca():
    plik_pociagi = pobieranie_z_pliku_pociagi()
    plik_osoby = pobieranie_z_pliku_osoby()
    trasa = ["Wschodnia", "Stadion", "Powisle", "Srodmiescie", "Ochota"]
    osoba = Osoba("test", "testowy", True)
    pociag = Pociag("pociag_testowy", trasa, 2, True)
    zbyszek = Osoba("Zbyszek", "Testowy", True)
    pociag.kup("Wschodnia", "Powisle", 2, "B", osoba)
    pociag.kup("Wschodnia", "Powisle", 2, "C", osoba)
    assert pociag.slownik["Wschodnia"][1][1] == "X"
    assert pociag.slownik["Wschodnia"][1][1] == "X"
    assert pociag.slownik["Wschodnia"][1][2] == "X"
    assert pociag.slownik["Wschodnia"][1][2] == "X"
    pociag.kup("Powisle", "Ochota", 2, "B", zbyszek)
    assert pociag.slownik["Powisle"][1][1] == "X"
    assert pociag.slownik["Srodmiescie"][1][1] == "X"
    nadpisywanie_pociagi(plik_pociagi)
    nadpisywanie_osoby(plik_osoby)


def test_kup_miejsce_rzad0():
    plik_pociagi = pobieranie_z_pliku_pociagi()
    plik_osoby = pobieranie_z_pliku_osoby()
    trasa = ["Wschodnia", "Stadion", "Powisle", "Srodmiescie", "Ochota"]
    osoba = Osoba("test", "testowy", True)
    pociag = Pociag("pociag_testowy", trasa, 2, True)
    with pytest.raises(BladNieIstniejeTakiRzad):
        pociag.kup("Wschodnia", "Powisle", 0, "B", osoba)
    nadpisywanie_pociagi(plik_pociagi)
    nadpisywanie_osoby(plik_osoby)


def test_kup_miejsce_rzad_ujemny():
    plik_pociagi = pobieranie_z_pliku_pociagi()
    plik_osoby = pobieranie_z_pliku_osoby()
    trasa = ["Wschodnia", "Stadion", "Powisle", "Srodmiescie", "Ochota"]
    osoba = Osoba("test", "testowy", True)
    pociag = Pociag("pociag_testowy", trasa, 2, True)
    with pytest.raises(BladNieIstniejeTakiRzad):
        pociag.kup("Wschodnia", "Powisle", -1, "B", osoba)
    nadpisywanie_pociagi(plik_pociagi)
    nadpisywanie_osoby(plik_osoby)


def test_kup_miejsce_typA():
    plik_pociagi = pobieranie_z_pliku_pociagi()
    plik_osoby = pobieranie_z_pliku_osoby()
    trasa = ["Wschodnia", "Stadion", "Powisle", "Srodmiescie", "Ochota"]
    osoba = Osoba("test", "testowy", True)
    pociag = Pociag("pociag_testowy", trasa, 2, True)
    pociag.kup("Wschodnia", "Powisle", 1, "A", osoba)
    pociag.kup("Wschodnia", "Powisle", 2, "A", osoba)
    assert pociag.slownik['Wschodnia'][0][0] == 'X'
    assert pociag.slownik['Wschodnia'][1][0] == 'X'
    nadpisywanie_pociagi(plik_pociagi)
    nadpisywanie_osoby(plik_osoby)


def test_kup_miejsce_typB():
    plik_pociagi = pobieranie_z_pliku_pociagi()
    plik_osoby = pobieranie_z_pliku_osoby()
    trasa = ["Wschodnia", "Stadion", "Powisle", "Srodmiescie", "Ochota"]
    osoba = Osoba("test", "testowy", True)
    pociag = Pociag("pociag_testowy", trasa, 2, True)
    pociag.kup("Wschodnia", "Powisle", 1, "B", osoba)
    pociag.kup("Wschodnia", "Powisle", 2, "B", osoba)
    assert pociag.slownik['Wschodnia'][0][1] == 'X'
    assert pociag.slownik['Wschodnia'][1][1] == 'X'
    nadpisywanie_pociagi(plik_pociagi)
    nadpisywanie_osoby(plik_osoby)


def test_kup_miejsce_typC():
    plik_pociagi = pobieranie_z_pliku_pociagi()
    plik_osoby = pobieranie_z_pliku_osoby()
    trasa = ["Wschodnia", "Stadion", "Powisle", "Srodmiescie", "Ochota"]
    osoba = Osoba("test", "testowy", True)
    pociag = Pociag("pociag_testowy", trasa, 2, True)
    pociag.kup("Wschodnia", "Powisle", 1, "C", osoba)
    pociag.kup("Wschodnia", "Powisle", 2, "C", osoba)
    assert pociag.slownik['Wschodnia'][0][2] == 'X'
    assert pociag.slownik['Wschodnia'][1][2] == 'X'
    nadpisywanie_pociagi(plik_pociagi)
    nadpisywanie_osoby(plik_osoby)


def test_anuluj():
    plik_pociagi = pobieranie_z_pliku_pociagi()
    plik_osoby = pobieranie_z_pliku_osoby()
    trasa = ["Wschodnia", "Stadion", "Powisle", "Srodmiescie", "Ochota"]
    osoba = Osoba("test", "testowy", True)
    pociag = Pociag("pociag_testowy", trasa, 2, True)
    pociag.kup("Wschodnia", "Powisle", 1, "C", osoba)
    pociag.kup("Wschodnia", "Powisle", 2, "C", osoba)
    assert pociag.slownik['Wschodnia'][0][2] == 'X'
    assert pociag.slownik['Stadion'][0][2] == 'X'
    assert pociag.slownik['Wschodnia'][1][2] == 'X'
    pociag.anuluj("Wschodnia", "Powisle", 1, "C", osoba)
    assert pociag.slownik['Wschodnia'][0][2] == 'O'
    assert pociag.slownik['Stadion'][0][2] == 'O'
    nadpisywanie_pociagi(plik_pociagi)
    nadpisywanie_osoby(plik_osoby)


def test_anuluj_blad_poczatek():
    plik_pociagi = pobieranie_z_pliku_pociagi()
    plik_osoby = pobieranie_z_pliku_osoby()
    trasa = ["Wschodnia", "Stadion", "Powisle", "Srodmiescie", "Ochota"]
    osoba = Osoba("test", "testowy", True)
    pociag = Pociag("pociag_testowy", trasa, 2, True)
    pociag.kup("Wschodnia", "Powisle", 1, "C", osoba)
    with pytest.raises(BladPodanaOsobaNieMaTakiegoBiletu):
        pociag.anuluj("Blad", "Powisle", 1, "C", osoba)
    nadpisywanie_pociagi(plik_pociagi)
    nadpisywanie_osoby(plik_osoby)


def test_anuluj_blad_koniec():
    plik_pociagi = pobieranie_z_pliku_pociagi()
    plik_osoby = pobieranie_z_pliku_osoby()
    trasa = ["Wschodnia", "Stadion", "Powisle", "Srodmiescie", "Ochota"]
    osoba = Osoba("test", "testowy", True)
    pociag = Pociag("pociag_testowy", trasa, 2, True)
    pociag.kup("Wschodnia", "Powisle", 1, "C", osoba)
    with pytest.raises(BladPodanaOsobaNieMaTakiegoBiletu):
        pociag.anuluj("Wschodnia", "Blad", 1, "C", osoba)
    nadpisywanie_pociagi(plik_pociagi)
    nadpisywanie_osoby(plik_osoby)


def test_anuluj_blad_rzad():
    plik_pociagi = pobieranie_z_pliku_pociagi()
    plik_osoby = pobieranie_z_pliku_osoby()
    trasa = ["Wschodnia", "Stadion", "Powisle", "Srodmiescie", "Ochota"]
    osoba = Osoba("test", "testowy", True)
    pociag = Pociag("pociag_testowy", trasa, 2, True)
    pociag.kup("Wschodnia", "Powisle", 1, "C", osoba)
    with pytest.raises(BladPodanaOsobaNieMaTakiegoBiletu):
        pociag.anuluj("Wschodnia", "Powisle", 0, "C", osoba)
    nadpisywanie_pociagi(plik_pociagi)
    nadpisywanie_osoby(plik_osoby)


def test_anuluj_blad_typ():
    plik_pociagi = pobieranie_z_pliku_pociagi()
    plik_osoby = pobieranie_z_pliku_osoby()
    trasa = ["Wschodnia", "Stadion", "Powisle", "Srodmiescie", "Ochota"]
    osoba = Osoba("test", "testowy", True)
    pociag = Pociag("pociag_testowy", trasa, 2, True)
    pociag.kup("Wschodnia", "Powisle", 1, "C", osoba)
    with pytest.raises(BladPodanaOsobaNieMaTakiegoBiletu):
        pociag.anuluj("Wschodnia", "Powisle", 1, "Blad", osoba)
    nadpisywanie_pociagi(plik_pociagi)
    nadpisywanie_osoby(plik_osoby)


def test_anuluj_blad_osoba():
    plik_pociagi = pobieranie_z_pliku_pociagi()
    plik_osoby = pobieranie_z_pliku_osoby()
    trasa = ["Wschodnia", "Stadion", "Powisle", "Srodmiescie", "Ochota"]
    osoba = Osoba("test", "testowy", True)
    pociag = Pociag("pociag_testowy", trasa, 2, True)
    pociag.kup("Wschodnia", "Powisle", 1, "C", osoba)
    with pytest.raises(BladNieZdefiniowanaOsoba):
        pociag.anuluj("Wschodnia", "Powisle", 1, "C", 123)
    nadpisywanie_pociagi(plik_pociagi)
    nadpisywanie_osoby(plik_osoby)


def test_anuluj_rezerwacje_osoby_bez_rezerwacji():
    plik_pociagi = pobieranie_z_pliku_pociagi()
    plik_osoby = pobieranie_z_pliku_osoby()
    trasa = ["Wschodnia", "Stadion", "Powisle", "Srodmiescie", "Ochota"]
    osoba = Osoba("test", "testowy", True)
    darek = Osoba("Darek", "Marek")
    pociag = Pociag("pociag_testowy", trasa, 2, True)
    pociag.kup("Wschodnia", "Powisle", 1, "C", osoba)
    with pytest.raises(BladOsobaNieMaBiletow):
        pociag.anuluj("Wschodnia", "Powisle", 2, "A", darek)
    nadpisywanie_pociagi(plik_pociagi)
    nadpisywanie_osoby(plik_osoby)


def test_anuluj_nieistniejaca_rezerwacja():
    plik_pociagi = pobieranie_z_pliku_pociagi()
    plik_osoby = pobieranie_z_pliku_osoby()
    trasa = ["Wschodnia", "Stadion", "Powisle", "Srodmiescie", "Ochota"]
    osoba = Osoba("test", "testowy", True)
    pociag = Pociag("pociag_testowy", trasa, 2, True)
    pociag.kup("Wschodnia", "Powisle", 1, "C", osoba)
    with pytest.raises(BladPodanaOsobaNieMaTakiegoBiletu):
        pociag.anuluj("Wschodnia", "Powisle", 2, "C", osoba)
    nadpisywanie_pociagi(plik_pociagi)
    nadpisywanie_osoby(plik_osoby)


def test_anuluj_rezerwacje_innej_osoby():
    plik_pociagi = pobieranie_z_pliku_pociagi()
    plik_osoby = pobieranie_z_pliku_osoby()
    trasa = ["Wschodnia", "Stadion", "Powisle", "Srodmiescie", "Ochota"]
    osoba = Osoba("test", "testowy", True)
    darek = Osoba("Darek", "Testowy", True)
    pociag = Pociag("pociag_testowy", trasa, 2, True)
    pociag.kup("Wschodnia", "Powisle", 1, "C", osoba)
    pociag.kup("Wschodnia", "Powisle", 1, "A", darek)
    with pytest.raises(BladPodanaOsobaNieMaTakiegoBiletu):
        pociag.anuluj("Wschodnia", "Powisle", 2, "A", osoba)
    nadpisywanie_pociagi(plik_pociagi)
    nadpisywanie_osoby(plik_osoby)


def test_wyswietl_poczatek_nie_jest_przystankiem_trasy():
    plik_pociagi = pobieranie_z_pliku_pociagi()
    trasa = ["Wschodnia", "Stadion", "Powisle", "Srodmiescie", "Ochota"]
    pociag = Pociag("pociag_testowy", trasa, 2, True)
    with pytest.raises(BladPoczatekNieJestPrzystankiemTrasyPociagu):
        pociag.wyswietl('blad', 'Powisle')
    nadpisywanie_pociagi(plik_pociagi)


def test_wyswietl_koniec_nie_jest_przystankiem_trasy():
    plik_pociagi = pobieranie_z_pliku_pociagi()
    trasa = ["Wschodnia", "Stadion", "Powisle", "Srodmiescie", "Ochota"]
    pociag = Pociag("pociag_testowy", trasa, 2, True)
    with pytest.raises(BladKoniecNieJestPrzystankiemTrasyPociagu):
        pociag.wyswietl('Powisle', 'blad')
    nadpisywanie_pociagi(plik_pociagi)


def test_kup_BladNieZdefiniowanaOsoba():
    plik_pociagi = pobieranie_z_pliku_pociagi()
    trasa = ["Wschodnia", "Stadion", "Powisle", "Srodmiescie", "Ochota"]
    pociag = Pociag("pociag_testowy", trasa, 2, True)
    with pytest.raises(BladNieZdefiniowanaOsoba):
        pociag.kup("Wschodnia", "Powisle", 1, "B", 'Blad')
    nadpisywanie_pociagi(plik_pociagi)
