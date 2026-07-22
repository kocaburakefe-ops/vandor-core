import random
import re
from pathlib import Path

# 🏛️ Vandor'S Estetik Ekleri (İngilizce kökü bozmayan akıcı ekler)
ENGLISH_VANDOR_SUFFIXES = ["is", "or", "en", "ir", "ar"]

# 🗣️ Doğrudan İngilizce Temel Kelimeler (Kelime Havuzu)
ENGLISH_CORE_WORDS = [
    "Stone", "Water", "Fire", "Moon", "Sun", "Light", "Mind", "Heart",
    "Star", "Night", "Day", "Wind", "Earth", "Life", "Time", "Word",
    "Voice", "Path", "House", "Peace", "Power", "Dream", "Shadow", "Flame",
    "River", "Ocean", "Space", "Sound", "Truth", "Honor", "Vision", "Memory"
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

def convert_to_vandor_english(word: str, suffix: str) -> str:
    """İngilizce kelimeyi bozmadan Vandor'S formuna getirir."""
    base = word.lower()
    
    # Kelime sonundaki e harfini temizleyip eki yapıştırır (Stone -> Ston + ir = Stonir)
    if base.endswith("e"):
        base = base[:-1]
    
    vandor_word = base + suffix
    return vandor_word.capitalize()

def generate_batch(count=10000, batch_num=1):
    raw_dir = Path("data/raw")
    raw_dir.mkdir(parents=True, exist_ok=True)
    
    print("[+] Database taranıyor...")
    existing_roots = load_existing_roots(raw_dir)
    
    new_words = []
    total_base = len(ENGLISH_CORE_WORDS)
    
    print(f"[+] {count} adet İngilizce tabanlı Vandor'S kökü üretiliyor...")
    
    for idx in range(count):
        # İngilizce kelimeyi ve eklenecek Vandor'S ekini seçer
        base_word = ENGLISH_CORE_WORDS[idx % total_base]
        suffix = ENGLISH_VANDOR_SUFFIXES[(idx // total_base) % len(ENGLISH_VANDOR_SUFFIXES)]
        
        vandor_root = convert_to_vandor_english(base_word, suffix)
        
        # Eğer aynısı daha önce üretilmediyse ekle
        if vandor_root.lower() not in existing_roots:
            existing_roots.add(vandor_root.lower())
            
            # Varyasyon mantığı
            variant = (idx // total_base) + 1
            meaning_label = f"{base_word}" if variant == 1 else f"{base_word} (Type {variant})"
            
            new_words.append((vandor_root, meaning_label))

    output_file = raw_dir / f"generated_{batch_num:02d}.txt"
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"--- VANDOR'S ENGLISH-BASED BATCH {batch_num:02d} ---\n")
        for i, (root, meaning) in enumerate(new_words, start=1):
            f.write(f"{i:05d}. {root} -> {meaning}\n")

    print(f"[✔] BATCH {batch_num:02d} TAMAMLANDI: {output_file} ({len(new_words)} kelime yazıldı)")

if __name__ == "__main__":
    raw_dir = Path("data/raw")
    existing_batches = len(list(raw_dir.glob("generated_*.txt"))) if raw_dir.exists() else 0
    next_batch = existing_batches + 1
    
    generate_batch(count=10000, batch_num=next_batch)
    
