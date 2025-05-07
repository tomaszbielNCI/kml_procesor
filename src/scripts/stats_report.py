# src/scripts/stats_report.py
import os
import pandas as pd
from src.core.analyzer import RouteAnalyzer
from src.core.processor import RouteProcessor


def generate_report():
    try:
        # Ścieżki absolutne
        project_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        input_dir = os.path.join(project_dir, 'data', 'input')
        output_dir = os.path.join(project_dir, 'data', 'output')

        # Sprawdzenie folderu wejściowego
        if not os.path.exists(input_dir):
            raise FileNotFoundError(f"Folder wejściowy {input_dir} nie istnieje")

        if len(os.listdir(input_dir)) == 0:
            raise ValueError("Brak plików w folderze input")

        # Inicjalizacja procesora
        processor = RouteProcessor(input_dir=input_dir, output_dir=output_dir)
        df = processor.merge_files()

        if df.empty:
            raise ValueError("Brak danych do analizy - sprawdź pliki wejściowe")

        # Generowanie raportu
        analyzer = RouteAnalyzer()
        stats = analyzer.calculate_basic_stats(df)

        if stats.empty:
            raise ValueError("Nie udało się wygenerować statystyk")

        # Tworzenie folderu output jeśli nie istnieje
        os.makedirs(output_dir, exist_ok=True)

        # Formatowanie raportu
        report = f"""
        Raport statystyk tras
        --------------------
        Liczba tras: {len(stats)}
        Średnia długość trasy: {stats['distance_meters'].mean():.2f} m
        Maksymalna wysokość: {stats['altitude']['max'].max()} m n.p.m.
        Średnie nachylenie: {stats['avg_slope'].mean():.2f} %
        """

        # Zapis raportu
        output_path = os.path.join(output_dir, 'stats_report.txt')
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)

        print(f"Raport zapisano w: {output_path}")
        return stats

    except Exception as e:
        print(f"Błąd podczas generowania raportu: {str(e)}")
        return pd.DataFrame()


if __name__ == "__main__":
    generate_report()