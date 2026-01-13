#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>
#include <algorithm>
#include <map>
#include <iomanip>
#include <cctype>
using namespace std;

// -------------------- Data Structures --------------------

struct User {
    string username;
    string password;
    string role;       // "admin" or "client"
    string status;     // "approved" or "pending"
};

struct Flight {
    string flightID;
    string origin;
    string destination;
    string date;       // YYYY-MM-DD
    string time;       // HH:MM
    int priceFirst;
    int seatsFirstTotal;
    int seatsFirstAvailable;
    int priceBusiness;
    int seatsBusinessTotal;
    int seatsBusinessAvailable;
    int priceEconomy;
    int seatsEconomyTotal;
    int seatsEconomyAvailable;
    int discountFirst;    // percentage 0-100
    int discountBusiness;
    int discountEconomy;
};

struct Booking {
    string clientName;
    string flightID;
    string origin;
    string destination;
    string date;
    string time;
    char seatClass;      // 'F' / 'B' / 'E'
    vector<string> seatsBooked;
    int pricePerSeat;
    int discountPercent;
    int totalAmount;
};

// -------------------- Globals --------------------

vector<User> users;
vector<Flight> flights;
vector<Booking> bookings;

// -------------------- Helper Functions --------------------

// Removes leading/trailing whitespace (spaces, tabs, newlines, carriage returns)
void trim(string &s) {
    size_t start = s.find_first_not_of(" \n\r\t");
    size_t end = s.find_last_not_of(" \n\r\t");
    if (start == string::npos || end == string::npos) {
        s.clear();
        return;
    }
    s = s.substr(start, end - start + 1);
}

// Converts a string to lowercase
string toLower(const string &s) {
    string res = s;
    for (char &c : res) c = static_cast<char>(tolower(static_cast<unsigned char>(c)));
    return res;
}

// Converts all characters in seat string to uppercase
string normalizeSeat(const string& seat) {
    string normalized;
    for (char ch : seat)
        normalized += static_cast<char>(toupper(static_cast<unsigned char>(ch)));
    return normalized;
}

// -------------------- File I/O --------------------

void loadUsers() {
    users.clear();
    ifstream fin("users.txt");
    if (!fin) return;

    string line;
    while (getline(fin, line)) {
        if (line.empty()) continue;
        stringstream ss(line);
        User u;
        ss >> u.username >> u.password >> u.role >> u.status;
        users.push_back(u);
    }
    fin.close();
}

void saveUsers() {
    ofstream fout("users.txt");
    for (auto &u : users) {
        fout << u.username << " " << u.password << " " << u.role << " " << u.status << "\n";
    }
    fout.close();
}

void loadFlights() {
    flights.clear();
    ifstream fin("flight.txt");
    if (!fin) return;

    string line;
    while (getline(fin, line)) {
        if (line.empty()) continue;
        stringstream ss(line);
        Flight f;
        ss >> f.flightID >> f.origin >> f.destination >> f.date >> f.time
           >> f.priceFirst >> f.seatsFirstTotal >> f.seatsFirstAvailable
           >> f.priceBusiness >> f.seatsBusinessTotal >> f.seatsBusinessAvailable
           >> f.priceEconomy >> f.seatsEconomyTotal >> f.seatsEconomyAvailable
           >> f.discountFirst >> f.discountBusiness >> f.discountEconomy;
        flights.push_back(f);
    }
    fin.close();
}

void saveFlights() {
    ofstream fout("flight.txt");
    for (auto &f : flights) {
        fout << f.flightID << " " << f.origin << " " << f.destination << " " << f.date << " " << f.time << " "
             << f.priceFirst << " " << f.seatsFirstTotal << " " << f.seatsFirstAvailable << " "
             << f.priceBusiness << " " << f.seatsBusinessTotal << " " << f.seatsBusinessAvailable << " "
             << f.priceEconomy << " " << f.seatsEconomyTotal << " " << f.seatsEconomyAvailable << " "
             << f.discountFirst << " " << f.discountBusiness << " " << f.discountEconomy << "\n";
    }
    fout.close();
}

void loadBookings() {
    bookings.clear();
    ifstream fin("bill.txt");
    if (!fin) return;

    string line;
    while (getline(fin, line)) {
        if (line.empty()) continue;
        stringstream ss(line);
        Booking b;
        int seatsCount;
        ss >> b.clientName >> b.flightID >> b.origin >> b.destination >> b.date >> b.time >> b.seatClass >> seatsCount;
        b.seatsBooked.clear();
        for (int i = 0; i < seatsCount; i++) {
            string seat;
            ss >> seat;
            b.seatsBooked.push_back(seat);
        }
        ss >> b.pricePerSeat >> b.discountPercent >> b.totalAmount;
        bookings.push_back(b);
    }
    fin.close();
}

