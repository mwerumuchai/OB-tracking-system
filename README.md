# OB-tracking-system

** Created by **[Erick Mutua](https://github.com/rickmutua), [Esther Muchai](https://github.com/mwerumuchai) and [Peter Maina](https://github.com/petersoleeh)

## Description
This is an integrated Occurrence Book application system that captures and manages all activities in a police station where manual occurrence books and registers are used.

Occurences such as reporting a crime, cash bail payment and booking a suspect are logged electronically by the officers on duty.The system interfaces with users on all levels and has an according set of rules to guide the user through mandatory fields to correctly capture occurrence data. This process ensures the integrity of the data and also speeds up capturing of information and at the same time enforces standardisation.

The system is web based and makes use of a centralised database to store all system information.The system is designed to be user friendly and easy to use.

System security is achieved using usernames and passwords linked to specific roles and rights as well as built-in database security mechanisms. To further extend the system’s security options, it can be set up to run securely using encryption.

## User Stories
As a user, I would like to;
1. Register to the app to start using the application.
2. Add in a new criminal by accessing a new registration form to key in the details.
3. View a list of all  the different records fetched from the database.
4. Filter crime data by date.
5. Filter crime data by nature of crime.
6. See the repeat offenders.
7. See different categories of crimes.
8. See the time a criminal was brought in.


## Specifications

| Behaviour | Input | Output |
| ------------ |:----------:| -------: | 
| Sign up for an account| Account name: Ceaser <br> Password: Julius | An account is created and a message is displayed|
| Login User | Email: ceaser@gmail.com <br> Password:*****| Logged in into the account and directed to the index page|
| Display search form | Search by Name, ID No. or Year| Once authenticated, the user will be able to view suspect information if any |
| Display suspect profile | **Add Crime** | An authenticated user can view Suspect information inclusive of previous records if any|
| Display Occurrence Book |**Add Report** | An authenticated user can view reports taken from different people can be view|
| Display Occurrence Book |**Add Suspect** | An authenticated user can enter new suspect information into the database|
| Display Archive | **Enter year**| An authenticated user can view all information from the specific year|
| Display Cash Bail Book |**Click Add Bail**| An authenticated user can view Suspects who have paid bail |

## Deployed Site
[Click here](http://icop.herokuapp.com) to go to the deployed site <br/>
or <br>
[Copy](http://icop.herokuapp.com) this and paste to your desired web browser

## Known Bugs
* Cash bail Book, flag when cash is refunded

## Technologies Used
* Python3.6 
* Django
* Bootstrap
* Postgres Database
* Css
* HTML
* Javascript 
* Heroku

## License
MIT &copy;2018 **[Erick Mutua](https://github.com/rickmutua), [Esther Muchai](https://github.com/mwerumuchai) and [Peter Maina](https://github.com/petersoleeh)
