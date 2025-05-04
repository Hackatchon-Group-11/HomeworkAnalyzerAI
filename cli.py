# cli.py
import argparse
from app.analyzer import HomeworkAnalyzer

def main(file_path: str, filetype: str):
    analyzer = HomeworkAnalyzer(file_path, filetype)
    result = analyzer.analyze()

    print("\n📌 Bulunan Konular:")
    for konu in result["bulunan_konular"]:
        print(f"- {konu}")

    print("\n📚 Eksik Konular ve Önerilen Kaynaklar:")
    for item in result["eksik_konular"]:
        print(f"- {item['konu']} → {item['kaynak_link']} ({item['tip']})")

    print("\n🛠️ Gramer ve Yazım Kontrolü:\n")
    for issue in result["gramer_hatalari"]:
        print(f"- {issue}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ödev dosyası analiz aracı")
    parser.add_argument("--file", required=True, help="PDF veya DOCX dosya yolu")
    parser.add_argument("--type", choices=["pdf", "docx"], required=True, help="Dosya tipi")
    args = parser.parse_args()

    main(args.file, args.type)
