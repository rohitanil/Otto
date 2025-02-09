import heapq
from collections import defaultdict

import db_connection as db
import pandas as pd

max_posters_per_judge = 6
judge_assignments = defaultdict(int)
poster_assignments = {}

def fetch_poster_data():
    conn, cursor = db.get_cursor()
    try:
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM poster_judge_mapping;"
        cursor.execute(query)
        rows = cursor.fetchall()
        df = pd.DataFrame(rows)
        columns = ["id", "poster_number", "judge1_id", "judge1_score", "judge2_id", "judge2_score", "judge3_id",
                   "judge3_score", "judge4_id", "judge4_score", "judge5_id", "judge5_score"]
        data_frame = pd.DataFrame(df, columns=columns)
        return data_frame
    finally:
        if cursor:
            cursor.close()
        conn.close()

def calculate_delta(df,poster_ids,i):
    df.set_index("poster_number", inplace=True)
    delta_dict = {}
    for id in poster_ids:
        row = df.loc[id]
        delta = row[f"judge{i}_score"] - row[f"judge{i+1}_score"]
        delta_dict[id] = delta
    top = [poster for poster, _ in heapq.nlargest(max_posters_per_judge, delta_dict.items(), key=lambda x: x[1])]
    for id in top:
        if(len(poster_assignments.get(id,[])) <2 and judge_assignments[df.loc[id][f"judge{i}_id"]] < max_posters_per_judge):
            poster_assignments.setdefault(id,[]).append([df.loc[id][f"judge{i}_id"]])
            judge_assignments[df.loc[id][f"judge{i}_id"]] += 1



def check_for_conflicts(data,judge_id,i):
    poster_ids = []
    count = 0
    for _, row in data.iterrows():
        if row[f"judge{i}_id"] == judge_id:
            poster_id = row["poster_number"]
            poster_ids.append(poster_id)
            count += 1

    if(count > max_posters_per_judge):
        calculate_delta(data,poster_ids,i)
        return True
    return False

def assign_judges():
    df = fetch_poster_data()
    for _, row in df.iterrows():
        for i in range(1,6):
            if (len(poster_assignments.get(row["poster_number"],[])) < 2):
                judge_id = row[f"judge{i}_id"]
                check_for_conflicts(df,judge_id, i)
                if judge_assignments[judge_id] < max_posters_per_judge:
                    poster_assignments.setdefault(row["poster_number"],[]).append([judge_id])
                    judge_assignments[judge_id] += 1
            else:
                break
    assigned_df = pd.DataFrame(list(poster_assignments.items()), columns=["poster_number", "assigned_judges"])
    return assigned_df


def save_to_db():
    judge_query = "SELECT id FROM judges j WHERE j.judge_number = %s"
    abstract_query = "SELECT id FROM abstracts WHERE poster_number = %s"
    insert_query = "INSERT INTO poster_score (judge_id, abstract_id, score) VALUES (%s, %s, %s)"

    conn, cursor = db.get_cursor()
    cursor = conn.cursor(buffered=True)
    for poster_id, judges in poster_assignments.items():

        cursor.execute(abstract_query, (poster_id,))
        abstract_result = cursor.fetchone()

        if not abstract_result:
            print(f"No abstract_id found for poster_id {poster_id}, skipping...")
            continue

        abstract_id = abstract_result[0]  # Extracting abstract_id from the result


        for judge_list in judges:
            for judge_number in judge_list:
                # Fetch judge_id
                cursor.execute(judge_query, (int(judge_number),))
                judge_result = cursor.fetchone()

                if not judge_result:
                    print(f"No judge_id found for judge_number {judge_number}, skipping...")
                    continue

                judge_id = judge_result[0]  #


                cursor.execute(insert_query, (judge_id, abstract_id, 0))


    conn.commit()
    cursor.close()
    conn.close()
#assign_judges()
#save_to_db()