void viewAllBookings() {
    if (bookings.empty()) {
        cout << "\nNo bookings found.\n";
        return;
    }

    cout << "\n========== All Bookings ==========\n";
    int count = 1;
    for (const auto& b : bookings) {
        cout << "\nBooking #" << count++
             << "\n-----------------------------------"
             << "\nClient Name   : " << b.clientName
             << "\nFlight ID     : " << b.flightID
             << "\nRoute         : " << b.origin << " to " << b.destination
             << "\nDate & Time   : " << b.date << " " << b.time
             << "\nClass         : " << b.seatClass
             << "\nSeats Booked  : ";

        for (const auto& seat : b.seatsBooked)
            cout << seat << " ";
        
        cout << "\nPrice per Seat: $" << fixed << setprecision(2) << b.pricePerSeat
             << "\nDiscount      : " << b.discountPercent << "%"
             << "\nTotal Amount  : $" << fixed << setprecision(2) << b.totalAmount
             << "\n-----------------------------------\n";
    }
    cout << "========== End of Bookings ==========\n";
}

void saveBookings() {
    ofstream fout("bill.txt");
    for (auto &b : bookings) {
        fout << b.clientName << " " << b.flightID << " " << b.origin << " " << b.destination << " "
             << b.date << " " << b.time << " " << b.seatClass << " " << b.seatsBooked.size() << " ";
        for (auto &seat : b.seatsBooked) {
            fout << seat << " ";
        }
        fout << b.pricePerSeat << " " << b.discountPercent << " " << b.totalAmount << "\n";
    }
    fout.close();
}

// -------------------- User Management --------------------

bool usernameExists(const string &username) {
    for (const auto &u : users) {
        if (u.username == username) return true;
    }
    return false;
}

User* findUser(const string &username) {
    for (auto &u : users) {
        if (u.username == username) return &u;
    }
    return nullptr;
}


void signup() {
    string username, password, role;
    cout << "Choose username: ";
    cin >> username;

    if (usernameExists(username)) {
        cout << "Username already taken.\n";
        return;
    }

    cout << "Choose password: ";
    cin >> password;

    cout << "Choose role (admin/client): ";
    cin >> role;
    transform(role.begin(), role.end(), role.begin(), ::tolower);

    if (role != "admin" && role != "client") {
        cout << "Invalid role choice. Please enter 'admin' or 'client'.\n";
        return;
    }

    string status = (role == "admin") ? "pending" : "approved";
    users.push_back({username, password, role, status});
    saveUsers();

    cout << "Signup successful. ";
    if (role == "admin") cout << "Waiting for admin approval.\n";
    else cout << "You can login now.\n";
}


User* login() {
    string username, password;
    cout << "Username: ";
    cin >> username;
    cout << "Password: ";
    cin >> password;

    User* user = findUser(username);
    if (!user) {
        cout << "User not found.\n";
        return nullptr;
    }

    if (user->password != password) {
        cout << "Incorrect password.\n";
        return nullptr;
    }

    if (user->role == "admin" && user->status != "approved") {
        cout << "Your admin registration is still pending approval.\n";
        return nullptr;
    }

    cout << "Login successful. Welcome " << user->role << " " << user->username << ".\n";
    return user;
}

Flight* findFlight(const string &flightID) {
    for (auto &f : flights) {
        if (f.flightID == flightID) return &f;
    }
    return nullptr;
}

void modifyFlight() {
    string flightID;
    cout << "\n--- Modify Flight Details ---\n";
    cout << "Enter Flight ID to modify: ";
    cin >> flightID;

    Flight* f = findFlight(flightID);
    if (!f) {
        cout << "Flight not found.\n";
        return;
    }

    cout << "\nCurrent Flight Details:\n";
    cout << "Date: " << f->date << "\n";
    cout << "Time: " << f->time << "\n";

    cout << "\nWhat would you like to modify?\n";
    cout << "1. Date\n";
    cout << "2. Time\n";
    cout << "3. Both Date and Time\n";
    cout << "4. Cancel\n";
    cout << "Choice: ";

    int choice;
    cin >> choice;

    switch (choice) {
        case 1:
            cout << "Enter new date (YYYY-MM-DD): ";
            cin >> f->date;
            break;
        case 2:
            cout << "Enter new time (HH:MM): ";
            cin >> f->time;
            break;
        case 3:
            cout << "Enter new date (YYYY-MM-DD): ";
            cin >> f->date;
            cout << "Enter new time (HH:MM): ";
            cin >> f->time;
            break;
        case 4:
            cout << "Modification cancelled.\n";
            return;
        default:
            cout << "Invalid choice. No changes made.\n";
            return;
    }

    saveFlights();
    cout << "Flight updated successfully.\n";
}


