# 🌌 Vandor'S Engine & Dictionary

> **"A constructed world built on logic, vast scale, and algorithmic linguistics."**

[![Status](https://img.shields.io/badge/Status-Active_Generation-brightgreen)](https://github.com/)
[![Target Words](https://img.shields.io/badge/Lexicon_Target-1%2C000%2C000-blue)](https://github.com/)
[![License](https://img.shields.io/badge/License-MIT-orange)](LICENSE)

**Vandor'S** is an automated, algorithmic language generation engine and world-building system designed for complex fictional universes and constructed languages (conlangs).

Going beyond conventional fictional worlds, Vandor'S features **40-hour daily cycles**, **40 distinct continents**, unique climate/season frameworks, and a massive, rule-based lexicon targeted at **1,000,000 unique words**.

---

## 🌟 Key Features

* 🗣️ **Algorithmic Conlang Architecture:** A rich vocabulary generated through 40 strict grammatical rules and phonetic harmony matrices.
* 🤖 **Autonomous Data Generation:** Powered by GitHub Actions and a custom Python engine, ensuring zero collisions across 1 Million words.
* 🪐 **Advanced World Building:**
  * 40-Hour Daily Cycle Logic
  * 40 Unique Continents & Geographies
  * Dynamic Seasonal & Temporal Frameworks
* 📦 **Modular & Open Data:** Clean, easily readable raw batches (`data/raw`) structured for future compilation into JSON/dictionary formats.

---

## ⚙️ Linguistic Engine & Generation Logic

The Vandor'S language is not built on random string generation. Every generated word strictly adheres to root mathematics, phonetic constraints, and grammatical patterns.



1. **Phonetic Filtering:** Each candidate root is parsed against strict Vandor'S phonetic rules.
2. **Uniqueness Enforcement:** The system validates new tokens against all historical batches to prevent duplicates.
3. **Automated Pipeline:** Continuous integration via GitHub Actions safely appends batches (`generated_XX.txt`) to the core dataset.

---

## 📁 Repository Structure

```text
VandorS/
├── .github/workflows/    # Automated generation pipelines
├── data/
│   └── raw/              # 10,000-word raw batches (Batch 01 through 106)
├── src/
│   └── generator.py      # Core lexical generation & validation engine
└── README.md             # Project documentation



# Clone the repository
git clone [https://github.com/your-username/VandorS.git](https://github.com/your-username/VandorS.git)

# Navigate into the directory
cd VandorS

# Run the generation engine locally
python src/generator.py
