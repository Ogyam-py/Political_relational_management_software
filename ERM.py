# IMPORTS
import sqlite3
from datetime import datetime
from datetime import date
import time
import pickle

# PERRIFERALS
underline="\n==========================================================="; num=0
confirm=None; name=None; contact=None; hostel=None; room=None; status=None; note=None; followup=None #App_data={}
# FUNCTIONS
def slp(x=int):
    time.sleep(x)

def title(x=str):
    x=x.upper(); # clr()
    print(x,underline)

def clr():
    import os
    cmd='clear'
    if os.name in ('nt', 'dos'):
        cmd="cls"
    os.system(cmd)
def ln():
    print("")

# CRETING AND LOADING DATABASE
con=sqlite3.connect("ERM_DB.sqlite")
cur=con.cursor()

clr()
try:
    cur.execute("CREATE TABLE User (App_user text, Pass_key, Security_key, App_data)")
    title("sign up")
    user_name=input("Create new user name\n>>> "); ln()
    while True:
        pass_key=input("Create new password\n>>> "); ln()
        confirm_pass_key=input("Confirm your password\n>>> "); ln()
        if pass_key == confirm_pass_key:
            security_key=input("What is your favourite English word?\n>>> "); ln()
            break
        else:
            print("Oops! It appears that your password does not match.\nTry again..."); ln()
            continue

    pass_key=pickle.dumps(pass_key); security_key=pickle.dumps(security_key)
    cur.execute("INSERT INTO User (App_user, Pass_key, Security_key) VALUES (?,?,?)", (user_name, pass_key, security_key))
    # print("Sign up was successful...")
    cont=input("Sign up was successful...",underline,"\n\nPress ENTER "); ln()
    if len(cont)<1:
        slp(2); con.commit(); main_app=True
        cur.execute("CREATE TABLE Electorate_Info (Electorate text, Contact text, Hostel text, Room text)")
        cur.execute("CREATE TABLE Electorate_Data (Electorate text, E_status text, Note text (150), Followup float, Entry_date float)")
        App_data={}; user_table=[None,None]
    else:
        print("No detail was saved.\nApp will close shortly..."); ln()
        cur.execute("DROP TABLE IF EXITS User")
        slp(3); exit()

except:
    title("login")
    user_name=input("Enter your user name [Forgot]\n>>> "); ln()
    pass_key=input("Enter your password [Forgot]\n>>> "); ln()
    cur.execute("SELECT * FROM User")
    user_table=cur.fetchone()
    pass_key=pickle.dumps(pass_key); use_name=str(user_table[0])
    while True:
        if user_name == use_name and pass_key == user_table[1]:
            print("Login successful..."); slp(2)
            App_data=user_table[3];
            if App_data != None: App_data=pickle.loads(App_data)
            else: App_data={}
            main_app=True;
            break
        else:
            title("Error message"); print("Login was unsuccessful..."); slp(3); clr; main_app= False; break
            # security_key= row[2]; security_key=pickle.loads(security_key);
            # sec=input("Press ENTER if you have forgotten your password...[NO]\n>>> ")
            # if len(sec)<1:
            #     sec=input("What is your favourite word\n>>> ")
            #     if pickle.dumps(sec) == security_key:
            #         while True:
            #             pass_key=input("Create new password\n>>> ")
            #             confirm_pass_key=input("Confirm your password\n>>> ")
            #             if pass_key == confirm_pass_key:
            #                 security_key=input("What is your favourite English word? [ENTER]\n>>> ")
            #                 if len(security_key)<1:
            #                     security_key= row[2]
            #                 break
            #             else:
            #                 print("Oops! It appears that your password does not match.\nTry again...")
            #                 continue
            #     cur.execute("UPDATE User SET Pass_key=?, Security_key=? WHERE App_user=?",(pass_key, security_key, use_name))
            # elif sec.lower() == "no":
            #     continue



