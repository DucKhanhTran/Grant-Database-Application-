import sqlite3
from faker import Faker


# Connect to the database
conn = sqlite3.connect('council.db')

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
    try: 
        int(user_input)
    except ValueError:
        print("Invalid command, please try again\n")
        print_command()

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
        JOIN proposal on competition.competitionID = proposal.competitionID
        WHERE (requestedAmount > 20000 OR (
            SELECT COUNT(email)
            FROM researching
            WHERE proposalID = proposal.proposalID
            GROUP BY proposalID) >= 10)
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
        print(f"Competition ID: {row[0]}, Competition Title: {row[1]}")
        
    
        
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
        JOIN competition ON competition.competitionID = proposal.competitionID
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
    
    # Check if there is any competition in the area
    sql_query = """
                    SELECT competitionID
                    FROM competition
                    WHERE area COLLATE NOCASE = ?
                    """
    cursor.execute(sql_query, (area,))
    results = cursor.fetchall()
    if len(results) == 0:
        print("No competition found in the area.\n")
        return
    # Define the query
    sql_query = """
        SELECT AVG(ABS(proposal.requestedAmount-proposal.awardAmount))
        FROM proposal
        WHERE competitionID IN (SELECT competitionID FROM competition WHERE area COLLATE NOCASE = ?)
        """
        
    # Execute the query
    cursor.execute(sql_query, (area,))
    
    # Fetch the results
    results = cursor.fetchall()
    
    # Exception handling
    if results[0][0] == None:
        print("There is no awarded proposal for this area yet.")
        return
    else: 
        # Print the results
        for row in results:
            print(f"Average Requested/Awarded Discrepancy: {row[0]}")
        return
        
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
    
    # Command menu for command_5
    command_5_menu(proposalID)    
        
    return

# Command menu for command_5
def command_5_menu(proposalID):
    user_input = input("What do you want to do?\n"
                       "1. Create new assignment\n"
                       "2. View existing assignments\n"
                       "3. Add reviewers to existing assignment\n"
                       "4. Check conflict of intererest for the proposal\n"
                       "5. Return to command menu\n"
                       "Enter your selection: ")
    
    if user_input == "1":
        create_assignment(proposalID)
        command_5_menu(proposalID)
    elif user_input == "2":
        view_assignment(proposalID)
        command_5_menu(proposalID)
    elif user_input == "3":
        add_reviewer(proposalID)
        command_5_menu(proposalID)
    elif user_input == "4":
        check_conflict(proposalID)
        command_5_menu(proposalID)
    elif user_input == "5":
        print_command()
        command_exe()
        
    return
# Check conflict of interest for the proposal
def check_conflict(proposalID): 
    # Check conflict of interest list for the proposal
    sql_query = """
                    SELECT firstName, lastName, researchers.email
                    FROM conflictsOfInterest
                    JOIN researchers ON researchers.email = conflictsOfInterest.email
                    WHERE proposalID = ?
                """
    
    cursor.execute(sql_query, (proposalID,))
    results = cursor.fetchall()
    if len(results) < 0:
        print("No conflict of interest found.")
    else: 
        print("Conflict of interest list: ")
        for row in results:
            print(f"Name: {row[0]} {row[1]}, Email Address: {row[2]}")
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
    print(f"Assignment created successfully with new assignmentID is: {assignmentID}.\n")
    
    # Asking for adding reviewers
    user_input = input("Do you want to add reviewers to the assignment? y/n: ")
    if user_input == "y":
        add_reviewer(proposalID)
        
    else: return
    
# Asking for viewing existing assignments
def view_assignment(proposalID):
    sql_query = """
        SELECT assignmentID
        FROM reviewAssignment
        WHERE proposalID = ?
        """
    cursor.execute(sql_query, (proposalID,))
    results = cursor.fetchall()
    if len(results) == 0:
        print("No existing assignment found.\n")
        user_input = input("Do you want to create a new assignment? y/n: ")
        if user_input == "y":
            create_assignment(proposalID)
        else: return
    else: 
        for row in results:
            print(f"Assignment ID: {row[0]}")
    return
        
        
# Add new reviewers to existing review assignment   
def add_reviewer(proposalID):
    # Declare variables
    email_list = []
    # Get user input
    email = input("Enter the email address of the reviewer, seperated by comma: ")
    
    # Validate the input
    try: 
        email_list = [item.strip() for item in email.split(',')]
    except ValueError:
        print("Invalid email address, please try again.\n")
        add_reviewer(proposalID)
        return
    # Check if the reviewer exists and add to the proposal
    exist_email = cursor.execute("SELECT email FROM researchers").fetchall()
    for each_email in email_list:
        email = each_email[0]
        sql_query = """
            SELECT email
            FROM researchers
            WHERE email = ?
            """
        cursor.execute(sql_query, (each_email,))
        results = cursor.fetchall()
        if len(results) == 0:
            print(f"Reviewer {email} does not exist.\n")
            continue

        # Check if the reviewer has a conflict of interest with the proposal
        sql_query = """
            SELECT *
            FROM conflictsOfInterest
            WHERE email = ? AND proposalID = ?
            """
        cursor.execute(sql_query, (each_email, proposalID))
        results = cursor.fetchall()
        if len(results) > 0:
            print(f"Reviewer {each_email} has a conflict of interest with the proposal.\n")
            continue
    
        # Check if the reviewer has been assigned to the proposal
        sql_query = """
            SELECT *
            FROM reviewing
            JOIN proposal ON proposal.proposalID = reviewing.proposalID
            WHERE email = ? AND proposalID = ?
            """
        cursor.execute(sql_query, (each_email, proposalID))
        if len(results) > 0:
            print(f"Reviewer {each_email} has already been assigned to the proposal.\n")
            continue
    
        # Add the reviewer to the assginment
        assignmentID_list = cursor.execute("SELECT reviewAssignment.assignmentID FROM reviewing JOIN reviewAssignment ON reviewAssignment.assignmentID = reviewing.assignmentID WHERE proposalID = ?", (proposalID,)).fetchall()
        
        for each_assignmentID in assignmentID_list:
            assignmentID = each_assignmentID[0]
            sql_query = """
                INSERT INTO reviewing (email, assignmentID)
                VALUES (?, ?)
                """
            cursor.execute(sql_query, (each_email, assignmentID))

    
        # Commit the changes
        conn.commit()
    
        print("Reviewer added successfully.")
def command_6():    
    # Declare variables
    first_name = ""
    last_name = ""
    # Get user input
    name = input("Enter your first and last name: ")
    try:
        first_name, last_name = name.split()
    except ValueError:
        print("Invalid name, please try again.\n")
        command_6()
        return
    
    # Define the query
    sql_query = """
        SELECT title, reviewAssignment.proposalID, assignmentDeadline
        FROM reviewAssignment
        JOIN reviewing ON reviewAssignment.assignmentID = reviewing.assignmentID
        JOIN researchers ON researchers.email = reviewing.email
        JOIN proposal ON proposal.proposalID = reviewAssignment.proposalID 
        JOIN competition ON competition.competitionID = proposal.competitionID 
        WHERE firstName = ? AND lastName = ? AND submissionStatus = "Not Submitted" AND competitionStatus = "Open"  
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
