import random
import re
from pathlib import Path
from collections import defaultdict

# --- VANDOR'S GENIŞLETILMIŞ SES HARİTASI ---
# ✅ Daha geniş vowel seti
VOWELS = [
    "a", "e", "i", "o", "u", "y",
    "aa", "ae", "ai", "ao", "au",
    "ea", "ee", "ei", "eo", "eu",
    "ia", "ie", "ii", "io", "iu",
    "oa", "oe", "oi", "oo", "ou",
    "ua", "ue", "ui", "uo", "uu",
    "ar", "er", "ir", "or", "ur",
    "al", "el", "il", "ol", "ul",
    "an", "en", "in", "on", "un",
    "as", "es", "is", "os", "us"
]

# ✅ Daha geniş consonant seti
CONSONANTS = [
    "b", "c", "d", "f", "g", "h", "j", "k", "l", "m",
    "n", "p", "q", "r", "s", "t", "v", "w", "x", "z",
    "bl", "br", "ch", "cl", "cr", "dr", "dw", "fl", "fr",
    "gh", "gl", "gr", "kh", "kl", "kr", "ph", "pl", "pr",
    "qu", "sh", "sk", "sl", "sm", "sn", "sp", "st", "sw",
    "th", "tr", "tw", "wh", "wr", "zh"
]

# ✅ İngilizce anlam bileşenleri
ENGLISH_ROOTS = [
    "light", "dark", "shadow", "fire", "water", "wind", "earth", "star", "sun", "moon",
    "sky", "stone", "iron", "blood", "spirit", "soul", "mind", "life", "death", "time",
    "space", "realm", "king", "queen", "path", "sword", "shield", "force", "power", "truth",
    "vision", "silent", "ancient", "eternal", "fury", "grace", "storm", "frost", "peak", "bound",
    "dream", "hope", "fear", "rage", "joy", "sorrow", "peace", "chaos", "order", "void",
    "light", "dawn", "dusk", "night", "day", "year", "age", "tide", "wave", "flow",
    "mountain", "valley", "river", "lake", "forest", "field", "desert", "ocean", "cliff", "cave"
]

ENGLISH_MODIFIERS = [
    "walker", "seeker", "bringer", "keeper", "weaver", "shaper", "bearer", "caller",
    "master", "blade", "heart", "guard", "song", "fall", "rise", "forge", "sight", "born",
    "breaker", "maker", "taker", "giver", "hunter", "rider", "flyer", "swimmer", "runner", "dancer",
    "keeper", "warden", "watcher", "seer", "healer", "builder", "destroyer", "protector", "warrior", "sage",
    "of", "the", "and", "blessed", "cursed", "eternal", "ancient", "wild", "free", "bound"
]

# --- VANDOR'S MELODIK KELIME YARATICI ---
def generate_melodic_word(pattern_type=None):
    """
    Doğal, akıcı ve melodik Vandor'S kelimesi türetir.
    ✅ Tekrar seçime izin verir (random.choice kullanır)
    ✅ 4-7 harf uzunluğunda kelimeler oluşturur
    """
    if pattern_type is None:
        pattern_type = random.randint(1, 8)
    
    # İçinde tekrar olabilir - daha fazla kombinasyon
    v = lambda: random.choice(VOWELS)
    c = lambda: random.choice(CONSONANTS)
    
    patterns = {
        1: lambda: f"{c()}{v()}{c()}{v()}",                    # CVCV
        2: lambda: f"{v()}{c()}{v()}{c()}",                    # VCVC
        3: lambda: f"{c()}{v()}{c()}{v()}{c()}",               # CVCVC
        4: lambda: f"{c()}{v()}{c()}{c()}{v()}",               # CVCCV
        5: lambda: f"{v()}{c()}{c()}{v()}{c()}",               # VCCVC
        6: lambda: f"{c()}{v()}{c()}{v()}{c()}{v()}",          # CVCVCV
        7: lambda: f"{c()}{v()}{c()}{c()}{v()}{c()}",          # CVCCVC
        8: lambda: f"{v()}{c()}{v()}{c()}{v()}{c()}",          # VCVCVC
    }
    
    try:
        word = patterns[pattern_type]()
        return word.capitalize()
    except Exception as e:
        print(f"[⚠️] Pattern {pattern_type} hatası: {e}")
        return generate_melodic_word(random.randint(1, 8))

def generate_meaning():
    """Anlaşılır ve karizmatik İngilizce karşılık üretir."""
    if random.random() < 0.5:
        return random.choice(ENGLISH_ROOTS)
    else:
        root = random.choice(ENGLISH_ROOTS)
        mod = random.choice(ENGLISH_MODIFIERS)
        return f"{root} {mod}"

