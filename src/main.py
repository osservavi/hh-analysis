import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from parsing_data import main as parse_main
from preprocessing_data import main as preprocess_main

def main():
    print("🚀 Запуск pipeline...")
    
    parse_main()
    preprocess_main()

if __name__ == "__main__":
    main()