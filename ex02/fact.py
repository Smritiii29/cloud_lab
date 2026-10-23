
import Pyro4
from collections import Counter

@Pyro4.expose
class MathOperations:

    def factorial(self, n):
        if n < 0:
            return "Factorial is not defined for negative numbers"

        result = 1
        for i in range(1, n + 1):
            result *= i

        return result

    def mode(self, arr):
        if not arr:
            return "Array is empty"

        counts = Counter(arr)
        highest = max(counts.values())

        # Return the element with the highest frequency
        for element in arr:
            if counts[element] == highest:
                return element
