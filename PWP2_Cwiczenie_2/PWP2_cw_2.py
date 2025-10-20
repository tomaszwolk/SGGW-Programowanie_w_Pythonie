"""Ćwiczenia praktyczne 2 - deklaracja modeli i tworzenie bazy danych
• W nowym projekcie (nie powiązanym z poprzednim zadaniem) zainstaluj SQLAlchemy, przygotuj nowe połączenie z bazą
    danych SQLite.
• Stwórz dwie tabele:
    1. Experiment z kolumnami:
        id: int,
        title: string,
        created_at: datetime,
        type: int,
        finished: boolean(domyślnie False).
    2. DataPointz kolumnami:
        id: int,
        real_value: float,
        target_value: float.
• Stwórz wszystkie zdefiniowane tabele wraz z plikiem bazy danych.
• Na tym etapie jeszcze nie definiujmy relacji w tabelach.
"""

from datetime import datetime
from random import random
from typing import List, Optional

from sqlalchemy import (
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    create_engine,
    delete,
    select,
    update,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Experiment(Base):
    __tablename__ = "experiment"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(30))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    type: Mapped[int] = mapped_column(Integer)
    finished: Mapped[bool] = mapped_column(Boolean, default=False)

    data_points: Mapped[List["DataPoint"]] = relationship(back_populates="experiment")

    def __repr__(self) -> str:
        return f"Experiment(id={self.id}, title={self.title}, created_at={self.created_at}, " \
            "type={self.type}, finished={self.finished})"


class DataPoint(Base):
    __tablename__ = "datapoint"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    real_value: Mapped[float] = mapped_column(Float)
    target_value: Mapped[float] = mapped_column(Float)

    experiment_id: Mapped[Optional[int]] = mapped_column(ForeignKey("experiment.id"))
    experiment: Mapped["Experiment"] = relationship(back_populates="data_points")

    def __repr__(self) -> str:
        return f"DataPoint (id={self.id}, real_value={self.real_value:.4f}, " \
            "target_value={self.target_value:.4f})"


engine = create_engine("sqlite:///test.db", echo=False)
print(engine.connect())
Base.metadata.create_all(engine)

"""Ćwiczenia praktyczne 3
• Rozszerz program z poprzednich ćwiczeń by:
    1. Dodał 2 wiersze do tabeli Experiments.
    2. Dodał 10 wierszy do tabeli DataPoints.
    3. Pobrał dodane przed chwilą dane i wyświetlił informację o nich.
    4. Zaktualizował wszystkie wierszy Experiments poprzez ustawienie finished na True.
    5. Usunął wszystkie wiersze z obu tabel.
Wartości przy dodawaniu mogą być losowe, można użyć np.:
        import random
        random.random() # 0.6061456729486188
"""
# Dodanie 2 wierszy do tabeli Experiments
with Session(engine) as session:
    session.add_all(
        [
            Experiment(title="Experiment 1", type=0),
            Experiment(title="Experiment 2", type=1),
        ]
    )
    session.commit()

# Dodanie 10 wierszy do tabeli DataPoints
with Session(engine) as session:
    datapoints = []
    for _ in range(10):
        datapoint = DataPoint(real_value=random(), target_value=random())
        datapoints.append(datapoint)

    session.add_all(datapoints)
    session.commit()

# Pobierz dodane przed chwilą dane i wyświetl informacje o nich
with Session(engine) as session:
    exp_stmt = select(Experiment)
    experiments = session.scalars(exp_stmt).all()
    print("\nExperiment table:")
    for experiment in experiments:
        print(experiment)

    dp_stmt = select(DataPoint)
    datapoints = session.scalars(dp_stmt).all()  # type: ignore
    print("\nData point table:")
    for datapoint in datapoints:
        print(datapoint)

# Zaktualizował wszystkie wierszy Experiments poprzez ustawienie finished na True
with Session(engine) as session:
    stmt = update(Experiment).values(finished=True)
    session.execute(stmt)
    session.commit()

    # Sprawdzenie czy wszsytkie wiersze zostały zaktualizowane
    query = select(Experiment)
    experiments = session.scalars(query).all()

    print("\nZaktualizowana tabela Experiments:")
    for experiment in experiments:
        print(experiment)

# Usuń wszystkie wiersze z obu tabel.
with Session(engine) as session:
    del_exp_stmt = delete(Experiment)
    session.execute(del_exp_stmt)

    del_dp_stmt = delete(DataPoint)
    session.execute(del_dp_stmt)

    session.commit()

    # Sprawdzenie czy tabele są puste
    exp_count = session.scalar(select(Experiment))
    dp_count = session.scalar(select(DataPoint))

    print("\nIlość rekordów po wykonaniu delete")
    print(f"Experiments records: {exp_count}")
    print(f"Data Points records: {dp_count}")

"""Ćwiczenie praktyczne 4
• Usuń poprzednią bazę danych (usuń sam plik bazy danych).
• Dodaj relację jeden do wielu tak, by jeden Experiment posiadał wiele DataPoint'ów.
• Odpal program i stwórz bazę danych ponownie.
"""

"""Ćwiczenie praktyczne 5 - relacja wiele-do-wielu oraz migracja bazy danych
• Usuń poprzednią bazę danych (usuń sam plik bazy danych).
• Zainstaluj i zainicjuj Alembic w programie z poprzednich ćwiczeń.
• Wygeneruj pierwszą migrację i zaaplikuj ją na bazie danych.
• Dodaj nową tabelę Subject z kolumnami: id: int, gdpr_accepted: bool(domyślnie na False).
• Stwórz relację wiele-do-wielu pomiędzy Subject i Experiment.
• Wygeneruj nową migrację i zaaplikuj ją na bazie danych.
"""
