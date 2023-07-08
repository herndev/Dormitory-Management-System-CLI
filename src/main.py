import pyfingerprint.pyfingerprint as pyfp
import pymysql.cursors
import time
from datetime import datetime

# Initialize the fingerprint scanner
def initialize_scanner():
    try:
        # Replace 'COM3' with the actual port name you found in Device Manager.
        f = pyfp.PyFingerprint('COM3', 57600, 0xFFFFFFFF, 0x00000000)
        if not f.verifyPassword():
            raise ValueError('The given fingerprint sensor password is wrong!')
        return f
    except FileNotFoundError:
        print('Error: The specified port could not be found.')
    except Exception as e:
        print('Error: ' + str(e))
    return None

# Capture fingerprint and verify
def verify_fingerprint(f):
    try:
        print('Waiting for fingerprint...')
        while not f.readImage():
            pass
        f.convertImage(0x01)
        result = f.searchTemplate()
        position = result[0]

        if position >= 0:
            print('Fingerprint verified. User ID: ' + str(position))
            return position
        else:
            print('Fingerprint not recognized.')
            return -1
    except Exception as e:
        print('Error: ' + str(e))
        return -1

# Enroll fingerprint for an existing user ID
def enroll_fingerprint(f, position):
    try:
        print('Place your finger on the scanner...')
        while not f.readImage():
            pass
        f.convertImage(0x01)
        f.createTemplate()
        f.storeTemplate(position)
        print('Fingerprint enrolled successfully for User ID: ' + str(position))
        return position
    except Exception as e:
        print('Error: ' + str(e))
        return -1

# Clock in function
def clock_in(user_id, connection, cursor):
    try:
        # Insert the clock-in timestamp for the user
        sql = "INSERT INTO clock (user_id, clock_in) VALUES (%s, %s)"
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute(sql, (user_id, current_time))
        connection.commit()

        print('Clock in successful!')
    except Exception as e:
        print('Error: ' + str(e))

# Clock out function
def clock_out(user_id, connection, cursor):
    try:
        # Update the clock-out timestamp for the user
        sql = "UPDATE clock SET clock_out = %s WHERE user_id = %s"
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute(sql, (current_time, user_id))
        connection.commit()

        print('Clock out successful!')
    except Exception as e:
        print('Error: ' + str(e))

# Store fingerprint in database
def store_in_database(position, connection, cursor):
    try:
        # Insert the fingerprint data into the database
        sql = "INSERT INTO fingerprints (user_id) VALUES (%s)"
        cursor.execute(sql, position)
        connection.commit()

        print('Fingerprint stored in the database.')
    except Exception as e:
        print('Error: ' + str(e))

# Main program
def main():
    # Connect to the database
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='test',
        cursorclass=pymysql.cursors.DictCursor
    )

    scanner = initialize_scanner()
    if scanner is None:
        exit(1)

    try:
        while True:
            print('Dormitory Management System CLI')
            print('Please select an option:')
            print('1. Clock In')
            print('2. Clock Out')
            print('3. Enroll Fingerprint')
            print('4. Exit')
            choice = input('Enter your choice: ')

            if choice == '1':
                position = verify_fingerprint(scanner)
                if position >= 0:
                    clock_in(position, connection, connection.cursor())
            elif choice == '2':
                position = verify_fingerprint(scanner)
                if position >= 0:
                    clock_out(position, connection, connection.cursor())
            elif choice == '3':
                position = int(input('Enter the User ID: '))
                enrolled_position = enroll_fingerprint(scanner, position)
                if enrolled_position >= 0:
                    store_in_database(enrolled_position, connection, connection.cursor())
            elif choice == '4':
                break
            else:
                print('Invalid choice. Please try again.')

            time.sleep(1)
    finally:
        # Close the database connection
        connection.close()

    # Close the scanner
    scanner.close()

if __name__ == '__main__':
    main()