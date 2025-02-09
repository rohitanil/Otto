import traceback
import ingest
import selector
import assignment
import output
import web_scrape

def main():
    print("🚀 Starting the ECS Challenge Project...")

    try:
        print("\n📥 Step 1: Ingesting Data from Excel into Database...")
        ingest.insert_judges(ingest.read_excel("resources/Example_list_judges.xlsx"))
        ingest.insert_abstracts(ingest.read_excel("resources/Sample_input_abstracts.xlsx"))
        print("✅ Data ingestion completed.\n")
    except Exception as e:
        print("❌ Error in Data Ingestion:", str(e))
        traceback.print_exc()

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

    try:
        print("\n📝 Step 3: Running Abstracts based Judge Scoring using llm ...")
        selector.run()
        print("✅ Judges scored\n")
    except Exception as e:
        print("❌ Error in Judge Selection:", str(e))
        traceback.print_exc()

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

if __name__ == "__main__":
    main()
