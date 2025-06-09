from enum import Enum


class PatientSorted(str, Enum):
    weight = ("weight",)
    height = ("height",)
    bmi = "bmi"