void searchBookingByClient() {
    string name;
    cout << "Enter client name: ";
    cin.ignore();
    getline(cin, name);
    
    bool found = false;
    for (const auto& b : bookings) {
        if (b.clientName == name) {  // Could enhance with `strcasecmp()` or transform to lower
            cout << "\nClient: " << b.clientName
                 << "\nFlight ID: " << b.flightID
                 << "\nRoute: " << b.origin << " to " << b.destination
                 << "\nDate & Time: " << b.date << " " << b.time
                 << "\nClass: " << b.seatClass
                 << "\nSeats: ";
            for (const auto& seat : b.seatsBooked) cout << seat << " ";
            cout << "\nTotal Amount: $" << b.totalAmount << "\n";
            cout << "-----------------------------------\n";
            found = true;
        }
    }

    if (!found) cout << "No bookings found for this client.\n";
}

void viewPassengersOnFlight() {
    string flightID;
    cout << "Enter Flight ID: ";
    cin >> flightID;

    bool found = false;
    cout << "Passengers on Flight " << flightID << ":\n";

    for (const auto& b : bookings) {
        if (b.flightID == flightID) {
            cout << "- Client: " << b.clientName 
                 << " | Class: " << b.seatClass 
                 << " | Seats: ";
            for (const auto& seat : b.seatsBooked)
                cout << seat << " ";
            cout << "\n";
            found = true;
        }
    }

    if (!found) 
        cout << "No bookings found for this flight.\n";
}

void viewFlights() {
    if (flights.empty()) {
        cout << "\n??  No flights available.\n";
        return;
    }

    cout << "\n================================= Available Flights =================================\n\n";
    cout << left
         << setw(8)  << "ID"
         << setw(10) << "Origin"
         << setw(14) << "Destination"
         << setw(12) << "Date"
         << setw(8)  << "Time"
         << setw(18) << "First (Price, Avail)"
         << setw(20) << "Business (Price, Avail)"
         << setw(20) << "Economy (Price, Avail)"
         << setw(20) << "Discounts (F, B, E)" << "\n";

    cout << string(120, '-') << "\n";

    for (const auto& f : flights) {
        cout << left
             << setw(8)  << f.flightID
             << setw(10) << f.origin
             << setw(14) << f.destination
             << setw(12) << f.date
             << setw(8)  << f.time;

        string fstInfo = to_string(f.priceFirst) + " (" + to_string(f.seatsFirstAvailable) + ")";
        string busInfo = to_string(f.priceBusiness) + " (" + to_string(f.seatsBusinessAvailable) + ")";
        string ecoInfo = to_string(f.priceEconomy) + " (" + to_string(f.seatsEconomyAvailable) + ")";
        string discInfo = to_string(f.discountFirst) + "%, " + to_string(f.discountBusiness) + "%, " + to_string(f.discountEconomy) + "%";

        cout << setw(18) << fstInfo
             << setw(20) << busInfo
             << setw(20) << ecoInfo
             << setw(20) << discInfo
             << "\n";
    }

    cout << "\n====================================================================================\n";
}


