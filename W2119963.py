# Author: Anuja Jayasinghe
# Date: 26/11/2024
# Student ID: 20231258 | W2119963

import csv

def validate_date_input(): # Task A: Input Validation
    while True: # Loop until a valid day is entered
        try:
            day = int(input("Please enter the day of the survey (DD): "))
            if 1 <= day <= 31: # Check input is in the range
                break 
            else:
                print("Out of range - day must be between 1 and 31.")
        except ValueError:
            print("Invalid input - Please enter integer values only for day.")

    while True: # Loop until a valid month is entered
        try:
            month = int(input("Please enter the month of the survey (MM): "))
            if 1 <= month <= 12: # Check input is in the range
                break  
            else:
                print("Out of range - month must be between 1 and 12.")
        except ValueError:
            print("Invalid input - Please enter integer values only for month.")

    while True: # Loop until a valid year is entered
        try:
            year = int(input("Please enter the year of the survey (YYYY): "))
            if 2000 <= year <= 2024: # Check input is in the range
                break  
            else:
                print("Out of range - year must be between 2000 and 2024.")
        except ValueError:
            print("Invalid input - Please enter integer values only for year.")

    # Return the validated date in ddmmyyyy format
    return f"{day:02d}{month:02d}{year}"

def validate_continue_input(): # Validate input for looping
    while True:
        user_choice = input("Do you want to analyze another file? (Y/N): ").strip().lower()
        if user_choice == 'y':
            return True  # User wants to continue
        elif user_choice == 'n':
            print("Exiting program.")
            return False  # User wants to exit
        else:
            print("Invalid input - please enter 'Y' to continue or 'N' to exit.")

def process_csv_data(file_name): # Task B: Processed Outcomes  
    total_trucks = 0
    total_electric = 0
    total_two_wheeled = 0
    busses_north = 0
    not_turning = 0
    percentage_trucks = 0
    bike_count = 0
    average_bikes_per_hour = 0
    total_speeding = 0
    elm_ave_count = 0
    hanley_highway_count = 0
    scooters_at_elm = 0
    scooters_percentage = 0
    hanley_data = []
    peak_hours = []
    rainy_hours = set()
    total_rain_hours = 0

    try:
        with open(file_name, mode='r') as csv_file: # extract the data from csv file
            reader = csv.DictReader(csv_file)
            data = [{key.strip(): value.strip() for key, value in row.items()} for row in reader]

        # extract and process metrics
        total_vehicles = len(data) # find total vehicles

        for row in data: # find total trucks
            if row['VehicleType'].lower() == 'truck':
                total_trucks +=1

        for row in data: # find total elctricHybrid vehicles
            if row['elctricHybrid'].lower() =='true':
                total_electric +=1

        for row in data: # find total two wheeed vehicles
            if row['VehicleType'].lower() in ['bicycle','motorcycle','scooter']:
                total_two_wheeled += 1

        for row in data: # find busses went north through elm avenue
            if (row['JunctionName'] == 'Elm Avenue/Rabbit Road'
                and row['travel_Direction_out'] == 'N'
                and row['VehicleType'].lower() == 'buss'):
                busses_north += 1
   
        for row in data: # vehicles not trun 
            if row['travel_Direction_in'] == row['travel_Direction_out']:
                not_turning += 1

        if total_vehicles > 0: # percentage of trucks    
            percentage_trucks = round((total_trucks/total_vehicles)*100)
        else:
            percentage_trucks = 0

        for row in data: # find total bicycles
            if row['VehicleType'].lower() == 'bicycle':
                bike_count += 1

        average_bikes_per_hour = round(bike_count / 24) # find the average bikes per hour 

        for row in data: # vehicles over the speed limit
            if int(row['VehicleSpeed']) > int(row['JunctionSpeedLimit']):
                total_speeding += 1

        for row in data: # vehicles through elm avenue
            if row['JunctionName'] == 'Elm Avenue/Rabbit Road':
                elm_ave_count += 1

 
        for row in data: # vehicles through hanley highway
            if row['JunctionName'] == 'Hanley Highway/Westway':
                hanley_highway_count += 1

        for row in data: # scooters through elm avenue
            if (row['VehicleType'].lower() == 'scooter'
                and row['JunctionName'] == 'Elm Avenue/Rabbit Road'):
                scooters_at_elm += 1
        if elm_ave_count > 0: # percentage of scooters through elm avenue  
            scooters_percentage = round((scooters_at_elm/elm_ave_count)*100)
        else:
            scooters_percentage = 0

        for row in data: # calculatoin peak vehicle count
            if row['JunctionName'] == 'Hanley Highway/Westway':
                hanley_data.append(row['timeOfDay'][:2]) 
        hour_counts = [0] * 24
        for hour in hanley_data:
            hour_counts[int(hour)] += 1 
        peak_vehicle_count = max(hour_counts)

        for hour, count in enumerate(hour_counts): # calculate peak hours
            if count == peak_vehicle_count:
                peak_hours.append(f"Between {hour:02d}:00 and {hour + 1:02d}:00")

        for row in data: # calculate the total rain hours of the day
            if 'Rain' in row['Weather_Conditions']:
                time_of_day = row['timeOfDay']
                hour = int(time_of_day.split(':')[0])
                rainy_hours.add(hour)
        total_rain_hours = len(rainy_hours)


        # Return a list of outcomes
        outcomes = [
             file_name,
             total_vehicles,
             total_trucks,
             total_electric,
             total_two_wheeled,
             busses_north,
             not_turning,
             percentage_trucks,
             average_bikes_per_hour,
             total_speeding,
             elm_ave_count,
             hanley_highway_count,
             scooters_percentage,
             peak_vehicle_count,
             peak_hours,
             total_rain_hours,
        ]
        
        return outcomes, data

    except FileNotFoundError:
        # print(f"Error: File '{file_name}' not found.")
        return None
    except KeyError as e:
        print(f"KeyError: Column '{e}' not found. Please check the CSV file format.")
        return None

                                                             
