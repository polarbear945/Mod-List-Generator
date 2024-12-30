import csv
import webbrowser

def open_links_from_csv(file_path):
    try:
        with open(file_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            
            for row in reader:
                link = row[1].strip()
                if link.startswith("http"):
                    webbrowser.open(link)
                    
        print("All links have been opened successfully.")
    except FileNotFoundError:
        print(f"Error: The file "{file_path}" was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

csv_file = "mods_details.csv"
open_links_from_csv(csv_file)
