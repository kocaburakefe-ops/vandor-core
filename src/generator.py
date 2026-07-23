import random
import re
from pathlib import Path

# --- VANDOR'S MELODİK SES HARİTASI ---
VOWELS = ["a", "e", "i", "o", "u", "ar", "el", "is"]
CONSONANTS = ["b", "d", "f", "g", "k", "l", "m", "n", "p", "r", "s", "t", "v", "z"]

# --- SÖZLÜK ANLAM BİLEŞENLERİ (ENGLISH MEANING BUILDERS) ---
ENGLISH_ROOTS = [
    "light", "dark", "shadow", "fire", "water", "wind", "earth", "star", "sun", "moon",
    "sky", "stone", "iron", "blood", "spirit", "soul", "mind", "life", "death", "time",
    "space", "realm", "king", "queen", "path", "sword", "shield", "force", "power", "truth",
    "vision", "silent", "ancient", "eternal", "fury", "grace", "storm", "frost", "peak", "bound"
]

ENGLISH_MODIFIERS = [
    "walker", "seeker", "bringer", "keeper", "weaver", "shaper", "bearer", "caller", 
    "master", "blade", "heart", "guard", "song", "fall", "rise", "forge", "sight", "born"
]

def generate_melodic_word():
    """Doğal, akıcı ve melodik Vandor'S kelimesi türetir."""
    pattern = random.choice([1, 2, 3])
    
    c1, c2, c3 = random.sample(CONSONANTS, 3)
    v1, v2 = random.sample(VOWELS, 2)
    
    if pattern == 1:
        # Örn: Van-dra, Kor-is
        word = f"{c1}{v1}{c2}{v2}"
    elif pattern == 2:
        # Örn: A-vel-is, O-mar-a
        word = f"{v1}{c1}{v2}{c2}"
    else:
        # Örn: Bel-or-a, Sil-ar-is
        word = f"{c1}{v1}{c2}{v2}{c3}"
        
    return word.capitalize()

def generate_meaning():
    """Anlaşılır ve karizmatik İngilizce karşılık üretir."""
    if random.random() < 0.4:
        return random.choice(ENGLISH_ROOTS)
    else:
        root = random.choice(ENGLISH_ROOTS)
        mod = random.choice(ENGLISH_MODIFIERS)
        return f"{root}-{mod}"

def load_existing_words(raw_dir: Path) -> set:
    """Mevcut kelimeleri hafızaya çeker."""
    existing_words = set()
    if raw_dir.exists():
        for file_path in raw_dir.glob("generated_*.txt"):
            with open(file_path, "r", encoding="utf-8") as f:
                for line in f:
                    if ":" in line:
                        word = line.split(":")[0].strip()
                        existing_words.add(word)
    return existing_words

def generate_batch(count=10000, batch_num=1):
    raw_dir = Path("data/raw")
    raw_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"[🔍] Geçmiş kelimeler taranıyor...")
    existing_words = load_existing_words(raw_dir)
    print(f"[ℹ️] Toplam {len(existing_words)} kelime hafızada.")
    
    new_entries = []
    attempts = 0
    max_attempts = count * 30
    
    while len(new_entries) < count and attempts < max_attempts:
        attempts += 1
        v_word = generate_melodic_word()
        
        if v_word not in existing_words:
            existing_words.add(v_word)
            meaning = generate_meaning()
            new_entries.append(f"{v_word} : {meaning}")
            
    file_path = raw_dir / f"generated_{batch_num:02d}.txt"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("\n".join(new_entries) + "\n")
        
    print(f"[✅] Batch {batch_num:02d} başarıyla oluşturuldu! Basılan kelime: {len(new_entries)}")

if __name__ == "__main__":
    raw_dir = Path("data/raw")
    
    existing_numbers = []
    if raw_dir.exists():
        for f in raw_dir.glob("generated_*.txt"):
            match = re.search(r"generated_(\d+)\.txt", f.name)
            if match:
                existing_numbers.append(int(match.group(1)))
                
    next_batch = max(existing_numbers) + 1 if existing_numbers else 1
    MAX_BATCH_COUNT = 106
    
    if next_batch > MAX_BATCH_COUNT:
        print(f"[🛑] HEDEF ULAŞILDI: Toplam {MAX_BATCH_COUNT} batch tamamlandı!")
    else:
        print(f"[🚀] Üretim Başlatılıyor -> Batch {next_batch:02d} / {MAX_BATCH_COUNT}")
        generate_batch(count=10000, batch_num=next_batch)
        
