import random 
dice = random.SystemRandom()



def single_test(n, a):
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

def is_prime(n, r=64):
    if n % 2 == 0:
        return False
    
    for i in range(r):
        a = dice.randrange(2, n-2)

        if not single_test(n, a):
            return False 
    return True 

def get_key(n_bits=1024):
    while True:
        random_number = dice.getrandbits(n_bits)
        if(is_prime(random_number)):
            return random_number 
    

