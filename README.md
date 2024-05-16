# Hostel Price Analysis
#### Project Status: Active

## Project Objective
When planning the next city trip, finding a great hostel is crucial. For maximum flexibility, you would like to book as late as possible. 
However, at this time, the best hostels might already be booked out or the price exceeds your budget.
So, when is the perfect time to book to achieve highest flexibility and variety, while not wasting unnecessary money.

## Technologies
* MongoDB
* Unittest
* Pandas, PyMongo, Selenium
* Github Actions
* Jupyter Notebook

## Project Description
### Data Collecting
Data is collected from `hostelworld.com`, one of the largest platforms for hostel booking worldwide. 
The `Selenium` framework is used to call the website with given specifications, such as city, duration of stay, etc.

### Deployment
Data taking is deployed to GitHub Actions for continuous testing and automized data taking.

### Data Storage
After data is collected, it is written to a MongoDB database.

### Analysis
Interesting figures were narrowed down to the following:
- price(days_before) and n_hostels(days_before ) for a given minimum rating, maximum distance from the city center, arrival date and duration of stay
The relation between these variables is investigated using `pandas` and `Jupyter Notebook`

## First results
- Stronger correlation between rating and price for later booking
- This development of the correlation will be further validated after taking more data