void addFlight() {
    Flight f;
    cout << "Enter Flight ID: ";
    cin >> f.flightID;
    if (findFlight(f.flightID)) {
        cout << "Flight ID already exists.\n";
        return;
    }

    cout << "Enter Origin: ";
    cin >> f.origin;
    cout << "Enter Destination: ";
    cin >> f.destination;
    cout << "Enter Date (YYYY-MM-DD): ";
    cin >> f.date;
    cout << "Enter Time (HH:MM): ";
    cin >> f.time;

    cout << "Enter price for First class: ";
    cin >> f.priceFirst;
    cout << "Enter number of First class seats: ";
    cin >> f.seatsFirstTotal;

    cout << "Enter price for Business class: ";
    cin >> f.priceBusiness;
    cout << "Enter number of Business class seats: ";
    cin >> f.seatsBusinessTotal;

    cout << "Enter price for Economy class: ";
    cin >> f.priceEconomy;
    cout << "Enter number of Economy class seats: ";
    cin >> f.seatsEconomyTotal;

    if (f.priceFirst < 0 || f.priceBusiness < 0 || f.priceEconomy < 0 ||
        f.seatsFirstTotal < 0 || f.seatsBusinessTotal < 0 || f.seatsEconomyTotal < 0) {
        cout << "Prices and seats must be non-negative.\n";
        return;
    }

    f.seatsFirstAvailable = f.seatsFirstTotal;
    f.seatsBusinessAvailable = f.seatsBusinessTotal;
    f.seatsEconomyAvailable = f.seatsEconomyTotal;
    f.discountFirst = f.discountBusiness = f.discountEconomy = 0;

    flights.push_back(f);
    saveFlights();
    cout << "Flight added successfully.\n";
}

void deleteFlight() {
    string flightID;
    cout << "Enter Flight ID to delete: ";
    cin >> flightID;

    auto it = find_if(flights.begin(), flights.end(), [&](const Flight& f) { return f.flightID == flightID; });
    if (it == flights.end()) {
        cout << "Flight ID not found.\n";
        return;
    }

    // Check if bookings exist for this flight
    for (const auto& b : bookings) {
        if (b.flightID == flightID) {
            cout << "Cannot delete flight. Bookings exist for this flight.\n";
            return;
        }
    }

    flights.erase(it);
    saveFlights();
    cout << "Flight deleted successfully.\n";
}

void addDiscount() {
    string flightID;
    cout << "Enter Flight ID: ";
    cin >> flightID;
    Flight* f = findFlight(flightID);
    if (!f) {
        cout << "Flight not found.\n";
        return;
    }

    int dF, dB, dE;
    cout << "Enter discount % for First class (0-100): ";
    cin >> dF;
    cout << "Enter discount % for Business class (0-100): ";
    cin >> dB;
    cout << "Enter discount % for Economy class (0-100): ";
    cin >> dE;

    if (dF < 0 || dF > 100 || dB < 0 || dB > 100 || dE < 0 || dE > 100) {
        cout << "Invalid discount values. Must be between 0 and 100.\n";
        return;
    }

    f->discountFirst = dF;
    f->discountBusiness = dB;
    f->discountEconomy = dE;
    saveFlights();
    cout << "Discounts updated successfully.\n";
}

void setClassPrice() {
    string flightID;
    cout << "Enter Flight ID: ";
    cin >> flightID;
    Flight* f = findFlight(flightID);
    if (!f) {
        cout << "Flight not found.\n";
        return;
    }

    int pF, pB, pE;
    cout << "Enter new price for First class: ";
    cin >> pF;
    cout << "Enter new price for Business class: ";
    cin >> pB;
    cout << "Enter new price for Economy class: ";
    cin >> pE;

    if (pF < 0 || pB < 0 || pE < 0) {
        cout << "Prices must be non-negative.\n";
        return;
    }

    f->priceFirst = pF;
    f->priceBusiness = pB;
    f->priceEconomy = pE;
    saveFlights();
    cout << "Class prices updated successfully.\n";
}

void approveAdmins() {
    bool anyPending = false;
    for (auto &u : users) {
        if (u.role == "admin" && u.status == "pending") {
            anyPending = true;
            cout << "Pending admin: " << u.username << "\nApprove? (y/n): ";
            char ch;
            cin >> ch;
            if (ch == 'y' || ch == 'Y') {
                u.status = "approved";
                cout << "Admin approved.\n";
            } else {
                cout << "Admin not approved.\n";
            }
        }
    }
    if (!anyPending) {
        cout << "No pending admins.\n";
    }
    saveUsers();
}


// -------------------- Client Features --------------------

void filterFlights() {
    cout << "Filter by:\n1. Origin\n2. Destination\n3. Date\nChoice: ";
    int choice; cin >> choice;
    string filter;
    vector<Flight> filtered;
    switch (choice) {
        case 1:
            cout << "Enter origin to filter: ";
            cin >> filter;
            for (auto &f : flights) if (toLower(f.origin) == toLower(filter)) filtered.push_back(f);
            break;
        case 2:
            cout << "Enter destination to filter: ";
            cin >> filter;
            for (auto &f : flights) if (toLower(f.destination) == toLower(filter)) filtered.push_back(f);
            break;
        case 3:
            cout << "Enter date (YYYY-MM-DD) to filter: ";
            cin >> filter;
            for (auto &f : flights) if (f.date == filter) filtered.push_back(f);
            break;
        default:
            cout << "Invalid choice.\n";
            return;
    }
    if (filtered.empty()) {
        cout << "No flights found.\n";
        return;
    }
    for (auto &f : filtered) {
        cout << f.flightID << " - " << f.origin << " to " << f.destination << " - " << f.date << " " << f.time << "\n";
    }
}

