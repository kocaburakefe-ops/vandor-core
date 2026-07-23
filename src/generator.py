import random
import re
from pathlib import Path

# --- 1. ADIM: GENİŞLETİLMİŞ FONETİK HAVUZ VE DİNAMİK KOMBİNASYONLAR ---
VOWELS = ["a", "e", "i", "o", "u", "ae", "ai", "ea", "eo", "ia"]
CONSONANTS = ["b", "c", "d", "f", "g", "h", "k", "l", "m", "n", "p", "r", "s", "t", "v", "z", "th", "sh", "kr", "dr"]
PREFIXES = ["val", "xar", "vor", "kor", "zer", "dra", "mor", "syr", "tar", "bel", ""]
SUFFIXES = ["is", "os", "um", "ar", "en", "or", "ath", "ys", "al", "im", ""]

def generate_unique_word():
    """Vandor'S kurallarına uygun, milyarlarca kombinasyon üreten kelime motoru."""
    pattern = random.choice([1, 2, 3, 4])
    
    prefix = random.choice(PREFIXES)
    suffix = random.choice(SUFFIXES)
    
    if pattern == 1:
        # C-V-C-V-C (Örn: K-a-r-o-n)
        core = random.choice(CONSONANTS) + random.choice(VOWELS) + random.choice(CONSONANTS) + random.choice(VOWELS) + random.choice(CONSONANTS)
    elif pattern == 2:
        # V-C-V-C (Örn: A-r-o-n)
        core = random.choice(VOWELS) + random.choice(CONSONANTS) + random.choice(VOWELS) + random.choice(CONSONANTS)
    elif pattern == 3:
        # C-V-C-C-V (Örn: D-r-a-k-o)
        core = random.choice(CONSONANTS) + random.choice(VOWELS) + random.choice(CONSONANTS) + random.choice(CONSONANTS) + random.choice(VOWELS)
    else:
        # C-V-C (Örn: V-o-r)
        core = random.choice(CONSONANTS) + random.choice(VOWELS) + random.choice(CONSONANTS)
        
    word = f"{prefix}{core}{suffix}"
    return word.lower()

# --- 2. ADIM: AKILLI HAFIZA VE SIFIR ÇAKIŞMA YÖNETİMİ ---
def load_existing_words(raw_dir: Path) -> set:
    """Mevcut tüm batch dosyalarını tarayıp üretilmiş kelimeleri hafızaya çeker."""
    existing_words = set()
    if raw_dir.exists():
        for file_path in raw_dir.glob("generated_*.txt"):
            with open(file_path, "r", encoding="utf-8") as f:
                for line in f:
                    word = line.strip()
                    if word:
                        existing_words.add(word)
    return existing_words

def generate_batch(count=10000, batch_num=1):
    raw_dir = Path("data/raw")
    raw_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"[🔍] Geçmiş kelimeler taranıyor...")
    existing_words = load_existing_words(raw_dir)
    print(f"[ℹ️] Toplam {len(existing_words)} benzersiz kelime hafızada.")
    
    new_words = []
    attempts = 0
    max_attempts = count * 20  # Sonsuz döngüyü önleme emniyeti
    
    while len(new_words) < count and attempts < max_attempts:
        attempts += 1
        candidate = generate_unique_word()
        
        if candidate not in existing_words:
            existing_words.add(candidate)
            new_words.append(candidate)
            
    file_path = raw_dir / f"generated_{batch_num:02d}.txt"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("\n".join(new_words) + "\n")
        
    print(f"[✅] Batch {batch_num:02d} başarıyla oluşturuldu! Basılan kelime sayısı: {len(new_words)}")

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
        
