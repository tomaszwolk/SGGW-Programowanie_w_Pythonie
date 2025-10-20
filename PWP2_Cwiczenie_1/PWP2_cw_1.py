class Logger:
    """1. Utwórz klasę Logger, która:
    • przy wejściu do kontekstu (__enter__) wypisuje „Start sekcji logowania”,
    • przy wyjściu(__exit__) wypisuje „Koniec sekcji logowania”.
    • Użyj jej w bloku with, wypisując coś w środku.
    """
    def __init__(self):
        pass

    def __enter__(self):
        print("Start sekcji logowania")

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Koniec sekcji logowania")
        return False


print("Test Logger.")

with Logger() as logger:
    print("\tTesting Logger class")

print("-" * 40, "\n")


class FileWriter:
    """2. Napisz klasę FileWriter, która:
    • w __init__ przyjmuje ścieżkę do pliku,
    • w __enter__ otwiera plik do zapisu i zwraca uchwyt (file handle),
    • w __exit__ zamyka plik niezależnie od tego, czy wystąpił wyjątek.
    • Przetestuj zapis tekstu do pliku w bloku with.
    """
    def __init__(self, path):
        self.path = path
        self.file = None

    def __enter__(self):
        self.file = open(self.path, 'w')
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            self.file.close()
        return False


print("Test FileWriter.")
filename = "test_FileWriter.txt"
with FileWriter(filename) as file:
    file.write("Test 1\n")
    file.write("Test 2\n")

print(f"File saved as {filename}")
print("-" * 40, "\n")


class FileWriter2:
    """3. Zmodyfikuj FileWriter, tak by:
    • gdy w środku bloku with wystąpi wyjątek, __exit__ wypisał komunikat: „Błąd podczas zapisu: <treść wyjątku>”.
    • wyjątek nie był tłumiony(czyli dalej przerywał program).
    """
    def __init__(self, path):
        self.path = path
        self.file = None

    def __enter__(self):
        self.file = open(self.path, 'w')
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            self.file.close()

        if exc_type:
            print(f"Błąd podczas zapisu: {exc_val}")
        return False


print("Test FileWriter2.")
filename2 = "test_FileWriter2"
try:
    with FileWriter2(filename2) as file:
        file.write("Test 1 FileWriter2\n")
        raise ValueError("Value Error")
except ValueError as e:
    print(f"File Writer 2 error: {e}")

print("-" * 40, "\n")


class SafeDivision:
    """4. Napisz klasę SafeDivision, która:
    • w __enter__ zwraca samą siebie.
    • ma metodę divide(a, b) dzielącą liczby,
    • w __exit__ tłumi wyjątki typu ZeroDivisionError, wypisując komunikat 'Nie można podzielić przez zero.
    """
    def __init__(self):
        pass

    def __enter__(self):
        return self

    def divide(self, a, b):
        return a / b

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is ZeroDivisionError:
            print("Nie można dzielić przez zero.")
            return True
        return False


print("Test SafeDivision nr 1. Bez błędu.")
with SafeDivision() as sd:
    result = sd.divide(5, 2)
    print(f"Result of SafeDivision test 1: {result}")

print("\nTest SafeDivision nr 2. Z błędem.")
with SafeDivision() as sd:
    sd.divide(5, 0)
