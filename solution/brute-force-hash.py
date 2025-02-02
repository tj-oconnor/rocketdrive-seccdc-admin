import hashlib
import itertools
import string
from tqdm import tqdm
import multiprocessing
import random
import math
from sympy import nextprime


def string_to_number(data: str):
    hash_obj = hashlib.sha256(data.encode())
    hash_int = int(hash_obj.hexdigest(), 16)
    return hash_int % (10**9)


def number_to_string(target_number):
    charset = string.ascii_letters + string.digits + " "
    for length in range(1, 7):
        for attempt in itertools.product(charset, repeat=length):
            candidate = "".join(attempt)
            if string_to_number(candidate) == target_number:
                return candidate
    return None


def unsalt(salted_number: str):
    print("[*] Starting un~salting~ attack...")
    salted_number = int(salted_number)
    SEED = int(math.e * 1e9)
    random.seed(SEED)
    a = nextprime(random.randint(10**8, 10**9))
    b = nextprime(random.randint(10**8, 10**9))
    m = 10**9
    a_inv = pow(a, -1, m)
    recovered_number = ((salted_number - b) * a_inv) % m
    recovered_string = number_to_string(recovered_number)
    print("[+] Recovered salt...")
    return recovered_string


def brute_force_worker(start, end, target_hash, queue):
    for salt in range(start, end):
        salt_str = f"{salt:09d}"
        if hashlib.md5(str(salt_str).encode("utf-8")).hexdigest() == target_hash:
            queue.put(salt_str)
            return


def brute_force_salt(target_hash, num_processes=None):
    print("[*] Starting brute-force attack against interim ~salt~...")

    if num_processes is None:
        num_processes = multiprocessing.cpu_count()

    print(f"[*] Using {num_processes} processes for brute force.")

    total_range = 10**9
    chunk_size = total_range // num_processes
    processes = []
    queue = multiprocessing.Queue()

    for i in range(num_processes):
        start = i * chunk_size
        end = (i + 1) * chunk_size if i != num_processes - 1 else total_range
        p = multiprocessing.Process(
            target=brute_force_worker, args=(start, end, target_hash, queue)
        )
        processes.append(p)
        p.start()

    with tqdm(total=total_range, desc="Searching", unit=" attempts") as pbar:
        while any(p.is_alive() for p in processes):
            pbar.update(chunk_size // 10)
            if not queue.empty():
                found_salt = queue.get()
                print(f"\n[+] Salt Found: {found_salt}")
                for p in processes:
                    p.terminate()
                return found_salt

    print("\n[-] No matching salt found.")
    return None


if __name__ == "__main__":
    recover_salt = brute_force_salt("dc2e9cb5cafe7fbe888273bed40f353e")
    if recover_salt != None:
        recover_password = unsalt(recover_salt)
    if recover_password != None:
        print(f"Password Recovered {recover_password}")
