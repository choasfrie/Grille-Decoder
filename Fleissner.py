import numpy as np

# Funktion zur Rotation einer Koordinate um 90° im Uhrzeigersinn
def rotate_coord(coord, k, n):
    i, j = coord
    for _ in range(k):
        i, j = j, n - 1 - i
    return i, j


def main():
    # Rastergröße einlesen
    try:
        n = int(input("Geben Sie die Rastergröße n (gerade Zahl) ein: "))
    except ValueError:
        print("Ungültige Eingabe für n. Programm beendet.")
        return
    if n % 2 != 0:
        print("n muss gerade sein. Programm beendet.")
        return

    # Maske einlesen (0 = Loch, alles andere = kein Loch)
    print(f"Geben Sie die Maske als {n} Zeilen mit je {n} Werten ein (0=Loch), getrennt durch Leerzeichen oder Komma:")
    mask = []
    for i in range(n):
        parts = input(f"Maske Zeile {i+1}: ").replace(',', ' ').split()
        if len(parts) != n:
            print(f"Fehler: Zeile {i+1} hat nicht {n} Werte. Programm beendet.")
            return
        row = [0 if x == '0' else 1 for x in parts]
        mask.append(row)
    mask = np.array(mask)

    # Koordinaten der Löcher sammeln
    holes = list(zip(*np.where(mask == 0)))
    if not holes:
        print("Keine Löcher gefunden. Programm beendet.")
        return

    # kodierter Text als Raster einlesen
    print(f"\nGeben Sie nun den Chiffretext als {n} Zeilen mit je {n} Buchstaben ein, getrennt durch Leerzeichen oder Komma:")
    letter_rows = []
    for i in range(n):
        parts = input(f"Text Zeile {i+1}: ").replace(',', ' ').split()
        if len(parts) != n or any(len(ch) != 1 for ch in parts):
            print(f"Fehler: Zeile {i+1} muss {n} einzelne Buchstaben enthalten. Programm beendet.")
            return
        letter_rows.append(parts)
    letter_grid = np.array(letter_rows)

    # Entschlüsselung: vier Drehungen, Löcher sortiert von links nach rechts
    plaintext = []
    for k in range(4):
        # Löcher für diese Drehung berechnen
        rotated = [rotate_coord(coord, k, n) for coord in holes]
        # Sortieren: nach Zeile aufsteigend, Spalte aufsteigend (links->rechts)
        rotated_sorted = sorted(rotated, key=lambda x: (x[0], x[1]))
        for i, j in rotated_sorted:
            plaintext.append(letter_grid[i, j])

    # Ergebnis ausgeben
    print("\nEntschlüsselter Text:")
    print(''.join(plaintext))

if __name__ == "__main__":
    main()
