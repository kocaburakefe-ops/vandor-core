import random
import re
from pathlib import Path

# 🏛️ Vandor'S Ritmik Bitiş Ekleri (Kelimeye Epik Havasını Veren Ekler)
VANDOR_SUFFIXES = ["ar", "or", "is", "os", "en", "is", "an"]

# 🗣️ İngilizce / Latince Temelli Akılda Kalıcı Kelime Haritası
BASE_WORD_MAP = {
    "Stone": ["Ston", "Petr", "Rock"],
    "Water": ["Watr", "Aqu", "Hydr"],
    "Fire": ["Fyr", "Ign", "Pyro"],
    "Moon": ["Mon", "Lun", "Cyn"],
    "Sun": ["Sun", "Sol", "Hel"],
    "Light": ["Lyt", "Lum", "Lux"],
    "Mind": ["Mind", "Ment", "Psych"],
    "Heart": ["Hart", "Cord", "Card"],
    "Star": ["Star", "Astr", "Stell"],
    "Night": ["Nyt", "Noct", "Nox"],
    "Day": ["Day", "Diar", "Sol"],
    "Wind": ["Wynd", "Vent", "Aeol"],
    "Earth": ["Erth", "Terr", "Geor"],
    "Life": ["Lyf", "Vita", "Bio"],
    "Time": ["Tym", "Chron", "Temp"],
    "Word": ["Word", "Verb", "Ligo"],
    "Voice": ["Voys", "Phon", "Voc"],
    "Path": ["Path", "Viar", "Rout"],
    "House": ["Hous", "Dom", "Cas"],
    "Peace": ["Pes", "Pac", "Pax"]
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

def generate_intuitive_word(english_word: str) -> str:
    """İngilizce/Latince köklerden türeyen, akılda kalıcı Vandor'S kelimesi üretir."""
    base_options = BASE_WORD_MAP.get(english_word, [english_word[:4]])
    base = random.choice(base_options)
    suffix = random.choice(VANDOR_SUFFIXES)
    
    # Çift sesli veya garip harf çakışmalarını temizle
    full_word = base + suffix
    full_word = re.sub(r"(.)\1{2,}", r"\1", full_word) # Aynı harf 3 kere gelemez
    return full_word.capitalize()

def generate_batch(count=10000, batch_num=1):
    raw_dir = Path("data/raw")
    raw_dir.mkdir(parents=True, exist_ok=True)
    
    print("[+] Scanning database...")
    existing_roots = load_existing_roots(raw_dir)
    
    new_words = []
    english_keys = list(BASE_WORD_MAP.keys())
    
    print(f"[+] Generating {count} intuitive Vandor'S roots...")
    
    attempts = 0
    while len(new_words) < count and attempts < count * 10:
        attempts += 1
        english_word = english_keys[len(new_words) % len(english_keys)]
        root = generate_intuitive_word(english_word)
        
        if root.lower() not in existing_roots:
            existing_roots.add(root.lower())
            
            # Anlam formatı
            variant = (len(new_words) // len(english_keys)) + 1
            meaning = f"{english_word}" if variant == 1 else f"{english_word} (Variant {variant})"
            
            new_words.append((root, meaning))

    output_file = raw_dir / f"generated_{batch_num:02d}.txt"
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"--- VANDOR'S EASY-RECALL BATCH {batch_num:02d} ---\n")
        for idx, (root, meaning) in enumerate(new_words, start=1):
            f.write(f"{idx:05d}. {root} -> {meaning}\n")

    print(f"[✔] COMPLETED: {output_file} ({len(new_words)} intuitive roots written)")


if __name__ == "__main__":
    raw_dir = Path("data/raw")
    # Mevcut batch dosyalarını sayıp otomatik bir sonraki part numarasını verir
    existing_batches = len(list(raw_dir.glob("generated_*.txt"))) if raw_dir.exists() else 0
    next_batch = existing_batches + 1
    
    print(f"[🚀] Part {next_batch:02d} üretimi başlatılıyor...")
    generate_batch(count=10000, batch_num=next_batch)
    
    