void viewPrices() {
    string flightID;
    cout << "Enter Flight ID to view prices: ";
    cin >> flightID;
    Flight* f = findFlight(flightID);
    if (!f) {
        cout << "Flight not found.\n";
        return;
    }
    cout << "Prices for flight " << flightID << ":\n";
    cout << "First class: $" << f->priceFirst << " (Discount: " << f->discountFirst << "%)\n";
    cout << "Business class: $" << f->priceBusiness << " (Discount: " << f->discountBusiness << "%)\n";
    cout << "Economy class: $" << f->priceEconomy << " (Discount: " << f->discountEconomy << "%)\n";
}

Flight* getFlightByID(const string& flightID) {
    return findFlight(flightID);
}

int getAvailableSeats(Flight* f, char seatClass) {
    switch (seatClass) {
        case 'F': return f->seatsFirstAvailable;
        case 'B': return f->seatsBusinessAvailable;
        case 'E': return f->seatsEconomyAvailable;
    }
    return 0;
}

int getPrice(Flight* f, char seatClass) {
    switch (seatClass) {
        case 'F': return f->priceFirst;
        case 'B': return f->priceBusiness;
        case 'E': return f->priceEconomy;
    }
    return 0;
}

int getDiscount(Flight* f, char seatClass) {
    switch (seatClass) {
        case 'F': return f->discountFirst;
        case 'B': return f->discountBusiness;
        case 'E': return f->discountEconomy;
    }
    return 0;
}

vector<string> getAllSeats(const Flight& flight, char seatClass) {
    vector<string> seats;
    int totalSeats = 0;

    switch (seatClass) {
        case 'F': totalSeats = flight.seatsFirstTotal; break;
        case 'B': totalSeats = flight.seatsBusinessTotal; break;
        case 'E': totalSeats = flight.seatsEconomyTotal; break;
        default: return seats;
    }

    if (totalSeats == 0) return seats;

    int fullRows = totalSeats / 6;
    int leftoverSeats = totalSeats % 6;
    int totalRows = fullRows + (leftoverSeats > 0 ? 1 : 0);

    char columns[] = {'A', 'B', 'C', 'D', 'E', 'F'};

    for (int r = 1; r <= totalRows; r++) {
        int seatsInRow = (r == totalRows && leftoverSeats > 0) ? leftoverSeats : 6;
        for (int c = 0; c < seatsInRow; c++) {
            seats.push_back(to_string(r) + columns[c]);
        }
    }

    return seats;
}


vector<string> getBookedSeats(const string& flightID, char seatClass) {
    vector<string> booked;
    for (auto &b : bookings) {
        if (b.flightID == flightID && b.seatClass == seatClass) {
            booked.insert(booked.end(), b.seatsBooked.begin(), b.seatsBooked.end());
        }
    }
    return booked;
}


