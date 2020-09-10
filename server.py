from flask import Flask, request, redirect, url_for
from flask_cors import CORS
import json
import getADUser as g

app = Flask(__name__)
cors = CORS(app)

@app.route('/')
def hello_world():
    return 'Welcome to PAM Tool API'

#calls the getADUserAll() method from getADUser.py and returns the list of All AD Users as a JSON Object
@app.route("/getAllADUsers")
def get_all_users():
    data = json.dumps(g.getADUserAll(),indent=1)
    return data

#calls the getADAdminPrincipalGroupMembership() method from getADUser.py and returns the list of All AD Admins as a JSON Object
@app.route("/getPrincipalGroupMembership/admin")
def get_admin_principal_mem():
    data = json.dumps(g.getADAdminPrincipalGroupMembership(),indent=1)
    return data

#calls the getAllUserPwdExpiryDate() method from getADUser.py and return the SID and password expiry date for each user a json object
@app.route("/getPwdExpiry/All")
def get_pwd_expiry_all():
    data = json.dumps(g.getAllUserPwdExpiryDate(),indent=1)
    return data

#starts the server on port 80 and accepts requests from all requesting IP Addreses
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=80)
