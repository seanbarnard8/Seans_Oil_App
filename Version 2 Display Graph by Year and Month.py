import pandas as pd
import matplotlib.pyplot as plt
from tkinter import Tk, filedialog, Button, Label, Entry

class BrentOilPriceApp:
    def select_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if self.file_path:
            self.data = pd.read_excel(self.file_path, header=None)  # No header
            self.data.columns = ['Date', 'Price']  # Manually set column names
            print(f"File selected: {self.file_path}")
            print("Raw Date column preview:\n", self.data['Date'].head())  # Debugging output for Date column

            # Correctly parse dates with the "M" in the format
            self.data['Date'] = pd.to_datetime(self.data['Date'].str.replace('M', ''), format='%Y%m', errors='coerce')
            self.data.dropna(subset=['Date'], inplace=True)  # Remove rows with invalid dates
            self.data['Year'] = self.data['Date'].dt.year  # Extract the year from the date
            self.data['Month'] = self.data['Date'].dt.month  # Extract the month from the date

            print("Parsed Date column preview:\n", self.data['Date'].head())  # Debugging output for parsed dates
            print("Available columns:", self.data.columns.tolist())
            print("Data preview:\n", self.data.head())  # Preview the first few rows of the data

    def display_graph_by_year(self):
        if self.data is None:
            print("Please select a data file first.")
            return

        years_input = self.year_entry.get()
        years_to_display = self.parse_years(years_input)
        print("Years to display:", years_to_display)  # Debugging output

        selected_data = self.data[self.data['Year'].isin(years_to_display)]
        print("Selected data preview:\n", selected_data.head())  # Preview the selected data

        if selected_data.empty:
            print(f"No data available for the year(s): {years_input}")
            return

        plt.figure(figsize=(10, 6))
        for year_range in years_input.split(','):
            if '-' in year_range:
                start_year, end_year = map(int, year_range.split('-'))
                range_data = selected_data[(selected_data['Year'] >= start_year) & (selected_data['Year'] <= end_year)]
                yearly_avg = range_data.groupby('Year').mean()
                plt.plot(yearly_avg.index, yearly_avg['Price'], label=f"{start_year}-{end_year}")
            else:
                year = int(year_range.strip())
                yearly_data = selected_data[selected_data['Year'] == year]
                yearly_avg = yearly_data.groupby('Year').mean()
                plt.plot(yearly_avg.index, yearly_avg['Price'], label=f"{year}")

        plt.xlabel('Year')
        plt.ylabel('Brent Crude Oil Price')
        plt.title('Brent Crude Oil Prices by Year')
        plt.legend()
        plt.xticks(ticks=years_to_display, rotation=45, ha='right')  # Set x-ticks to display every year
        plt.tight_layout()  # Adjust layout to make room for rotated labels
        plt.show()

    def display_graph_by_month(self):
        if self.data is None:
            print("Please select a data file first.")
            return

        year_input = self.year_entry.get()
        months_input = self.month_entry.get()
        months_to_display = self.parse_months(months_input)
        print("Year to display:", year_input)  # Debugging output
        print("Months to display:", months_to_display)  # Debugging output

        selected_data = self.data[(self.data['Year'] == int(year_input)) & (self.data['Month'].isin(months_to_display))]
        print("Selected data preview:\n", selected_data.head())  # Preview the selected data

        if selected_data.empty:
            print(f"No data available for the year {year_input} and month(s): {months_input}")
            return

        plt.figure(figsize=(10, 6))
        monthly_avg = selected_data.groupby('Month').mean()
        plt.plot(monthly_avg.index, monthly_avg['Price'], label=f"{year_input} {months_input}")

        plt.xlabel('Month')
        plt.ylabel('Brent Crude Oil Price')
        plt.title(f'Brent Crude Oil Prices for {year_input} by Month')
        plt.legend()
        plt.xticks(ticks=months_to_display)
        plt.tight_layout()  # Adjust layout to make room for rotated labels
        plt.show()

    def parse_years(self, years_input):
        years = []
        for part in years_input.split(','):
            if '-' in part:
                start_year, end_year = part.split('-')
                years.extend(range(int(start_year), int(end_year) + 1))
            else:
                years.append(int(part.strip()))
        return years

    def parse_months(self, months_input):
        months = []
        for part in months_input.split(','):
            if '-' in part:
                start_month, end_month = part.split('-')
                months.extend(range(int(start_month), int(end_month) + 1))
            else:
                months.append(int(part.strip()))
        return months

    def __init__(self, master):
        self.master = master
        master.title("Brent Crude Oil Price Analyzer")

        self.label = Label(master, text="Select an Excel file with Brent crude oil price data:")
        self.label.pack()

        self.select_file_button = Button(master, text="Select data file", command=self.select_file)
        self.select_file_button.pack()

        self.year_label = Label(master, text="Enter the year(s) to display (comma-separated for multiple years or ranges):")
        self.year_label.pack()

        self.year_entry = Entry(master)
        self.year_entry.pack()

        self.month_label = Label(master, text="Enter the months to display (comma-separated for multiple months or ranges):")
        self.month_label.pack()

        self.month_entry = Entry(master)
        self.month_entry.pack()

        self.display_year_button = Button(master, text="Display graph by year", command=self.display_graph_by_year)
        self.display_year_button.pack()

        self.display_month_button = Button(master, text="Display graph by month", command=self.display_graph_by_month)
        self.display_month_button.pack()

        self.file_path = None
        self.data = None

if __name__ == "__main__":
    root = Tk()
    app = BrentOilPriceApp(root)
    root.mainloop()
