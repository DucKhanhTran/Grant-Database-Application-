import sqlite3
import Data_Generator

# Function to drop all tables in the database
def database_drop(databaseName): 
    # Connect to the database
    conn = sqlite3.connect(databaseName)
    cursor = conn.cursor()
    try:
        # Get a list of all tables in the database
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        # Drop all tables
        for table in tables:
            cursor.execute("DROP TABLE IF EXISTS " + table[0])
        print("All tables dropped successfully.")

        # Commit the changes
        conn.commit()

    except sqlite3.Error as e:
        print("An error occurred:", e)
        
    # Close the connection
    conn.close()    

# Function to create a new database
def database_create(databaseName):
    # Connect to the database (or create it if it doesn't exist)
    conn = sqlite3.connect(databaseName)
    cursor = conn.cursor()

    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS researchers (
            email TEXT PRIMARY KEY,
            firstName TEXT,
            lastName TEXT,
            organization TEXT,
            department TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS proposal (
            proposalID INTEGER PRIMARY KEY,
            competitionID INTEGER,
            applicationStatus TEXT,
            requestedAmount REAL,
            awardAmount REAL,       
            submissionDate TEXT,
            awardDate TEXT,
            rejectDate TEXT,       
            FOREIGN KEY (competitionID) REFERENCES competition(competitionID)       
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS researching (
            email TEXT,
            proposalID INTEGER,
            principal BOOLEAN,
            PRIMARY KEY (email, proposalID),
            FOREIGN KEY (email) REFERENCES researchers(email),
            FOREIGN KEY (proposalID) REFERENCES proposal(proposalID)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS competition (
            competitionID INTEGER PRIMARY KEY,
            title TEXT,
            applicationDeadline TEXT,
            competitionStatus TEXT,
            area TEXT,
            description TEXT,
            openDate TEXT,
            closeDate TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reviewAssignment (
            assignmentID INTEGER PRIMARY KEY,
            proposalID INTEGER,
            assignmentDeadline TEXT,
            FOREIGN KEY (proposalID) REFERENCES proposal(proposalID)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reviewing (
            assignmentID INTEGER,
            email TEXT,
            submissionStatus TEXT,
            reviewSubmission TEXT,
            PRIMARY KEY (assignmentID, email),
            FOREIGN KEY (assignmentID) REFERENCES reviewAssignment(assignmentID),
            FOREIGN KEY (email) REFERENCES researchers(email)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS conflictsOfInterest (
            email TEXT,
            proposalID INTEGER,
            PRIMARY KEY (email, proposalID),
            FOREIGN KEY (email) REFERENCES researchers(email),
            FOREIGN KEY (proposalID) REFERENCES proposal(proposalID)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS committeesMeeting (
            meetingID INTEGER PRIMARY KEY,
            MeetingDate TEXT
        )
    ''')      
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS discussion (       
            meetingID INTEGER,
            competitionID INTEGER,
            discussionSummary TEXT,
            PRIMARY KEY (meetingID, competitionID),
            FOREIGN KEY (meetingID) REFERENCES committeesMeeting(meetingID),
            FOREIGN KEY (competitionID) REFERENCES competition(competitionID)
        )
    ''')      
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS discussing (
            meetingID INTEGER,
            competitionID INTEGER,
            email TEXT,   
            participatingStatus BOOLEAN,
            comment TEXT,       
            PRIMARY KEY (meetingID, competitionID, email),
            FOREIGN KEY (meetingID) REFERENCES committeesMeeting(meetingID),
            FOREIGN KEY (competitionID) REFERENCES competition(competitionID),
            FOREIGN KEY (email) REFERENCES researchers(email)       
        )
    ''')           

    # Create trigger to enforce constraint
    cursor.execute('''
        CREATE TRIGGER IF NOT EXISTS check_conflict_insert
        BEFORE INSERT ON reviewing
        FOR EACH ROW
        BEGIN
            -- Check if the reviewer has a conflict of interest with the proposal
            SELECT
                CASE
                    WHEN EXISTS (
                        SELECT * FROM conflictsOfInterest
                        WHERE email = NEW.email AND proposalID = (
                            SELECT proposalID FROM reviewAssignment
                            WHERE assignmentID = NEW.assignmentID
                        )
                    )
                    THEN RAISE(ABORT, 'Reviewer has a conflict of interest with the proposal')
                END;                  
        END;



    ''')

    # Commit changes and close connection
    conn.commit()
    conn.close()
    
    print("Database created successfully.")


    
database_drop("council.db")
database_create("council.db")
Data_Generator.data_generator("council.db")





