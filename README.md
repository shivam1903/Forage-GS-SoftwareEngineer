# Password Cracking using Hashcat

This project demonstrates how I utilized Hashcat to crack MD5 hashes using a combination of wordlists, salting, and brute-force techniques. Below, you'll find an explanation of the tools and techniques employed, along with a breakdown of the different phases used to systematically crack the hashes.

---

## Hashing Algorithm Used

The hashing algorithm employed to protect the passwords in this task was **MD5**. MD5 (Message Digest Algorithm 5) is a widely-used cryptographic hash function that generates a 128-bit hash value from any input. However, due to advancements in computing power and the discovery of vulnerabilities, MD5 is now considered weak for password storage as it is susceptible to fast brute-force and dictionary attacks.

---

## Introduction to Hashcat

**Hashcat** is a powerful and widely-used password recovery tool that supports a variety of hashing algorithms, including MD5. It is known for its flexibility, performance, and support for different attack modes.

### Dictionary Attack (Mode `-a 0`)
In a **dictionary attack**, Hashcat tests each password in a list of words (a dictionary) against the given hash until it finds a match. This is one of the most efficient ways to crack passwords when using common or known passwords.

### Brute Force Attack (Mode `-a 3`)
A **brute-force attack** involves systematically checking all possible combinations of characters. Unlike dictionary attacks, brute-force attempts every possible combination of characters until the correct password is found.

---

## Cracking Process

I approached the task of cracking the hashes in **three phases**, progressively using more complex methods.

### Phase 1: Cracking Using Wordlists

The **Phase1.py** script focuses on using pre-built wordlists to crack the hashes. This phase is based on the assumption that many users pick passwords from commonly available wordlists.

1. **Wordlists Used**:
   - **SecLists by Daniel Miessler**: A collection of commonly used passwords and words.
   - **RockYou Wordlist**: One of the most well-known password lists compiled from the RockYou leak.
   - **Piotrcki’s 16GB Wordlist** ([GitHub Repo](https://github.com/piotrcki/wordlist)): A comprehensive and massive wordlist.

2. **Potfile Check**:  
   To optimize the process, before checking the wordlists, I first ensured that any previously cracked passwords were found using Hashcat's **potfile**. The potfile keeps a record of already-cracked hashes. This speeds up the process by skipping hashes that were already solved.

3. **Command Used**:
   ```bash
   hashcat -m 0 -a 0 hash.txt wordlist.txt --show
   ```
   Where:
   - `-m 0`: MD5 hash type.
   - `-a 0`: Dictionary attack mode.
   - `hash.txt`: The file containing the MD5 hashes.
   - `wordlist.txt`: The wordlist being used.
   - `--show`: Checks if the hash is already cracked in the potfile.

This phase successfully cracked a significant portion of the hashes using wordlists.

### Phase 2: Salting Method

The **Phase2.py** script introduced **salting** to the cracking process. Salting involves adding additional data (in this case, the usernames) to the password before hashing. The salt ensures that even if two users have the same password, their hashes will differ.

1. **Method**:  
   For this phase, I took the usernames provided along with the hashes and combined them with words from the wordlists. This created a new set of salted candidate passwords.
   
   Example:  
   ```
   Username: bandalls  
   Hash: bdda5f03128bcbdfa78d8934529048cf  
   Combined Word: bandalls + wordlist candidates
   ```

2. **Command Used**:
   ```bash
   hashcat -m 0 -a 0 hash.txt salted_wordlist.txt
   ```
   Where `salted_wordlist.txt` contains combinations of usernames and words from the wordlist.

This phase successfully cracked some hashes that were otherwise resistant to standard dictionary attacks due to the salting mechanism.

### Phase 3: Brute Force with Salting

The **Phase3.py** script used a more advanced method, combining **brute-force** techniques with **salting**. In this phase, I generated passwords by adding **two characters** on either side of the username or hash and then ran the attack.

1. **Method**:
   - First, two characters were added to the **left** of the username.
   - Then, two characters were added to the **right** of the username.
   - Finally, two characters were added to **both sides** of the username.

   Example:  
   ```
   Username: bandalls  
   Hash: bdda5f03128bcbdfa78d8934529048cf  
   Generated Candidate Passwords:
   - xxbandalls
   - bandallsxx
   - xxbandallsxx
   ```

2. **Command Used**:
   ```bash
   hashcat -m 0 -a 3 hash.txt ?a?a{username}?a?a
   ```
   Where `?a` represents any possible ASCII character.

This phase aimed to crack the remaining tough hashes by trying different character combinations, leveraging both brute-force and salting.

---

## Conclusion

Throughout this project, I used various techniques to crack MD5 hashes, including dictionary attacks with pre-built wordlists, salting, and brute-force combined with salting. The potfile functionality helped optimize the process by skipping already-cracked hashes, and the flexibility of Hashcat made it possible to apply advanced techniques like salting and character manipulation to crack even more resistant passwords.

If you’re working with password recovery, it’s essential to understand the limitations of simple hashing mechanisms like MD5 and the importance of using stronger algorithms and proper salting techniques to secure sensitive data.

For further details, refer to the provided Python scripts:  
- **Phase1.py**  
- **Phase2.py**  
- **Phase3.py**

These scripts reflect the exact steps and methodologies used in this project.
