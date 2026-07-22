import random
import re
from pathlib import Path

# 🏛️ English / Latin Friendly Phonetic Structure (Easy to Speak)
VOWELS = "aeiou"
CONSONANTS = "bcdfghjlmnprstvw" # Zor okunan x, z, j gibi harfler azaltıldı

# 🗣️ Daily English Base Vocabulary (For Easy Learning)
DAILY_ENGLISH_WORDS = [
    "Water", "Fire", "Sun", "Moon", "Sky", "Earth", "Light", "Time",
    "Friend", "House", "Road", "Life", "Heart", "Mind", "Word", "Voice",
    "Hand", "Eye", "Night", "Day", "River", "Stone", "Wind", "Star",
    "City", "Path", "Door", "Book", "Name", "Sound", "Peace", "Hope"
]

def load_existing_roots(raw_dir: Path) -> set:
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

def is_easy_to_pronounce(word: str) -> bool:
    """Ensures the generated word flows naturally like English/Latin."""
    word_lower = word.lower()
    
    # Dili burkan sert bitişleri engelle
    if word_lower.endswith(("b", "c", "d", "f", "g", "v", "w")):
        return False

    # Yan yana 3 aynı tür harf gelemez
    for i in range(len(word_lower) - 2):
        ch1, ch2, ch3 = word_lower[i], word_lower[i+1], word_lower[i+2]
        if (ch1 in VOWELS and ch2 in VOWELS and ch3 in VOWELS) or \
           (ch1 in CONSONANTS and ch2 in CONSONANTS and ch3 in CONSONANTS):
            return False
            
    return True

def generate_easy_root() -> str:
    """Generates melodic, easy-to-speak root words."""
    patterns = [
        ("C", "V", "C", "V"),     # Ex: Vina, Lora, Pura
        ("C", "V", "C", "C"),     # Ex: Vard, Meln, Rest
        ("C", "V", "C", "V", "C") # Ex: Valen, Miras, Solen
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
        if is_easy_to_pronounce(word):
            return word

def generate_batch(count=10000, batch_num=1):
    raw_dir = Path("data/raw")
    raw_dir.mkdir(parents=True, exist_ok=True)
    
    print("[+] Scanning existing database...")
    existing_roots = load_existing_roots(raw_dir)
    
    new_words = []
    print(f"[+] Generating {count} easy-to-learn Vandor'S roots...")
    
    while len(new_words) < count:
        root = generate_easy_root()
        if root.lower() not in existing_roots:
            existing_roots.add(root.lower())
            
            # Daily English meaning assignment
            english_meaning = random.choice(DAILY_ENGLISH_WORDS)
            new_words.append((root, english_meaning))

    output_file = raw_dir / f"generated_{batch_num:02d}.txt"
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"--- VANDOR'S EASY-LEARN BATCH {batch_num:02d} ---\n")
        for idx, (root, meaning) in enumerate(new_words, start=1):
            f.write(f"{idx:05d}. {root} -> {meaning}\n")

    print(f"[✔] COMPLETED: {output_file} ({len(new_words)} smooth roots written)")

if __name__ == "__main__":
    generate_batch(count=10000, batch_num=1)
    
