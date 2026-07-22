import random
import re
from pathlib import Path

# 🏛️ Akıcı & Kolay Telaffuz Edilen Harf Grupları (Sert harfler çıkarıldı)
VOWELS = ["a", "e", "i", "o", "u"]
START_CONSONANTS = ["b", "c", "d", "f", "g", "h", "k", "l", "m", "n", "p", "r", "s", "t", "v"]
END_CONSONANTS = ["r", "l", "n", "s", "st", "nd"] # Sadece akıcı bitişler

# 🗣️ İngilizce Temel Kelimeler Listesi
ENGLISH_VOCAB = [
    "Water", "Fire", "Sun", "Moon", "Sky", "Earth", "Light", "Time", "Space",
    "Friend", "House", "Road", "Life", "Heart", "Mind", "Word", "Voice", "Soul",
    "Hand", "Eye", "Night", "Day", "River", "Stone", "Wind", "Star", "Ocean",
    "City", "Path", "Door", "Book", "Name", "Sound", "Peace", "Hope", "Dream",
    "Force", "Power", "Truth", "Honor", "Vision", "Memory", "Shadow", "Flame"
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

def generate_melodic_word() -> str:
    """İngilizce/Latinceye benzeyen, okunması aşırı kolay kelimeler üretir."""
    patterns = [
        # Örn: Lora, Mina, Tora, Fala
        lambda: random.choice(START_CONSONANTS) + random.choice(VOWELS) + random.choice(START_CONSONANTS) + random.choice(VOWELS),
        # Örn: Solen, Merin, Valor, Karon
        lambda: random.choice(START_CONSONANTS) + random.choice(VOWELS) + random.choice(START_CONSONANTS) + random.choice(VOWELS) + random.choice(END_CONSONANTS),
        # Örn: Aris, Elor, Onis, Astan
        lambda: random.choice(VOWELS) + random.choice(START_CONSONANTS) + random.choice(VOWELS) + random.choice(END_CONSONANTS),
        # Örn: Crest, Land, Torst
        lambda: random.choice(START_CONSONANTS) + random.choice(VOWELS) + random.choice(END_CONSONANTS)
    ]
    
    word = random.choice(patterns)()
    return word.capitalize()

def generate_batch(count=10000, batch_num=1):
    raw_dir = Path("data/raw")
    raw_dir.mkdir(parents=True, exist_ok=True)
    
    print("[+] Scanning database...")
    existing_roots = load_existing_roots(raw_dir)
    
    new_words = []
    vocab_size = len(ENGLISH_VOCAB)
    
    print(f"[+] Generating {count} clean and melodic Vandor'S roots...")
    
    while len(new_words) < count:
        root = generate_melodic_word()
        if root.lower() not in existing_roots:
            existing_roots.add(root.lower())
            
            # Anlam ataması
            base_meaning = ENGLISH_VOCAB[len(new_words) % vocab_size]
            meaning_suffix = f" (Root Type {len(new_words) // vocab_size + 1})" if len(new_words) >= vocab_size else ""
            full_meaning = f"{base_meaning}{meaning_suffix}"
            
            new_words.append((root, full_meaning))

    output_file = raw_dir / f"generated_{batch_num:02d}.txt"
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"--- VANDOR'S MELODIC BATCH {batch_num:02d} ---\n")
        for idx, (root, meaning) in enumerate(new_words, start=1):
            f.write(f"{idx:05d}. {root} -> {meaning}\n")

    print(f"[✔] BATCH {batch_num:02d} COMPLETED: {output_file} ({len(new_words)} smooth roots written)")

if __name__ == "__main__":
    generate_batch(count=10000, batch_num=1)
    
