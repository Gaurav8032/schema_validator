
Assumptions - 1
We have a moving inout.json file which has list of all the events coming from application (name & empname are two events lets assume that)
e.x - 
{"name": "jane doe", "rollnumber": 25, "marks": 72}
{"empname": "jane doe", "rollnumber": 25, "marks": 72}

All events are present at each new line.

Assumption - 2
we have a schema csv file which contains a uniqueidentifier and points to valid schema defintioen for each event. 
e.x - 
studentSchema|{"type": "object","properties": {"name": {"type": "string"},"rollnumber": {"type": "number"},"marks": {"type": "number"}}}
empSchema|{"type": "object","properties": {"empname": {"type": "string"},"rollnumber": {"type": "number"},"marks": {"type": "number"}}}

Assumption - 3
-->due to memory constraints we can not read all schema.csv file in one go. 
-->hence we need to read limited events at a time

Approach - 
We build solution by using jsonschema library which helps us validate a schema against a valid input. 
We parse the exception and segregate relevant error message that we need. 
Create and specify locations of schema and error log file
Start reading input events file line by line as string, once a line is read - pass it to iterator func
Iterator func converts. string events to json using json.load
Search for unique key in event to understand what is the event type
Once identified - load relevant schema from schema file object. 
Now we have event, we know matching schema (or not) and all we need to do is validate these 
We use jsn schema validator and check it - if there are errors then log these in log else we move to next event line. 
