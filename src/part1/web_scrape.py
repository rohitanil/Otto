import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from rapidfuzz import process, fuzz
from anthropic import Anthropic
from db_connection import get_cursor

options = Options()
options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)

url = "https://ecs.syracuse.edu/faculty-staff/?category=0&people="
faculty_data = {}
faculty_profiles = {}


def scrape_data():
    driver.get(url)
    faculty_members = driver.find_elements(By.CLASS_NAME, "ecs-profile")

    for faculty in faculty_members:
        try:
            name_element = faculty.find_element(By.CLASS_NAME, "profile-name")
            name = name_element.text.strip()
            profile_url = name_element.find_element(By.TAG_NAME, "a").get_attribute("href")

            faculty_profiles[name] = profile_url
        except Exception as e:
            print(f"Error scraping {name}: {e}")

    for name, profile_url in faculty_profiles.items():
        driver.get(profile_url)
        # time.sleep(1)
        page_text = driver.find_element(By.CLASS_NAME, "entry-content").text.strip()
        faculty_data[name] = page_text
        #print(f"Scraped {name}'s profile.")
    driver.quit()
    print(f"Scraped {len(faculty_data)} faculty profiles successfully!")

    # for key, value in list(faculty_data.items())[:2]:
    #     print(f"\n🔹 {key}: {value[:500]}...\n")


def save_to_file():
    with open("faculty_profiles.txt", "w", encoding="utf-8") as f:
        print(len(faculty_data))
        for prof, text in faculty_data.items():
            f.write(f"{prof}\n{'=' * 50}\n{text}\n\n")


def name_match_service():
    conn, cursor = get_cursor()
    cursor.execute("SELECT first_name, last_name FROM judges")
    db_names = cursor.fetchall()

    db_name_dict = {" ".join(name): name for name in db_names}

    updates = []
    unmatched = []
    for faculty_name in faculty_data.keys():
        match_data = process.extractOne(faculty_name, db_name_dict.keys(), scorer=fuzz.ratio)

        if match_data:
            match, score, _ = match_data

            if score > 70:
                first_name, last_name = db_name_dict[match]
                research_text = faculty_data[faculty_name]

                updates.append((research_text, first_name, last_name))
                # print(f"Matched {faculty_name} -> {match} (Score: {score})")
            else:
                unmatched.append(faculty_name)

    update_query = """
        UPDATE judges 
        SET research_interests = %s 
        WHERE first_name = %s AND last_name = %s
    """

    cursor.executemany(update_query, updates)
    conn.commit()

    print(f"✅ Updated {len(updates)} records successfully!")


    cursor.close()
    conn.close()


def generate_research_categories_prompt(research_text: str) -> str:
    """Generate a structured prompt to extract the top 10 research categories from a given research text."""
    prompt = f"""As a research expert, analyze the following research text and provide the top 10 research categories that best describe the research areas covered.

    Research Text:
    {research_text}

    Please provide the top 10 research labels relevant to this research text as a comma-separated list. Do not add unnecessary text, just the answer."""
    return prompt


def get_research_labels(research_text):
    """Call Claude API to get research labels for the given research text."""
    api_key = os.getenv("ANTHROPIC_KEY")
    client = Anthropic(api_key=api_key)
    prompt = generate_research_categories_prompt(research_text)

    response = client.messages.create(
        model="claude-3-5-sonnet-latest",
        max_tokens=100,
        temperature=0,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text.strip()


def generate_research_labels():
    """Fetch research interests, generate research labels, and update the judges table."""
    conn, cursor = get_cursor()
    cursor.execute("SELECT id, research_interests FROM judges WHERE research_interests IS NOT NULL")
    judges = cursor.fetchall()

    for judge in judges:
        judge_id = judge[0]
        research_text = judge[1]
        research_labels = get_research_labels(research_text)
        print(judge_id, research_labels)
        cursor.execute(
            "UPDATE judges SET research_labels = %s WHERE id = %s",
            (research_labels, judge_id)
        )
    conn.commit()
    print("Updated research labels successfully.")


# scrape_data()
# name_match_service()
# generate_research_labels()
#
