import random
import json
from pathlib import Path

# Vandor'S Fonetik Yapısı
VOWELS = "aeiouyó"
CONSONANTS = "bcdfghjklmnprstvwxz"

# Var olan kelimeleri çekip çakışmayı önleme
def load_existing_roots(raw_dir: Path):
    existing = set()
    for file_path in raw_dir.glob("*.txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                if "->" in line:
                    parts = line.split("->")
                    root_part = parts[0].split(".")[-1].strip()
                    existing.add(root_part.lower())
    return existing

def generate_root():
    """Vandor'S kurallarına uygun ritmik kök türetici"""
    patterns = [
        ("C", "V", "C"),         # Örn: Kar, Vok
        ("C", "V", "C", "C"),    # Örn: Karn, Vord
        ("C", "V", "C", "V", "C")# Örn: Karon, Vadir
    ]
    pattern = random.choice(patterns)
    word = ""
    for char_type in pattern:
        if char_type == "C":
            word += random.choice(CONSONANTS)
        else:
            word += random.choice(VOWELS)
    return word.capitalize()

def generate_batch(count=50000, batch_num=1):
    raw_dir = Path("data/raw")
    raw_dir.mkdir(parents=True, exist_ok=True)
    
    existing_roots = load_existing_roots(raw_dir)
    new_words = []
    
    print(f"[+] {count} adet benzersiz kelime üretimi başlatıldı...")
    
    while len(new_words) < count:
        root = generate_root()
        if root.lower() not in existing_roots:
            existing_roots.add(root.lower())
            new_words.append(root)

    output_file = raw_dir / f"generated_{batch_num:02d}.txt"
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"--- GENERATED BATCH {batch_num} ---\n")
        for idx, root in enumerate(new_words, start=1):
            f.write(f"{idx:05d}. {root} -> [Otomatik Türetilen Kök - Part {batch_num}]\n")

    print(f"[✔] {output_file} başarıyla oluşturuldu! Toplam: {len(new_words)} kelime.")

if __name__ == "__main__":
    # Tek seferde 50.000 kelimelik 1. Part'ı üretir
    generate_batch(count=50000, batch_num=1)
  
