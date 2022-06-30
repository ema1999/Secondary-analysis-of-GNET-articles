import numpy as np
import matplotlib.pyplot as plt

Twitter = [0, 0, 0, 0, 2, 0, 3, 1, 3, 0, 3, 1, 0, 1, 0, 0, 0, 3, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
dates = ['12/2019', '01/2020', '02/2020', '03/2020', '04/2020', '05/2020', '06/2020', '07/2020', '08/2020', '09/2020', '10/2020', '11/2020', '12/2020', '01/2021', '02/2021', '03/2021','04/2021', '05/2021', '06/2021', '07/2021', '08/2021', '09/2021', '10/2021', '11/2021', '12/2021', '01/2022', '02/2022', '03/2022', '04/2022']


plt.bar (dates,Twitter, color='#0504aa') #bar properties
plt.xlabel('Time')  # plotting labels of axis
plt.xticks(dates, rotation=45)
plt.ylabel('Number of articles posted')
plt.title('Articles about al-Qaeda over time')  # title
plt.show()  # exporting the graph




