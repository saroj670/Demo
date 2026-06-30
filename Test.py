from abc import ABC, abstractmethod
class Flight(ABC):
    def __init__(self):
        print("This is a flight class")
    @abstractmethod
    def fly(self):
        print("Flying in the sky")
    @abstractmethod
    def run(self):
        print("Running on the ground")
class Airplane(Flight):
    def __init__(self):
        print("This is an airplane class")
    def fly(self):
        print("Flying in the sky")
    def run(self):
        print("Running on the ground")

a = Airplane()
a.fly()
a.run()
