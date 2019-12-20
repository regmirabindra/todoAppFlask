from flask import Flask, redirect, url_for,flash,render_template,request
from flask_pymongo import PyMongo
from forms import InsertForm
from bson.objectid import ObjectId


app = Flask(__name__)

#SECRET KEY IS REQUIRED FOR SECURITY PURPOSE
app.config['SECRET_KEY'] = "fhskudhfksdbfkjsdf"

'''
THIS LINE TELLS OUR APP WHERE TO FIND MONGO DATABASE IN THE SERVER
IN OUR CASE, IT'S LOCATED IN localhost server in port no 27017
 you can give any name to the database, here if todoDatabase is already in the connection it will use that database otherwise
it will create one and use that'''
app.config["MONGO_URI"] = "mongodb://localhost:27017/todoDatabase"

#This line is to initialize our app with mongo server
mongo = PyMongo(app)

#We created two collections for our project, one for to store completed task and another for incomplete
comp_collec =mongo.db.complete_collection
incomp_collec = mongo.db.incomplete_collection

#app.route is decorator, whenever this route is requested, this method will be executed.
#METHOD PARAMETER IS USED TO ALLOW BOTH GET AND POST REQUEST, OTHERWISE GET IS IN BY DEFAULT.
@app.route('/', methods = ['GET', 'POST'])
def index():
    form = InsertForm() #created object of class InsertForm
    if form.validate_on_submit(): # this will return true iff form is validate for eg CSRF token.
        flash(f'New Data inserted', 'sucess') #Flash is used to send message to next immediate request.
        newDict = {}
        newDict['title'] = form.title.data #form.title.data gives the value of title field in the form
        newDict['Description'] = form.description.data
        incomp_collec.insert_one(newDict) #insert_one function is used here to insert that item in the database
        return redirect('/')   #redirect method is to redirect to that route, in this case this method redirect to the index page.
        #parameter of redirect is always route. We can also use url_for() method in which we give function name instead of route name.
    return render_template('index.html', title='Insert', form=form, incomp_collec = incomp_collec.find(), comp_collec =
                           comp_collec.find())
    '''render_template method is used to render html file to the browser, first parameter of render_template is html file and other pa
    parameter should be given as key-value pair. Key is used in JINJA to access that certain value'''


#Complete method is used to mark incomplete task as completed. <el> is route parameter, value of which should be passed when calling this route
@app.route ('/complete/<el>')
def complete(el):
    el = ObjectId(el) #'el' is variable name so can be named anything, and also since it gives item id, first it should be converted to ObjectId
    itemToUpdate = incomp_collec.find_one ({"_id":el}) #Find_one method returns specific element, in this case we are concerned with finding certain element to move that in completed list
    incomp_collec.delete_one({"_id": el}) # Since we are moving that item to completed list, we should remove that item from incomplete list.

    comp_collec.insert_one(itemToUpdate) # Now that item is inserted to completed list
    return redirect(url_for('index'))

@app.route('/update/<el>', methods = ['GET', 'POST'])
def update(el):
    el = ObjectId(el)
    form = InsertForm()
    itemToUpdate = incomp_collec.find_one({"_id":el}) #Unlike insert, we should populate form first if we want to update certain item so here we are retriving that element
    #from database to populate form field
    if form.validate_on_submit():
        newDict = {}
        newDict ['title'] = form.title.data
        newDict ['Description'] = form.description.data
        print(newDict)
        incomp_collec.update_one(itemToUpdate, {"$set": newDict}) #Parameter of update_one function should be object that need to be uodated and dictionary of form {'$set':<Insert here new Data That is Updated as a dictionary>}
        return redirect('/')
    #following two line is used to populate form field
    form.title.data = itemToUpdate['title']
    form.description.data = itemToUpdate['Description']
    return render_template('index.html', form= form)

if __name__ =='__main__':
    app.run(debug=True)


