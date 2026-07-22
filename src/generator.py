import random
import re
from pathlib import Path

# 🗣️ Zengin İngilizce Temel Kelime Listesi
ENGLISH_CORE_WORDS = [
    "Stone", "Water", "Fire", "Moon", "Sun", "Light", "Mind", "Heart",
    "Star", "Night", "Day", "Wind", "Earth", "Life", "Time", "Word",
    "Voice", "Path", "House", "Peace", "Power", "Dream", "Shadow", "Flame",
    "River", "Ocean", "Space", "Sound", "Truth", "Honor", "Vision", "Memory",
    "Glass", "Paper", "Steel", "Blood", "Cloud", "Storm", "Frost", "Rain"
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

def transform_to_vandor(word: str, rule_index: int) -> str:
    """İngilizce kelimeyi 4 farklı doğal fonetik kuralına göre dönüştürür."""
    w = word.lower()
    
    # Kural 1: Sonundaki e/er eklerini yumuşatıp a/as yap (Water -> Watar, Stone -> Stana)
    if rule_index % 4 == 0:
        if w.endswith("er"):
            res = w[:-2] + "ar"
        elif w.endswith("e"):
            res = w[:-1] + "a"
        else:
            res = w + "a"
            
    # Kural 2: 'ight' bitişlerini 'ytis', 'ind' bitişlerini 'mida' yap (Light -> Lytis, Mind -> Mida)
    elif rule_index % 4 == 1:
        if "ight" in w:
            res = w.replace("ight", "ytis")
        elif "ind" in w:
            res = w.replace("ind", "mida")
        elif w.endswith("e"):
            res = w[:-1] + "is"
        else:
            res = w + "is"
            
    # Kural 3: Çift seslileri teke düşür ve 'en' ekle (Moon -> Monen, Rain -> Ranen)
    elif rule_index % 4 == 2:
        res = re.sub(r"(oo|ee|ai|ea)", lambda m: m.group(0)[0], w)
        if res.endswith("e"):
            res = res[:-1]
        res = res + "en"
        
    # Kural 4: Kelimenin ortasındaki sesli harfi Vandor estetiğine kaydır (Fire -> Fira, Wind -> Wenda)
    else:
        if "i" in w:
            res = w.replace("i", "e")
        elif "o" in w:
            res = w.replace("o", "a")
        else:
            res = w + "os"
        if not res.endswith(("a", "e", "i", "o", "u", "s", "n")):
            res += "a"

    return res.capitalize()

def generate_batch(count=10000, batch_num=1):
    raw_dir = Path("data/raw")
    raw_dir.mkdir(parents=True, exist_ok=True)
    
    print("[+] Database taranıyor...")
    existing_roots = load_existing_roots(raw_dir)
    
    new_words = []
    total_base = len(ENGLISH_CORE_WORDS)
    
    print(f"[+] {count} adet doğal İngilizce kaydırmalı Vandor'S kökü üretiliyor...")
    
    for idx in range(count):
        base_word = ENGLISH_CORE_WORDS[idx % total_base]
        rule_type = idx // total_base
        
        vandor_root = transform_to_vandor(base_word, rule_type)
        
        if vandor_root.lower() not in existing_roots:
            existing_roots.add(vandor_root.lower())
            
            variant = rule_type + 1
            meaning_label = f"{base_word}" if variant == 1 else f"{base_word} (Shift {variant})"
            
            new_words.append((vandor_root, meaning_label))

    output_file = raw_dir / f"generated_{batch_num:02d}.txt"
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"--- VANDOR'S NATURAL ENGLISH SHIFT BATCH {batch_num:02d} ---\n")
        for i, (root, meaning) in enumerate(new_words, start=1):
            f.write(f"{i:05d}. {root} -> {meaning}\n")

    print(f"[✔] BATCH {batch_num:02d} TAMAMLANDI: {output_file} ({len(new_words)} kelime yazıldı)")

if __name__ == "__main__":
    raw_dir = Path("data/raw")
    existing_batches = len(list(raw_dir.glob("generated_*.txt"))) if raw_dir.exists() else 0
    next_batch = existing_batches + 1
    
    generate_batch(count=10000, batch_num=next_batch)
    
