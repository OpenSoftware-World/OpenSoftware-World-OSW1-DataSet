import json
import random
import os

print("=" * 40)
print(" OpenSoftware-World-OSW1 Math Dataset Creator")
print("=" * 40)
print("[1] Turkish (TR)")
print("[2] English (EN)")

lang_choice = input("\nSelect Language: ").strip()

if lang_choice == "1":
    LANG = "TR"
elif lang_choice == "2":
    LANG = "EN"
else:
    print("Invalid selection.")
    exit()

try:
    intent_count = int(input("Intent count: "))
except:
    print("Invalid number.")
    exit()

filename = "math_dataset.json"

index = 1
while os.path.exists(filename):
    filename = f"math_dataset{index}.json"
    index += 1

if LANG == "TR":
    templates = {
        "+": [
            "{} + {}",
            "{} artı {}",
            "{} ile {} topla",
            "{} ve {} kaç eder"
        ],
        "-": [
            "{} - {}",
            "{} eksi {}",
            "{}'den {} çıkar",
            "{} ile {} farkı"
        ],
        "*": [
            "{} * {}",
            "{} çarpı {}",
            "{} ile {} çarp",
            "{} x {}"
        ],
        "/": [
            "{} / {}",
            "{} bölü {}",
            "{}'yi {}'ye böl"
        ],
        "%": [
            "{} % {}",
            "{} mod {}",
            "{} modulo {}"
        ],
        "**": [
            "{} üzeri {}",
            "{} ^ {}",
            "{} ** {}"
        ]
    }
else:
    templates = {
        "+": [
            "{} + {}",
            "Add {} and {}",
            "{} plus {}",
            "What is {} + {}?"
        ],
        "-": [
            "{} - {}",
            "Subtract {} from {}",
            "{} minus {}"
        ],
        "*": [
            "{} * {}",
            "{} times {}",
            "Multiply {} and {}"
        ],
        "/": [
            "{} / {}",
            "{} divided by {}",
            "Divide {} by {}"
        ],
        "%": [
            "{} % {}",
            "{} mod {}",
            "{} modulo {}"
        ],
        "**": [
            "{} ** {}",
            "{} to the power of {}",
            "{} ^ {}"
        ]
    }

dataset = {
    "intents": []
}

operations = ["+", "-", "*", "/", "%", "**"]

for i in range(intent_count):
    op = random.choice(operations)

    a = random.randint(1, 200)
    b = random.randint(1, 200)

    if op in ["/", "%"]:
        while b == 0:
            b = random.randint(1, 200)
    if op == "+":
        result = a + b
    elif op == "-":
        result = a - b
    elif op == "*":
        result = a * b
    elif op == "/":
        result = round(a / b, 6)
    elif op == "%":
        result = a % b
    elif op == "**":
        a = random.randint(1, 15)
        b = random.randint(2, 5)
        result = a ** b

    patterns = []

    for temp in templates[op]:
        patterns.append(temp.format(a, b))

    responses = [
        str(result),
        f"{result}",
        f"Result: {result}" if LANG == "EN" else f"Sonuç: {result}"
    ]

    dataset["intents"].append({
        "tag": f"math_{i+1}",
        "patterns": patterns,
        "responses": responses
    })

with open(filename, "w", encoding="utf-8") as f:
    json.dump(dataset, f, indent=4, ensure_ascii=False)

print("\nDataset created successfully.")
print("File:", filename)
print("Total intents:", len(dataset["intents"]))