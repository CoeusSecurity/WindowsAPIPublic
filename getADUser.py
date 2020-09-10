import subprocess as sp
from datetime import datetime, date

#queries the AD using the subprocess module and Powershell to retreive the list of AD Users,
#formats it in a readable python object and returns it as a JSON compatible list of dictionaries
def getADUserAll():
    pr = sp.Popen(["powershell.exe","get-ADUser -Filter *"],stdout=sp.PIPE)

    ad_users = []
    count_r = 0
    idx = 0
    prev = None
    while True:
        output = pr.stdout.readline().decode("utf-8")
        if prev == '' and output == '':
            count_r = count_r + 1
        else:
            count_r = 0
        if count_r > 3:
            break
        if output == "" and pr.poll() is not None:
            break
        if output:
            if output != '':
                if idx == 0:
                    idx = 1
                    data = {}
                if output.find(":") > -1:
                    idx = idx + 1
                    parts = output.split(":")
                    data[parts[0].replace(" ","")] = parts[1].replace(" ","").replace('\r','').replace('\n','')
        if idx == 11:
            ad_users.append(data)
            idx = 0
        prev = output
        
        rc = pr.poll()

    return ad_users

#queries the AD using the subprocess module and Powershell to retreive the list of AD Admins,
#formats it in a readable python object and returns it as a JSON compatible list of dictionaries
def getADAdminPrincipalGroupMembership():
    pr = sp.Popen(["powershell.exe","Get-ADPrincipalGroupMembership -Identity Administrator"],stdout=sp.PIPE)

    ad_users = []
    count_r = 0
    idx = 0
    prev = None
    while True:
        output = pr.stdout.readline().decode("utf-8")
        if prev == '' and output == '':
            count_r = count_r + 1
        else:
            count_r = 0
        if count_r > 3:
            break
        if output == "" and pr.poll() is not None:
            break
        if output:
            if output != '':
                if idx == 0:
                    idx = 1
                    data = {}
                if output.find(":") > -1:
                    idx = idx + 1
                    parts = output.split(":")
                    data[parts[0].replace(" ","")] = parts[1].replace(" ","").replace('\r','').replace('\n','')
        if idx == 9:
            ad_users.append(data)
            idx = 0
        prev = output
        
        rc = pr.poll()

    return ad_users

def str_empty(out_str):
    for i in out_str:
        if i != ' ':
            return False
    return True

#queries the AD using the subprocess module and Powershell to retreive the password expiry and SID of all users,
#formats it in a readable python object and returns it as a JSON compatible list of dictionaries

#Get-ADUser -filter {Enabled -eq $True -and PasswordNeverExpires -eq $False} –Properties "DisplayName", "SID", "msDS-UserPasswordExpiryTimeComputed" | Select-Object -Property "Displayname", "SID",@{Name="ExpiryDate";Expression={[datetime]::FromFileTime($_."msDS-UserPasswordExpiryTimeComputed")}}
def getAllUserPwdExpiryDate():
    pr = sp.Popen(["powershell.exe",
                   'Get-ADUser -filter {PasswordNeverExpires -eq $True -or PasswordNeverExpires -eq $False} –Properties "SID", "msDS-UserPasswordExpiryTimeComputed" | Select-Object -Property "SID",@{Name="ExpiryDate";Expression={[datetime]::FromFileTime($_."msDS-UserPasswordExpiryTimeComputed")}}'],
                  stdout=sp.PIPE)
    idx = 0
    sep_index = -1
    count_r = 0
    user_expiry = {}
    prev = None
    while True:
        output = pr.stdout.readline().decode("utf-8")
        if prev == '' and output == '':
            count_r = count_r + 1
        else:
            count_r = 0
        if count_r > 10:
            break
        if idx == 1:
            sep_index = output.find("ExpiryDate")
        elif idx >= 3:
            if output != '':
                name = output[:sep_index].replace('\r','').replace('\n','')
                expiry = output[sep_index:].replace('\r','').replace('\n','')
                if not str_empty(expiry) and name != '':
                    date_obj = datetime.strptime(expiry,"%m/%d/%Y %H:%M:%S %p")
                    date_str = datetime.strftime(date_obj,"%Y-%m-%d %H:%M:%S")
                    user_expiry[name] = date_str
                elif name != "":
                    user_expiry[name] = None
        prev = output

        rc = pr.poll()
        idx = idx + 1
        
    return user_expiry

            