def load_existing_words(raw_dir: Path) -> set:
    """Mevcut kelimeleri hafızaya çeker."""
    existing_words = set()
    if raw_dir.exists():
        for file_path in sorted(raw_dir.glob("generated_*.txt")):
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    for line in f:
                        if line.strip() and ":" in line:
                            word = line.split(":")[0].strip()
                            if word:
                                existing_words.add(word.lower())
            except Exception as e:
                print(f"[⚠️] {file_path} okuma hatası: {e}")
    return existing_words

def generate_batch(count=10000, batch_num=1, verbose=True):
    """
    ✅ Yeni batch oluşturur
    ✅ Collision detection ile çakışma engeller
    ✅ Progress gösterir
    """
    raw_dir = Path("data/raw")
    raw_dir.mkdir(parents=True, exist_ok=True)
    
    if verbose:
        print(f"\n[🔍] Batch {batch_num:03d} için geçmiş kelimeler taranıyor...")
    
    existing_words = load_existing_words(raw_dir)
    initial_count = len(existing_words)
    
    if verbose:
        print(f"[ℹ️] Toplam {initial_count} kelime hafızada.")
        print(f"[🚀] Üretim başlıyor: {count} kelime hedefleniyor...")
    
    new_entries = []
    attempts = 0
    max_attempts = count * 50  # ✅ Daha yüksek attempt
    collision_count = 0
    
    # Pattern dağılımı - çeşitlilik için
    pattern_dist = [1, 2, 3, 4, 5, 6, 7, 8]
    
    while len(new_entries) < count and attempts < max_attempts:
        attempts += 1
        
        # Pattern seç (döngüsel şekilde)
        pattern = pattern_dist[(attempts - 1) % len(pattern_dist)]
        v_word = generate_melodic_word(pattern_type=pattern)
        v_word_lower = v_word.lower()
        
        if v_word_lower not in existing_words:
            existing_words.add(v_word_lower)
            meaning = generate_meaning()
            new_entries.append(f"{v_word} : {meaning}")
        else:
            collision_count += 1
        
        # Progress göster (her 1000 kelimede)
        if verbose and len(new_entries) % 1000 == 0:
            print(f"  [{len(new_entries):5d}/{count}] kelime oluşturuldu... (çakışma: {collision_count})")
    
    # Dosyaya yaz
    file_path = raw_dir / f"generated_{batch_num:03d}.txt"
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("\n".join(new_entries) + "\n")
        
        if verbose:
            success_rate = (len(new_entries) / attempts * 100) if attempts > 0 else 0
            print(f"\n[✅] Batch {batch_num:03d} başarıyla oluşturuldu!")
            print(f"    📊 Başarılı kelime: {len(new_entries)}/{count}")
            print(f"    🎯 Başarı oranı: {success_rate:.1f}%")
            print(f"    💾 Dosya: {file_path}")
            print(f"    📈 Toplam kelime havuzu: {initial_count + len(new_entries)}")
    except Exception as e:
        print(f"[❌] Dosya yazma hatası: {e}")

def batch_generator_loop(start_batch=1, end_batch=106, resume=True):
    """
    ✅ Otomatik batch döngüsü
    ✅ Kesintiden devam edebilir
    """
    raw_dir = Path("data/raw")
    
    # Mevcut batch'leri bul
    existing_numbers = []
    if raw_dir.exists() and resume:
        for f in raw_dir.glob("generated_*.txt"):
            match = re.search(r"generated_(\d+)\.txt", f.name)
            if match:
                num = int(match.group(1))
                existing_numbers.append(num)
    
    next_batch = max(existing_numbers) + 1 if existing_numbers else start_batch
    
    print(f"\n{'='*60}")
    print(f"🌌 VANDOR'S ENGINE v2.0 - BATCH GENERATOR")
    print(f"{'='*60}")
    print(f"📊 Tamamlanan: {len(existing_numbers)} batch")
    print(f"🔄 Sonraki batch: {next_batch:03d}")
    print(f"🎯 Hedef: {end_batch:03d}")
    print(f"{'='*60}\n")
    
    if next_batch > end_batch:
        total_words = len(load_existing_words(raw_dir))
        print(f"[🛑] HEDEF ULAŞILDI!")
        print(f"✅ {end_batch} batch tamamlandı!")
        print(f"📈 Toplam kelime: {total_words:,}")
        return
    
    # Single batch oluştur
    generate_batch(count=10000, batch_num=next_batch, verbose=True)

if __name__ == "__main__":
    # ✅ SEÇENEK 1: Tek batch oluştur
    batch_generator_loop(start_batch=1, end_batch=106, resume=True)
    
    # ✅ SEÇENEK 2: Manuel batch
    # generate_batch(count=10000, batch_num=1, verbose=True)
    
