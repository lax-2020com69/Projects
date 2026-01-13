# International Airline Management System

## Overview

This project is a console-based airline management system written in C++. It allows admins and clients to manage flights and bookings efficiently. The system supports user registration and login, flight management, seat booking, billing, and account deletion.

---

## Features

### For Admins
- View all flights
- Add new flights
- Delete flights
- Add discounts on flights
- Set prices for different seat classes (First, Business, Economy)
- Approve admin accounts
- View all bookings
- View passengers on a specific flight
- Search bookings by client username
- Modify flight information

### For Clients
- View all available flights
- Filter flights based on criteria
- View prices for different classes
- Book seats on flights
- Cancel booked seats
- View detailed billing for bookings
- View seat layout and availability
- Delete user account (removes user and all associated bookings)

---

## Installation

### Requirements
- A C++ compiler supporting C++11 or later (e.g., g++, clang++)
- Terminal or command prompt for running the executable
   or
- Dev-C++

### Steps
1. Clone or download the source code.
2. Compile the code using your preferred C++ compiler. Example:

```bash
g++ main.cpp -o airline_system
Run the executable:

bash
Copy code
./airline_system   # on Linux/macOS
airline_system.exe # on Windows

Usage
On startup, you can login or signup as a user.

Users have roles: admin or client.

Admins have access to advanced flight and booking management menus.

Clients can browse flights, book seats, and view their bookings and bills.

File Structure
main.cpp - Contains the entire program source code, including user management, flight management, and booking handling.

Data files (created and maintained by the program):

users.txt

flights.txt

bookings.txt

License
This project is licensed under the MIT License. See the MIT License for details.

Notes
This is a console application designed for learning and basic management purposes.

Data persistence is handled by saving and loading from data files.

User input is validated to prevent crashes due to invalid entries.

Seat layouts and bookings are handled with simple arrays and vectors for ease of management.

Discounts and pricing are applied per seat class and booking.

Future Improvements
Add graphical user interface (GUI).

Support for online payment simulation.

More complex flight filtering (by date range, price range, airline).

Email notification system on booking.

Multi-language support.

Contact
For questions or suggestions, please open an issue or contact the project maintainer.
