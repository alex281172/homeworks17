from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

engine = create_engine('sqlite:///city_new_test.sqlite', echo=True)
Base = declarative_base()


class SkillTest(Base):
    __tablename__ = 'skill_city_new_test'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    percent = Column(Integer, nullable=True)
    count = Column(Integer, nullable=True)

    def __init__(self, name, percent, count):
        self.name = name
        self.percent = percent
        self.count = count

    def __str__(self):
        return f'{self.id}) {self.name}: {self.percent}: {self.count}'


# Создание таблицы

Base.metadata.create_all(engine)


class CityTest(Base):
    __tablename__ = 'city_new_test'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    percent = Column(Integer, nullable=True)
    count = Column(Integer, nullable=True)

    def __init__(self, name, percent, count):
        self.name = name
        self.percent = percent
        self.count = count

    def __str__(self):
        return f'{self.id}) {self.name}: {self.percent}: {self.count}'
