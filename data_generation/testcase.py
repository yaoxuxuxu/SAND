
import random
import math

class Generator:
    """
    Generator class to produce test cases for the Omega-Resonant Integer problem.
    The problem requires finding the n-th integer x such that:
    1. omega(x) == k
    2. sigma(x) % phi(x) == 0
    3. P(x) (product of non-zero digits) is a perfect power a^b (b > 1)
    4. x > k^n
    """

    def _get_p_x(self, x: int) -> int:
        """Calculates the product of non-zero digits of x."""
        prod = 1
        for digit in str(x):
            d = int(digit)
            if d != 0:
                prod *= d
        return prod

    def _is_perfect_power(self, m: int) -> bool:
        """Checks if m is a perfect power a^b where a > 0 and b > 1."""
        if m < 1:
            return False
        if m == 1:
            return True  # 1^2 = 1
        
        # Check for b from 2 up to log2(m)
        for b in range(2, m.bit_length() + 1):
            # Use root approximation
            a = round(m**(1/b))
            if a < 1: continue
            if a**b == m:
                return True
        return False

    def _get_metrics(self, x: int):
        """Returns (omega, phi, sigma) for a given integer x."""
        omega = 0
        phi = x
        sigma = 1
        temp = x
        d = 2
        while d * d <= temp:
            if temp % d == 0:
                omega += 1
                phi -= phi // d
                p_pow = d
                p_sum = 1 + d
                temp //= d
                while temp % d == 0:
                    p_pow *= d
                    p_sum += p_pow
                    temp //= d
                sigma *= p_sum
            d += 1
        if temp > 1:
            omega += 1
            phi -= phi // temp
            sigma *= (1 + temp)
        return omega, phi, sigma

    def _solve(self, n: int, k: int) -> int:
        """Brute force search to find the n-th resonant integer."""
        count = 0
        x = (k ** n) + 1
        
        while True:
            # Constraint 3: Digital Product (Fastest check)
            px = self._get_p_x(x)
            if self._is_perfect_power(px):
                # Constraint 1 & 2: Prime Factorization and Totient-Divisor
                omega, phi, sigma = self._get_metrics(x)
                if omega == k and sigma % phi == 0:
                    count += 1
                    if count == n:
                        return x
            x += 1

    def main(self) -> dict:
        """
        Generates a random test case.
        Returns: {'input': [n, k], 'output': [x]}
        """
        # We limit n and k for the generator to ensure it returns in a reasonable time,
        # as the search space for these specific constraints can be very sparse.
        n = random.randint(1, 5)
        k = random.randint(1, 3)
        print(n,k)
        result = self._solve(n, k)
        
        return {
            'input': [n, k],
            'output': [result]
        }

# Example of how to use the generator:
if __name__ == "__main__":
    gen = Generator()
    # Generate 3 random test cases
    for i in range(3):
        print(f"Test Case {i+1}: {gen.main()}")
