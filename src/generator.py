import random
import re
from pathlib import Path

# 🏛️ Vandor'S Fonetik ve Ses Yapısı
VOWELS = "aeiouyó"
CONSONANTS = "bcdfghjklmnprstvwxz"

CATEGORIES_WITH_MEANINGS = {
    "VANDOR_TEKNOLOJI_SISTEM": [
        "Veri Düğümü", "Ağ Matrisi", "İşlem Çekirdeği", "Sinyal Yuvası", 
        "Alt Sistem Protokolü", "Enerji Hücresi", "Kod Akışı", "Terminal Arayüzü"
    ],
    "VANDOR_EVREN_KAVRAM": [
        "Yıldız Tozu", "Yörünge Katmanı", "Zaman Derinliği", "Uzak Işık", 
        "Çekim Alanı", "Kozmik Toz", "Gök Cismi", "Boşluk Boyutu"
    ],
    "VANDOR_FELSEFE_YAZILIM": [
        "Temel Mantık", "Varlık Durumu", "Sonsuz Döngü", "Sistem Kuralı", 
        "Gözlem Katmanı", "Soyut Yapı", "Ana Denklem", "Dönüşüm Kuramı"
    ]
}

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

def is_phonetically_valid(word: str) -> bool:
    word_lower = word.lower()
    for i in range(len(word_lower) - 2):
        ch1, ch2, ch3 = word_lower[i], word_lower[i+1], word_lower[i+2]
        if (ch1 in VOWELS and ch2 in VOWELS and ch3 in VOWELS) or \
           (ch1 in CONSONANTS and ch2 in CONSONANTS and ch3 in CONSONANTS):
            return False
    return True

def generate_root() -> str:
    patterns = [
        ("C", "V", "C"),
        ("C", "V", "C", "C"),
        ("C", "V", "C", "V", "C")
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
    
    print("[+] Veritabanı taranıyor...")
    existing_roots = load_existing_roots(raw_dir)
    print(f"[+] Mevcut {len(existing_roots)} kelime çakışma korumasına alındı.")
    
    new_words = []
    categories = list(CATEGORIES_WITH_MEANINGS.keys())
    
    print(f"[+] {count} adet benzersiz Vandor'S kökü üretiliyor...")
    
    while len(new_words) < count:
        root = generate_root()
        if root.lower() not in existing_roots:
            existing_roots.add(root.lower())
            
            cat = random.choice(categories)
            meaning_base = random.choice(CATEGORIES_WITH_MEANINGS[cat])
            meaning_full = f"{meaning_base} (Part {batch_num:02d})"
            
            new_words.append((root, meaning_full, cat))

    output_file = raw_dir / f"generated_{batch_num:02d}.txt"
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"--- GENERATED BATCH {batch_num:02d} ---\n")
        for idx, (root, meaning, cat) in enumerate(new_words, start=1):
            f.write(f"{idx:05d}. {root} -> {meaning} [{cat}]\n")

    print(f"[✔] BATCH {batch_num:02d} TAMAMLANDI: {output_file} ({len(new_words)} kelime yazıldı)")

if __name__ == "__main__":
    generate_batch(count=10000, batch_num=1)
    
