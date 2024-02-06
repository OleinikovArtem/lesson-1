### Virtual Env

```python3
# create virtual env 
python3 -m venv myprojectenv

# activation
source myprojectenv/bin/activate
```

## Ticket 2: Database Setup for Utility Readings

### Description

- Create a SQLite database to store user addresses and their utility readings.

### Requirements

- Define the database schema for addresses and readings.
- Implement database initialization in the bot.

### Tech Requirements

- SQLite3 for database management.
- Python for scripting database setup.

### Acceptance Criteria

- SQLite database is initialized with tables for addresses and readings.
- Bot can successfully connect to and interact with the database.

---

## Ticket 3: Implement Add Address Command

### Description

- Allow users to add a new address with initial utility readings.

### Requirements

- Implement `/add_address` command in the bot.
- Capture user input for address and initial readings.
- Store the new address and readings in the database.

### Tech Requirements

- `python-telegram-bot` library for command handling.
- Validation for user input.

### Acceptance Criteria

- Users can add a new address with initial readings via the `/add_address` command.
- New address and readings are stored in the database.

---

## Ticket 4: Implement Update Readings Command

### Description

- Enable users to update utility readings for an existing address.

### Requirements

- Implement `/update_readings` command.
- Allow users to select an address and enter new readings.
- Update readings in the database and calculate differences from the previous entry.

### Tech Requirements

- Interface for selecting an address.
- Mechanism for calculating reading differences.

### Acceptance Criteria

- Users can update readings for an address.
- Database is updated with new readings, and differences are calculated.

---

## Ticket 5: Implement Viewing History and Analytics Commands

### Description

- Provide users with the ability to view their reading history and consumption analytics.

### Requirements

- Implement `/history` command to show reading history.
- Implement `/analytics` command to show consumption analytics.
- Retrieve data from the database and present it to the user.

### Tech Requirements

- Algorithms for calculating analytics (average consumption, trends, etc.).
- User-friendly presentation of data.

### Acceptance Criteria

- Users can view their reading history and analytics through respective commands.
- Data presented is accurate and easy to understand.

---

## Ticket 6: Testing and Deployment

### Description

- Conduct thorough testing of the bot and deploy it to a live environment.

### Requirements

- Test all bot functionalities.
- Deploy the bot to a server or cloud platform.

### Tech Requirements

- Testing framework compatible with Python.
- Deployment platform (e.g., Heroku, AWS).

### Acceptance Criteria

- All bot functionalities work as expected with no critical bugs.
- Bot is successfully deployed and accessible to users.

---

## Database Schema

### Addresses Table

- `ID` (Primary Key)
- `Address` (Text)
- `UserID` (Text, Foreign Key to Users Table if needed)

### Readings Table

- `ID` (Primary Key)
- `AddressID` (Integer, Foreign Key to Addresses Table)
- `ReadingDate` (Date)
- `Water` (Integer)
- `Electricity` (Integer)
- `Gas` (Integer)

This schema supports storing multiple addresses per user and tracking different utility readings by date for each address. Adjustments can be made based on specific requirements or additional features.
