from rsa_key import get_key

class RSA:
    def get_keys(self):
        p = get_key()
        q = get_key()

        while p == q:
            q = get_key()
        return {'p': p, 'q': q}
        
a = RSA().get_keys()

print(a)