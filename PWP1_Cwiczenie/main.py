import requests
from pathlib import Path

"""Ćwiczenie I - instalacja Poetry, stworzenie nowej aplikacji i definicja funkcji
    • Zainstaluj Poetry i stwórz nową aplikację.
    • Zainstaluj bibliotekę requests.
    • Stwórz plik main.py w którym zdefiniuj funkcję pobierającą plik z podanego URL i zapisującą 
        pobrany plik na dysku o podanej nazwie.
    • Upewnij się, że funkcja oczekuje dwa parametry: adres url do pobrania pliku oraz nazwę pliku 
        do zapisywania na dysku.
    • Jeśli nazwa pliku nie została podana, powinna domyślnie wynosić latest.txt.
    • URL z którego należy pobrać plik: https://oleksandr-fedoruk.com/wp-content/uploads/2025/10/sample.csv
"""
URL = "https://oleksandr-fedoruk.com/wp-content/uploads/2025/10/sample.csv"
# URL = "https://httpbin.org/status/403"
# URL = "https://httpbin.org/status/404"

FILE_PATH = Path(__file__).parent / "latest.csv"

"""Ćwiczenie II - dodanie obsługi wyjątków
• W aplikacji z poprzedniego ćwiczenia zdefiniuj klasę wyjątku dziedziczącą po Exception.
• Stwórz dwie klasy wyjątków dziedziczące po tej klasie - NotFoundError i AccessDeniedError.
• Dodaj obsługę kodów odpowiedzi serwera 404 i 403 by pojawienie się takich kodów rzucało odpowiedni wyjątek.
"""


class NotFoundError(Exception):
    def __init__(self, message: str, error_code: int):
        self.message = message
        super().__init__(self.message)
        self.error_code = error_code

    def __str__(self):
        return f"{self.message} (Error Code: {self.error_code})"


class AccessDeniedError(Exception):
    def __init__(self, message: str, error_code: int):
        self.message = message
        super().__init__(self.message)
        self.error_code = error_code

    def __str__(self):
        return f"{self.message} (Error Code: {self.error_code})"


def get_data(url: str, save_path: Path | str = "latest.csv"):
    response = requests.get(url)
    if response.status_code == 404:
        raise NotFoundError("File not found", response.status_code)
    elif response.status_code == 403:
        raise AccessDeniedError("Access denied", response.status_code)

    with open(save_path, "wb") as file:
        file.write(response.content)
    print(f"File saved as {save_path}")


"""Ćwiczenie III - transformacja plików
• Przejrzyjmy się pobieranym przez nas plikom - są to pliki CSV, zawierające 8 kolumn z liczbami.
    Kolumna o indeksie 0 oznacza numer porządkowy.
• Niektóre wartości nie są wypełnione, zamiast nich są wpisane myślniki.
• Napisz klasę która symuluje prosty proces ETL korzystając z generatorów:
    • Wczytuje pobrany plik linijka po linijce
    • Dla każdej linijki liczy sumę, średnią oraz zapsujeindeksy brakujących wartości (użyj list comprehension)
    • Zapisuje dwa pliki CSV:
        • values.csv z kolumnami: numer porządkowy, suma, średnia.
        • missing_values.csv z kolumnami: numer porządkowy oraz indeksami kolumn ze myślnikami zamiast wartości.
"""


class ETL:
    def __init__(self):
        self.lines = None

    def open_file(self, path: Path):
        with open(path) as file:
            self.lines = [line.strip() for line in file]

    def count_sum_avg(self, save_path: Path | str = "values.csv"):
        if self.lines is None:
            print("Use open_file method first.")
            return

        values = [[float(x) for x in line.split(",") if x != "-"] for line in self.lines]
        results = [(int(value[0]), x := sum(value[1:]), x / (len(value) - 1)) for value in values]

        with open(save_path, "w") as file:
            file.write("\n".join("%s,%s,%s" % result for result in results))
        print(f"File saved as {save_path}")

    def missing_values_idx(self, save_path: Path | str = "missing_values.csv"):
        if self.lines is None:
            print("Use open_file method first.")
            return

        missing_values = [(line[0], [i for i, v in enumerate(line.split(",")) if v == "-"]) for line in self.lines]
        with open(save_path, "w") as file:
            file.write("\n".join(self._tuple_to_string(result) for result in missing_values))
        print(f"File saved as {save_path}")

    def _tuple_to_string(self, item: tuple[str, list]) -> str:
        string = item[0]
        for element in item[1]:
            string += "," + str(element)
        return string


if __name__ == "__main__":
    try:
        print(f"Downloading file from {URL}")
        get_data(URL)
    except NotFoundError as e:
        print(e)
    except AccessDeniedError as e:
        print(e)

    etl = ETL()
    etl.open_file(FILE_PATH)
    print("\nCounting sum and average values.")
    etl.count_sum_avg()
    print("\nSearching for missing values.")
    etl.missing_values_idx()
