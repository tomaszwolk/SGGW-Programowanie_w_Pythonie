import requests
from pathlib import Path

"""Ćwiczenie I - instalacja Poetry, stworzenie nowej aplikacji i definicja funkcji
    • Zainstaluj Poetry i stwórz nową aplikację.
    • Zainstaluj bibliotekę requests.
    • Stwórz plik main.py w którym zdefiniuj funkcję pobierającą plik z podanego URL i zapisującą pobrany plik na dysku o podanej nazwie.
    • Upewnij się, że funkcja oczekuje dwa parametry: adres url do pobrania pliku oraz nazwę pliku do zapisywania na dysku.
    • Jeśli nazwa pliku nie została podana, powinna domyślnie wynosić latest.txt.
    • URL z którego należy pobrać plik: https://oleksandr-fedoruk.com/wp-content/uploads/2025/10/sample.csv
"""
URL = "https://oleksandr-fedoruk.com/wp-content/uploads/2025/10/sample.csv"
# URL = "https://httpbin.org/status/403"
# URL = "https://httpbin.org/status/404"

PATH = Path(__file__).parent / "latest.csv"


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


def get_data(url: str, save_path: str = "latest.csv"):
    response = requests.get(url)
    if response.status_code == 404:
        raise NotFoundError("File not found", response.status_code)
    elif response.status_code == 403:
        raise AccessDeniedError("Access denied", response.status_code)

    with open(save_path, "wb") as file:
        file.write(response.content)


# def process_data(path: Path):
#     with open(path, "r") as file:
#         for line in file:
#             values = line.split(",")
#             print(values)
# with open(values.csv, "w") as values_file:
#     pass

# a = process_data(PATH)
# print(a)


def process_data(path: Path):
    pass


if __name__ == "__main__":
    try:
        get_data(URL)
    except NotFoundError as e:
        print(e)
    except AccessDeniedError as e:
        print(e)
