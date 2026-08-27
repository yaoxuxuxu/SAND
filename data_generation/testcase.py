import random

class Generator:
    """
    Generator class to produce test cases for the Transcendental Recursive Summation problem.
    Since the problem requires an O(log^2 N) or O(sqrt(N)) solution for N up to 10^16,
    the reference implementation in this generator uses a linear approach.
    To ensure the generator returns the output in a reasonable time, N is capped at 10^6.
    """

    def is_prime(self, n):
        """Helper function to check if a number is prime."""
        if n < 2: return False
        if n == 2 or n == 3: return True
        if n % 2 == 0: return False
        for i in range(3, int(n**0.5) + 1, 2):
            if n % i == 0:
                return False
        return True

    def get_random_prime(self, low, high):
        """Generates a random prime number within the specified range."""
        while True:
            p = random.randint(low, high)
            if self.is_prime(p):
                return p

    def main(self):
        """
        Generates a single test case.
        Returns:
            dict: {'input': [N, K, M], 'output': [S]}
        """
        # Constraints: 1 <= N <= 10^16, 1 <= K <= 10^9, 10^9 < M < 2*10^9 (Prime)
        # We limit N to 10^6 for the reference output to be computable in reasonable time.
        N = random.randint(1, 10**6) 
        K = random.randint(1, 10**9)
        M = self.get_random_prime(10**9 + 1, 2 * 10**9 - 1)
        
        # Reference implementation to calculate the output S(N, K, M)
        # f(n) definition:
        # f(0) = 0, f(1) = 1
        # n = 2k: f(n) = (f(k) + popcount(n)) mod (10^9 + 7)
        # n = 2k+1: f(n) = (f(k) XOR f(k+1)) + rev(n)
        
        f = [0] * (N + 1)
        f[0] = 0
        if N >= 1:
            f[1] = 1
        
        MOD_F = 10**9 + 7
        
        for i in range(2, N + 1):
            if i % 2 == 0:
                # Even case
                k = i // 2
                popcount = bin(i).count('1')
                f[i] = (f[k] + popcount) % MOD_F
            else:
                # Odd case
                k = i // 2
                # rev(n) reverses bits based on minimum bit-length
                # bin(i)[2:] gives the binary string without '0b'
                rev_n = int(bin(i)[2:][::-1], 2)
                f[i] = (f[k] ^ f[k+1]) + rev_n
        
        # Calculate S(N, K, M) = sum(f(i)^K mod M)
        total_sum = 0
        for i in range(1, N + 1):
            # Using modular exponentiation for f(i)^K mod M
            total_sum = (total_sum + pow(f[i], K, M)) % M
            
        return {
            'input': [N, K, M],
            'output': [total_sum]
        }

# Example usage:
gen = Generator()
print(gen.main())
