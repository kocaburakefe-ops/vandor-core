import random
import re
import urllib.request
from pathlib import Path

def get_large_english_vocab() -> list:
    """GitHub üzerindeki 10.000 kelimelik listeden veriyi çeker."""
    url = "https://raw.githubusercontent.com/first20hours/google-10000-english/master/google-10000-english-usa-no-swears.txt"
    try:
        print("[+] Dev İngilizce kelime havuzu indiriliyor...")
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            words = response.read().decode('utf-8').splitlines()
            clean_words = [w.capitalize() for w in words if len(w) >= 3]
            print(f"[✔] {len(clean_words)} adet İngilizce kelime hafızaya yüklendi!")
            return clean_words
    except Exception as e:
        print(f"[!] İnternet indirilemedi, dahili geniş yedek listeye geçiliyor...")
        return ["Stone", "Water", "Fire", "Moon", "Sun", "Light", "Mind", "Heart", "Star", "Night", "Wind", "Earth", "Life", "Time", "Cloud", "Storm"]

ENGLISH_CORE_WORDS = get_large_english_vocab()

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
    """İngilizce kelimeyi Vandor'S fonetiğine kaydırır."""
    w = word.lower()
    
    # Esnek kurallar
    r = rule_index % 6
    if r == 0:
        res = (w[:-2] + "ar") if w.endswith("er") else ((w[:-1] + "a") if w.endswith("e") else w + "a")
    elif r == 1:
        res = w.replace("ight", "ytis").replace("ind", "mida") if ("ight" in w or "ind" in w) else ((w[:-1] + "is") if w.endswith("e") else w + "is")
    elif r == 2:
        res = re.sub(r"(oo|ee|ai|ea|ou)", lambda m: m.group(0)[0], w)
        res = (res[:-1] if res.endswith("e") else res) + "en"
    elif r == 3:
        res = w.replace("i", "e").replace("o", "a") if ("i" in w or "o" in w) else w + "os"
        if not res.endswith(("a", "e", "i", "o", "u", "s", "n")): res += "a"
    elif r == 4:
        res = (w[:-1] + "or") if w.endswith("e") else w + "or"
    else:
        res = (w[:-1] + "in") if w.endswith("e") else w + "in"

    # Eğer çok fazla tekrar ettiyse kelime sonuna ritmik hece atarak kilitlenmeyi önler
    if rule_index >= 6:
        extra_suffixes = ["is", "on", "ar", "en", "or"]
        res += extra_suffixes[(rule_index // 6) % len(extra_suffixes)]

    return res.capitalize()

def generate_batch(count=10000, batch_num=1):
    raw_dir = Path("data/raw")
    raw_dir.mkdir(parents=True, exist_ok=True)
    
    print("[+] Database taranıyor...")
    existing_roots = load_existing_roots(raw_dir)
    
    new_words = []
    total_base = len(ENGLISH_CORE_WORDS)
    
    print(f"[+] {count} adet Vandor'S kökü üretiliyor...")
    
    idx = 0
    max_attempts = count * 20  # Sonsuz döngü koruması
    attempts = 0
    
    while len(new_words) < count and attempts < max_attempts:
        attempts += 1
        base_word = ENGLISH_CORE_WORDS[idx % total_base]
        rule_type = idx // total_base
        
        vandor_root = transform_to_vandor(base_word, rule_type)
        
        if vandor_root.lower() not in existing_roots:
            existing_roots.add(vandor_root.lower())
            variant = rule_type + 1
            meaning_label = f"{base_word}" if variant == 1 else f"{base_word} (Shift {variant})"
            new_words.append((vandor_root, meaning_label))
        idx += 1

    output_file = raw_dir / f"generated_{batch_num:02d}.txt"
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"--- VANDOR'S BATCH {batch_num:02d} ---\n")
        for i, (root, meaning) in enumerate(new_words, start=1):
            f.write(f"{i:05d}. {root} -> {meaning}\n")

    print(f"[✔] BATCH {batch_num:02d} TAMAMLANDI: {output_file} ({len(new_words)} kelime yazıldı)")

if __name__ == "__main__":
    raw_dir = Path("data/raw")
    
    # Klasördeki mevcut generated_XX.txt dosyalarından en büyük numarayı bulur
    existing_numbers = []
    if raw_dir.exists():
        for f in raw_dir.glob("generated_*.txt"):
            match = re.search(r"generated_(\d+)\.txt", f.name)
            if match:
                existing_numbers.append(int(match.group(1)))
                
    next_batch = max(existing_numbers) + 1 if existing_numbers else 1
    
    print(f"[+] Yeni Batch Numarası: {next_batch:02d}")
    generate_batch(count=10000, batch_num=next_batch)
    
