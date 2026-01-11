#!/usr/bin/env python3
"""
Skrypt do generowania spisu wszystkich przepisów z plików Markdown.
Przeszukuje wszystkie pliki .md i wyciąga tytuły (linie zaczynające się od #).
"""

import os
import re
from pathlib import Path


def extract_title_from_md(file_path):
    """
    Wyciąga pierwszy tytuł z pliku Markdown (linia zaczynająca się od #).

    Args:
        file_path: Ścieżka do pliku .md

    Returns:
        Tytuł przepisu lub None jeśli nie znaleziono
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                # Szukamy linii zaczynającej się od #
                if line.startswith("#"):
                    # Usuwamy znaki # i spacje
                    title = re.sub(r"^#+\s*", "", line)
                    return title.strip()
    except Exception as e:
        print(f"Błąd podczas czytania pliku {file_path}: {e}")
    return None


def find_all_recipes(root_dir):
    """
    Znajduje wszystkie pliki .md w katalogu i wyciąga ich tytuły.

    Args:
        root_dir: Katalog główny do przeszukania

    Returns:
        Lista krotek (nazwa_pliku, tytuł_przepisu)
    """
    recipes = []
    root_path = Path(root_dir)

    # Przeszukaj wszystkie pliki .md
    for md_file in sorted(root_path.rglob("*.md")):
        # Pomiń plik README.md
        if md_file.name == "README.md":
            continue

        title = extract_title_from_md(md_file)
        if title:
            # Ścieżka relatywna względem katalogu głównego
            relative_path = md_file.relative_to(root_path)
            recipes.append((str(relative_path), title))

    return recipes


def generate_recipe_list_file(recipes, output_file):
    """
    Generuje plik tekstowy ze spisem przepisów.

    Args:
        recipes: Lista krotek (nazwa_pliku, tytuł_przepisu)
        output_file: Ścieżka do pliku wyjściowego
    """
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("=" * 60 + "\n")
        f.write("SPIS WSZYSTKICH PRZEPISÓW\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Łącznie przepisów: {len(recipes)}\n")
        f.write(f"Data wygenerowania: {Path(output_file).stat().st_mtime}\n\n")
        f.write("-" * 60 + "\n\n")

        for idx, (file_path, title) in enumerate(recipes, 1):
            f.write(f"{idx}. {title}\n")
            f.write(f"   Plik: {file_path}\n\n")

        f.write("-" * 60 + "\n")
        f.write(f"Koniec spisu ({len(recipes)} przepisów)\n")


def main():
    """Główna funkcja skryptu."""
    # Katalog ze skryptem
    script_dir = Path(__file__).parent

    print("Szukam przepisów w katalogu:", script_dir)

    # Znajdź wszystkie przepisy
    recipes = find_all_recipes(script_dir)

    print(f"Znaleziono {len(recipes)} przepisów")

    # Wygeneruj plik ze spisem
    output_file = script_dir / "spis_przepisow.txt"
    generate_recipe_list_file(recipes, output_file)

    print(f"Spis przepisów zapisany do: {output_file}")

    # Wyświetl podsumowanie
    print("\nZnalezione przepisy:")
    for file_path, title in recipes:
        print(f"  - {title} ({file_path})")


if __name__ == "__main__":
    main()
