import re
import json
from pathlib import Path

def parse_txt_files(raw_dir: Path):
    dictionary = []
    current_category = "General"
    global_id = 1

    # raw/ içindeki tüm .txt dosyalarını alfabetik oku
    txt_files = sorted(raw_dir.glob("*.txt"))

    for file_path in txt_files:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                # Kategori Başlıklarını Yakala (örn: --- I. SİSTEM... ---)
                if line.startswith("---") and line.endswith("---"):
                    current_category = line.replace("-", "").strip()
                    continue

                # Kelime Satırlarını Yakala (örn: 0001. Karnor -> Çekirdek...)
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

def main():
    raw_dir = Path("data/raw")
    json_output = Path("data/dictionary.json")
    md_output = Path("docs/DICTIONARY.md")

    if not raw_dir.exists():
        print("data/raw klasörü bulunamadı!")
        return

    dictionary = parse_txt_files(raw_dir)
    print(f"Toplam {len(dictionary)} kelime ayrıştırıldı.")

    # 1. JSON Çıktısı Oluştur
    json_output.parent.mkdir(parents=True, exist_ok=True)
    with open(json_output, "w", encoding="utf-8") as f:
        json.dump(dictionary, f, ensure_ascii=False, indent=2)

    # 2. Markdown Çıktısı Oluştur
    md_output.parent.mkdir(parents=True, exist_ok=True)
    with open(md_output, "w", encoding="utf-8") as f:
        f.write("# 📖 Vandor Core Dictionary\n\n")
        f.write(f"**Toplam Kök Kelime Sayısı:** {len(dictionary)}\n\n")
        f.write("| ID | Kök (Root) | Türkçe Anlamı | Kategori |\n")
        f.write("|---|---|---|---|\n")
        for item in dictionary:
            f.write(f"| {item['id']} | **{item['root']}** | {item['meaning_tr']} | `{item['category']}` |\n")

    print("Derleme tamamlandı!")

if __name__ == "__main__":
    main()
  
