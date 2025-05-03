from app.analyzer import HomeworkAnalyzer
import argparse

def main(file_path, filetype):
    analyzer = HomeworkAnalyzer(file_path, filetype)
    result = analyzer.analyze()

    print("\n📌 Konular:", result["bulunan_konular"])
    print("\n📚 Eksik Konular ve Öneriler:")
    for k in result["eksik_konular"]:
        print(f"- {k['konu']} → {k['kaynak_link']} ({k['tip']})")

    print("\n🛠️ Yazım ve Gramer Analizi:\n", result["gramer_hatalari"])

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True, help="PDF veya DOCX dosya yolu")
    parser.add_argument("--type", choices=["pdf", "docx"], required=True, help="Dosya tipi")
    args = parser.parse_args()

    main(args.file, args.type)