void bookSeat(const string& clientName) {
    cout << "Available flights:\n";
    for (auto &f : flights) {
        cout << f.flightID << " - " << f.origin << " to " << f.destination << " - " << f.date << " " << f.time << "\n";
    }

    string flightID;
    cout << "Enter Flight ID: ";
    cin >> flightID;
    Flight* f = getFlightByID(flightID);
    if (!f) {
        cout << "Flight not found.\n";
        return;
    }

    cout << "Select class (F/B/E): ";
    char seatClass; cin >> seatClass; seatClass = toupper(seatClass);
    if (seatClass != 'F' && seatClass != 'B' && seatClass != 'E') {
        cout << "Invalid class.\n";
        return;
    }

    int available = getAvailableSeats(f, seatClass);
    if (available == 0) {
        cout << "No available seats in this class.\n";
        return;
    }

    // Show seat layout
    cout << "\nAvailable seats in class " << seatClass << ":\n";
    vector<string> allSeats = getAllSeats(*f, seatClass);
    vector<string> bookedSeats = getBookedSeats(f->flightID, seatClass);

    int rows = allSeats.size() / 6;
    if (allSeats.size() % 6 != 0) rows++;
    char columns[] = {'A', 'B', 'C', 'D', 'E', 'F'};

    for (int row = 1; row <= rows; row++) {
        for (char col : columns) {
            string seat = to_string(row) + col;
            if (find(allSeats.begin(), allSeats.end(), seat) != allSeats.end()) {
                if (find(bookedSeats.begin(), bookedSeats.end(), seat) == bookedSeats.end()) {
                    cout << seat << " ";
                } else {
                    cout << "[X] ";
                }
            }
        }
        cout << "\n";
    }

    int n;
    cout << "\nEnter number of seats to book (available: " << available << "): ";
    cin >> n;
    if (n <= 0 || n > available) {
        cout << "Invalid seat number.\n";
        return;
    }

    vector<string> seats;
    cout << "Enter seat numbers (e.g. 3C 3D): ";
    for (int i = 0; i < n; i++) {
        string seatInput;
        cin >> seatInput;

        string seat = normalizeSeat(seatInput);

        if (find(allSeats.begin(), allSeats.end(), seat) == allSeats.end() ||
            find(bookedSeats.begin(), bookedSeats.end(), seat) != bookedSeats.end()) {
            cout << "Seat " << seat << " is invalid or already booked. Try again.\n";
            i--;
            continue;
        }

        seats.push_back(seat);
    }

    int pricePerSeat = getPrice(f, seatClass);
    int discount = getDiscount(f, seatClass);
    double subtotal = pricePerSeat * n;
    double discountAmt = subtotal * discount / 100.0;
    double total = subtotal - discountAmt;

    switch (seatClass) {
        case 'F': f->seatsFirstAvailable -= n; break;
        case 'B': f->seatsBusinessAvailable -= n; break;
        case 'E': f->seatsEconomyAvailable -= n; break;
    }

    bookings.push_back({clientName, f->flightID, f->origin, f->destination, f->date, f->time,
                        seatClass, seats, pricePerSeat, discount, static_cast<int>(total)});
    saveFlights();
    saveBookings();
    
	cout << "\n-------------------------------\n"
         << "          Booking Summary\n"
         << "-------------------------------\n";
    cout << "Client Name      : " << clientName << "\n";
    cout << "Flight ID        : " << f->flightID << "\n";
    cout << "Route            : " << f->origin << " --> " << f->destination << "\n";
    cout << "Date & Time      : " << f->date << " " << f->time << "\n\n";
    cout << "Class            : " << seatClass << "\n";
    cout << "Seats Booked     : ";
    for (auto &s : seats) cout << s << " ";
    cout << "\nPrice per Seat   : $" << pricePerSeat
         << "\nDiscount         : " << discount << "%"
         << "\n-------------------------------\n";
    cout << fixed << setprecision(2)
         << "Total Amount     : $" << total << "\n"
         << "-------------------------------\n";
    cout << "Thank you for booking with International Airlines!\n\n";
}

void cancelSeat(const string& clientName) {
    vector<int> clientBookings;
    for (int i = 0; i < (int)bookings.size(); i++) {
        if (bookings[i].clientName == clientName) {
            clientBookings.push_back(i);
        }
    }
    if (clientBookings.empty()) {
        cout << "You have no bookings.\n";
        return;
    }

    cout << "Your bookings:\n";
    for (int i = 0; i < (int)clientBookings.size(); i++) {
        Booking &b = bookings[clientBookings[i]];
        cout << i + 1 << ". Flight: " << b.flightID << ", Class: " << b.seatClass
             << ", Seats: ";
        for (auto &s : b.seatsBooked) cout << s << " ";
        cout << "\n";
    }

    cout << "Select booking number to cancel seats from: ";
    int choice; cin >> choice;
    if (choice < 1 || choice > (int)clientBookings.size()) {
        cout << "Invalid choice.\n";
        return;
    }

    Booking &b = bookings[clientBookings[choice - 1]];

    cout << "Enter seat numbers to cancel (space-separated): ";
    vector<string> seatsToCancel;
    string temp;
    getline(cin >> ws, temp);
    stringstream ss(temp);
    while (ss >> temp) seatsToCancel.push_back(temp);

    int seatsCancelledCount = 0;
    Flight* f = findFlight(b.flightID);

    for (auto &seat : seatsToCancel) {
        auto it = find(b.seatsBooked.begin(), b.seatsBooked.end(), seat);
        if (it != b.seatsBooked.end()) {
            b.seatsBooked.erase(it);
            seatsCancelledCount++;

            // Increase availability in flight if flight found
            if (f) {
                switch (b.seatClass) {
                    case 'F': f->seatsFirstAvailable++; break;
                    case 'B': f->seatsBusinessAvailable++; break;
                    case 'E': f->seatsEconomyAvailable++; break;
                }
            }
        } else {
            cout << "Seat " << seat << " not found in your booking.\n";
        }
    }

    if (seatsCancelledCount > 0) {
        // Recalculate total amount after cancellation
        double subtotal = b.pricePerSeat * b.seatsBooked.size();
        double discountAmt = subtotal * b.discountPercent / 100.0;
        b.totalAmount = static_cast<int>(subtotal - discountAmt);
    }

    if (b.seatsBooked.empty()) {
        // Remove booking entirely if no seats left
        bookings.erase(bookings.begin() + clientBookings[choice - 1]);
        cout << "All seats cancelled, booking removed.\n";
    } else {
        cout << "Selected seats cancelled.\n";
    }

    saveFlights();
    saveBookings();
}


