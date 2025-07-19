import tkinter as tk
import W2119963 as process

class HistogramApp: # Task D
    def __init__(self, file_name, data):
        self.file_name = file_name
        self.traffic_data = data
        self.date = file_name.replace("traffic_data", "").replace(".csv", "")
        self.junctions = ['Elm Avenue/Rabbit Road', 'Hanley Highway/Westway']
        self.canvas_width = 1100
        self.canvas_height = 585
        self.root = tk.Tk()
        self.canvas = None


    def setup_window(self):
        # Set the window title
        self.root.title(f"Histogram of {self.file_name}")

        # Set the window background 
        dark_bg = "#2b2b2b"  # HEX code for Dark gray color
        self.root.configure(bg=dark_bg)

        # Make the window pop up
        self.root.attributes("-topmost", True)
        self.root.after(100, lambda: self.root.attributes("-topmost", False))

        # Createing the canvas
        self.canvas = tk.Canvas(
            self.root,
            width=self.canvas_width,
            height=self.canvas_height,
            bg="#1e1e1e",  # HEX code for Darker gray color
            highlightthickness=0  # Remove borders around the canvas
        )
        self.canvas.pack()

        # Add a title at the top-middle section
        formatted_date = f"{self.date[:2]}/{self.date[2:4]}/{self.date[4:]}"  # Format date as DD/MM/YYYY
        self.canvas.create_text(
            self.canvas_width / 2, 30,  # Position of the title
            text=f"Histogram of Vehicle Frequency per Hour ({formatted_date})",
            font=("Verdana", 16, "bold"),
            fill="white"  
        ) 


    def draw_histogram(self):
        # Extracting data 
        junction_data = {junction: [0] * 24 for junction in self.junctions} # Creating a dictionary to store vehicle count
        for row in self.traffic_data:
            junction = row['JunctionName']
            time_of_day = row['timeOfDay']
            hour = int(time_of_day.split(":")[0])
            if junction in self.junctions:
                junction_data[junction][hour] += 1 # Increment the count for the hour

        # Settings for Histogram
        bar_width = 15 
        spacing = 14 
        left_margin = 50
        bottom_margin = 5
        max_count = max(max(junction_data[junction]) for junction in self.junctions) or 1
        y_scale = 400 / max_count 
        x_start = left_margin 

        # Adjust canvas width dynamically based on bar count
        total_width = left_margin + spacing + 24 * (bar_width * len(self.junctions) + spacing)
        if total_width > self.canvas_width:
            self.canvas_width = max(self.canvas_width, total_width)
            self.canvas.config(width=self.canvas_width)

        # Draw bars for each hour 
        for hour in range(24): # Setting bar sizes, spacing and positions of the bars
            for j, junction in enumerate(self.junctions):
                count = junction_data[junction][hour]
                x1 = x_start + hour * (bar_width * len(self.junctions) + spacing) + j * bar_width
                y1 = 500 - bottom_margin - count * y_scale
                x2 = x1 + bar_width
                y2 = 500 - bottom_margin
                color = "#ff0054" if junction == "Elm Avenue/Rabbit Road" else "#ffd500"
                
                # Creat the bars
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="#001233", width=1)

                # Show individual count on top of each bar
                self.canvas.create_text(
                    (x1 + x2) / 2, y1 - 15,
                    text=str(count),
                    anchor="n", font=("Arial", 8), fill="white" 
                )
            # Draw axes
            self.canvas.create_line(left_margin, 500 - bottom_margin, total_width - spacing, 500 - bottom_margin, fill="#888888", width=2)  # X-axis 
            self.canvas.create_line(left_margin, 500 - bottom_margin, left_margin, 105, fill="#888888", width=2)  # Y-axis 

            # X-Axis Label
            self.canvas.create_text(
                total_width / 2, 500 - bottom_margin + 48, 
                text="Hours from 00:00 to 23:00", 
                anchor="n", font=("Verdana", 10), fill="#D3D3D3"
            )

            # Y-Axis Label (Vertical)
            self.canvas.create_text(
                left_margin - 30, 100 + (500 - bottom_margin) / 2, 
                text="Vehicle count", 
                anchor="w", font=("Verdana", 12), fill="#D3D3D3", angle=90
            )

            # Add hour labels below the bars
            x_label = x_start + hour * (bar_width * len(self.junctions) + spacing) + (bar_width * len(self.junctions)) / 2
            self.canvas.create_text(
                x_label, 500 - bottom_margin + 15,
                text=f"{hour}:00",
                anchor="n", font=("Arial", 10), fill="#D3D3D3" 
            )

    def add_legend(self):
        legend_x = self.canvas_width - 1065
        legend_y = 60
        self.canvas.create_rectangle(legend_x, legend_y, legend_x + 15, legend_y + 15, fill="#ff0054", outline="#ff0054")
        self.canvas.create_text(
            legend_x + 20, legend_y + 7,
            text="Elm Avenue/Rabbit Road",
            anchor="w",
            font=("Arial", 10),
            fill="white"  
        )
        self.canvas.create_rectangle(legend_x, legend_y + 20, legend_x + 15, legend_y + 35, fill="#ffd500", outline="#ffd500")
        self.canvas.create_text(
            legend_x + 20, legend_y + 27,
            text="Hanley Highway/Westway",
            anchor="w",
            font=("Arial", 10),
            fill="white"  
        )

    def add_quit_button(self):
        # Define the quit action
        def on_quit():
            self.root.destroy()  # Closes the root window immediately

        # Add the Quit button with styling
        quit_button = tk.Button(
            self.root,
            text="Quit",
            command=on_quit,
            font=("Arial", 12),
            bg="#444444",  
            fg="white",    
            activebackground="#666666",  
            activeforeground="white",    
            relief="flat"
        )
        quit_button.pack(side="bottom", pady=5) 


    def run(self):
        self.setup_window()
        self.draw_histogram()
        self.add_legend()
        self.add_quit_button() 
        self.root.mainloop()

