import random
import re
from pathlib import Path

# 🏛️ Vandor'S Phonetic & Sound Structure
VOWELS = "aeiouyó"
CONSONANTS = "bcdfghjklmnprstvwxz"

def load_existing_roots(raw_dir: Path) -> set:
    """Scans all existing .txt files to retrieve generated root words and avoid duplicates."""
    existing = set()
    if not raw_dir.exists():
        return existing
        
    for file_path in raw_dir.glob("*.txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                match = re.search(r"^\d+\.\s*([\w\-]+)", line.strip())
                if match:
                    existing.add(match.group(1).strip().lower())
                elif "->" in line:
                    parts = line.split("->")
                    root_part = parts[0].split(".")[-1].strip()
                    if root_part:
                        existing.add(root_part.lower())
    return existing

def is_phonetically_valid(word: str) -> bool:
    """Filter to prevent 3 consecutive vowels or consonants."""
    word_lower = word.lower()
    for i in range(len(word_lower) - 2):
        ch1, ch2, ch3 = word_lower[i], word_lower[i+1], word_lower[i+2]
        if (ch1 in VOWELS and ch2 in VOWELS and ch3 in VOWELS) or \
           (ch1 in CONSONANTS and ch2 in CONSONANTS and ch3 in CONSONANTS):
            return False
    return True

def generate_root() -> str:
    """Generates rhythmic Vandor'S roots based on syllable patterns."""
    patterns = [
        ("C", "V", "C"),          # Ex: Kar, Vok, Zan
        ("C", "V", "C", "C"),     # Ex: Karn, Vord, Zalm
        ("C", "V", "C", "V", "C") # Ex: Karon, Vadir, Zelkor
    ]
    
    while True:
        pattern = random.choice(patterns)
        word = ""
        for char_type in pattern:
            if char_type == "C":
                word += random.choice(CONSONANTS)
            else:
                word += random.choice(VOWELS)
        
        word = word.capitalize()
        if is_phonetically_valid(word):
            return word

def generate_batch(count=10000, batch_num=1):
    raw_dir = Path("data/raw")
    raw_dir.mkdir(parents=True, exist_ok=True)
    
    print("[+] Scanning existing database...")
    existing_roots = load_existing_roots(raw_dir)
    print(f"[+] Protected {len(existing_roots)} existing roots from duplication.")
    
    new_words = []
    print(f"[+] Generating {count} unique Vandor'S roots...")
    
    while len(new_words) < count:
        root = generate_root()
        if root.lower() not in existing_roots:
            existing_roots.add(root.lower())
            new_words.append(root)

    output_file = raw_dir / f"generated_{batch_num:02d}.txt"
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"--- GENERATED BATCH {batch_num:02d} ---\n")
        for idx, root in enumerate(new_words, start=1):
            # Clean English output format
            f.write(f"{idx:05d}. {root} -> [Generated Root - Part {batch_num:02d}]\n")

    print(f"[✔] BATCH {batch_num:02d} COMPLETED: {output_file} ({len(new_words)} roots written)")

if __name__ == "__main__":
    generate_batch(count=10000, batch_num=1)
    
