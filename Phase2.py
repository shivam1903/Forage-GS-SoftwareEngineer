import subprocess
import time

def check_hash_in_potfile(hash_value):
    """Check if the hash exists in the potfile using Hashcat."""
    command = f"hashcat -m 0 -a 0 {hash_value} darkweb2017-top10000.txt --show"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout.strip()

def crack_hash_with_hashcat(username, hash_value):
    """Crack the hash using Hashcat if not found in the potfile."""
    # Create a combined wordlist that includes username variations
    with open('xato-net-10-million-passwords.txt', 'r') as wordlist:
        with open('custom_wordlist.txt', 'w') as custom_list:
            for line in wordlist:
                password = line.strip()
                custom_list.write(f"{username}{password}\n")  # Prepend username
                custom_list.write(f"{password}{username}\n")  # Append username
                custom_list.write(f"{password}\n")  # Original password
            
    # Run Hashcat with the custom wordlist
    command = f"hashcat -m 0 -a 0 {hash_value} custom_wordlist.txt"
    subprocess.run(command, shell=True)
    time.sleep(10)  # Wait for some time to ensure Hashcat has started processing
    # Now check the potfile again for the cracked password
    return check_hash_in_potfile(hash_value)

def main():
    input_file = 'hashed_passwords.txt'  # Replace with your actual file path
    output_file = 'cracked_passwords.txt'
    
    with open(input_file, 'r') as f:
        hashes = f.readlines()

    with open(output_file, 'w') as f_out:
        for line in hashes:
            username, hash_value = line.strip().split(':')
            # Check if the hash is in the potfile first
            cracked_password = check_hash_in_potfile(hash_value)
            
            if cracked_password:
                f_out.write(f"{cracked_password}\n")  # Write the cracked password to the output file
                print(f"Found in potfile: {cracked_password}")
            else:
                # If not found in the potfile, attempt to crack with Hashcat
                print(f"Attempting to crack: {hash_value} with username: {username}")
                cracked_password = crack_hash_with_hashcat(username, hash_value)
                
                if cracked_password:
                    f_out.write(f"{cracked_password}\n")  # Write the cracked password to the output file
                    print(f"Successfully cracked: {cracked_password}")
                else:
                    print(f"Failed to crack: {hash_value}")

if __name__ == '__main__':
    main()
