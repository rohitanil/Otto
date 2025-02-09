import traceback
import ingest
import selector
import assignment
import output
import web_scrape
import db_connection as db
def main():
    print("🚀 Starting the ECS Challenge Project...")

    skip_ingestion = ingestion_check()
    if not skip_ingestion:
        try:
            print("\n📥 Step 1: Ingesting Data from Excel into Database...")
            ingest.insert_judges()
            ingest.insert_abstracts()
            print("✅ Data ingestion completed.\n")
        except Exception as e:
            print("❌ Error in Data Ingestion:", str(e))
            traceback.print_exc()
    else:
        print("⏭️ Skipping Step 1: Data already exists in the database.\n")

    scrape_check = web_scrape_check()
    if not scrape_check:
        try:
            print("\n🔎 Step 2: Scraping Faculty Profiles for Research Interests from ECS Website...")
            print("🔗 Sit Back, Will take some time (3-5 minutes )...")
            web_scrape.scrape_data()
            web_scrape.name_match_service()
            print("🔗 Creating Faculty's Research Interests Labels using llm\n")
            web_scrape.generate_research_labels()
            print("✅ Faculty profiles scraped and matched successfully.\n")
        except Exception as e:
            print("❌ Error in Web Scraping:", str(e))
            traceback.print_exc()
    else:
        print("⏭️ Skipping Step 2: Data already scraped\n")

    # research_label = research_label_check()
    # if not research_label:
    try:
        print("\n📝 Step 3: Running Abstracts based Judge Scoring using llm ...")
        selector.run()
        print("✅ Judges scored\n")
    except Exception as e:
        print("❌ Error in Judge Selection:", str(e))
        traceback.print_exc()
    # else:
    #     print("⏭️ Skipping Step 3: Research Labels already created\n")

    try:
        print("\n📌 Step 4: Assigning Judges to Posters Based on Constraints (Core Algo)...")
        assignment.assign_judges()
        assignment.save_to_db()
        print("✅ Poster assignments saved.\n")
    except Exception as e:
        print("❌ Error in Poster Assignments:", str(e))
        traceback.print_exc()

    try:
        print("\n📊 Step 5: Generating Excel Reports for Output...")
        output.file1()
        output.file2()
        output.file3()
        print("✅ Output files generated successfully.\n")
    except Exception as e:
        print("❌ Error in Generating Reports:", str(e))
        traceback.print_exc()

    print("\n🎉 Project Execution Completed Successfully!")


def ingestion_check():
    conn, cursor = db.get_cursor()

    query_judges = "SELECT COUNT(*) FROM judges"
    query_abstracts = "SELECT COUNT(*) FROM abstracts"

    cursor.execute(query_judges)
    judge_count = cursor.fetchone()[0]

    cursor.execute(query_abstracts)
    abstract_count = cursor.fetchone()[0]

    cursor.close()
    conn.close()
    return judge_count > 1 and abstract_count > 1

def web_scrape_check():
    conn, cursor = db.get_cursor()

    query_judges = "SELECT COUNT(*) FROM judges j where j.research_interests is not null"

    cursor.execute(query_judges)
    count = cursor.fetchone()[0]


    cursor.close()
    conn.close()
    return count > 1

def research_label_check():
    conn, cursor = db.get_cursor()

    query_judges = "SELECT COUNT(*) FROM judges j where j.research_labels is not null"

    cursor.execute(query_judges)
    count = cursor.fetchone()[0]


    cursor.close()
    conn.close()
    return count > 1

if __name__ == "__main__":
    main()
