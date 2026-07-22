import random
import re
from pathlib import Path

# 🗣️ Zenginleştirilmiş Geniş İngilizce Kelime Havuzu
ENGLISH_CORE_WORDS = [
    # Doğa & Evren
    "Stone", "Water", "Fire", "Moon", "Sun", "Light", "Mind", "Heart",
    "Star", "Night", "Day", "Wind", "Earth", "Life", "Time", "Word",
    "Voice", "Path", "House", "Peace", "Power", "Dream", "Shadow", "Flame",
    "River", "Ocean", "Space", "Sound", "Truth", "Honor", "Vision", "Memory",
    "Glass", "Paper", "Steel", "Blood", "Cloud", "Storm", "Frost", "Rain",
    "Mountain", "Forest", "Valley", "Desert", "Island", "Wave", "Thunder", "Lightning",
    "Gold", "Silver", "Iron", "Copper", "Crystal", "Smoke", "Ash", "Ice",
    
    # İnsan & Yaşam
    "Friend", "Brother", "Sister", "Mother", "Father", "Child", "King", "Queen",
    "Warrior", "Leader", "Master", "Hero", "Ghost", "Spirit", "Body", "Soul",
    "Hand", "Eye", "Head", "Foot", "Face", "Blood", "Bone", "Breath",
    "City", "Town", "Bridge", "Tower", "Gate", "Door", "Wall", "Room",
    
    # Eylemler & Kavramlar
    "Hope", "Love", "Fear", "War", "Faith", "Force", "Will", "Thought",
    "Reason", "Wisdom", "Knowledge", "Secret", "Mystery", "Destiny", "Fate", "Glory",
    "Victory", "Justice", "Freedom", "Order", "Chaos", "Harmony", "Silence", "Echo"
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
    """İngilizce kelimeyi doğal Vandor'S fonetik kurallarına göre kaydırır."""
    w = word.lower()
    
    # Kural 0: Sonundaki e/er yumuşatması (Water -> Watar, Stone -> Stana)
    if rule_index % 6 == 0:
        if w.endswith("er"):
            res = w[:-2] + "ar"
        elif w.endswith("e"):
            res = w[:-1] + "a"
        else:
            res = w + "a"
            
    # Kural 1: -is / -ytis dönüşümü (Light -> Lytis, Mind -> Mida)
    elif rule_index % 6 == 1:
        if "ight" in w:
            res = w.replace("ight", "ytis")
        elif "ind" in w:
            res = w.replace("ind", "mida")
        elif w.endswith("e"):
            res = w[:-1] + "is"
        else:
            res = w + "is"
            
    # Kural 2: Çift sesli sadeleştirmesi ve -en eki (Moon -> Monen, Rain -> Ranen)
    elif rule_index % 6 == 2:
        res = re.sub(r"(oo|ee|ai|ea|ou)", lambda m: m.group(0)[0], w)
        if res.endswith("e"):
            res = res[:-1]
        res = res + "en"
        
    # Kural 3: Sesli harf kaydırması (Fire -> Fira, Wind -> Wenda)
    elif rule_index % 6 == 3:
        if "i" in w:
            res = w.replace("i", "e")
        elif "o" in w:
            res = w.replace("o", "a")
        else:
            res = w + "os"
        if not res.endswith(("a", "e", "i", "o", "u", "s", "n")):
            res += "a"
            
    # Kural 4: Akıcı -or / -ar ritmik uzatması (Star -> Staron, Heart -> Hartor)
    elif rule_index % 6 == 4:
        if w.endswith("e"):
            res = w[:-1] + "or"
        else:
            res = w + "or"
            
    # Kural 5: Akıcı -in / -is yumuşak türetimi (Storm -> Storin, Frost -> Frostis)
    else:
        if w.endswith("e"):
            res = w[:-1] + "in"
        else:
            res = w + "in"

    return res.capitalize()

def generate_batch(count=10000, batch_num=1):
    raw_dir = Path("data/raw")
    raw_dir.mkdir(parents=True, exist_ok=True)
    
    print("[+] Database taranıyor...")
    existing_roots = load_existing_roots(raw_dir)
    
    new_words = []
    total_base = len(ENGLISH_CORE_WORDS)
    
    print(f"[+] {count} adet genişletilmiş İngilizce kaydırmalı Vandor'S kökü üretiliyor...")
    
    idx = 0
    while len(new_words) < count:
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
        f.write(f"--- VANDOR'S EXTENDED ENGLISH SHIFT BATCH {batch_num:02d} ---\n")
        for i, (root, meaning) in enumerate(new_words, start=1):
            f.write(f"{i:05d}. {root} -> {meaning}\n")

    print(f"[✔] BATCH {batch_num:02d} TAMAMLANDI: {output_file} ({len(new_words)} kelime yazıldı)")

if __name__ == "__main__":
    raw_dir = Path("data/raw")
    existing_batches = len(list(raw_dir.glob("generated_*.txt"))) if raw_dir.exists() else 0
    next_batch = existing_batches + 1
    
    generate_batch(count=10000, batch_num=next_batch)
    
