from flask import Flask, jsonify, abort, make_response, url_for, request
from flask_httpauth import HTTPBasicAuth


reminder= Flask(__name__)
## setting up an authentication

auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
    if username == 'annie':
        return "LYT20010102"
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)


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
@auth.login_required
def get_reminders():
    tempList = []
    for each in reminders:
        tempList.append(make_public_reminder(each))  
    return jsonify({'reminders': tempList})


def make_public_reminder(reminder):
    newreminder={}
    for field in reminder:
        if field == 'id':
            newreminder['uri']= url_for('get_specific_reminder', reminders_id=reminder['id'], _external=True)
        else:
            newreminder[field] = reminder[field]
    return newreminder




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

    for each_reminder in reminders:
        if(each_reminder['id']== reminders_id):
            return jsonify({'specific reminder': each_reminder['id']})

    abort(404)


@reminder.route('/reminder/api/v1.0/reminders', methods=['POST'])
def make_new_reminder():
    #request.json has the requested data 
    if not request.json or not 'title' in request.json and not 'categ' in request.json:
        abort(400)
    reminder = {
        'categ': request.json['categ'],
        'id': reminders[-1]['id']+1,
        'title': request.json['title'],
        ## second argument in the description: what you would replace it with if there isn't a description
        'description': request.json.get('description', ""),
        'completed': False
    }
    reminders.append(reminder)
    return jsonify({'reminder': reminder}), 201


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
    theone = {}
    for each_ele in reminders:
        if each_ele['id']== reminders_id:
            theone = each_ele
    if not request.json:
        abort(400)
        ## when "title" is in the json data but its value is not in string 
    if 'title' in request.json and type(request.json['title']) is not str:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not str:
        abort(400)
    if 'completed' in request.json and type(request.json['completed']) is not bool:
        abort (400)
    if 'categ' in request.json and type(request.json['categ']) is not int:
        abort (400)


    ##change it, or default 
    theone['title']=  request.json.get('title', theone['title'])
    theone['description']= request.json.get('description', theone['description'])
    theone['completed']= request.json.get('completed', theone['completed'])
    theone['categ'] = request.json.get('categ', theone['completed'])
    return jsonify({'reminder': theone})

@reminder.errorhandler(404)
def notfound(error):
    return make_response(jsonify({'error': "Not found oop"}), 404)


@reminder.errorhandler(400)
def notworking(error):
    return make_response(jsonify({'error': "Not working"}), 400)


if __name__ == "__main__":
    reminder.run(debug=True)






