import sqlite3


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
    user_input = input("Would you like to add a reviewer? y/n")
    
    if user_input == "n":
        return
    else:
        email_input = input("Enter the reviewers email, seperated by comma: ")
    
    # Split the emails
    email_list = [item.strip() for item in email_input.split(',')]
    
    # Define the query
    sql_query = """
        INSERT INTO reviewing (proposalID, email)
        VALUES (?, ?)
        """
        
    # Execute the query
    for item in email_list:
        cursor.execute(sql_query, (proposalID, item))
    
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
