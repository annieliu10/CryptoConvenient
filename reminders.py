from flask import Flask
from flask import jsonify
from flask import abort 
from flask import make_response
from flask import request

reminder= Flask(__name__)


## items with the same categ id belong to the same category 
## the unique id is the unique identifier 
reminders = [
{
'categ': 1,
'id': 1,
'title': "Trade the coin",
'description': "Trade BTC",
'completed' : False
},
{
'categ': 2,
'id': 2,
'title': "Buy the coin",
'description': "Buy BTC",
'completed': False
},

{
'categ': 2,
'id': 3,
'title': "Buy the coin",
'description': "Buy LINK",
'completed': False 
}
]



@reminder.route('/reminder/api/v1.0/reminders', methods = ['GET'])
def get_reminders():
    return jsonify({'reminders': reminders})


## get reminders that have the same id//category 
@reminder.route('/reminder/api/v1.0/reminders/<int:reminders_categ>', methods = ['GET'])
def get_specific_reminders(reminders_categ):
    ## only keep the tasks that have the associated id 
    specificreminders = filter(lambda reminder: reminder['categ'] == reminders_categ, reminders)
    if(len(specificreminders)==0):
        abort(404)
    return jsonify({'specific reminders': specificreminders})



@reminder.route('/reminder/api/v1.0/reminders/<int:reminders_id>', methods = ['GET'])
def get_specific_reminder(reminders_id):
    specificreminder = {}
    for each_reminder in reminders:
        if(each_reminder['id']== reminders_id):
            return jsonify({'specific reminder': specificreminder})

    abort(404)


@reminder.route('/reminder/api/v1.0/reminders', methods=['POST'])
def make_new_reminder():
    #request.json has the requested data 
    if not request.json or not 'title' in request.json or not 'categ' in request.json:
        abort(400)
    reminder = {
        'categ': request.json['categ'],
        'id': reminders[-1]['id']+1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'completed': False
    }
    reminders.append(reminder)
    return jsonify({'reminders': reminders}), 201


@reminder.route('/reminder/api/v1.0/reminders/<int:reminders_id>', methods = ['DELETE'])
def delete_specific_reminder(reminders_id):
    saveitem= 0
    for each_reminder in reminders:
        if each_reminder['id']== reminders_id:
            saveitem = reminders.index(each_reminder)

    reminders.remove(reminders[saveitem])
    return jsonify({'reminders': reminders})


@reminder.route('/reminder/api/v1.0/reminders/<int:reminders_categ>', methods = ['DELETE'])
def delete_categ(reminders_categ):
    tempList = []
    for ele in reminders:
        if ele['categ']== reminders_categ:
            tempList.append(reminders.index(ele))

    for each_ele in tempList:
        reminders.remove(reminders[each_ele])

    return jsonify({'reminders': reminders})


@reminder.route('/reminder/api/v1.0/reminders/<int:reminders_id>', methods = ['PUT'])
def update_reminder(reminders_id):
    



@reminder.errorhandler(404)
def notfound(error):
    return make_response(jsonify({'error': "Not found oop"}), 404)



if __name__ == "__main__":
    reminder.run(debug=True)



