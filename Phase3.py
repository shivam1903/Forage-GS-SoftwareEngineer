import hashlib
import itertools
import string

def generate_left_combinations(salt, length=2):
    """Generate combinations by adding characters to the left of the salt."""
    charset = string.ascii_letters + string.digits + string.punctuation
    for prefix in itertools.product(charset, repeat=length):
        yield ''.join(prefix) + salt

def generate_right_combinations(salt, length=2):
    """Generate combinations by adding characters to the right of the salt."""
    charset = string.ascii_letters + string.digits + string.punctuation
    for suffix in itertools.product(charset, repeat=length):
        yield salt + ''.join(suffix)

def generate_both_combinations(salt, length=2):
    """Generate combinations by adding characters to both sides of the salt."""
    charset = string.ascii_letters + string.digits + string.punctuation
    for prefix in itertools.product(charset, repeat=length):
        for suffix in itertools.product(charset, repeat=length):
            yield ''.join(prefix) + salt + ''.join(suffix)

def check_hash(hash_value, password):
    """Check if the hash of the generated password matches the target hash."""
    return hashlib.md5(password.encode()).hexdigest() == hash_value

def brute_force_attack(hash_value, salt):
    """Perform brute force attacks for all configurations."""
    # 1. Add 2 characters to the left
    for password in generate_left_combinations(salt):
        if check_hash(hash_value, password):
            return password

    # 2. Add 2 characters to the right
    for password in generate_right_combinations(salt):
        if check_hash(hash_value, password):
            return password

    # 3. Add 2 characters to both sides
    for password in generate_both_combinations(salt):
        if check_hash(hash_value, password):
            return password

    return None

def main():
    # Read hashes from the file
    with open('hashed_passwords.txt', 'r') as file:
        lines = file.readlines()

    for line in lines:
        salt, hash_value = line.strip().split(':')
        
        # Attempt to crack the hash
        cracked_password = brute_force_attack(hash_value, salt)
        
        if cracked_password:
            print(f"Successfully cracked the hash for {salt}: {cracked_password}")
        else:
            print(f"Failed to crack the hash for {salt}.")

if __name__ == '__main__':
    main()
