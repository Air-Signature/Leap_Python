# Python program to demonstrate
# writing to CSV


# import csv

# # field names
# fields = ['Name', 'Branch', 'Year', 'CGPA']

# # data rows of csv file
# rows = [ ['Nikhil3', 'COE', '2', '9.0'],
#          ['Sanchit', 'COE', '2', '9.1'],
#          ['Aditya', 'IT', '2', '9.3'],
#          ['Sagar', 'SE', '1', '9.5'],
#          ['Prateek', 'MCE', '3', '7.8'],
#          ['Sahil', 'EP', '2', '9.1']]

# # name of csv file
# filename = "university_records.csv"

# # writing to csv file
# with open(filename, 'a') as csvfile:
#     # creating a csv writer object
#     csvwriter = csv.writer(csvfile)

#     # writing the fields
#     csvwriter.writerow(fields)

#     # writing the data rows
#     csvwriter.writerows(rows)


# import matplotlib.pyplot as plt

# # Data for the 2D line
# x = [1, 2, 3, 4, 5]

# y = [2, 4, 6, 8, 10]

# # Create a 2D plot
# plt.plot(x, y, marker="o", linestyle="-", color="blue", label="Line Example")

# # Set axis labels
# plt.xlabel("X-axis")
# plt.ylabel("Y-axis")

# # Set plot title
# plt.title("2D Line Plot Example")

# # Add a legend
# plt.legend()

# # Show the plot
# plt.show()



from datetime import datetime

now = datetime.now() # current date and time

year = now.strftime("%Y")
print("year:", year)


date_time = now.strftime("%m.%d.%Y_%H.%M.%S")
print("date and time:",date_time)