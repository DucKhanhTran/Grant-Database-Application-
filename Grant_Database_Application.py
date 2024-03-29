import sqlite3
from faker import Faker


# Connect to the database
conn = sqlite3.connect('grant.db')

# Create a cursor object to interact with the database
cursor = conn.cursor()

# Define global variables
user_input = ""

# Start the interfere
print("Welcome to the Grant Database!\n")

# Define functions
def print_command():
    # Declare global variables
    global user_input
    
    # Print out command list
    print("\nPlease select your request by enter command number.\n"
        "0: Exit\n"
        "1: Find grant competition with at least one submitted significant proposal\n"
        "2: Find proposal with highest requested amount in an area\n"
        "3: Find highest awarded proposal submitted before a date\n"
        "4: Find average request/awarded discrepancy for an area\n"
        "5: Assign reviewers for a grant proposal\n"
        "6: Find proposal to review\n")
    
    # Validate user_input
    value_to_check = {0,1,2,3,4,5,6}
    
    user_input = input("Enter your command number: ")
    if int(user_input) not in value_to_check:
        print("Invalid command, please try again\n")
        print_command()

# Convert user_input to integer
        
def command_exe():
    # Declare global variables
    global user_input
    command = int(user_input)
    if command == 0:
        command_0()
    elif command == 1:
        command_1()
    elif command == 2:
        command_2()
    elif command == 3:
        command_3()
    elif command == 4:
        command_4()
    elif command == 5:
        command_5()
    elif command == 6:
        command_6()
    else:
        print("Invalid command, please try again\n")
        print_command()
    user_input= input("Would you like to perform another command? y/n ")
    if user_input == "y":
        print_command()
        command_exe()
    else:
        print("Goodbye!")
        conn.close()
        exit()
    
# Define command functions
       
def command_0():
    print("Goodbye!")
    conn.close()
    exit()

def command_1():
    # Get user input
    month = input("Enter the month %mm: ")
    
    # Define the query to find the competition with at least one submitted significant proposal with requested amount > 20000 or competition with at least 20 researchers at a specific month
    
    sql_query = """
        SELECT DISTINCT competition.competitionID, competition.title
        FROM competition
        JOIN proposal 
        WHERE (requestedAmount > 20000 OR (
            SELECT COUNT(email)
            FROM researching
            WHERE proposalID = proposal.proposalID) >= 10)
        AND strftime('%m', competition.openDate) = ?
        ORDER BY competition.competitionID
    """        
    # Execute the query
    cursor.execute(sql_query, (month,))
    
    # Fetch the results
    results = cursor.fetchall()

    # Exception handling
    if len(results) == 0:
        print("No results found.")    
        
    # Print the results without the brackets
    for row in results:
        print(f"Competition ID: {row[0]}, Competition Title: {row[0]}")
        
    
        
def command_2():
    # Get user input
    area = input("Enter the area: ")
    
    # Define the query
    sql_query = """
        SELECT proposalID, requestedAmount
        FROM proposal 
        JOIN competition ON competition.competitionID = proposal.competitionID
        WHERE area COLLATE NOCASE = ?
        ORDER BY requestedAmount DESC
        LIMIT 1
        """
        
    # Execute the query
    cursor.execute(sql_query, (area,))
    
    # Fetch the results
    results = cursor.fetchall()
    
    # Exception handling
    if len(results) == 0:
        print("No results found.")
        
    # Print the results
    for row in results: 
        print(f"Proposal ID: {row[0]}, Requested Amount: {row[1]}")
        
def command_3():
    # Get user input
    date = input("Enter the date in format YYYY-MM-DD: ")
    
    # Define the query
    sql_query = """
        SELECT proposalID, awardAmount
        FROM proposal
        JOIN competition
        WHERE strftime('%Y-%m-%d' ,submissionDate) < strftime('%Y-%m-%d', ?)
        ORDER BY awardAmount DESC
        LIMIT 1
        """
        
    # Execute the query
    cursor.execute(sql_query, (date,))
    
    # Fetch the results
    results = cursor.fetchall()
    
    # Exception handling
    if len(results) == 0:
        print("No results found.")
        
    # Print the results
    for row in results:
        print(f"Proposal ID: {row[0]}, Award Amount: {row[1]}")
    
def command_4():
    # Get user input
    area = input("Enter the area: ")
    
    # Define the query
    sql_query = """
        SELECT AVG(ABS(requestedAmount - awardAmount))
        FROM proposal
        JOIN competition
        WHERE area COLLATE NOCASE = ?
        GROUP BY area
        """
        
    # Execute the query
    cursor.execute(sql_query, (area,))
    
    # Fetch the results
    results = cursor.fetchall()
    
    # Exception handling
    if len(results) == 0:
        print("No results found.")
    
    # Print the results
    for row in results:
        print(f"Average Requested/Awarded Discrepancy: {row[0]}")
        
