# Objective
To build a simple web app which will give a user an estimate of the value of a car depending on a number of set features which represent the condition of the car.

# Purpose
Buying a car is a large investment of money and individuals usually have a difficult time determining if the value of a car is fair. They need a way to be able to measure the value or worth of a car they are interested in buying compared to similar cars according to it's condition. This will help the buyer in budgeting and negotiation.

It can also serve to help sellers to appropriately price their vehicles according to market conditions.

# Approach
- Scrape data from online second hand car markets of UAE
- Clean, analyze and prepare the data
- Build an ensemble model where we have 2 models trained on separate sections of the data. One is trained on luxury vehicle and the other on non-luxury vehicles
- Build a web app interface for users to get market evaluations for the vehicles they are interested in

# Key Findings
1. **Dubai has the highest number of listed vehicles:** Although we don't have data on the actual sales, it is safe to assume that the most transaction and sales will happen in Dubai as well.
![Screenshot from 2024-11-27 12-19-10](https://github.com/user-attachments/assets/ad510ccd-a10a-4007-9ecd-046bfd08b5b9)

2. **Mercedes-Benz are the most frequently bought cars:** Seeing as Dubai and the United Arab Emirates is well renowned for luxury living, it seems plausible that people would flock to buy luxury vehicles. Mercedes-Benz seems to be one of the most frequently listed cars.
![Screenshot from 2024-11-27 12-19-45](https://github.com/user-attachments/assets/cf69f441-a330-4288-bb31-37b0d9c736ec)

3. **Mercedes-Benz has some of the most expensive cars:** We saw a lot of outliers in the data where there were vehicles that were absurdly priced. Most of these cars were customized G-Wagons from Mercedes-Benz. This later down the line lead to a change in decision of how we approached the model building phase.
![Screenshot from 2024-11-27 12-18-03](https://github.com/user-attachments/assets/9eb051cc-f250-4e3b-ab79-f1b73515df24)

# Model Considerations
We found that we got the best prediction results when training 2 separate models. One was trained on luxury cars and the other on non-luxury cars. An ensemble of these two models gave us the most accurate predictions for all cars.<br>

# Finished Product
![image](https://github.com/user-attachments/assets/3fbf9c4a-b5b8-49ca-b573-2fb137794cf8)
