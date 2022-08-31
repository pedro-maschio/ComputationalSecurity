import random 
dice = random.SystemRandom()

class Key:  

    def single_test(self, n, a):
        exp = n - 1
        
        while exp % 2 == 0:
            exp //= 2
        
        if pow(a, exp, n) == 1:
            return True     
        
        while exp < n - 1:
            if pow(a, exp, n) == n-1:
                return True 
            exp *= 2
        return False 

    def is_prime(self, n, r=64):
        
        for i in range(r):
            a = dice.randrange(2, n-2)

            if not self.single_test(n, a):
                return False 
        return True 

    def get_key(self, n_bits=1024):
        while True:
            random_number = dice.getrandbits(n_bits)
            if(self.is_prime(random_number)):
                return random_number 
    

