import streamlit as st
import sqlite3
from datetime import datetime

# Initialize the database
def init_db():
    conn = sqlite3.connect("learning_app.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS entries (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        date TEXT,
                        topic TEXT,
                        what_i_know TEXT,
                        questions TEXT,
                        aha_moments TEXT)''')
    conn.commit()
    conn.close()

# Add a new entry to the database
def add_entry(topic, what_i_know, questions, aha_moments):
    conn = sqlite3.connect("learning_app.db")
    cursor = conn.cursor()
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''INSERT INTO entries (date, topic, what_i_know, questions, aha_moments)
                      VALUES (?, ?, ?, ?, ?)''', (date, topic, what_i_know, questions, aha_moments))
    conn.commit()
    conn.close()

# Retrieve all entries from the database
def get_entries():
    conn = sqlite3.connect("learning_app.db")
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM entries''')
    rows = cursor.fetchall()
    conn.close()
    return rows

# Update an existing entry
def update_entry(entry_id, topic, what_i_know, questions, aha_moments):
    conn = sqlite3.connect("learning_app.db")
    cursor = conn.cursor()
    cursor.execute('''UPDATE entries
                      SET topic = ?, what_i_know = ?, questions = ?, aha_moments = ?
                      WHERE id = ?''', (topic, what_i_know, questions, aha_moments, entry_id))
    conn.commit()
    conn.close()

# Delete an entry
def delete_entry(entry_id):
    conn = sqlite3.connect("learning_app.db")
    cursor = conn.cursor()
    cursor.execute('''DELETE FROM entries WHERE id = ?''', (entry_id,))
    conn.commit()
    conn.close()

# Streamlit App
def main():
    st.title("Learning Journal App")

    # Initialize database
    init_db()

    menu = ["Add Entry", "View Entries", "Edit Entry", "Delete Entry"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Add Entry":
        st.subheader("Add a New Entry")
        with st.form(key="entry_form"):
            topic = st.text_input("Topic")
            what_i_know = st.text_area("What I Know for Sure")
            questions = st.text_area("Questions That I Have")
            aha_moments = st.text_area("Ah-Ha Moments")
            submit_button = st.form_submit_button("Submit")

        if submit_button:
            add_entry(topic, what_i_know, questions, aha_moments)
            st.success("Entry added successfully!")

    elif choice == "View Entries":
        st.subheader("All Entries")
        entries = get_entries()
        if entries:
            for entry in entries:
                st.write(f"**Date:** {entry[1]}")
                st.write(f"**Topic:** {entry[2]}")
                st.write(f"**What I Know for Sure:** {entry[3]}")
                st.write(f"**Questions That I Have:** {entry[4]}")
                st.write(f"**Ah-Ha Moments:** {entry[5]}")
                st.write("---")
        else:
            st.info("No entries found.")

    elif choice == "Edit Entry":
        st.subheader("Edit an Entry")
        entries = get_entries()
        if entries:
            entry_id = st.selectbox("Select an Entry to Edit", [entry[0] for entry in entries])
            entry = next((e for e in entries if e[0] == entry_id), None)
            if entry:
                with st.form(key="edit_form"):
                    updated_topic = st.text_input("Topic", value=entry[2])
                    updated_what_i_know = st.text_area("What I Know for Sure", value=entry[3])
                    updated_questions = st.text_area("Questions That I Have", value=entry[4])
                    updated_aha_moments = st.text_area("Ah-Ha Moments", value=entry[5])
                    update_button = st.form_submit_button("Update")

                if update_button:
                    update_entry(entry_id, updated_topic, updated_what_i_know, updated_questions, updated_aha_moments)
                    st.success("Entry updated successfully!")
        else:
            st.info("No entries found.")

    elif choice == "Delete Entry":
        st.subheader("Delete an Entry")
        entries = get_entries()
        if entries:
            entry_id = st.selectbox("Select an Entry to Delete", [entry[0] for entry in entries])
            delete_button = st.button("Delete")

            if delete_button:
                delete_entry(entry_id)
                st.success("Entry deleted successfully!")
        else:
            st.info("No entries found.")

if __name__ == "__main__":
    main()