def display_outcomes(outcomes):
    print("\n*************** Results ***************")
    print(f"1.  Survey File Name : {outcomes[0]}")
    print(f"2.  Total Vehicles in this survey: {outcomes[1]}")
    print(f"3.  Total Trucks in this survey: {outcomes[2]}")
    print(f"4.  Total Electric Vehicles in this survey: {outcomes[3]}")
    print(f"5.  Total Two-Wheeled Vehicles in this survey: {outcomes[4]}")
    print(f"6.  Buses Heading North (Elm Avenue/Rabbit Road): {outcomes[5]}")
    print(f"7.  Vehicles Not Turning left or right: {outcomes[6]}")
    print(f"8.  Percentage of Trucks in this survey: {outcomes[7]}%")
    print(f"9.  Average Number of Bikes Per Hour according to this survey: {outcomes[8]}")
    print(f"10. Total Vehicles Over Speed Limit: {outcomes[9]}")
    print(f"11. Total Vehicles recorded through (Elm Avenue/Rabbit Road) is: {outcomes[10]}")
    print(f"12. Total Vehicles recorded through (Hanley Highway/Westway) is: {outcomes[11]}")
    print(f"13. Percentage of Scooters recorded through (Elm Avenue/Rabbit Road) is: {outcomes[12]}%")
    print(f"14. The highest number of vehicles in an hour on (Hanley Highway/Westway) is: {outcomes[13]}")
    print(f"15. Peak Traffic Hours according to this survey through (Hanley Highway/Westway) is: {', '.join(outcomes[14])}")
    print(f"16. Total Rainy Hours in this survey: {outcomes[15]}")
    print("***************************************")

def save_results_to_file(outcomes): # Task C: Save Results to Text File
    try:
        with open('results.txt', mode='a') as file:  # Open the file in append mode
            file.write("\n*************** Results ***************\n")
            file.write(f"1.  Survey File Name: {outcomes[0]}\n")
            file.write(f"2.  Total Vehicles in this survey: {outcomes[1]}\n")
            file.write(f"3.  Total Trucks in this survey: {outcomes[2]}\n")
            file.write(f"4.  Total Electric Vehicles in this survey: {outcomes[3]}\n")
            file.write(f"5.  Total Two-Wheeled Vehicles in this survey: {outcomes[4]}\n")
            file.write(f"6.  Buses Heading North (Elm Avenue/Rabbit Road): {outcomes[5]}\n")
            file.write(f"7.  Vehicles Not Turning left or right: {outcomes[6]}\n")
            file.write(f"8.  Percentage of Trucks in this survey: {outcomes[7]}%\n")
            file.write(f"9.  Average Number of Bikes Per Hour: {outcomes[8]}\n")
            file.write(f"10. Total Vehicles Over Speed Limit: {outcomes[9]}\n")
            file.write(f"11. Total Vehicles through (Elm Avenue/Rabbit Road): {outcomes[10]}\n")
            file.write(f"12. Total Vehicles through (Hanley Highway/Westway): {outcomes[11]}\n")
            file.write(f"13. Percentage of Scooters through (Elm Avenue/Rabbit Road): {outcomes[12]}%\n")
            file.write(f"14. Highest Number of Vehicles in an Hour (Hanley Highway/Westway): {outcomes[13]}\n")
            file.write(f"15. Peak Traffic Hours (Hanley Highway/Westway): {', '.join(outcomes[14])}\n")
            file.write(f"16. Total Rainy Hours: {outcomes[15]}\n")
            file.write("*****************************************\n")

        print("Results saved as results.txt")  # Confirm save operation
    
    except IOError as e:
        print(f"An error occurred while writing to the file: {e}")  # Handle file I/O errors
import os
def main(): # Main program execution
    base_path = r"D:\IIT\Year 1\Semester 1\4COSC006C_SD1_Pro\CW_01"####
    while True:
        # Validate date input and construct file name
        survey_date = validate_date_input()  # Returns date as ddmmyyyy
        file_name = f"traffic_data{survey_date}.csv"
        full_path = os.path.join(base_path, file_name)####
        outcomes,_ = process_csv_data(file_name)
        if outcomes:
            display_outcomes(outcomes)
            save_results_to_file(outcomes)
        
        # Ask the user if they want to analyze another file
        if not validate_continue_input():
            break



# Running the main program
if __name__ == "__main__":
    main()