def command_5():
    # Declare global variables
    global user_input

    # Get user input
    proposalID = input("Enter the proposal ID: ")
    
    # Check if the proposal exists and open for review
    sql_query =     """
                    SELECT *
                    FROM proposal
                    WHERE proposalID = ? 
                    AND applicationStatus = 'Pending'
                    """
                    
    cursor.execute(sql_query, (proposalID,))
    results = cursor.fetchall()
    if len(results) == 0: 
        print("Proposal does not exist or has been closed.\n")
        return
    
    # Check conflict of interest list for the proposal
    user_input = input("Do you want to check conflict of interest list? y/n: ")
    if user_input == "y":
        sql_query = """
                        SELECT firstName, lastName, researchers.email
                        FROM conflictsOfInterest
                        JOIN researchers 
                        WHERE proposalID = ?
                    """
    
    cursor.execute(sql_query, (proposalID,))
    results = cursor.fetchall()
    if len(results) < 0:
        print("No conflict of interest found.")

    for row in results:
        print(f"Name: {row[0]} {row[1]}, Email Address: {row[2]}")
        
    # Get user input
    user_input = input("What do you want to do?\n"
                       "1. Create new assignment\n"
                       "2. Add reviewers to existing assignment\n"
                       "3. Return to command menu\n"
                       "Enter your selection: ")
    
    if user_input == "3":
        return
    elif user_input == "1":
        create_assignment(proposalID)
    elif user_input == "2":
        add_reviewer(proposalID)
        
    return
    
# Create a new review assignment 
def create_assignment(proposalID):
    # Generate a new assignment ID
    cursor.execute("SELECT MAX(assignmentID) FROM reviewAssignment ")
    assignmentID = cursor.fetchone()[0]
    assignmentID = 0 if assignmentID is None else assignmentID + 1
    
    # Create a new review assignment
    sql_query = """
        INSERT INTO reviewAssignment (assignmentID, proposalID)
        VALUES (?, ?)
        """
    cursor.execute(sql_query, (assignmentID, proposalID))
    
    # Commit the changes
    conn.commit()
    print("Assignment created successfully.\n")
    
    # Asking for adding reviewers
    user_input = input("Do you want to add reviewers to the assignment? y/n: ")
    if user_input == "y":
        add_reviewer(proposalID)
        
    else: return
    

# Add new reviewers to existing review assignment   
def add_reviewer(proposalID):
    # Get user input
    email = input("Enter the email address of the reviewer, seperated by comma: ")
    email_list = [item.strip() for item in email.split(',')]
    
    # Check if the reviewer exists
    for email in email_list:
        sql_query = """
            SELECT *
            FROM researchers
            WHERE email = ?
            """
        cursor.execute(sql_query, (email,))
        results = cursor.fetchall()
        if len(results) == 0:
            print("Reviewer does not exist.")
            continue
        else: 
            
    
    # Check if the reviewer has a conflict of interest with the proposal
    sql_query = """
        SELECT *
        FROM conflictsOfInterest
        WHERE email = ? AND proposalID = ?
        """
    cursor.execute(sql_query, (email, proposalID))
    results = cursor.fetchall()
    if len(results) > 0:
        print("Reviewer has a conflict of interest with the proposal.")
        return
    
    # Check if the reviewer has been assigned to the proposal
    sql_query = """
        SELECT *
        FROM reviewing
        WHERE email = ? AND proposalID = ?
        """
    cursor.execute(sql_query, (email, proposalID))
    results = cursor.fetchall()
    if len(results) > 0:
        print("Reviewer has already been assigned to the proposal.")
        return
    
    # Add the reviewer to the proposal
    sql_query = """
        INSERT INTO reviewing (email, proposalID)
        VALUES (?, ?)
        """
    cursor.execute(sql_query, (email, proposalID))
    
    # Commit the changes
    conn.commit()
    
    print("Reviewer added successfully.")
def command_6():    
    # Get user input
    name = input("Enter your first and last name: ")
    first_name, last_name = name.split()
    
    # Define the query
    sql_query = """
        SELECT proposalID, title, area, requestedAmount
        FROM proposal
        JOIN competition ON competitionID
        WHERE proposalID NOT IN (
            SELECT proposalID
            FROM reviewing
            WHERE email = (
                SELECT email
                FROM researcher
                WHERE firstName = ? AND lastName = ?))
        """
    
    # Execute the query
    cursor.execute(sql_query, (first_name, last_name))
    
    # Fetch the results
    results = cursor.fetchall()
    
    # Exception handling
    if len(results) == 0:
        print("No results found.")
        
    # Print the results
    for row in results:
        print(row)    
        
     
# Main program
print_command()
command_exe()