class MultiCSVProcessor: # Task E
    def __init__(self):
        self.date = None
        self.file_name = None
        self.outcomes = None
        self.data = None
        self.canvas = None

    def load_csv_file(self):
        while True:
            date = process.validate_date_input() # take the validated date 
            file_name = f"traffic_data{date}.csv" # assembling the file_name 
            result = process.process_csv_data(file_name) # processing and extracting the data from the csv file

            if result is None: # throw error if csv file is empty or formatted incorrectly
                print(f"Error: File '{file_name}' not found or could not be processed.")
                
                while True:  # Handle retry input
                    retry = input("Do you want to try another file? (Y/N): ").strip().lower()
                    if retry == 'n':
                        return None, None, None  # Exit the function user doesn't want to continue
                    elif retry == 'y':
                        break  # Break out of this loop to restart the main loop
                    else:
                        print("Invalid input. Please enter 'Y' for Yes or 'N' for No.")
            else:
                outcomes, data = result
                return file_name, outcomes, data 

    def clear_previous_data(self):
        # Clearing  the data has been stores previously
        self.date = None
        self.file_name = None
        self.outcomes = None
        self.data = None
        self.canvas = None

    def handle_user_interaction(self):
        return process.validate_continue_input()
         # This handles whether the user wants to continue using the program or not   

    def process_files(self):
        while True:
            file_name, outcomes, data = self.load_csv_file()

            # Proceed only if a valid file and data are loaded
            if file_name and data:
                if outcomes:
                    process.display_outcomes(outcomes) # Displaying outcomes in the terminal
                    process.save_results_to_file(outcomes) # saving the results in results.txt

                app = HistogramApp(file_name, data) 
                app.run() # creating the histogram

                if not self.handle_user_interaction(): #ask user need to continue or close the program
                    break

                self.clear_previous_data() # clearing the data previouslt saved
            else:
                print("Exiting application.")
                break # Exit if no valid file is loaded and the user doesn't want to retry

if __name__ == "__main__": # main program runner
    processor = MultiCSVProcessor()
    processor.process_files()