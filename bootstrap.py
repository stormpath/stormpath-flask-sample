"""
    bootstrap.py
    ~~~~~~~~~~~~

    This simple command line script will 'bootstrap' this simple Flask
    application by performing a few simple tasks:

    - It will collect your Stormpath credentials from you (via the command
      line).
    - It will create a new Stormpath Application in your account named
      'flask-stormpath-sample' (so that we can run this project).

    - It will create a `.env` file in this directory which holds 3 environment
      variables needed for this sample application to run successfully.

    - Lastly, it will tell you how to run this website!
"""


from stormpath.client import Client


print """
Hi, and welcome to the flask-stormpath-sample bootstrap app!

I'll help get you up and running in no time!  If you don't already have a
Stormpath account, please create one: https://api.stormpath.com/register

Once you've made an account, be sure to create an API keypair in your
dashboard, and download your credentials.  You'll need these to continue.
"""

id = None
while not id:
    id = raw_input('To get started, please enter your Stormpath API Key ID: ')

secret = None
while not secret:
    secret = raw_input('Please enter your Stormpath API Key Secret: ')


client = Client(id=id, secret=secret)
try:
    client.applications.create({
        'name': 'flask-stormpath-sample',
        'description': 'A sample application required to run the flask-stormpath-sample application.  Feel free to delete this!',
    }, create_directory=True)
    print """\n
I've just created a new Stormpath application in your account named:
flask-stormpath-sample, when you're done using this sample application, feel
free to delete this!
"""
except:
    pass

env_file = open('.env', 'wb')
env_file.write('export STORMPATH_API_KEY_ID=%s\n' % id)
env_file.write('export STORMPATH_API_KEY_SECRET=%s\n' % secret)
env_file.write('export STORMPATH_APPLICATION=flask-stormpath-sample\n')
env_file.close()

print """I've just created a new file in this directory named .env

This file contains all of the necessary environment variables to make this
sample application run!

Now that we've completed all bootstrapping stuff, all you need to do to get
your sample application running is to execute the following commands:

    $ source .env
    $ python app.py

You should then be able to visit 'http://localhost:5000' in your browser to
play around with the sample application!

Have questions?  Email us!  support@stormpath.com
"""
