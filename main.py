import pickle
from dataclasses import dataclass
from typing import Self


@dataclass
class Briefcase:
    item1: str
    item2: str


@dataclass
class BiggerBriefcase(Briefcase):
    item3: str
    # also has `item1` and `item2`


class BusinessMan[BriefcaseType: Briefcase]:
    def __init__(self):
        self.item1 = ""
        self.item2 = ""

    @classmethod
    def from_briefcase(cls, briefcase: BriefcaseType) -> Self:
        businessman = cls()
        businessman.item1 = briefcase.item1
        businessman.item2 = briefcase.item2
        return businessman


class BiggerBusinessMan(BusinessMan[BiggerBriefcase]):
    def __init__(self):
        super().__init__()
        self.item3 = ""

    @classmethod
    def from_briefcase(cls, briefcase: BiggerBriefcase) -> Self:  # mypy error on this line
        # I want to be able to use the base class constructor
        businessman = super().from_briefcase(briefcase)
        businessman.item3 = briefcase.item3
        return businessman


# these two lines would really be run by some sort of JSON loader to create the dataclasses
basic_briefcase = Briefcase("notes", "cards")
bigger_briefcase = BiggerBriefcase("pens", "pencils", "letters")

# I'm not trying to use `from_briefcase()` polymorphically, it's supposed to be like a constructor
basic_businessman = BusinessMan.from_briefcase(basic_briefcase)
bigger_businessman = BiggerBusinessMan.from_briefcase(bigger_briefcase)

x = pickle.dumps(bigger_businessman)
print(x)
y = pickle.loads(x)
print(y.item1)
