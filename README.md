# About This Project

This is a proof of concept web scraping exercise that allows the user to input the type of yield curve
they want to see(nominal or real), then also select the year and month for which they want.  The application
then reaches out to the US Treasury website and retrieves, via web scrape, the tabular data in the on screen
grid.

The goal is to integrate other assets, a database connection and a front end for inputs that will ultimately
drive the data acquisition.

# Setting up the Project

- Set up Virtual environment
`python -m venv .venv`

1.) Loop through urls
2.) log into workday site
3.) navigate to candidate home
4.) scrape active applications

Data Models
1.) Company
- name
- website
- career_url
- equity_ticker

2.) Applications
- company_id
- is_active
- date_applied