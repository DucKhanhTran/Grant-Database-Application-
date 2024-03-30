import sqlite3
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()

def data_generator(databaseName):
    conn = sqlite3.connect(databaseName)
    cursor = conn.cursor()

    # Generate researchers
    for _ in range(50):
        email = fake.email()
        firstName = fake.first_name()
        lastName = fake.last_name()
        organization = fake.company()
        department = fake.job()
        cursor.execute("INSERT OR IGNORE INTO researchers (email, firstName, lastName, organization, department) VALUES (?, ?, ?, ?, ?)", (email, firstName, lastName, organization, department))


    # Generate competitions
    for _ in range(20):
         # Generate random openDate
        today = datetime.now()
        start_date = today - timedelta(days=365 * 20)  # 20 years ago
        end_date = today  # Today
        openDate = fake.date_between(start_date=start_date, end_date=end_date).strftime('%Y-%m-%d')
    
        # Generate random closeDate after openDate
        closeDate = fake.date_between(start_date=datetime.strptime(openDate, '%Y-%m-%d'), end_date=end_date)
    
        # Generate random applicationDeadline between openDate and closeDate
        applicationDeadline = fake.date_between(start_date=datetime.strptime(openDate, '%Y-%m-%d'), end_date=closeDate).strftime('%Y-%m-%d')
    
        # Generate other random attributes
        competitionID = fake.unique.random_number()
        competitionStatus = random.choice(['Open', 'Closed'])
        # Generate random area from a list of 20 areas
        area = fake.random_element(elements=['Agriculture', 'Arts', 'Biotechnology', 'Business', 'Chemistry', 'Computer Science', 'Economics', 'Education', 'Engineering', 'Environment', 'Geology', 'Health', 'History', 'Humanities', 'Law', 'Mathematics', 'Physics', 'Psychology', 'Sociology', 'Statistics'])
        title = ''
        # Generate random title based on the area
        if area == 'Agriculture':
            title = fake.random_element(elements=['Agricultural Research', 'Crop Production', 'Soil Science', 'Plant Breeding', 'Agricultural Economics'])
        elif area == 'Arts':
            title = fake.random_element(elements=['Visual Arts', 'Performing Arts', 'Literature', 'Music', 'Film'])
        elif area == 'Biotechnology':
            title = fake.random_element(elements=['Genetic Engineering', 'Pharmaceuticals', 'Bioinformatics', 'Biomedical Engineering', 'Biotechnology Research'])
        elif area == 'Business':
            title = fake.random_element(elements=['Finance', 'Marketing', 'Management', 'Accounting', 'Business Analytics'])
        elif area == 'Chemistry':
            title = fake.random_element(elements=['Organic Chemistry', 'Inorganic Chemistry', 'Physical Chemistry', 'Analytical Chemistry', 'Biochemistry'])
        elif area == 'Computer Science':
            title = fake.random_element(elements=['Artificial Intelligence', 'Machine Learning', 'Data Science', 'Cybersecurity', 'Computer Vision'])
        elif area == 'Economics':
            title = fake.random_element(elements=['Microeconomics', 'Macroeconomics', 'Econometrics', 'Development Economics', 'International Economics'])
        elif area == 'Education':
            title = fake.random_element(elements=['Curriculum Development', 'Educational Technology', 'Special Education', 'Educational Psychology', 'Education Policy'])
        elif area == 'Engineering':
            title = fake.random_element(elements=['Civil Engineering', 'Mechanical Engineering', 'Electrical Engineering', 'Chemical Engineering', 'Computer Engineering'])
        elif area == 'Environment':
            title = fake.random_element(elements=['Environmental Science', 'Environmental Engineering', 'Environmental Policy', 'Sustainability', 'Climate Change'])
        elif area == 'Geology':
            title = fake.random_element(elements=['Geophysics', 'Geochemistry', 'Hydrogeology', 'Mineralogy', 'Petrology'])
        elif area == 'Health':
            title = fake.random_element(elements=['Public Health', 'Epidemiology', 'Health Policy', 'Health Informatics', 'Health Economics'])
        elif area == 'History':
            title = fake.random_element(elements=['Ancient History', 'Medieval History', 'Modern History', 'Military History', 'Social History'])
        elif area == 'Humanities':
            title = fake.random_element(elements=['Philosophy', 'Religion', 'Linguistics', 'Cultural Studies'])
        elif area == 'Law':
            title = fake.random_element(elements=['Criminal Law', 'Civil Law', 'International Law', 'Constitutional Law', 'Human Rights Law'])
        elif area == 'Mathematics':
            title = fake.random_element(elements=['Algebra', 'Calculus', 'Geometry', 'Statistics', 'Number Theory'])
        elif area == 'Physics':
            title = fake.random_element(elements=['Classical Mechanics', 'Quantum Mechanics', 'Thermodynamics', 'Astrophysics', 'Particle Physics'])
        elif area == 'Psychology':
            title = fake.random_element(elements=['Clinical Psychology', 'Cognitive Psychology', 'Developmental Psychology', 'Social Psychology', 'Educational Psychology'])
        elif area == 'Sociology':
            title = fake.random_element(elements=['Criminology', 'Demography', 'Social Stratification', 'Sociological Theory', 'Urban Sociology'])
        elif area == 'Statistics':
            title = fake.random_element(elements=['Descriptive Statistics', 'Inferential Statistics', 'Bayesian Statistics', 'Time Series Analysis', 'Statistical Modelling'])
        
        # Generate random description based on the title for all possible titles
        # For each title, generate a description that fits the title
        # Define descriptions for each title
        title_descriptions = {
            'Agricultural Research': 'Agricultural research focuses on studying methods and techniques to improve crop yield, soil health, and agricultural sustainability.',
            'Crop Production': 'Crop production involves the cultivation and management of crops for food, fiber, and other purposes.',
            'Soil Science': 'Soil science explores the composition, structure, and properties of soils, as well as their role in supporting plant growth and ecosystems.',
            'Plant Breeding': 'Plant breeding is the science of modifying plants to develop new varieties with desired traits such as higher yield, disease resistance, and nutritional content.',
            'Agricultural Economics': 'Agricultural economics examines the allocation of resources in agricultural production, distribution, and consumption, as well as the economic factors influencing agricultural markets and policies.',
            'Visual Arts': 'Visual arts encompass various forms of artistic expression, including painting, sculpture, drawing, photography, and printmaking.',
            'Performing Arts': 'Performing arts include live performances such as theater, dance, music, and opera, where artists present their work to an audience.',
            'Literature': 'Literature refers to written works of fiction, non-fiction, poetry, drama, and prose that convey ideas, emotions, and experiences through language and storytelling.',
            'Music': 'Music involves the creation, performance, and appreciation of sound organized in time, including vocal and instrumental compositions across various genres and styles.',
            'Film': 'Film encompasses the art and industry of motion pictures, including the production, direction, cinematography, editing, and distribution of movies and documentaries.',
            'Genetic Engineering': 'Genetic engineering is the process of modifying an organism\'s genetic material to introduce desired traits or characteristics, such as increased resistance to pests or diseases.',
            'Pharmaceuticals': 'Pharmaceuticals are medicinal drugs or compounds used for the prevention, diagnosis, and treatment of diseases and medical conditions.',
            'Bioinformatics': 'Bioinformatics combines biology, computer science, and information technology to analyze and interpret biological data, such as DNA sequences, for research and medical applications.',
            'Biomedical Engineering': 'Biomedical engineering applies engineering principles and design concepts to healthcare and medicine, focusing on developing technologies and devices to improve patient care and diagnosis.',
            'Biotechnology Research': 'Biotechnology research involves the study and application of biological processes, organisms, or systems to develop products and technologies for various fields, including medicine, agriculture, and industry.',
            'Finance': 'Finance is the management of money and investments, including activities such as banking, lending, investing, and budgeting, as well as the study of financial markets and institutions.',
            'Marketing': 'Marketing involves the promotion and sale of products or services through advertising, branding, public relations, and other strategies to attract and retain customers.',
            'Management': 'Management is the process of planning, organizing, directing, and controlling resources to achieve organizational goals and objectives effectively and efficiently.',
            'Accounting': 'Accounting is the recording, analysis, and reporting of financial transactions and information to support decision-making, financial planning, and regulatory compliance.',
            'Business Analytics': 'Business analytics involves the use of data analysis and statistical methods to interpret and predict business trends, performance, and outcomes to inform decision-making and strategy development.',
            'Organic Chemistry': 'Organic chemistry is the branch of chemistry that deals with the study of organic compounds, which contain carbon atoms bonded to hydrogen, oxygen, nitrogen, and other elements.',
            'Inorganic Chemistry': 'Inorganic chemistry is the branch of chemistry that focuses on the study of inorganic compounds, which do not contain carbon-hydrogen bonds, including metals, minerals, and salts.',
            'Physical Chemistry': 'Physical chemistry is the branch of chemistry that applies the principles and techniques of physics to study the properties and behavior of chemical systems, including thermodynamics, kinetics, and quantum chemistry.',
            'Analytical Chemistry': 'Analytical chemistry is the branch of chemistry concerned with the identification, separation, and quantification of chemical compounds and elements in various substances and samples.',
            'Biochemistry': 'Biochemistry is the study of the chemical processes and substances that occur within living organisms, including the structure, function, and interactions of biomolecules such as proteins, carbohydrates, lipids, and nucleic acids.',
            'Artificial Intelligence': 'Artificial intelligence (AI) is the simulation of human intelligence by computer systems, including processes such as learning, reasoning, problem-solving, perception, and language understanding.',
            'Machine Learning': 'Machine learning is a subset of artificial intelligence that focuses on developing algorithms and models that enable computers to learn from and make predictions or decisions based on data without explicit programming.',
            'Data Science': 'Data science is an interdisciplinary field that uses scientific methods, algorithms, and systems to extract knowledge and insights from structured and unstructured data, including statistics, machine learning, and data mining.',
            'Cybersecurity': 'Cybersecurity involves the protection of computer systems, networks, and data from cyber threats, attacks, and unauthorized access to ensure confidentiality, integrity, and availability of information and resources.',
            'Computer Vision': 'Computer vision is a field of artificial intelligence and computer science that focuses on enabling computers to interpret and understand visual information from digital images or videos, such as object recognition, image segmentation, and motion analysis.',
            'Microeconomics': 'Microeconomics is the branch of economics that studies the behavior of individuals, households, and firms in making decisions regarding the allocation of scarce resources and the interactions between buyers and sellers in markets.',
            'Macroeconomics': 'Macroeconomics is the branch of economics that focuses on the aggregate behavior of the economy as a whole, including topics such as economic growth, inflation, unemployment, monetary policy, and fiscal policy.',
            'Econometrics': 'Econometrics is the application of statistical and mathematical methods to analyze economic data and test hypotheses about economic theories and relationships, such as supply and demand, consumer behavior, and investment decisions.',
            'Development Economics': 'Development economics is the branch of economics that focuses on understanding and addressing the economic, social, and political factors influencing the development and growth of low-income and developing countries, including poverty, inequality, education, healthcare, and infrastructure.',
            'International Economics': 'International economics is the branch of economics that studies the economic interactions and relationships between countries, including international trade, finance, investment, globalization, and economic policies.',
            'Curriculum Development': 'Curriculum development is the process of designing, implementing, and evaluating educational programs, courses, and learning experiences to meet the needs and goals of students, teachers, and educational institutions.',
            'Educational Technology': 'Educational technology (EdTech) encompasses the use of technology, digital tools, and multimedia resources to enhance teaching, learning, and educational outcomes in formal and informal educational settings.',
            'Special Education': 'Special education involves the provision of tailored instructional programs, services, and accommodations to meet the unique learning needs of students with disabilities or special needs, including intellectual, physical, sensory, emotional, or behavioral challenges.',
            'Educational Psychology': 'Educational psychology is the branch of psychology that focuses on understanding and improving teaching, learning, and educational processes through research, theory, and evidence-based practices, including cognitive, motivational, and social-emotional factors.',
            'Education Policy': 'Education policy refers to the laws, regulations, standards, and guidelines established by governments, educational institutions, and other stakeholders to shape and govern the structure, funding, organization, curriculum, and practices of education systems and schools.',
            'Civil Engineering': 'Civil engineering is the branch of engineering that focuses on the design, construction, and maintenance of infrastructure and public works projects, including buildings, roads, bridges, dams, airports, and water supply systems.',
            'Mechanical Engineering': 'Mechanical engineering is the branch of engineering that applies principles of physics, mathematics, and materials science to design, analyze, manufacture, and maintain mechanical systems and devices, including machines, engines, and mechanical components.',
            'Electrical Engineering': 'Electrical engineering is the branch of engineering that deals with the study, design, and application of electrical systems, circuits, and devices, including power generation, transmission, distribution, and utilization, as well as electronics, telecommunications, and control systems.',
            'Chemical Engineering': 'Chemical engineering is the branch of engineering that combines chemistry, physics, biology, and mathematics to design, develop, and operate processes for the production, transformation, and utilization of chemicals, materials, and energy.',
            'Computer Engineering': 'Computer engineering is the branch of engineering that integrates principles and practices of computer science and electrical engineering to design, develop, and analyze hardware and software components and systems, including computers, networks, and embedded systems.',
            'Environmental Science': 'Environmental science is the interdisciplinary study of the physical, chemical, biological, and social aspects of the environment, including ecosystems, natural resources, pollution, climate change, and sustainability, as well as their interactions and impacts on human health and well-being.',
            'Environmental Engineering': 'Environmental engineering is the branch of engineering that applies scientific and engineering principles to address environmental challenges and protect human health and the natural environment, including air and water pollution control, waste management, and environmental remediation.',
            'Environmental Policy': 'Environmental policy refers to laws, regulations, and strategies established by governments, organizations, and communities to address environmental issues, protect natural resources, and promote sustainable development, conservation, and environmental stewardship.',
            'Sustainability': 'Sustainability is the capacity to meet the needs of the present without compromising the ability of future generations to meet their own needs, encompassing environmental, social, and economic dimensions of development and resource management.',
            'Climate Change': 'Climate change refers to long-term shifts in global or regional climate patterns, including changes in temperature, precipitation, sea level, and weather extremes, primarily due to human activities such as burning fossil fuels, deforestation, and industrial processes.',
            'Geophysics': 'Geophysics is the branch of Earth science that applies principles of physics to study the physical properties and processes of the Earth, including its interior structure, composition, seismic waves, magnetic fields, and gravitational fields.',
            'Geochemistry': 'Geochemistry is the branch of Earth science that examines the chemical composition, distribution, and behavior of elements and compounds in rocks, minerals, soils, water, and the atmosphere, as well as their interactions and processes within the Earth system.',
            'Hydrogeology': 'Hydrogeology is the branch of geology that focuses on the study of groundwater, including its occurrence, movement, quality, and interaction with surface water and geological formations, as well as its role in the hydrologic cycle and human activities.',
            'Mineralogy': 'Mineralogy is the branch of geology that studies minerals, which are naturally occurring inorganic substances with characteristic chemical compositions and crystal structures, as well as their properties, classifications, occurrences, and uses.',
            'Petrology': 'Petrology is the branch of geology that investigates the origin, composition, structure, and evolution of rocks, including their formation processes, classification schemes, and geological significance, as well as their distribution and associations within the Earth\'s crust.',
            'Public Health': 'Public health is the science and practice of preventing disease, promoting health, and prolonging life through organized efforts and informed choices of society, communities, and individuals, focusing on population health outcomes and disease prevention strategies.',
            'Epidemiology': 'Epidemiology is the study of the distribution and determinants of health-related states or events in populations, as well as the application of this knowledge to control and prevent diseases and health problems through surveillance, research, and intervention programs.',
            'Health Policy': 'Health policy refers to decisions, plans, and actions undertaken by governments, organizations, and stakeholders to achieve specific health-related goals and objectives, including healthcare access, quality, affordability, and outcomes, as well as public health priorities and regulations.',
            'Health Informatics': 'Health informatics is the interdisciplinary field that combines healthcare, information technology, and data science to manage and analyze health-related data, information, and knowledge for clinical, administrative, research, and public health purposes, including electronic health records, medical imaging, and health information systems.',
            'Health Economics': 'Health economics is the branch of economics that studies the allocation of resources, costs, and outcomes in healthcare systems and markets, including the analysis of healthcare financing, insurance, reimbursement, provider payment, and healthcare delivery models.',
            'Ancient History': 'Ancient history is the study of human societies, cultures, and civilizations in the period before written records, encompassing prehistoric times, ancient civilizations such as Mesopotamia, Egypt, Greece, and Rome, and early historical periods.',
            'Medieval History': 'Medieval history is the study of European history from the fall of the Western Roman Empire in the 5th century to the Renaissance and the Age of Discovery in the 15th and 16th centuries, including the Middle Ages, feudalism, monarchies, crusades, and cultural developments.',
            'Modern History': 'Modern history is the study of global history from the Renaissance and the Age of Discovery in the 15th and 16th centuries to the present day, including the early modern period, the Enlightenment, revolutions, colonialism, imperialism, world wars, and contemporary events.',
            'Military History': 'Military history is the study of armed conflicts, wars, battles, and military strategies and tactics throughout history, including the analysis of military organizations, technologies, leadership, and the impact of warfare on societies, cultures, and civilizations.',
            'Social History': 'Social history is the study of everyday life, customs, beliefs, behaviors, and institutions of past societies and cultures, focusing on social structures, inequalities, identities, relationships, and cultural practices within communities, families, and social groups.',
            'Philosophy': 'Philosophy is the study of fundamental questions about existence, knowledge, values, reason, mind, language, ethics, politics, aesthetics, and reality, as well as the methods of inquiry and critical thinking used to address them.',
            'Religion': 'Religion is the belief in and worship of a supernatural power or powers, deity or deities, divine or sacred beings, principles, scriptures, rituals, and practices, as well as the moral and ethical codes and spiritual experiences associated with them, often organized into religious institutions and communities.',
            'Linguistics': 'Linguistics is the scientific study of language, including its structure, sounds, meanings, grammar, syntax, semantics, pragmatics, evolution, acquisition, variation, and use by individuals and communities, as well as the cognitive processes and social functions of language.',
            'Cultural Studies': 'Cultural studies is an interdisciplinary field that explores the production, consumption, and meanings of cultural artifacts, texts, practices, and representations, including media, literature, art, music, film, fashion, rituals, and identities, within social, historical, and political contexts.',
            'Criminal Law': 'Criminal law is the branch of law that defines offenses, crimes, and punishable acts, as well as the legal principles, procedures, and penalties governing criminal justice, including investigations, trials, sentencing, and corrections.',
            'Civil Law': 'Civil law is the branch of law that deals with disputes and conflicts between individuals, organizations, or entities, including matters such as contracts, property rights, torts, family law, inheritance, and civil rights, as well as the legal remedies and procedures for resolving them.',
            'International Law': 'International law is the body of legal rules, principles, treaties, agreements, and customs that govern relations between states, international organizations, and individuals, as well as the resolution of disputes and conflicts in the international community.',
            'Constitutional Law': 'Constitutional law is the branch of law that deals with the interpretation, implementation, and enforcement of constitutions, including the fundamental principles, rights, powers, and structures of government, as well as the relationships between branches of government and the rights of individuals.',
            'Human Rights Law': 'Human rights law is the branch of international law and domestic law that protects and promotes the inherent rights and freedoms of individuals, groups, and communities, as enshrined in international human rights treaties, declarations, conventions, and customary practices.',
            'Algebra': 'Algebra is the branch of mathematics that deals with symbols, equations, and operations to represent and solve mathematical problems, including algebraic structures such as groups, rings, fields, vectors, matrices, and equations.',
            'Calculus': 'Calculus is the branch of mathematics that studies rates of change and accumulation, including differential calculus, which deals with derivatives and rates of change, and integral calculus, which deals with integrals and accumulation processes.',
            'Geometry': 'Geometry is the branch of mathematics that focuses on the study of shapes, sizes, dimensions, positions, and properties of objects in space, including points, lines, angles, curves, surfaces, and solids, as well as geometric transformations and constructions.',
            'Statistics': 'Statistics is the branch of mathematics that deals with the collection, analysis, interpretation, presentation, and organization of data, including techniques such as descriptive statistics, inferential statistics, probability, hypothesis testing, and regression analysis.',
            'Number Theory': 'Number theory is the branch of mathematics that focuses on the properties and relationships of integers and their mathematical structures, including prime numbers, divisibility, congruences, arithmetic functions, and algebraic number theory.',
            'Classical Mechanics': 'Classical mechanics is the branch of physics that studies the motion and behavior of macroscopic objects under the influence of forces, including Newton\'s laws of motion, conservation principles, and mechanical energy.',
            'Quantum Mechanics': 'Quantum mechanics is the branch of physics that describes the behavior of particles at the atomic and subatomic scales, including phenomena such as wave-particle duality, superposition, entanglement, and probabilistic outcomes.',
            'Thermodynamics': 'Thermodynamics is the branch of physics that deals with the relationships and transformations of heat, energy, and work in physical systems, including the laws of thermodynamics, heat engines, entropy, and thermal equilibrium.',
            'Astrophysics': 'Astrophysics is the branch of astronomy that applies the principles of physics and chemistry to study the properties, behavior, and evolution of celestial objects and phenomena in the universe, including stars, galaxies, black holes, and cosmology.',
            'Particle Physics': 'Particle physics is the branch of physics that studies the fundamental particles and forces of nature, including their interactions, properties, symmetries, and the structure of matter at the smallest scales, as well as the fundamental laws and theories governing the universe.',
            'Clinical Psychology': 'Clinical psychology is the branch of psychology that focuses on assessing, diagnosing, treating, and preventing mental, emotional, and behavioral disorders and problems, as well as promoting psychological health, well-being, and resilience through therapeutic interventions and psychotherapy.',
            'Cognitive Psychology': 'Cognitive psychology is the branch of psychology that studies mental processes such as perception, memory, attention, language, problem-solving, reasoning, and decision-making, as well as the underlying cognitive mechanisms and representations involved.',
            'Developmental Psychology': 'Developmental psychology is the branch of psychology that examines the physical, cognitive, emotional, and social development and changes that occur throughout the lifespan, from infancy and childhood to adolescence, adulthood, and old age, including the influences of genetics, environment, and experience.',
            'Social Psychology': 'Social psychology is the branch of psychology that explores how individuals think, feel, and behave in social situations, groups, and cultures, as well as the social influences, norms, attitudes, stereotypes, relationships, and interactions that shape human behavior and experience.',
            'Educational Psychology': 'Educational psychology is the branch of psychology that applies psychological principles and theories to understand and improve teaching, learning, and educational processes, including motivation, learning styles, cognitive development, assessment, and instructional strategies.',
            'Criminology': 'Criminology is the interdisciplinary study of crime, criminal behavior, law enforcement, criminal justice systems, and the social, psychological, and environmental factors influencing crime rates, patterns, and trends, as well as crime prevention and intervention strategies.',
            'Demography': 'Demography is the scientific study of human populations, including their size, structure, distribution, migration, fertility, mortality, aging, and other demographic characteristics, as well as the social, economic, and environmental factors shaping population dynamics and trends.',
            'Social Stratification': 'Social stratification is the hierarchical arrangement of individuals and groups within societies based on social status, wealth, power, occupation, education, ethnicity, gender, and other criteria, as well as the processes of social mobility, inequality, and social class formation.',
            'Sociological Theory': 'Sociological theory is the framework of concepts, ideas, and perspectives used to analyze and explain social phenomena, structures, processes, and patterns, including theories such as functionalism, conflict theory, symbolic interactionism, feminism, and postmodernism.',
            'Urban Sociology': 'Urban sociology is the branch of sociology that examines the social structure, organization, dynamics, and problems of urban areas and communities, including topics such as urbanization, globalization, urban development, segregation, poverty, inequality, and urban social movements.',
            'Descriptive Statistics': 'Descriptive statistics are statistical methods and techniques used to summarize, organize, and describe the main features, patterns, and characteristics of data sets, including measures of central tendency, dispersion, frequency distributions, and graphical representations.',
            'Inferential Statistics': 'Inferential statistics are statistical methods and techniques used to make predictions, inferences, and generalizations about populations based on sample data, including hypothesis testing, confidence intervals, regression analysis, and analysis of variance.',
            'Bayesian Statistics': 'Bayesian statistics is a statistical approach that combines prior knowledge, beliefs, or probabilities with observed data to update and revise probability distributions and make probabilistic predictions or decisions, using Bayesian inference and Bayes\' theorem.',
            'Time Series Analysis': 'Time series analysis is a statistical method used to analyze and model time-ordered data points or observations collected at regular intervals over time, including techniques such as trend analysis, seasonality detection, forecasting, and autoregressive models.',
            'Statistical Modelling': 'Statistical modeling is the process of developing mathematical models or equations to describe, explain, and predict relationships and patterns in data sets, using statistical methods such as regression analysis, generalized linear models, and Bayesian inference.'
        }

        # Generate a description for each title based on the predefined descriptions
        description = title_descriptions.get(title, 'No description available')


        # Execute SQL query to insert data into the competition table
        cursor.execute("INSERT OR IGNORE INTO competition (title, applicationDeadline, competitionStatus, area, description, openDate, closeDate) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                       (title, applicationDeadline, competitionStatus, area, description, openDate, closeDate))

    # Generate proposals
    for _ in range(70):
        proposalID = fake.unique.random_number()
        competitionID = fake.random_element(elements=[c[0] for c in cursor.execute("SELECT competitionID FROM competition").fetchall()])
        applicationStatus = random.choice(['Pending', 'Accepted', 'Rejected'])
        requestedAmount = random.uniform(1000, 100000)
        
        # Generate random submissionDate, awardDate and rejectDate
        openDate = cursor.execute("SELECT openDate FROM competition WHERE competitionID = ?", (competitionID,)).fetchone()[0]
        closeDate = cursor.execute("SELECT closeDate FROM competition WHERE competitionID = ?", (competitionID,)).fetchone()[0]
        
        submissionDate = fake.date_between(start_date=datetime.strptime(openDate, '%Y-%m-%d'), end_date=datetime.strptime(closeDate, '%Y-%m-%d')).strftime('%Y-%m-%d')
        
        if applicationStatus == 'Accepted':
            awardDate = fake.date_between(start_date=datetime.strptime(submissionDate, '%Y-%m-%d'), end_date=datetime.strptime(closeDate, '%Y-%m-%d')).strftime('%Y-%m-%d')
            awardAmount = random.uniform(1000, requestedAmount)
            cursor.execute("INSERT OR IGNORE INTO proposal (proposalID, competitionID, submissionDate, applicationStatus, requestedAmount, awardDate, awardAmount) VALUES (?, ?, ?, ?, ?, ?, ?)", (proposalID, competitionID, submissionDate, applicationStatus, requestedAmount, awardDate, awardAmount))
        elif applicationStatus == 'Rejected': 
            rejectDate = fake.date_between(start_date=datetime.strptime(submissionDate, '%Y-%m-%d'), end_date=datetime.strptime(closeDate, '%Y-%m-%d')).strftime('%Y-%m-%d')
            cursor.execute("INSERT OR IGNORE INTO proposal (proposalID, competitionID, submissionDate, applicationStatus, requestedAmount, rejectDate) VALUES (?, ?, ?, ?, ?, ?)", (proposalID, competitionID, submissionDate, applicationStatus, requestedAmount, rejectDate))
        else:
            cursor.execute("INSERT OR IGNORE INTO proposal (proposalID, competitionID, submissionDate, applicationStatus, requestedAmount) VALUES (?, ?, ?, ?, ?)", (proposalID, competitionID, submissionDate, applicationStatus, requestedAmount))
        


    # Generate researching
    for _ in range(120):
        email = fake.random_element(elements=[r[0] for r in cursor.execute("SELECT email FROM researchers").fetchall()])
        proposalID = fake.random_element(elements=[p[0] for p in cursor.execute("SELECT proposalID FROM proposal").fetchall()])
        
        if cursor.execute("SELECT COUNT(principal) FROM researching WHERE proposalID = ? AND principal = 1", (proposalID,)).fetchone()[0] == 0:
            principal = 1
        else:
            principal = 0

        cursor.execute("INSERT OR IGNORE INTO researching (email, proposalID, principal) VALUES (?, ?, ?)", (email, proposalID, principal))
        

    
    # Generate reviewAssignment
    for _ in range(100):
        assignmentID = fake.unique.random_number()
        proposalID = fake.random_element(elements=[p[0] for p in cursor.execute("SELECT proposalID FROM proposal").fetchall()])
        
        # Fetch date information from proposal table
        submissionDate = cursor.execute("SELECT submissionDate FROM proposal WHERE proposalID = ?", (proposalID,)).fetchone()[0]
        awardDate = cursor.execute("SELECT awardDate FROM proposal WHERE proposalID = ?", (proposalID,)).fetchone()[0]
        rejectDate = cursor.execute("SELECT rejectDate FROM proposal WHERE proposalID = ?", (proposalID,)).fetchone()[0]
        
        # Fetch reviewDeadline from competition table
        applicationStatus = cursor.execute("SELECT applicationStatus FROM proposal WHERE proposalID = ?", (proposalID,)).fetchone()[0]
        competitionID = cursor.execute("SELECT competitionID FROM proposal WHERE proposalID = ?", (proposalID,)).fetchone()[0]
        closeDate = cursor.execute("SELECT closeDate FROM competition WHERE competitionID = ?", (competitionID,)).fetchone()[0]


        if applicationStatus == 'Accepted':
            assignmentDeadline = fake.date_between(start_date=datetime.strptime(submissionDate, '%Y-%m-%d'), end_date=datetime.strptime(awardDate, '%Y-%m-%d')).strftime('%Y-%m-%d')
        elif applicationStatus == 'Rejected':
            assignmentDeadline = fake.date_between(start_date=datetime.strptime(submissionDate, '%Y-%m-%d'), end_date=datetime.strptime(rejectDate, '%Y-%m-%d')).strftime('%Y-%m-%d')
        else:
            assignmentDeadline = fake.date_between(start_date=datetime.strptime(submissionDate, '%Y-%m-%d'), end_date=datetime.strptime(closeDate, '%Y-%m-%d') - timedelta(days=1)).strftime('%Y-%m-%d')

        cursor.execute("INSERT OR IGNORE INTO reviewAssignment (assignmentID, proposalID, assignmentDeadline) VALUES (?, ?, ?)", (assignmentID, proposalID, assignmentDeadline))

    # Generate Reviewing
    for _ in range(100):
        assignmentID = fake.random_element(elements=[a[0] for a in cursor.execute("SELECT assignmentID FROM reviewAssignment").fetchall()])
        proposalID = cursor.execute("SELECT proposalID FROM reviewAssignment WHERE assignmentID = ?", (assignmentID,)).fetchone()[0]
        email = fake.random_element(elements=[r[0] for r in cursor.execute("SELECT email FROM researchers WHERE email NOT IN (SELECT email FROM researching WHERE proposalID = ?)", (proposalID,)).fetchall()])
        submissionStatus = random.choice(['Submitted', 'Not Submitted'])
        reviewSubmission = fake.text()
        cursor.execute("INSERT OR IGNORE INTO Reviewing (assignmentID, email, submissionStatus, reviewSubmission) VALUES (?, ?, ?, ?)", (assignmentID, email, submissionStatus, reviewSubmission))


    # Generate conflictsOfInterest
    for _ in range(30):
        email = fake.random_element(elements=[r[0] for r in cursor.execute("SELECT email FROM researchers").fetchall()])
        proposalID = fake.random_element(elements=[p[0] for p in cursor.execute("SELECT proposalID FROM proposal").fetchall()])
        cursor.execute("INSERT OR IGNORE INTO conflictsOfInterest (email, proposalID) VALUES (?, ?)", (email, proposalID))


    # Generate committeesMeeting
    for _ in range(10):
        
        # Generate random meetingDate
        today = datetime.now()
        start_date = today - timedelta(days=365 * 20)  # 20 years ago
        end_date = today  # Today
        meetingDate = fake.date_between(start_date=start_date, end_date=end_date).strftime('%Y-%m-%d')

        meetingID = fake.unique.random_number()

        cursor.execute("INSERT OR IGNORE INTO committeesMeeting (meetingID, meetingDate) VALUES (?, ?)", (meetingID, meetingDate))


    # Generate discussion
    for _ in range(30):
        meetingID = fake.random_element(elements=[m[0] for m in cursor.execute("SELECT meetingID FROM committeesMeeting").fetchall()])
        
        # Fetch competitionID from competition table where openDate is before meetingDate and closeDate is after meetingDate
        
        # Check if there is any competition that meets the condition
        if len(cursor.execute("SELECT competitionID FROM competition WHERE openDate < (SELECT meetingDate FROM committeesMeeting WHERE meetingID = ?) AND closeDate > (SELECT meetingDate FROM committeesMeeting WHERE meetingID = ?)", (meetingID, meetingID)).fetchall()) == 0:
            continue
        competitionID = fake.random_element(elements=[c[0] for c in cursor.execute("SELECT competitionID FROM competition WHERE openDate < (SELECT meetingDate FROM committeesMeeting WHERE meetingID = ?) AND closeDate > (SELECT meetingDate FROM committeesMeeting WHERE meetingID = ?)", (meetingID, meetingID)).fetchall()])

        discussionSummary = fake.text()
        cursor.execute("INSERT OR IGNORE INTO discussion (meetingID, competitionID, discussionSummary) VALUES (?, ?, ?)", (meetingID, competitionID, discussionSummary))


    # Generate discussing
    for _ in range(1):
        meetingID = cursor.execute("SELECT meetingID FROM committeesMeeting").fetchall()
        
        # Fetch all competitionID from  discussion table where meetingID is the same as the current meetingID
        for each_meeting in meetingID:
            competitionID_list = cursor.execute("SELECT competitionID FROM discussion WHERE meetingID = ?", (each_meeting[0],)).fetchall() 
            # For each competitionID in competitionID_list, fetch all proposalID from proposal table where competitionID is the same as the current competitionID
            for each_competition in competitionID_list:
                proposalID_list = cursor.execute("SELECT proposalID FROM proposal WHERE competitionID = ?", (each_competition[0],)).fetchall()
                # For each proposalID in proposalID_list, fetch all assignmentID from reviewAssignment table where proposalID is the same as the current proposalID
                for each_proposal in proposalID_list:
                    assignmentID_list = cursor.execute("SELECT assignmentID FROM reviewAssignment WHERE proposalID = ?", (each_proposal[0],)).fetchall()
                    # For each assignmentID in assignmentID_list, fetch all email from Reviewing table where assignmentID is the same as the current assignmentID
                    for each_assignment in assignmentID_list:
                        email_list = cursor.execute("SELECT email FROM Reviewing WHERE assignmentID = ?", (each_assignment[0],)).fetchall()
                        # For each email in email_list, insert data into discussing table
                        for each_email in email_list:
                            participatingStatus = random.choice([0, 1])
                            if participatingStatus == 1:
                                comment = fake.text()
                            else:
                                comment = None
                            cursor.execute("INSERT OR IGNORE INTO discussing (meetingID, competitionID, email, participatingStatus, comment) VALUES (?, ?, ?, ?, ?)", (each_meeting[0], each_competition[0], each_email[0], participatingStatus, comment))
                            
    
    

    conn.commit()   
    conn.close()

    print("Generating data successfully.")

