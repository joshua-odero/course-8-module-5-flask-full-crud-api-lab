#Initialize Flask app
from flask import Flask, jsonify, request

app = Flask(__name__)

#Simulated data
#in-memory object called EVENT is used to simulate the database
class Event:
    #instanciate object attributes
    def __init__(self, id, title):
        self.id = id
        self.title = title

    #instance method to convert object to a dictionary
    def to_dict(self):
        return {"id": self.id, "title": self.title}

# In-memory "database"
events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]

# Create a new event from JSON input
@app.route("/events", methods=["POST"])
def create_event():
    #Handle incoming JSON data with request.get_json()
    incoming_data = request.get_json()

    #if the list exists, find the maximum id in the list and increment the new id by 1
    #if the list does not exist, the new id is just 1
    new_id = max([event.id for event in events]) + 1 if events else 1

    #create new event => it is an object instance
    new_event = Event(id=new_id,title=incoming_data["title"])

    #Append the new event to the existing list
    events.append(new_event)

    #return a JSON and appropriate HTTP status code
    return jsonify(new_event.to_dict()),201


# Update the title of an existing event
@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    #Handle incoming JSON data with request.get_json()
    incoming_data = request.get_json()

    #Determine the event to be updated in the events list
    event_to_update = next((event for event in events if event.id == event_id), None)

    #if the event is not in the events list, return an error => HTTP STATUS 404
    if not event_to_update:
        return ("Event not found", 404)

    #ELSE: EVENT IS IN THE EVENT LIST
    #check if title key is in the incoming data
    #if the title key is in the incoming data, update the event title with a specific ID
    if "title" in incoming_data:
        event_to_update.title = incoming_data["title"]
    
    #return the updated event in form of JSON
    return jsonify(event_to_update.to_dict())



# Remove an event from the list
@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):

    #declare the events list above as a global variable => to be used inside delete_event function
    global events

    #Determine the event to be deleted in the events list
    event_to_delete = next((event for event in events if event.id == event_id), None)

    #if the event is not in the events list, return an error => HTTP STATUS 404
    if not event_to_delete:
        return ("Event not found", 404)
    
    #ELSE: EVENT IS IN THE EVENT LIST
    #Now,return all events without the specified ID
    events = [event for event in events if event.id != event_id]

    #return a message that an event has been deleted => HTTP STATUS 204
    return ("Event deleted", 204)


# Auto-run script with 'python app.py' command
if __name__ == "__main__":
    app.run(debug=True)
