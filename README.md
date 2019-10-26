# Clock_Tool
Clock Tool including Stopwatch, Timer and Alarm

# Open Main.py to run the app.
stopwatch.py - includes logic for stopwatch tab
timer.py - logic for timer part
alarm.py - main logic for alarm
         - database_connector.py has class for reading, editing and deleting data from database
         - data_class.py contains class for handling data from the database
         - mapping.py mapping the index to database fiels for better readability of alarm.py
database_alarm.db is the database for the app, Column (id) has Primary Key Autoincrement, Column (name) Not Null, Column (time) Not Null, Column (repeats) Default '0'.
