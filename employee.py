import mysql.connector
from mysql.connector import Error
import logging
import configparser

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Reading database configuration from a file
config = configparser.ConfigParser()
config.read('db_config.ini')

class EmployeeManagement:
    def __init__(self):
        self.connection = self.create_connection()

    def create_connection(self):
        try:
            connection = mysql.connector.connect(
                host=config['mysql']['host'],
                user=config['mysql']['user'],
                password=config['mysql']['password'],
                database=config['mysql']['database']
            )
            if connection.is_connected():
                logging.info("Connected to the database")
                return connection
        except Error as e:
            logging.error(f"Error: {e}")
            return None

    def add_employee(self):
        if not self.connection:
            print("Failed to connect to the database. Please check your configuration.")
            return
        
        cursor = None
        try:
            id = input("Enter Employee Id: ")
            if not id.isdigit():
                print("Invalid Id. Please enter a numeric value.")
                return

            if self.check_employee(id):
                print("Employee already exists. Try Again.")
                return

            name = input("Enter Employee Name: ")
            post = input("Enter Employee Post: ")
            salary = input("Enter Employee Salary: ")
            if not salary.isdigit():
                print("Invalid Salary. Please enter a numeric value.")
                return

            data = (id, name, post, salary)
            sql = 'INSERT INTO empd (id, name, post, salary) VALUES (%s, %s, %s, %s)'
            
            cursor = self.connection.cursor()
            cursor.execute(sql, data)
            self.connection.commit()
            logging.info("Employee Added Successfully")
        except Error as e:
            logging.error(f"Error: {e}")
        finally:
            if cursor:
                cursor.close()

    def promote_employee(self):
        if not self.connection:
            print("Failed to connect to the database. Please check your configuration.")
            return

        cursor = None
        try:
            id = input("Enter Employee Id: ")
            if not id.isdigit():
                print("Invalid Id. Please enter a numeric value.")
                return

            if not self.check_employee(id):
                print("Employee does not exist. Try Again.")
                return

            amount = input("Enter increase in Salary: ")
            if not amount.isdigit():
                print("Invalid amount. Please enter a numeric value.")
                return
            amount = int(amount)

            cursor = self.connection.cursor()
            cursor.execute('SELECT salary FROM empd WHERE id=%s', (id,))
            current_salary = cursor.fetchone()[0]

            new_salary = current_salary + amount
            cursor.execute('UPDATE empd SET salary=%s WHERE id=%s', (new_salary, id))
            self.connection.commit()
            logging.info("Employee Promoted")
        except Error as e:
            logging.error(f"Error: {e}")
        finally:
            if cursor:
                cursor.close()

    def remove_employee(self):
        if not self.connection:
            print("Failed to connect to the database. Please check your configuration.")
            return

        cursor = None
        try:
            id = input("Enter Employee Id: ")
            if not id.isdigit():
                print("Invalid Id. Please enter a numeric value.")
                return

            if not self.check_employee(id):
                print("Employee does not exist. Try Again.")
                return

            cursor = self.connection.cursor()
            cursor.execute('DELETE FROM empd WHERE id=%s', (id,))
            self.connection.commit()
            logging.info("Employee Removed")
        except Error as e:
            logging.error(f"Error: {e}")
        finally:
            if cursor:
                cursor.close()

    def check_employee(self, employee_id):
        if not self.connection:
            logging.error("No database connection available.")
            return False

        cursor = None
        try:
            cursor = self.connection.cursor(buffered=True)
            cursor.execute('SELECT * FROM empd WHERE id=%s', (employee_id,))
            return cursor.rowcount == 1
        except Error as e:
            logging.error(f"Error: {e}")
            return False
        finally:
            if cursor:
                cursor.close()

    def display_employees(self):
        if not self.connection:
            print("Failed to connect to the database. Please check your configuration.")
            return

        cursor = None
        try:
            cursor = self.connection.cursor()
            cursor.execute('SELECT * FROM empd')
            rows = cursor.fetchall()

            for row in rows:
                print(f"Employee Id: {row[0]}")
                print(f"Employee Name: {row[1]}")
                print(f"Employee Post: {row[2]}")
                print(f"Employee Salary: {row[3]}")
                print("----------------------------")

        except Error as e:
            logging.error(f"Error: {e}")
        finally:
            if cursor:
                cursor.close()

    def menu(self):
        while True:
            print("\nWelcome to Employee Management Record")
            print("1. Add Employee")
            print("2. Remove Employee")
            print("3. Promote Employee")
            print("4. Display Employees")
            print("5. Exit")

            choice = input("Enter your Choice: ")
            if choice == '1':
                self.add_employee()
            elif choice == '2':
                self.remove_employee()
            elif choice == '3':
                self.promote_employee()
            elif choice == '4':
                self.display_employees()
            elif choice == '5':
                break
            else:
                print("Invalid Choice. Please try again.")

# Calling menu function
if __name__ == "__main__":
    emp_mgmt = EmployeeManagement()
    emp_mgmt.menu()
