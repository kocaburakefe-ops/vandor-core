import re
import json
from pathlib import Path

# 🏛️ Vandor Core Gramer Kuralları & Sabit Tanımlamaları
GRAMMAR_RULES = {
    "structure": "SOV (Özne + Nesne + Yüklem)",
    "suffix_rule": "Tüm ekler doğrudan kelimeye bitişik yazılır, tire (-) kullanılmaz.",
    "tenses": {
        "Şimdiki Zaman": "in (Örn: Eatin)",
        "Geçmiş Zaman": "ed (Örn: Eated)",
        "Gelecek Zaman": "az (Örn: Eataz)"
    },
    "pronouns": {
        "Been": "Ben",
        "Son": "Sen",
        "Ó": "O",
        "Yizz": "Biz",
        "Sizz": "Siz",
        "Óntar": "Onlar"
    },
    "cases": {
        "un": "Yönelme (-e hali) -> Varun",
        "is": "Bulunma (-de hali) -> Varis",
        "om": "Ayrılma (-den hali) -> Varom",
        "ia": "Belirtme (-i hali) -> Varia"
    },
    "modifiers": {
        "no": "Olumsuzluk (Örn: Eatno)",
        "qu": "Soru Yapısı (Örn: Eatqu? / Eatnoqu?)"
    }
}

def parse_txt_files(raw_dir: Path):
    """raw/ içindeki tüm .txt dosyalarını okuyup regex ile ayrıştırır."""
    dictionary = []
    current_category = "General"
    global_id = 1

    txt_files = sorted(raw_dir.glob("*.txt"))

    for file_path in txt_files:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                if line.startswith("---") and line.endswith("---"):
                    current_category = line.replace("-", "").strip()
                    continue

                match = re.match(r"^\d+\.\s*([\w\-]+)\s*->\s*(.+)$", line)
                if match:
                    root = match.group(1).strip()
                    meaning_tr = match.group(2).strip()

                    dictionary.append({
                        "id": global_id,
                        "root": root,
                        "meaning_tr": meaning_tr,
                        "category": current_category,
                        "type": "noun"
                    })
                    global_id += 1

    return dictionary

def generate_markdown(dictionary, md_output: Path):
    """Sözlük ve Gramer Motorunu birleştirip Markdown dokümanı basar."""
    md_output.parent.mkdir(parents=True, exist_ok=True)
    
    with open(md_output, "w", encoding="utf-8") as f:
        f.write("# 📖 Vandor Core Dictionary & Grammar System\n\n")
        f.write("Vandor'S dili için oluşturulmuş evrensel gramer kuralları ve kelime kökleri motorudur.\n\n")
        
        # 1. Gramer Bölümü
        f.write("## 🏛️ Gramer ve Dil Mimarisi\n\n")
        f.write(f"- **Cümle Dizilimi:** `{GRAMMAR_RULES['structure']}`\n")
        f.write(f"- **Ek Bitiştirme Kuralı:** `{GRAMMAR_RULES['suffix_rule']}`\n\n")

        f.write("### ⏳ Zaman Ekleri (Bitişik)\n")
        for tense, desc in GRAMMAR_RULES["tenses"].items():
            f.write(f"- **{tense}:** `{desc}`\n")

        f.write("\n### 👤 Kişi Zamirleri\n")
        for pronoun, meaning in GRAMMAR_RULES["pronouns"].items():
            f.write(f"- `{pronoun}`: {meaning}\n")

        f.write("\n### 📍 İsmin Halleri\n")
        for case, desc in GRAMMAR_RULES["cases"].items():
            f.write(f"- Ek `{case}`: {desc}\n")

        f.write("\n### 🚫 Olumsuzluk ve Soru\n")
        for mod, desc in GRAMMAR_RULES["modifiers"].items():
            f.write(f"- Ek `{mod}`: {desc}\n")

        # 2. Sözlük Tablosu
        f.write("\n---\n\n")
        f.write(f"## 📚 Kelime Kökleri (Toplam: {len(dictionary)})\n\n")
        f.write("| ID | Kök (Root) | Türkçe Anlamı | Kategori |\n")
        f.write("|:---|:---|:---|:---|:\n")
        for item in dictionary:
            f.write(f"| {item['id']} | **{item['root']}** | {item['meaning_tr']} | `{item['category']}` |\n")

def main():
    raw_dir = Path("data/raw")
    
    # 🎯 ANA DAMAR ÇIKTILARI
    json_output = Path("data/dictionary.json")
    md_output = Path("docs/DICTIONARY.md")

    if not raw_dir.exists():
        print("[-] data/raw klasörü bulunamadı!")
        return

    dictionary = parse_txt_files(raw_dir)
    print(f"[+] Toplam {len(dictionary)} kelime ayrıştırıldı.")

    # 1. JSON Çıktısı
    json_output.parent.mkdir(parents=True, exist_ok=True)
    with open(json_output, "w", encoding="utf-8") as f:
        json.dump(dictionary, f, ensure_ascii=False, indent=2)

    # 2. Markdown Çıktısı
    generate_markdown(dictionary, md_output)

    print(f"[+] Üretim tamamlandı: {json_output} ve {md_output}")

if __name__ == "__main__":
    main()
    
