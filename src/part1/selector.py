import uuid

from db_connection import get_cursor
import llm as llm
import json


class ResearchAbstract:
    def __init__(self, id, poster_number, title, abstract, advisor_first_name, advisor_last_name, program):
        self.id = id
        self.poster_number = poster_number
        self.title = title
        self.abstract = abstract
        self.advisor_first_name = advisor_first_name
        self.advisor_last_name = advisor_last_name
        self.program = program

    def __repr__(self):
        return f"ResearchAbstract({self.poster_number}, {self.title}, {self.advisor_last_name})"


def fetch_research_abstracts():
    conn, cursor = get_cursor()
    cursor = conn.cursor(dictionary=True)  # Use dictionary cursor for easy column access

    query = "SELECT * FROM abstracts where title IS NOT NULL"
    cursor.execute(query)

    abstracts = []

    for row in cursor.fetchall():
        abstract = ResearchAbstract(
            id=row["id"],
            poster_number=row["poster_number"],
            title=row["title"],
            abstract=row["abstract"],
            advisor_first_name=row["advisor_first_name"],
            advisor_last_name=row["advisor_last_name"],
            program=row["program"]
        )
        abstracts.append(abstract)

    cursor.close()
    conn.close()

    return abstracts


class ResearchJudge:
    def __init__(self, id, judge_number, first_name, last_name, department, hour_available, poster_count,
                 research_labels):
        self.id = id
        self.judge_number = judge_number
        self.first_name = first_name
        self.last_name = last_name
        self.department = department
        self.hour_available = hour_available
        self.poster_count = poster_count
        self.research_labels = research_labels

    def __repr__(self):
        return f"ResearchJudge({self.judge_number}, {self.first_name} {self.last_name}, {self.department})"


def fetch_research_judges():
    conn, cursor = get_cursor()
    cursor = conn.cursor(dictionary=True)  # Use dictionary cursor for easy column access

    query = "SELECT * FROM judges"
    cursor.execute(query)

    judges = []

    for row in cursor.fetchall():
        judge = ResearchJudge(
            id=row["id"],
            judge_number=row["judge_number"],
            first_name=row["first_name"],
            last_name=row["last_name"],
            department=row["department"],
            hour_available=row["hour_available"],
            poster_count=row["poster_count"],
            research_labels=row["research_labels"]
        )
        judges.append(judge)

    cursor.close()
    conn.close()
    return judges


research_judges = fetch_research_judges()
research_abstracts = fetch_research_abstracts()


def constraints(abst):
    judge_dict = {}
    even = True
    if (abst.poster_number % 2):
        even = False

    for judge in research_judges:
        if constraint_odd_even(even, judge.hour_available) and constraint_career_advisor(abst, judge):
            judge_dict[judge.judge_number] = {
                'name': judge.first_name + judge.last_name,  # Assuming the judge object has a 'name' attribute
                'research_labels': judge.research_labels
            }

    return judge_dict


def constraint_career_advisor(abst, judge):
    if (judge.first_name == abst.advisor_first_name and judge.last_name == abst.advisor_last_name):
        return False
    return True


def constraint_odd_even(even, hour_available):
    if even and (hour_available == "2" or hour_available == "both"):
        return True
    elif not even and (hour_available == "1" or hour_available == "both"):
        return True
    return False


def insert_data(data, poster_number, abstract_id):
    conn, cursor = get_cursor()

    sql = """   
    INSERT INTO poster_judge_mapping (
    id,
    poster_number, 
    judge1_id, judge1_score, 
    judge2_id, judge2_score, 
    judge3_id, judge3_score, 
    judge4_id, judge4_score, 
    judge5_id, judge5_score
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)

    """

    cursor.execute(sql, (abstract_id, poster_number, data[0]['id'], data[0]['relevance_score'], data[1]['id'],
                         data[1]['relevance_score'], data[2]['id'], data[2]['relevance_score'], data[3]['id'],
                         data[3]['relevance_score'], data[4]['id'], data[4]['relevance_score']))

    conn.commit()
    cursor.close()
    conn.close()
    print("Data inserted successfully!")


def get_llm_scores(abstract_text, judges_dict):
    return llm.top_k_judges(abstract_text, judges_dict)


def run():
    for abstract in research_abstracts:
        list_judges = constraints(abstract)
        llm_data = get_llm_scores(abstract.abstract, list_judges)
        parsed_data = json.loads(llm_data)
        print(parsed_data)
        insert_data(parsed_data, abstract.poster_number, abstract.id)


run()
