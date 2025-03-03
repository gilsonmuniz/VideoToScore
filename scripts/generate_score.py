import os

def generate_music_xml(music_name, detected_notes):
    output_dir = "music_scores"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f"{music_name}.xml")

    with open(output_file, "w") as f:
        f.write("<score-partwise version='3.0'>\n")
        f.write("  <part-list/>\n")
        f.write("  <part id='P1'>\n")

        for note in detected_notes:
            f.write(f"    <note>{note}</note>\n")

        f.write("  </part>\n")
        f.write("</score-partwise>\n")

    print(f"Partitura salva em: {output_file}")

if __name__ == "__main__":
    music_name = input("Insira o nome da música: ")
    generate_music_xml(music_name, ["C4", "D4", "E4", "F4"])
