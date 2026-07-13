import wikipediaapi
import json
import time
import re
import os

print("Select dataset language:")
print("[1] Turkish (TR)")
print("[2] English (EN)")

choice = input("Enter choice (1/2): ").strip()

if choice == "1":
    lang = "tr"
elif choice == "2":
    lang = "en"
else:
    print("Invalid choice, defaulting to English.")
    lang = "en"

wiki = wikipediaapi.Wikipedia(
    language=lang,
    user_agent='YOUR_USER_AGENT'
)

topics = {
    "en": [
        "Artificial intelligence",
        "Computer",
        "Python (programming language)",
        "C (programming language)",
        "Java (programming language)",
        "C++ (programming language)",
        "JavaScript (programming language)",
        "PyTorch",
        "TensorFlow",
        "Linux",
        "Deep learning",
        "Assembly language",
        "Neural network",
        "Windows 10",
        "Windows 11",
        "Microsoft",
        "Google",
        "OpenAI",
        "Microsoft Office",
        "LibreOffice",
        "ChatGPT",
        "Gemini",
        "Artificial neural network",
        "Deep neural network",
        "OS",
        "Office suite",
        "Cars",
        "BMW",
        "Ferrari",
        "Tesla",
        "Lamborghini",
        "Audi",
        "Mercedes",
        "Bentley",
        "Rolls-Royce",
        "Porsche",
        "Bugatti",
        "TOGG",
        "Machine learning",
        "Operating system",
        "Database",
        "History",
        "Science",
        "Physics",
        "Chemistry",
        "Biology",
        "Mathematics",
        "Computer science",
        "Artificial intelligence",
        "Programming languages",
        "Operating systems",
        "Computer networking",
        "Computer security",
        "Astronomy",
        "Geography",
        "Geology",
        "Economics",
        "Law",
        "Psychology",
        "Philosophy",
        "Religion",
        "Medicine",
        "Music",
        "Film",
        "Art",
        "Literature",
        "Sports",
        "Animals",
        "Plants"
    ],
    "tr": [
        "Yapay zeka",
        "Bilgisayar",
        "Python (programlama dili)",
        "C (programlama dili)",
        "Java (programlama dili)",
        "C++ (programlama dili)",
        "JavaScript (programlama dili)",
        "PyTorch",
        "TensorFlow",
        "Linux",
        "Derin öğrenme",
        "Makine öğrenmesi",
        "Assembly dili",
        "Windows 10",
        "Windows 11",
        "Microsoft",
        "Google",
        "Microsoft Office",
        "LibreOffice",
        "OpenAI",
        "ChatGPT",
        "Cars",
        "BMW",
        "Ferrari",
        "Tesla",
        "Lamborghini",
        "Audi",
        "Mercedes",
        "Bentley",
        "Rolls-Royce",
        "Porsche",
        "Bugatti",
        "TOGG",
        "Gemini",
        "Yapay sinir ağı",
        "Derin yapay sinir ağı",
        "Sinir ağı",
        "OS",
        "Office suite",
        "Makine öğrenmesi",
        "İşletim sistemi",
        "Veritabanı",
        "Tarih",
        "Bilim",
        "Fizik",
        "Kimya",
        "Biyoloji",
        "Matematik",
        "Bilgisayar bilimi",
        "Yapay zeka",
        "Programlama dilleri",
        "İşletim sistemleri",
        "Bilgisayar ağları",
        "Bilgisayar güvenliği",
        "Astronomi",
        "Coğrafya",
        "Jeoloji",
        "Ekonomi",
        "Hukuk",
        "Psikoloji",
        "Felsefe",
        "Din",
        "Tıp",
        "Müzik",
        "Sinema",
        "Sanat",
        "Edebiyat",
        "Spor",
        "Hayvanlar",
        "Bitkiler"
    ]
}

dataset = {"intents": []}

def clean_text(text, max_sentences=3):
    if not text:
        return None

    text = re.sub(r'\[[0-9]+\]', '', text)
    sentences = text.split(". ")
    return ". ".join(sentences[:max_sentences]).strip()

def build_patterns(topic):
    if lang == "tr":
        base = [
            f"{topic} nedir?",
            f"{topic} hakkında bilgi ver",
            f"{topic} açıkla",
            f"Bana {topic} anlat",
            f"{topic} ne demek?"
        ]
    else:
        base = [
            f"What is {topic}?",
            f"Tell me about {topic}",
            f"Explain {topic}",
            f"Define {topic}",
            f"Can you explain {topic}?"
        ]

    expanded = []

    for p in base:
        expanded.append(p)
        expanded.append(p.lower())

    return list(set(expanded))

def get_page(topic):
    page = wiki.page(topic)
    return clean_text(page.summary) if page.exists() else None

def build_intent(topic, summary):
    patterns = build_patterns(topic)
    if not summary or len(summary) < 50:
        return None

    return {
        "tag": topic.lower().replace(" ", "_").replace("(", "").replace(")", ""),
        "patterns": patterns,
        "responses": [summary]
    }

def save_versioned(data, base_name="wikipedia_dataset"):
    version = 0

    while True:
        filename = f"{base_name}.json" if version == 0 else f"{base_name}{version}.json"
        if not os.path.exists(filename):
            break

        version += 1

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    return filename

selected_topics = topics[lang]

for topic in selected_topics:
    print(f"[+] Processing: {topic}")
    summary = get_page(topic)
    intent = build_intent(topic, summary)

    if intent:
        dataset["intents"].append(intent)

    time.sleep(1)

filename = save_versioned(dataset)
print(f"DONE ✔ dataset saved as {filename}")
