import requests
from bs4 import BeautifulSoup
import os
import time
import json

# Target: 2M tokens (~1.5M words)
# We will pull from Wikipedia and NASA feeds

DATA_DIR = "data/raw"
os.makedirs(DATA_DIR, exist_ok=True)

def fetch_wikipedia_page(title):
    url = f"https://en.wikipedia.org/w/api.php"
    headers = {"User-Agent": "GraphRAG-Hackathon-Bot/1.0 (ronit@example.com)"}
    params = {
        "action": "query",
        "format": "json",
        "titles": title,
        "prop": "extracts",
        "explaintext": True,
    }
    response = requests.get(url, params=params, headers=headers)
    data = response.json()
    pages = data.get("query", {}).get("pages", {})
    for page_id in pages:
        return pages[page_id].get("extract", "")
    return ""

def get_category_members(category_name):
    url = "https://en.wikipedia.org/w/api.php"
    headers = {"User-Agent": "GraphRAG-Hackathon-Bot/1.0 (ronit@example.com)"}
    params = {
        "action": "query",
        "format": "json",
        "list": "categorymembers",
        "cmtitle": f"Category:{category_name}",
        "cmlimit": 50
    }
    response = requests.get(url, params=params, headers=headers)
    data = response.json()
    return [item["title"] for item in data.get("query", {}).get("categorymembers", [])]

def main():
    categories = [
        "SpaceX_missions", "NASA_missions", "Artemis_program", 
        "Human_spaceflight", "Space_launch_vehicles", "Space_stations",
        "Mars_exploration", "Lunar_exploration", "Robotic_spacecraft",
        "Space_agencies", "Astronomical_objects", "Space_telescopes", 
        "History_of_astronomy", "Aerospace_companies", "Satellite_constellations",
        "Rocket_engines", "Space_shuttle_program", "Apollo_program",
        "Soviet_space_program", "Planetary_science", "Astrophysics",
        "Cosmology", "Exoplanets", "Search_for_extraterrestrial_intelligence",
        "Lists_of_astronomers", "Space_exploration_stubs", "Unmanned_space_missions",
        "Deep_space_probes", "Extraterrestrial_life", "Astrobiology",
        "Space_mining", "Colonization_of_the_Moon", "Colonization_of_Mars",
        "Future_of_space_exploration", "Commercial_use_of_space"
    ]
    
    print("Starting aggressive data collection...", flush=True)
    with open(os.path.join(DATA_DIR, "space_data.txt"), "a", encoding="utf-8") as f:
        for cat in categories:
            try:
                print(f"Crawling Category: {cat}...", flush=True)
            except UnicodeEncodeError:
                print(f"Crawling Category: [Unicode Name]...", flush=True)
                
            members = get_category_members(cat)
            for member in members:
                try:
                    # Clean member name for console output
                    safe_member = member.encode('ascii', 'ignore').decode('ascii')
                    print(f"  Fetching: {safe_member}...", flush=True)
                except:
                    pass

                text = fetch_wikipedia_page(member)
                if text:
                    f.write(f"### {member}\n{text}\n\n")
                    f.flush()
                time.sleep(0.05) 

    # Read back to count words
    if os.path.exists(os.path.join(DATA_DIR, "space_data.txt")):
        with open(os.path.join(DATA_DIR, "space_data.txt"), "r", encoding="utf-8") as f:
            all_text = f.read()
        
        word_count = len(all_text.split())
        print(f"Total words collected: {word_count}", flush=True)
        print(f"Estimated tokens (words * 1.3): {int(word_count * 1.3)}", flush=True)

if __name__ == "__main__":
    main()
