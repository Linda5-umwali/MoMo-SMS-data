CREATE TABLE Users (
  user_id INT PRIMARY KEY COMMENT 'Unique ID',
  phone_number VARCHAR(20) COMMENT 'Phone',
  first_name VARCHAR(100) COMMENT 'First name',
  last_name VARCHAR(100) COMMENT 'Last name',
  email VARCHAR(100) COMMENT 'Email',
) COMMENT='Users table';

CREATE TABLE Transaction (
  transaction_id INT PRIMARY KEY COMMENT 'Unique ID',
  sender_id INT COMMENT 'FK user',
  receiver_id INT COMMENT 'FK user',
  amount DECIMAL(12,2) COMMENT 'Amount',
  initiated_at DATETIME COMMENT 'Date',
  completed_at DATETIME COMMENT 'Date',
  category_id INT COMMENT 'FK category',
  FOREIGN KEY (sender_id) REFERENCES User(user_id),
  FOREIGN KEY (receiver_id) REFERENCES User(user_id),
  FOREIGN KEY (category_id) REFERENCES Transaction_Categories(category_id)
) COMMENT='Transactions';


CREATE TABLE Transaction_Categories (
  category_id INT PRIMARY KEY COMMENT 'Unique ID',
  category_name VARCHAR(100) COMMENT 'Name',
  description TEXT COMMENT 'Details'
  created_at DATETIME COMMENT 'Date',
  updated_at DATETIME COMMENT 'Date',
) COMMENT='Transaction categories';

CREATE TABLE System_Logs (
  log_id INT PRIMARY KEY COMMENT 'Unique ID',
  message TEXT COMMENT 'Message',
  created_at DATETIME COMMENT 'Created',
  transaction_id INT COMMENT 'FK transaction',
  FOREIGN KEY (transaction_id) REFERENCES Transaction(transaction_id)
) COMMENT='Logs';

CREATE INDEX idx_user_userid ON User(user_id);
CREATE INDEX idx_transaction_transactionid ON Transaction(transaction_id);

INSERT INTO User VALUES
 (1,'Steph','Curry','58767','stephc@gmail.com','admin'),
 (2,'Robyn','Fenty','12648','robynf@gmail.com','customer'),
 (3,'Fridayy','Leblanc','83273','leblencf@gmail.com','customer'),
 (4,'Zendaya','Maree','98830','colemanmaree@gmail.com','customer'),
 (5,'cat','Burns','35436','cathlinb@gmail.com','customer');
 (6,'Sam','smith','12496','cathlinb@gmail.com','customer');

INSERT INTO Transaction_Categories VALUES
 (1,'Transfer','send money'),
 (2,'Airtime','buy airtime'),
 (3,'Bill','pay utility'),
  
INSERT INTO Transaction VALUES
 (11001,1,2,3,5000,'2025-09-17 10:00:00','completed'),
 (11002,2,3,2,2000,'2025-09-17 11:00:00','pending'),
 (12003,3,4,1,10000,'2025-09-17 12:00:00','failed'),
 (13004,4,5,4,1500,'2025-09-17 13:00:00','completed'),
 (14005,5,1,5,7500,'2025-09-17 14:00:00','completed');


INSERT INTO System_Logs VALUES
 (50009,'Done',,'2025-09-17 10:01:00',11001),
 (55544,'Pending','2025-09-17 11:05:00',11002),
 (54454,'Failed','2025-09-17 12:10:00',12003),
 (56454,'Done','2025-09-17 13:05:00',13004),
 (51532,'failed','2025-09-17 14:01:00',14005);

-- CRUD EXAMPLES
INSERT INTO User VALUES (2,'Robyn','Fenty','12648','robynf@gmail.com','customer');
UPDATE User SET phone_number='0789834772' WHERE user_id=12648;
DELETE FROM System_Logs WHERE log_id=55544;