// Helper function to print booking bill details
void printBookingBill(const Booking& b) {
    cout << "\n-------------------------------\n"
         << "          Booking Summary\n"
         << "-------------------------------\n";
    cout << "Client Name      : " << b.clientName << "\n";
    cout << "Flight ID        : " << b.flightID << "\n";
    cout << "Route            : " << b.origin << " --> " << b.destination << "\n";
    cout << "Date & Time      : " << b.date << " " << b.time << "\n\n";
    cout << "Class            : " << b.seatClass << "\n";
    cout << "Number of Seats  : " << b.seatsBooked.size() << "\n";
    cout << "Seat Numbers     : ";
    for (auto &s : b.seatsBooked) cout << s << " ";
    cout << "\n\n";

    cout << fixed << setprecision(2);
    double subtotal = b.pricePerSeat * b.seatsBooked.size();
    double discountAmt = subtotal * b.discountPercent / 100.0;
    double total = subtotal - discountAmt;

    cout << "Price per Seat   : $" << b.pricePerSeat << "\n";
    cout << "Discount Applied : " << b.discountPercent << "%\n";
    cout << "-------------------------------\n";
    cout << "Subtotal         : $" << subtotal << "\n";
    cout << "Discount Amount  : $" << discountAmt << "\n";
    cout << "-------------------------------\n";
    cout << "Total Amount     : $" << total << "\n\n";
    cout << "Thank you for booking with International Airlines!\n";
    cout << "-------------------------------\n";
}

void viewBill(const string& clientName) {
    vector<Booking*> clientBookings;
    for (auto &b : bookings) {
        if (b.clientName == clientName) {
            clientBookings.push_back(&b);
        }
    }

    if (clientBookings.empty()) {
        cout << "No bookings found.\n";
        return;
    }

    // If more than one booking, show brief summary and ask which one to view
    if (clientBookings.size() > 1) {
        cout << "Multiple bookings found:\n";
        for (size_t i = 0; i < clientBookings.size(); ++i) {
            Booking* b = clientBookings[i];
            cout << i+1 << ". Flight " << b->flightID << " on " << b->date << " " << b->time
                 << " (" << b->origin << " -> " << b->destination << "), Seats: " << b->seatsBooked.size() << "\n";
        }
        cout << "Enter the booking number to view details (or 0 to cancel): ";
        int choice;
        while (!(cin >> choice) || choice < 0 || choice > (int)clientBookings.size()) {
            cin.clear();
            cin.ignore(numeric_limits<streamsize>::max(), '\n');
            cout << "Invalid input. Enter a number between 0 and " << clientBookings.size() << ": ";
        }
        if (choice == 0) {
            cout << "Cancelled viewing bill.\n";
            return;
        }
        // Show selected booking details
        Booking* b = clientBookings[choice - 1];
        printBookingBill(*b);
    } else {
        // Only one booking, show directly
        printBookingBill(*clientBookings[0]);
    }
}


void deleteAccount(string username) {
    // Remove user
    users.erase(remove_if(users.begin(), users.end(),
        [&](const User& u){ return u.username == username; }), users.end());

    // Remove bookings
    bookings.erase(remove_if(bookings.begin(), bookings.end(),
        [&](const Booking& b){ return b.clientName == username; }), bookings.end());

    saveUsers();
    saveBookings();

    cout << "Account and all bookings deleted successfully.\n";
}

// -------------------- Menus --------------------

