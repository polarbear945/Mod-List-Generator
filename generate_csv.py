import os
import requests
import json
import zipfile
import csv

def get_modrinth_details(mod_name):
    base_url = "https://api.modrinth.com/v2/search"
    params = {"query": mod_name, "limit": 1}
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data["hits"]:
            mod = data["hits"][0]
            slug = mod["slug"]
            project_id = mod["project_id"]
            link = f"https://modrinth.com/mod/{slug}"
            api_route = f"https://api.modrinth.com/v2/project/{project_id}"
            mod_details_response = requests.get(api_route)
            if mod_details_response.status_code == 200:
                mod_details = mod_details_response.json()
                supported_versions = " ".join(
                    [version for version in mod_details.get("game_versions", [])]
                )
                print(f"Found {mod["title"]} on Modrinth")
                return mod["title"], link, slug, api_route, supported_versions
    print(f"Could not find {mod_name} on Modrinth")
    return mod_name, None, None, None, None

def extract_fabric_mod_name(jar_path):
    try:
        with zipfile.ZipFile(jar_path, "r") as jar:
            if "fabric.mod.json" in jar.namelist():
                with jar.open("fabric.mod.json") as mod_json:
                    data = json.load(mod_json)
                    return data.get("name", os.path.basename(jar_path))
    except Exception as e:
        print(f"Error reading {jar_path}: {e}")
    return os.path.basename(jar_path)

def generate_csv(mods, csv_file):
    with open(csv_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Link", "File Name", "Slug", "API Route", "Supported Versions"])
        for mod in mods:
            writer.writerow(mod)

def main():
    folder_path = "mods"
    csv_output_file = "mods_details.csv"

    if not os.path.exists(folder_path):
        print("The specified folder does not exist.")
        return

    mods = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".jar"):
            jar_path = os.path.join(folder_path, file_name)
            mod_name = extract_fabric_mod_name(jar_path)
            name, link, slug, api_route, supported_versions = get_modrinth_details(mod_name)
            mods.append((name, link, file_name, slug, api_route, supported_versions))

    generate_csv(mods, csv_output_file)
    print(f"CSV file generated: {csv_output_file}")

main()