# APP FUNCTIONALITIES
while main_app:
    clr(); title("App functionalities")
    ask=input("Select one of the following options to proceed [LOGOUT]:\n1. Input Data\n2. View Data\n>>> "); ln()
    if ask == "logout": break
    elif ask in ["1","input data"]:
        edit=[1, 5, 6, 7]; app=True
        while app:
            clr(); title("Data collection")
            if 1 in edit:
                while True:
                    name=input("Electorate's name [ENTER]\n>>> "); ln() #1
                    name=name.upper()
                    if len(name)>18: print("The lenght of the name should not exceed 18 characters including the spaces between them."); ln(); continue
                    else: break
            if name == "DONE" or name== "D": app= False; break

            # PERSONAL INFO
            if confirm == None:
                if App_data.get(name) == None: edit=[1,2,3,4,5,6,7];

            if 2 in edit:
                while True:
                    contact=input("Provide electorate's contact\n>>> "); ln() #2
                    if len(contact)<10 and len(contact)>0:
                        print("The contact entered is insufficient.\nAtleast, there must be a 9 digit with a leading zero or country code."); ln()
                        continue
                    elif len(contact)<1:
                        contact="Unknown"; break
                    else: break
            
            if 3 in edit:
                hostel=input("Provide electorate's hostel name\n>>> "); ln() #3
                if len(hostel)<1:
                    room="Unknown"

            if 4 in edit:
                room=input("Provide the room name/number of the electorate\n>>> "); ln() #4
                if len(room)<1:
                    room="Unknown"

            # POLITICAL INFO
            if 5 in edit:
                while True:
                    status=input("What is the status of the electorate\n1. Lead\n2. Opportunity\n3. Vote\n>>> "); ln() #5
                    if status.lower() == "1" or status.lower() == "lead": status="lead"; break
                    elif status.lower() == "2" or status.lower() == "opportunity": status="opportunity"; break
                    elif status.lower() == "3" or status.lower() == "vote": status="vote"; break
                    elif len(status)<1: status="unknown"
                    else: print("You are required to specify the status of the electorate.\nType 1 or Lead when the electorate is new.\n Type 2 or Opportunity when the electorate is assumed to be a potential vote.\nType 3 or Vote when the probability of the Electorate voting for your candidate is high."); ln(); continue  
            
            if 6 in edit:
                while True:
                    note=input("Briefly discribe the relationship between you and the electorate\n>>> "); ln() #6
                    if len(note.split())>40:
                        print("Your sentence must be brief and not have more than 40 words."); ln()
                        continue
                    else:
                        break
            
            if 7 in edit:
                while True:
                    followup=input("When do you intend in making followup on the Electorate?\n[eg: 27/01/1998]\n>>> "); ln() #7
                    if len(followup) != len("27/01/1998") and len(followup)<1:
                        print("The date provded does not conform to our date format DD/MM/YYYY."); ln()
                        continue
                    elif len(followup)<1:
                        followup=0.0
                        break
                    else:
                        try:
                            check=followup.split("/")
                            for n in check: int(n)
                        except:
                            print("The date provided does not conform to our date format DD/MM/YYYY."); ln()
                            continue
                    # processing date and time
                    followup1=datetime.strptime(followup, "%d/%m/%Y"); followup1=followup1.strftime("%d %b, %Y")
                    day=date.today()
                    import datetime
                    str_day=day.strftime("%d/%m/%Y")
                    entry_date=time.mktime(datetime.datetime.strptime(str_day, "%d/%m/%Y").timetuple())
                    followup=time.mktime(datetime.datetime.strptime(followup, "%d/%m/%Y").timetuple())
                    break

            # PRE-VIEW SESSION
            clr(); title("Preview Details")
            print("Name:",name,"\nContact:", contact, "\nHostel", hostel, room, "\nStatus:", status, "\nNote:",note,"\nFollowup Date:",followup1); ln()
            # EDIT SESSION
            confirm=input("Press ENTER to proceed [EDIT/DELETE]\n>>> "); ln()
            if confirm.lower() == "edit":
                edit.clear()
                ask=input("Select all the parts you want to change\n1. Name\n2. Contact\n3. Hostel\n4. Room\n5. Status\n6. Notes\n7. Followup date\n>>> "); ln()
                if len(ask)>0:
                    for n in ask:
                        try:
                            edit.append(int(n))
                        except:
                            print("Type only the digits assigned to attributes.\n[ex: For 1. Name and 4. Room type: >>> 14"); ln()
                    continue
            elif confirm.lower() == "delete":
                print("Recently, entered details of", name, "has been deleted from the system"); ln(); continue
            else:
                edit=[1,5,6,7]; confirm=None
                if App_data.get(name) == None:
                    cur.execute("INSERT INTO Electorate_Info (Electorate, Contact, Hostel, Room) VALUES (?, ?, ?, ?)",(name, contact, hostel, room))
                    cur.execute("INSERT INTO Electorate_Data (Electorate, E_status, Note, Followup, Entry_date) VALUES (?,?,?,?,?)",(name, status, note, followup, entry_date))
                    con.commit()

                else:
                    cur.execute("UPDATE Electorate_Data SET E_status=?, Note=?, Followup=?, Entry_date=? WHERE Electorate=?",(status, note, followup, entry_date, name))
                    if contact != None:
                        cur.execute("UPDATE Electorate_info SET Contact=? WHERE electorate=?", (contact, name))
                    if hostel != None:
                        cur.execute("UPDATE Electorate_info SET Hostel=? WHERE electorate=?", (hostel, name))
                    if room != None:
                        cur.execute("UPDATE Electorate_info SET Room=? WHERE electorate=?", (room, name))
                    con.commit()
                App_data[name]=App_data.get(name, 0)+1; num+=1
                name=None; contact=None; hostel=None; room=None; status=None; note=None; followup1=None
                if num>=1:
                    App_data_transfer=pickle.dumps(App_data)
                    cur.execute("UPDATE User SET App_data=? WHERE App_user=?", (App_data_transfer, user_name))


    #  VIEWING DATA...
    elif ask in ["2","view data"]:
        while True:
            clr(); title("Data Browsing")
            if len(App_data)<1: print("Oops! There is no data to be viewed"); slp(3); break
            action=input("Select one of the following options to proceed:\n1. View Data\n2. Statistics\n3. Followup Schedule\n>>> "); ln()
            # search for name using their location...
            if action.lower() in ["1", "view data"]:
                clr(); title("Viewing Data")
                print("  NAME --------------- CONTACT ------------- LOCATION -------"); c=0; state=True
                for row in cur.execute("SELECT * FROM Electorate_info ORDER BY electorate"):
                    c+=1; i=19 - len(str(row[0])); j=19 - len(str(row[1]))
                    print(c, str(row[0]), " "*i, str(row[1])," "*j, str(row[2]), str(row[3]))
                ln()
                while state:
                    ask=input("Search for a general name, or part of a name or group of names [SPECIFIC]:\n>>> "); c=0; ln(); clr()
                    if ask.lower() != "specific" and ask.lower() != "done":
                        clr(); title("Search Results - [general mode]")
                        print("  NAME --------------- CONTACT ------------- LOCATION -----")
                        for row in cur.execute("SELECT * FROM Electorate_info ORDER BY electorate"):
                            if ask.upper() in str(row[0]):
                                c+=1; i=19 - len(str(row[0])); j=19 - len(str(row[1]))
                                print(c, str(row[0]), " "*i, str(row[1])," "*j, str(row[2]), str(row[3]))
                        ln()
                        if c == 0:
                            print("Oops! your search does not match any name or part of a name in the database"); ln(); slp(2)
                        
                    elif ask.lower() == "done": break
                    else:
                        clr(); title("Search results - [specific Mode]")
                        while True:
                            ask=input("Search for specific name in the database [GENERAL]:\n>>> "); c=0; ln()
                            if ask.lower() != "general" and ask.lower() != "done":
                                clr(); title("Search results - [specific Mode]")
                                print("  NAME --------------- CONTACT ------------- LOCATION -----")
                                for row in cur.execute("SELECT * FROM Electorate_info ORDER BY electorate"):
                                    if ask.upper() == str(row[0]):
                                        c+=1; i=19 - len(str(row[0])); j=19 - len(str(row[1]))
                                        print(c, str(row[0]), " "*i, str(row[1])," "*j, str(row[2]), str(row[3]))
                                ln()
                                if c == 0:
                                    print("Oops! your search does not match any full name in the database.\nCheck to see if the name you entered was spelt correctly."); ln()
                            elif ask.lower() == "done": state=False; break
                            else: break

            elif action.lower() in ["2","statistics"]:
                clr(); total=0; lead_count=0; opp_count=0; vote_count=0; count=0
                for row in cur.execute("SELECT E_status FROM Electorate_Data"):
                    if row[0] == "lead": lead_count+=1; total+=1
                    elif row[0] == "opportunity": opp_count+=1; total+=1
                    elif row[0] == "vote": vote_count+=1; total+=1
                    else: count+=1; total+=1
                # COMPUTATIONS
                lead_percent=round(lead_count/total, 2)
                opp_percent=round(opp_count/total, 2)
                vote_percent=round(vote_count/total, 2)
                # DISPLAY
                while True:
                    clr(); title("Data Analysis")
                    print("Category ---------------- Precent % [Number]")
                    print("Electorates              ", "100 %", "[{}]".format(total))
                    print("Lead                     ", lead_percent, "%", "[{}]".format(lead_count))
                    print("Opportunity              ", opp_percent, "%", "[{}]".format(opp_count))
                    print("Vote                     ", vote_percent, "%", "[{}]".format(vote_count))
                    ln()
                    title("ADVANCE ANALYSIS")
                    browse=input("Select an option to proceed [DONE]\n1. Detailed names under each category\n2. Number of inputs recorded per individual\n3. Input Data History\n>>> "); ln()
                    if browse == "1":
                        print("VOTE\n-------------------------"); c=0
                        for row in cur.execute("SELECT Electorate, E_status FROM Electorate_Data"):
                            stat=str(row[1]); x=str(row[0]); check=0
                            if stat == "vote":
                                i=" "*(19-len(x))
                                c+=1; mod=c%3; change=0
                                if mod == 0: # mod = 0, 1, 2
                                    change+=1
                                if change%2 == 0: # change = 0, 1
                                    print(c, x, end="{}".format(i))
                                else:
                                    print(c, end="{}\n".format(i))
                                # ln()
                        if c==0: print("Oops! No name found")

                        print("\nOPPORTUNITY\n-------------------------------------------------------"); c=0
                        for row in cur.execute("SELECT Electorate, E_status FROM Electorate_Data"):
                            stat=str(row[1]); x=str(row[0]); check=0
                            if stat == "opportunity":
                                check+=1
                                i=" "*(19-len(x))
                                c+=1; mod=c%3; change=0
                                if mod == 0: # mod = 0, 1, 2
                                    change+=1
                                if change%2 == 0: # change = 0, 1
                                    print(c, x, end="{}".format(i))
                                else:
                                    print(c, end="{}\n".format(i))
                                # ln()
                        if c==0: print("Oops! No name found")

                        print("\nLEAD\n------------------------------------------------------"); c=0
                        for row in cur.execute("SELECT Electorate, E_status FROM Electorate_Data"):
                            stat=str(row[1]); x=str(row[0])
                            if stat == "lead":
                                i=" "*(19-len(x))
                                c+=1; mod=c%3; change=0
                                if mod == 0: # mod = 0, 1, 2
                                    change+=1
                                if change%2 == 0: # change = 0, 1
                                    print(c, x, end="{}".format(i))
                                else:
                                    print(c, x, end="{}\n".format(i))
                                # ln()
                        if c==0: print("Oops! No name found")

                        c=0
                        for row in cur.execute("SELECT Electorate, E_status FROM Electorate_Data"):
                            stat=str(row[1]); x=str(row[0]); check=0
                            if stat == "unknown":
                                if check == 0:
                                    print("\nUNKNOWN\n-------------------------------------------------------")
                                check+=1
                                i=" "*(19-len(x))
                                c+=1; mod=c%3; change=0
                                if mod == 0: # mod = 0, 1, 2
                                    change+=1
                                if change%2 == 0: # change = 0, 1
                                    print(c, x, end="{}".format(i))
                                else:
                                    print(c, end="{}\n".format(i))
                                ln()
                            else: pass
                        ask=input("Press ENTER  to proceed... ")

                    elif browse == "2":
                        print("  NAME --------------------- Updates"); c=0
                        for key, val in App_data.items():
                            c+=1; i=" "*(19-len(key))
                            print(c, key, i, val)
                        ask=input("Press ENTER to proeceed... ")

                    elif browse == "3":
                        lst=[]; c=0; day=0
                        for row in cur.execute("SELECT Entry_date FROM Electorate_Data"):
                            row=row[0]
                            if row not in lst:
                                lst.append(row)
                        lst.sort( reverse=True)

                        for timer in lst:
                            lst.remove(timer); day+=1
                            from datetime import datetime
                            date=datetime.fromtimestamp(timer).strftime("%d %b %Y")
                            print("\n",date,"\n----------------------------------------")
                            for row in cur.execute("SELECT Electorate, E_status FROM Electorate_Data WHERE Entry_date=?", (timer,)):
                                n=row[0]; i="-"*(19-len(n)); c+=1
                                print(c, n, i, str(row[1]))
                            if day>7:
                                ask=input("Press Enter to see late history [ANY KEY]\n>>> ")
                                if len(ask)<1:
                                    for timer in lst:
                                        lst.remove(timer)
                                        date=datetime.fromtimestamp(timer).strftime("%d %m, %Y")
                                        print("\n",date,"\n----------------------------------------")
                                    for row in cur.execute("SELECT Electorate, E_status FROM Electorate_Data WHERE Entry_data=?", (timer,)):
                                        n=row[0]; i="-"*(19-len(n))
                                        print(c, n, i, str(row[1]))
                                else: break
                        wait=input("Press Enter to proceed... ")

                    elif browse.lower() == "done": break
                    
            elif action.lower() in ["3", "followup schedule"]:
                active=None
                while True:
                    if active == "1":
                        active="Active Followup"
                    elif active == "2":
                        active="Pending Followup"
                    elif active == "3":
                        active="Expired Followup"
                    else:
                        active="Active Followup"
                    clr(); title(active)
                    print("  NAME ----------------- CONTACT -------------- LOCATION ---------"); c=0
                    if active == "Active Followup":
                        for row in cur.execute("SELECT Electorate, Contact, Hostel, Room FROM Electorate_Info where Followup=?",(entry_date,)):
                            c+=1
                            print(c, str(row[0]), i, str(row[1]), j, str(row[2:4]))
                    if c<1: print("Oops! it looks like you have no followups today.")
                    active=input("Enter the fullname of an Electorate to view Updates")
                    # TO BE CONTINUED
                    pass
            elif action.lower() == "done": break
            else:
                print("Your input is not defined. Try again...[DONE]\n[ex: type 1 or view data and press enter to proceed]")
    else:
        clr(); title("Error message"); print("You have entered the wrong input\nType 1 for  Input Data\nType 2 to View Data\n[Else type logout to logout]"); slp(3)

# it was here

# LOGING OUT
while main_app:
    clr(); title("logout protocol initiated")
    out=input("Press enter to logout safely [RESET]\n>>> "); ln()
    if len(out)<1:
        title("Logout sucessful"); break
    elif out.lower() == "reset":
        pas=input("To proceed provide your user password\n>>> "); pas=pickle.dumps(pas); ln()
        if pas == user_table[1] or pas == pass_key:
            print("Reseting the App will result in the permanent deletion of data.\nThis includes user account information.\n>> Press ENTER to proceed\n>> Press ANY KEY to CANCEL")
            pas=input(">>> "); ln()
            if len(pas)<1:
                cur.execute("DROP TABLE IF EXISTS User"); cur.execute("DROP TABLE IF EXISTS Electorate_Info"); cur.execute("DROP TABLE IF EXISTS Electorate_Data")
                title("Reset sucessful");
                print("App would close shortly after\nI hope to see you around soon..."); break
            else:
                print("Reset process cancelled\nApp would close shortly after\nSee yea..."); break
    else:
        print("You made the wrong input. Try again...")
        continue
con.commit()
cur.close()
slp(3)