void adminMenu(User* admin) {
    while (true) {
        cout << "\nAdmin Menu:\n"
             << "1. View Flights\n"
             << "2. Add Flight\n"
             << "3. Delete Flight\n"
             << "4. Add Discount\n"
             << "5. Set Class Price\n"
             << "6. Approve Admins\n"
             << "7. View All Bookings\n"
             << "8. View Passengers on Flight\n"
             << "9. Search Booking by Client\n"
             << "10. Modify Flight Info\n"
             << "11. Logout\n"
             << "Choice: ";
        int ch;
        while (!(cin >> ch)) {
            cin.clear();
            cin.ignore(numeric_limits<streamsize>::max(), '\n');
            cout << "Invalid input, please enter a number: ";
        }
        switch (ch) {
            case 1: viewFlights(); break;
            case 2: addFlight(); break;
            case 3: deleteFlight(); break;
            case 4: addDiscount(); break;
            case 5: setClassPrice(); break;
            case 6: approveAdmins(); break;
            case 7: viewAllBookings(); break;
            case 8: viewPassengersOnFlight(); break;
            case 9: searchBookingByClient(); break;
            case 10: modifyFlight(); break;
            case 11: return;
            default: cout << "Invalid choice.\n";
        }
    }
}

void clientMenu(User* client) {
    while (true) {
        cout << "\nClient Menu:\n"
             << "1. View Flights\n"
             << "2. Filter Flights\n"
             << "3. View Prices\n"
             << "4. Book Seat\n"
             << "5. Cancel Seat\n"
             << "6. View Bill\n"
             << "7. View Seat Layout\n"
             << "8. Delete Account\n"
             << "9. Logout\n"
             << "Choice: ";
        int ch;
        while (!(cin >> ch)) {
            cin.clear();
            cin.ignore(numeric_limits<streamsize>::max(), '\n');
            cout << "Invalid input, please enter a number: ";
        }

        switch (ch) {
            case 1: viewFlights(); break;
            case 2: filterFlights(); break;
            case 3: viewPrices(); break;
            case 4: bookSeat(client->username); break;
            case 5: cancelSeat(client->username); break;
            case 6: viewBill(client->username); break;
            case 7: {
                string flightID; char seatClass;
                cout << "Enter Flight ID: "; cin >> flightID;
                Flight* f = getFlightByID(flightID);
                if (!f) { cout << "Flight not found.\n"; break; }
                cout << "Enter class (F/B/E): "; cin >> seatClass; seatClass = toupper(seatClass);

                vector<string> allSeats = getAllSeats(*f, seatClass);
                vector<string> bookedSeats = getBookedSeats(flightID, seatClass);
                char columns[] = {'A', 'B', 'C', 'D', 'E', 'F'};
                int seatsPerRow = 6;
                int rows = (allSeats.size() + seatsPerRow - 1) / seatsPerRow;

                cout << "\nAvailable seats in class " << seatClass << ":\n";
                for (int row = 1; row <= rows; row++) {
                    for (char col : columns) {
                        string seat = to_string(row) + col;
                        if (find(allSeats.begin(), allSeats.end(), seat) != allSeats.end()) {
                            if (find(bookedSeats.begin(), bookedSeats.end(), seat) != bookedSeats.end())
                                cout << "[X] ";
                            else
                                cout << seat << " ";
                        }
                    }
                    cout << "\n";
                }
                break;
            }
            case 8: {
                cout << "Are you sure you want to delete your account? (y/n): ";
                char c; cin >> c;
                cin.ignore(numeric_limits<streamsize>::max(), '\n');
                if (c == 'y' || c == 'Y') {
                    deleteAccount(client->username);
                    return;
                }
                break;
            }
            case 9: return;
            default: cout << "Invalid choice.\n";
        }
    }
}

// -------------------- Main --------------------

int main() {
    loadUsers();
    loadFlights();
    loadBookings();

    while (true) {
        cout << "\n*** International Airline Management System ***\n"
             << "1. Login\n"
             << "2. Signup\n"
             << "3. Exit\n"
             << "Choice: ";
        int choice; cin >> choice;
        if (choice == 1) {
            User* user = login();
            if (!user) continue;
            if (user->role == "admin") {
                adminMenu(user);
            } else if (user->role == "client") {
                clientMenu(user);
            }
        } else if (choice == 2) {
            signup();
        } else if (choice == 3) {
            cout << "Exiting system. Goodbye!\n";
            break;
        } else {
            cout << "Invalid choice.\n";
        }
    }
    return 0;
}

