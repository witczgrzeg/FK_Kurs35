"""
Stwórz system zarządzania księgozbiorem bibliotecznym, który pozwoli na monitorowanie przepływu książek oraz śledzenie budżetu biblioteki.
Po uruchomieniu systemu użytkownik otrzymuje listę komend do wyboru:
- doładowanie
- wypożycz
- zakup
- bieżący_stan
- zestawienie
- szczegóły_książki
- dziennik
- zakończ
Funkcje po wywołaniu danych komend są następujące:
1. doładowanie - Umożliwia dodanie środków do budżetu biblioteki lub ich odjęcie.
2. wypożycz - Rejestruje wypożyczenie książki przez czytelnika. System żąda podania numeru ISBN. Koszt wypożyczenia jest dodawany do budżetu.
3. zakup - Rejestruje zakup nowych książek dla biblioteki. System pyta o tytuł książki, koszt zakupu i liczbę egzemplarzy. Zakupione książki są dodawane do zbioru, a środki są odprowadzane z budżetu, który nie może być negatywny po transakcji.
4. bieżący_stan - Wyświetla aktualny stan środków finansowych.
5. zestawienie - Podsumowuje cały księgozbiór biblioteki wraz z cenami zakupu i ich ilością.
6. szczegóły_książki - Wyświetla dostępność i dane dotyczące pojedynczej książki po wpisaniu numeru ISBN.
7. dziennik - Przegląd historii transakcji. Podając wartości "od" i "do", system wyświetla zapisane działania w podanym zakresie. W przypadku pustych pól lub wartości spoza zakresu, użytkownik jest informowany o błędzie i wyświetlana jest liczba wszystkich zarejestrowanych transakcji.
8. zakończ - Kończy działanie programu.
**Inne wymagania:**
- System działa do momentu wybrania komendy zakończ.
- Operacje doładowanie, wypożycz oraz zakup są zapisywane dla późniejszej referencji przy użyciu komendy dziennik.
- Po każdej komendzie system wyświetla ponownie listę dostępnych opcji i prosi o wybór kolejnej.
- Ochrona przed błędami użytkownika, takimi jak wpisywanie błędnych danych czy żądanie zakupu na wartości ujemne.
"""
# bedziemy dzialali w jednej petli while True:
# lista ksiazek
lista_ksiazek = [{
        "tytul": "Harry Potter i Kamień Filozoficzny",
        "autor": "J.K. Rowling",
        "rok_wydania": 1997,
        "cena": 39.99,
        "ilosc_na_stanie": 5,
        "kategoria": "fantasy",
        "ilosc": 5,
        "ISBN": "978-3-16-148410-0",
    },
    {
        "tytul": "Władca Pierścieni: Drużyna Pierścienia",
        "autor": "J.R.R. Tolkien",
        "rok_wydania": 1954,
        "cena": 49.99,
        "ilosc_na_stanie": 3,
        "kategoria": "fantasy",
        "ilosc": 3,
        "ISBN": "978-0-261-10221-7",
    },
    {
        "tytul": "Zbrodnia i kara",
        "autor": "Fiodor Dostojewski",
        "rok_wydania": 1866,
        "cena": 29.99,
        "ilosc_na_stanie": 0,
        "kategoria": "klasyka",
        "ilosc": 2,
        "ISBN": "978-0-14-044913-6",
    }
]
saldo = 10000
historia = ["Sprzedaż książki: Harry Potter i Kamień Filozoficzny, 39.99, 5 sztuk", "Zakup książki: Władca Pierścieni: Drużyna Pierścienia, 49.99, 3 sztuki"]
print("Witaj w systemie zarządzania księgozbiorem bibliotecznym!")
while True:
    print("Wybierz jedną z poniższych opcji(Podaj numer):")
    komenda = input("""
        1. doładowanie
        2. wypożycz
        3. zakup
        4. bieżący_stan
        5. zestawienie
        6. szczegóły_książki
        7. dziennik
        8. zakończ
    """)
    match komenda:
        case "1":
            kwota = float(input("Podaj kwotę o jaką chcesz zmienić saldo: "))
            if saldo + kwota < 0:
                print("Nie możesz ustawić salda na wartość ujemną.")
            else:
                saldo += kwota
            print(saldo)
        case "2":
            isbn = input("Podaj numer ISBN książki do wypożyczenia: ")
            ksiazka_znaleziona = False
            for ksiazka in lista_ksiazek:
                if ksiazka.get("ISBN") == isbn:
                    ksiazka_znaleziona = True
                    if ksiazka["ilosc_na_stanie"] <= 0:
                        print("Nie ma tej książki na stanie.")
                        break
                    ksiazka["ilosc_na_stanie"] -= 1
                    saldo += 10 # koszt wypożyczenia książki
                    historia.append(f"Wypożyczenie książki: {ksiazka['tytul']}, {ksiazka['autor']}, 1 sztuka")
                    break
            if not ksiazka_znaleziona:
                print("Taka książka nie istnieje.")
        case "3":
            tytul = input("Podaj tytuł książki: ")
            autor = input("Podaj autora książki: ")
            koszt = float(input("Podaj koszt zakupu książki: "))
            ilosc = int(input("Podaj ilość egzemplarzy: "))
            kategoria = input("Podaj kategorie książki: ")
            numer_isbn = input("Podaj numer ISBN książki: ")
            rok_wydania = int(input("Podaj rok wydania książki: "))
            if saldo - (koszt * ilosc) < 0:
                print("Nie możesz ustawić salda na wartość ujemną.")
                historia.append(f"Próba zakupu książki: {tytul}, {koszt}, {ilosc} sztuk - nieudana")
                continue
            else:
                saldo -= (koszt * ilosc)
            znaleziono_ksiazke = False
            for ksiazka in lista_ksiazek:
                if ksiazka.get("ISBN") == numer_isbn:
                    znaleziono_ksiazke = True
                    ksiazka["ilosc_na_stanie"] += ilosc
                    break
            if not znaleziono_ksiazke:
                lista_ksiazek.append({
                    "tytul": tytul,
                    "autor": autor,
                    "cena": koszt,
                    "ilosc_na_stanie": ilosc,
                    "ilosc": ilosc,
                    "kategoria": kategoria,
                    "ISBN": numer_isbn,
                    "rok_wydania": rok_wydania,
                })
                historia.append(f"Zakup książki: {tytul}, {koszt}, {ilosc} sztuk")
        case "5":
            print(f"Zestawienie księgozbioru:{lista_ksiazek}")
        case "7":
            od = input("Podaj wartość 'od' (numer transakcji): ")
            do = input("Podaj wartość 'do' (numer transakcji): ")
            if od:
                od = int(od)
            else:
                od = 0
            if do:
                do = int(do)
            else:
                do = len(historia)
            print(historia[od:do])
        case "8":
            print("Zakończono działanie programu.")
            break
    # if komenda in ("8", "zakoncz", "zakończ"):
    #     print("Zakończono działanie programu.")
    #     break
