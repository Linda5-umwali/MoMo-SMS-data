# MoMo-SMS-data Project

- Team name: Data pioneers
# project description
  Our designed project will process and analyse MoMo SMS data and will perform the following:

  - Parse data in XML format
  - clean, categorise and validate data
  - store the processed data in a relational database
  - provide a frontend interface for analysis and vizualisation of transaction made.

Our goal is to develop backend data processing, database management, and frontend implementation into a scalable solution with experience in collaborative software engineering processes.

# System architecture
  - backend: Handles XML parsing, data cleaning and APIs
  - Database: For a structured data storage
  - frontend: for visualisaation

# ErRD Design Documantation
This Entity-Relational Diagram illustrates the core components of the financial transaction system(MoMo app). The ERD has four entities. Transactions, users, transaction_categories, and system_logs. The transactions are the core entity, with money information like references to sender and receiver users, time information, and status. The user entity contains the user contact and identity and the entity refers the transactions to users using receiver_id and sender_id in a bid to reduce user history and render it readable. The Transaction_categories table establishes the types of transactions being performed like payment, transfer, and airtime. The entity simplifies working with categories and faster. System_logs hold vents as well as links optionally to the transaction performed. Logs are trackable and searchable worldwide.
My design option emphasized the connection of items outlined above by having foreign key values in a table always point to primary key values found in another table. The design further emphasizes traceability through identification of where the transactions are occurring.
Also, critical like amount employs exact notation (DECIMAL), and timestamp types to order events. Overall, the formal design ensures readability and traceability, allowing the system to easily monitor financial transactions while creating an auditable history of all user and system activity.

(The design was created using lucidcharts).

- design can be viewed directly here: docs/ERD_design.pdf or https://github.com/Linda5-umwali/MoMo-SMS-data/blob/main/docs/ERD_design.pdf 

# Team members
- Angel Wangui Kibui
- Brenda Nyambura Maina
- Linda Umwali
- Ndunge Mutheu Mbithi
  
