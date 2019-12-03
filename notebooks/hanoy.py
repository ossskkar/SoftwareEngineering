from typing import Dict, List

class Hanoi:
    def __init__(self, num_discs: int):
        self.num_discs = num_discs
        self._source = []
        self._temporary = []
        self._destination = []
        
        for i in range(num_discs, 0, -1):
            self._source.append(i)
    
    def draw(self):
        towers: Dict[str, List[int]] = {
            "SOURCE": self._source,
            "TEMPORARY": self._temporary,
            "DESTINATION": self._destination,
        }
        empty_level: str = "|"
        tower_base: str = "="

        for name, tower in towers.items():
            title = f"{name} Tower"
            print(title)
            print("=" * len(title) + "\n")

            print(empty_level)
            for disc in range(1, self.num_discs + 1):
                if disc in tower:
                    print("X" * disc)
                else:
                    print("|")
            print(tower_base * self.num_discs + "\n")
    
    def _hanoi(self, source: List[int], destination: List[int], temporary: List[int], num_discs: int):
        if num_discs == 1:
            # Just move disc from source to destination
            destination.append(source.pop())
        else:
            # Move N - 1 discs from the source to the temporary tower.
            # This means we "swap" destination and temporary
            self._hanoi(
                source=source,
                destination=temporary,
                temporary=destination,
                num_discs=num_discs - 1,
            )
            # Move the remaining disc from the source to the destination
            self._hanoi(
                source=source,
                destination=destination,
                temporary=temporary,
                num_discs=1,
            )
            # Finally, move the N - 1 discs from the first step to the destination.
            # This means that we are swapping the source and the temporary towers.
            self._hanoi(
                source=temporary,
                destination=destination,
                temporary=source,
                num_discs=num_discs - 1,
            )
    
    def solve(self):
        self._hanoi(
            source=self._source,
            destination=self._destination,
            temporary=self._temporary,
            num_discs=self.num_discs,
        )
    
    def draw_and_solve(self):
        print("Initial State:\n")
        self.draw()
        self.solve()
        print("\n\nFinal State:\n")
        self.draw()
