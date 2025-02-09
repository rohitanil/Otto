# 🏆 ECS Challenge Part1 - Research Poster-Judge Assignment

## 📌 Overview
This project automates the process of **assigning judges** to **research posters** based on constraints such as **expertise, availability, and conflicts of interest**. It also generates **various reports**, including **judge assignments, poster allocations, and a 0-1 matrix representation**.

### **🔹 Key Features**
- 📥 **Data Ingestion**: Reads judge and abstract data from Excel and stores it in a MySQL database.
- 🕵️‍♂️ **Web Scraping**: Scrapes faculty profiles for research interests and create research interests labels using llm.
- 🤖 **Judge scoring**: Uses **LLM (Claude 3.5)** to rank judges based on relevance to research topics.
- 🎯 **Constraint-Based Judges Assignments**: Allocates judges to posters filtering based on constraints, ensuring fairness and avoiding conflicts.
- 📊 **Excel Reports**: Generates files showing **poster assignments, judge allocations, and a 0-1 matrix**.



## 📁 Project Structure

```
📦 Hackathon Project
├── main.py                # Entry point of the project
├── assignment.py          # Judge-to-poster assignment logic
├── db_connection.py       # Database connection helper
├── ingest.py              # Reads & inserts data into the database
├── llm.py                 # Calls LLM API for judge ranking
├── output.py              # Generates Excel reports
├── selector.py            # Matches research abstracts to judges
├── web_scrape.py          # Scrapes judge research data
└── README.md              # This documentation file
```

---

## 🛠️ **Setup Instructions**

### **1️⃣ Install Required Packages**

Ensure you have **Python 3.8+** installed. Then, install dependencies:

```bash
pip install mysql-connector-python pandas selenium openpyxl rapidfuzz anthropic
```

### **2️⃣ Database Setup**

- Docker Composer should createthe db  Schema required for the project. If not, you can create the schema manually using the SQL commands in init.sql file found in root directory.  
- Also adding a master.sql * (resources folder) file with all of the data ( including scraping and llm responses) pre filled , for a just in case scenario if facing any issues with Anthropic Keys or miscellaneous issues. 


### **3️⃣ Required Input Files**

Ensure you have the following input files in the `resources/` directory:

- **Judges List**: `resources/Example_list_judges.xlsx`
- **Abstracts Data**: `resources/Sample_input_abstracts.xlsx`

These files are required for the ingestion process.

### **4️⃣ Setting Up Anthropic API Key**

This project requires an Anthropic API Key for AI-based judge ranking and research label generation.[How to generate Anthropic API Token?](https://docs.anthropic.com/en/api/getting-started)
To set it up, add the key as an environment variable:

````
export ANTHROPIC_KEY="your_anthropic_api_key"
````

Or, if using Windows Command Prompt:

````
set ANTHROPIC_KEY=your_anthropic_api_key
````

Make sure this environment variable is accessible before running the project.
## 🚀 **How to Run the Project**

After setting up dependencies and the database, run:

```bash
python main.py
```

This will execute all steps:

1. **Data Ingestion** (Excel to DB)
2. **Web Scraping** (Faculty Research Data)
3. **AI Judge Matching**
4. **Judge Assignment**
5. **Excel Report Generation**

---

## 📊 **Generated Output Files**

The project creates **three key Excel files**:

| File                            | Description                              |
| ------------------------------- | ---------------------------------------- |
| `abstracts_with_judges.xlsx`    | Judges assigned to each poster           |
| `judges_with_posters.xlsx`      | Posters assigned to each judge           |
| `poster_judge_full_matrix.xlsx` | 0-1 matrix showing poster-judge mappings |

---

## ⚠️ **Error Handling**

Each step in `main.py` has `` blocks to ensure the program continues running even if an error occurs.

Example:

```python
try:
    output.file1()
except Exception as e:
    print("❌ Error generating file1:", str(e))
