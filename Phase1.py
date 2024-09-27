import subprocess

def check_potfile(hash, mode):
    # Command to check if the hash is in the potfile
    command = ['hashcat', '-m', mode, '--show', hash]
    
    try:
        # Run the command to check for the hash in the potfile
        result = subprocess.run(command, capture_output=True, text=True)
        
        # If there is any output, it means the hash is in the potfile
        if result.stdout.strip():
            return result.stdout.strip()  # Return the cracked hash:password from the potfile
        return None
    except Exception as e:
        return f"Error checking potfile: {e}"

def run_hashcat(hash, dictionary_file, mode):
    # Command to run hashcat for MD5 (mode 0) and attack mode 0 (dictionary attack)
    command = ['hashcat', '-m', mode, '-a', '0', '-r', 'rules/best64.rule',  hash, dictionary_file]

    try:
        # Running the command
        result = subprocess.run(command, capture_output=True, text=True)
        
        
        # Look for the line where the hash is followed by a colon
        for line in result.stdout.splitlines():
            if line.startswith(hash + ":"):
                return line  # Return the line with {hash}:password format
        return f"No result for hash {hash}"
    except Exception as e:
        return f"Error running hashcat: {e}"

def main(hashes_file, dictionary_file, output_file, mode='0'):
    with open(hashes_file, 'r') as hashes, open(output_file, 'w') as output:
        for line in hashes:
            # Split the line by colon and extract the hash
            parts = line.strip().split(':')
            if len(parts) == 2:
                hash = parts[1].strip()  # Get the hash part (after colon)
                print(f"Processing hash: {hash}")
                
                # First check if the hash exists in the potfile
                potfile_result = check_potfile(hash, mode)
                
                if potfile_result:
                    print(f"Hash found in potfile: {potfile_result}")
                    output.write(f"{potfile_result}\n")  # Write potfile result to output
                else:
                    print(f"Hash not found in potfile, cracking with hashcat...")
                    # Run hashcat if the hash is not found in the potfile
                    result = run_hashcat(hash, dictionary_file, mode)
                    output.write(f"{result}\n")
                    



if __name__ == '__main__':
    # File containing MD5 hashes (one per line in format 'experthead:hash')
    hashes_file = 'hashes.txt'
    
    # Path to your dictionary file
    dictionary_file = 'xato-net-10-million-passwords.txt'
    
    # File to save the output
    output_file = 'cracked.txt'
    
    # Hash mode (0 for MD5)
    mode = '0'
    
    # Run the main function
    main(hashes_file, dictionary_file, output_file, mode)
