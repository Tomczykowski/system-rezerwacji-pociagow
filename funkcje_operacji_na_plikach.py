import json


def pobieranie_z_pliku_osoby():
    """
    Pobiera i zwraca dane z pliku osoby.json.
    """
    with open('osoby.json', 'r') as reader:
        osoby = json.load(reader)
    return osoby


def pobieranie_z_pliku_pociagi():
    """
    Pobiera i zwraca dane z pliku pociagi.json.
    """
    with open('pociagi.json', 'r') as reader:
        dane = json.load(reader)
    return dane


def nadpisywanie_pociagi(dane):
    """
    Nadpisuje plik pociagi.json podanym argumentem.
    """
    with open('pociagi.json', 'w') as writer:
        json.dump(dane, writer, indent=3)


def nadpisywanie_osoby(dane):
    """
    Nadpisuje plik osoby.json podanym argumentem.
    """
    with open('osoby.json', 'w') as writer:
        json.dump(dane, writer, indent=2)
