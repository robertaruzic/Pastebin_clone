# Used for generating the slug (document ID)
import random
import string
# Backend used for database (similar to Firebase)
from appwrite.client import Client
from appwrite.services.databases import Databases
# Used for hosting the website
from flask import Flask, render_template, redirect
from flask import request
import consts  # Import secret keys

# Initiate Flask app
app = Flask(__name__)

# Initiate Appwrite connection
client = Client()
client.set_endpoint(consts.endpoint).set_project(consts.project_id).set_key(consts.api_key)

# Initiate Appwrite database connection
database = Databases(client)


@app.route("/", methods=['POST', 'GET'])
def home():
    # Checks if the page made a POST request, sent the data, or is just being loaded
    if request.method == 'POST':
        # If sent data, get the data generate the slug and create the database document with it
        content = request.form['content']
        name = request.form['name']
        slug = ''.join(random.choices(string.ascii_lowercase + string.digits, k=32))
        database.create_document('6468e7dc3aa954467ee7', '6468e7e214c71e1ed2f6', slug,
                                 dict(content=content, name=name))
        return redirect(f'/paste/{slug}')

    # If first load just render the website
    return render_template('home.html')


@app.route("/pastelist")
def pastelist():
    # Gets all pastes from database and cleans them up in a form of a list
    documents = [[document['name'], document['content'], document['$id']]
                 for document in database.list_documents('6468e7dc3aa954467ee7', '6468e7e214c71e1ed2f6')['documents']]
    return render_template('pastelist.html', documents=documents)


@app.route("/paste/<paste_slug>")
def paste(paste_slug):
    # Loads paste based on provided slug that is also the document id
    result = database.get_document('6468e7dc3aa954467ee7', '6468e7e214c71e1ed2f6', paste_slug)
    return render_template('paste.html', name=result['name'], content=result['content'], slug=paste_slug)


@app.route("/remove/<slug>")
def remove(slug):
    # Gets all pastes from database and cleans them up in a form of a list
    database.delete_document('6468e7dc3aa954467ee7', '6468e7e214c71e1ed2f6', slug)
    return redirect('/')


@app.errorhandler(404)
def page_not_found():
    return redirect('/')


if __name__ == '__main__':
    # Sets the host and the port on which the website will be running
    app.run(debug=False, host="0.0.0.0", port=8010)
