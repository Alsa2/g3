from flask import Flask, render_template, request, make_response, session
import os


STATIC_FOLDER = 'templates/assets'
app=Flask(__name__, static_folder=STATIC_FOLDER) #initiating flask object

@app.route("/",methods = ['GET'])
def index():
    return render_template('index.html')

@app.route("/submit",methods = ['GET', 'POST'])
def submit():
    if request.method == 'POST':
        #get the data from the form
        if request.form['code'] == '123':
            # save the file input to the server
            f = request.files['file']
            #remove old file
            os.remove('templates/assets/menu.png')
            #save the file with the name menu.png
            f.save('templates/assets/menu.png')
            return render_template('index.html', message='File uploaded successfully')
        else:
            return render_template('index.html', message='Invalid code')

    else:
        return render_template('file_sumbission.html')



if __name__ == "__main__":
    app.debug=True #setting the debugging option for the application instance
    app.run(host='0.0.0.0', port=80) #launching the flask's integrated development webserver