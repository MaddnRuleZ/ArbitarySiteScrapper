import pandas as pd
import pyodbc

class MSSQLDatabase:
    def __init__(self):
        self.server = "192.168.178.22"
        self.database = "WhiteWidow"
        self.username = "maddinRulez"
        self.password = "dx~pWf714$TxRy98"
        self.conn = self._create_connection()

    def _create_connection(self):
        conn_str = f'DRIVER={{SQL Server}};SERVER={self.server};DATABASE={self.database};UID={self.username};PWD={self.password}'
        try:
            conn = pyodbc.connect(conn_str)
            return conn
        except pyodbc.Error as e:
            print(f"Error connecting to the database: {e}")
            return None


    # -------------------------------------Inserting Data---------------------------------------------------------

    # execute before Looping
    def create_table(self, table_name):
        if not self.conn:
            print("Connection error. Unable to create the table.")
            return

        try:
            cursor = self.conn.cursor()
            create_table_query = f'''CREATE TABLE {table_name} (
                                    id INT PRIMARY KEY IDENTITY(1,1),
                                    Name VARCHAR(MAX),
                                    Stadt VARCHAR(MAX),
                                    PriceRange VARCHAR(MAX),
                                    Rating VARCHAR(MAX),
                                    NrRatings INT,
                                    SiteURL VARCHAR(MAX),
                                    TelNr VARCHAR(MAX),
                                    Reservieren VARCHAR(MAX),
                                    Bestellung VARCHAR(MAX),
                                    Menu VARCHAR(MAX),
                                    Claimed BIT,
                                    Contacted BIT
                                    );'''
            cursor.execute(create_table_query)
            print(f"Table '{table_name}' created successfully.")
            cursor.close()
            self.conn.commit()  # Commit the changes after creating the table
        except pyodbc.Error as e:
            print(f"Error creating table: {e}")


    # check if Entry is present, if not insert it into the Database
    def insert_scrape_result(self, result, table_name):
        if not self.conn:
            print("Connection error. Unable to insert data.")
            return

        cursor = self.conn.cursor()

        # Check if the entry already exists
        cursor.execute(
            "SELECT COUNT(*) FROM " + table_name + " WHERE Name = ? AND PriceRange = ? AND Rating = ? AND NrRatings = ? AND SiteURL = ? AND TelNr = ? AND Menu = ? AND Claimed = ?",
            (result.name, result.price_range, result.rating, result.nr_ratings, result.site_url, result.tel_nr,
             result.menu, result.claimed))
        existing_count = cursor.fetchone()[0]

        if existing_count == 0:
            try:
                cursor.execute(
                    f"INSERT INTO {table_name} (Name, Stadt, PriceRange, Rating, NrRatings, SiteURL, TelNr, Reservieren, Bestellung, Menu, Claimed, Contacted) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (result.name, result.stadt, result.price_range, result.rating, result.nr_ratings, result.site_url, result.tel_nr,
                     result.tisch_reservieren, result.bestellung, result.menu, result.claimed, False))
                self.conn.commit()
                print("Inserted successfully!")
            except pyodbc.Error as e:
                print(f"Error inserting data: {e}")
        else:
            print("Entry already exists.")

        cursor.close()

    def print_table_data(self, table_name):
        try:
            cursor = self.conn.cursor()
            select_query = f"SELECT * FROM {table_name};"
            cursor.execute(select_query)
            rows = cursor.fetchall()

            if rows:
                for row in rows:
                    print(row)
            else:
                print(f"No data found in table '{table_name}'")

            cursor.close()
        except pyodbc.Error as e:
            print(f"Error retrieving data: {e}")



    def get_all_facebooks(self, table_name, sheet_name):
        query = "SELECT * FROM " + table_name + " WHERE SiteURL LIKE '%facebook%'"
        self.save_as_excel_querry(sheet_name, query)

    def save_as_excel(self, table_name, sheet_name):
        query = 'SELECT * FROM ' + table_name + ' ORDER BY Stadt ASC'
        self.save_as_excel_querry(sheet_name, query)


    def save_as_excel_querry(self, sheet_name, query):
        # Use pandas to read Program query results into a DataFrame
        df = pd.read_sql(query, self.conn)

        excel_file_path = "XLS_FILES/" + sheet_name + ".xlsx"
        df.to_excel(excel_file_path, index=False)
        print(f"Data has been exported to {sheet_name}")

