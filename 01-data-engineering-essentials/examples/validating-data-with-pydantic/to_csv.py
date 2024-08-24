import csv
import json
from decimal import Decimal
from typing import Iterable

from pydantic import BaseModel


class Person(BaseModel):
    """ Person domain model. """
    name: str
    height: Decimal


class PersonOut(Person):
    """ Person model used for serialization. """
    class Config:
        # https://docs.pydantic.dev/usage/exporting_models/#json_encoders
        json_encoders = { Decimal: lambda v: float(round(v, 2)) }


def store(persons: Iterable[Person]):
    fieldnames = list(Person.schema()["properties"].keys())

    with open("test.csv", "w") as fp:
        writer = csv.DictWriter(fp, fieldnames=fieldnames)
        writer.writeheader()
        for person in persons:
            writer.writerow(json.loads(PersonOut(**person.dict()).json()))


if __name__=="__main__":
    person = Person(name='test', height=1.743)

    # https://docs.pydantic.dev/usage/exporting_models/
    print(person)
    print(person.dict())
    print(person.json())

    person_out = PersonOut(name='test', height=1.743)
    print("PersonOut: ", person_out.json())

    persons = [person]
    store(persons)
