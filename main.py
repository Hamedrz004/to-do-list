import csv 

class  task():
    def __init__(self,name,descr,prio):
        self.name=name
        self.descr=descr
        self.prio=prio
    def change_prio(self, newprio):
        self.prio=newprio
    def __str__(self):
        return f"{"**"if self.prio==1 else "*" if self.prio==2 else ""}{self.name}: description: {self.descr}"
    def __call__(self):
        return (self.name,self.descr,self.prio)
    
class tdlist():
    def __init__(self,name):
        self.name=name
        self.list=[]
    def load_from_csv(self,path):
        with open(path,"r", encoding="utf-8") as file:
            creader=csv.reader(file)
            for row in creader:
                if len(row) == 3 and str(row[2]).isdigit():
                    name, descr, prio = row
                    self.list.append(task(name, descr, int(prio)))
    def save_to_csv(self,path=None):
        if path==None:
            path=f"{self.name}.csv"
        with open(path,"w", encoding="utf-8") as file:
            cwriter=csv.writer(file)
            cwriter.writerows([t() for t in self.list])
    def __str__(self):
        if len(self.list) == 0:
            return f"{self.name} is empty"
        else:
            sl=[]
            c=1
            for task in self.list:
                sl.append(f"{c}- {task}")
                c+=1
            return f"{self.name}:\n" + "\n".join(sl)
    def __call__(self):
        return (self.name, [task() for task in self.list])
    def add_task(self, name, descr, prio):
        self.list.append(task(name, descr, prio))
    def remove_task(self, name):
        self.list = [i for i in self.list if i.name != name]
    def sortbyprio(self):
        self.list.sort(key=lambda x: x.prio)
    def tasks(self):
        return [task.name for task in self.list]

def menue():
    if aclist==None:
        print("\nno active list detected. create a list or import one to show it here.\n")
    else:
        print("\nactive list tasks:\n")
        print(f"{tlists[aclist]}\n")
        print("_____________________________________________________\n")

    print("1- create a new to-do list\n\n" \
    "2- import a list from a csv file\n\n" \
    "3- add an item to a list\n\n" \
    "4- remove an item from the list\n\n" \
    "5- export a list to a csv file\n\n" \
    "6- view all lists and change te active to-do list\n\n" \
    "7- sort the current active list by priority\n\n" \
    "8- exit\n")
    while True:
        finp= input("select an option (type the number from the menue and press ENTER): ")
        try:
            if int(finp) in (range(1,9)):
                return int(finp)
            else:
                print ("invalid input. try again.\n" \
                "you can only ENTER numbers between 1 to 8 in number format\n")
        except:
            print ("invalid input. try again.\n" \
            "you can only ENTER numbers between 1 to 8 in number format\n")

def createlist():
    finp=input("\nplease ENTER your to-do list name: ")
    global tlists
    global aclist
    tlists[finp]=tdlist(finp)
    print(f"{finp} created.")
    aclist=finp
    input("press ENTER to continue")


def importfromcsv():
    global aclist
    finp= input("\nenter the list name you want csv data imported to\n" \
    "or type a new name to have it imported to a fresh list\n" \
    "or leave it empty to import to the current active list: ")
    if finp in tlists.keys():
        tlists[finp]=tdlist(finp)
        aclist= finp
        print(f"{finp} list got activated")
    elif( finp=="" and aclist!=None):
        print(f"adding to current active list: {aclist}\n")
    elif finp=="" and aclist==None:
        print("no active list detected. creating a new list.")
        finp=input("\nplease ENTER a name for the new list: ")
        tlists[finp]=tdlist(finp)
        aclist=finp
        print(f"{finp} created and activated\n")
    else:
        tlists[finp]=tdlist(finp)
        aclist= finp
        print(f"a new list created and got activated\n")
    while True:
        finp=input("type the path of your csv file: ")
        try:
            tlists[aclist].load_from_csv(finp)
            break
        except FileNotFoundError:
            print("file not found. try again.\n" \
            "make sure the file exists and you entered the correct path")
    print("imported successfully")
    input("press ENTER to continue")



def addtolist():
    finp1= input("\nenter a task: ")
    finp2= input("\nenter a description for the task: ")
    while True:
        try:
            finp3= input("\nplease ENTER priority of the task (1, 2 or 3): ")
            if int(finp3) in (range(1,4)):
                finp3= int(finp3)
                break
            else:
                print ("invalid input. try again.\n" \
                "you can only ENTER one of the numbers 1, 2 or 3 in number format")
        except:
            print ("invalid input. try again.\n" \
            "you can only ENTER one of the numbers 1, 2 or 3 in number format")
    tlists[aclist].add_task(finp1,finp2,finp3)
    print("added succesfully")
    input("press ENTER to continue")

def removefromlist():
    print(f"tasks in current active list:")
    c=1
    for task in tlists[aclist].tasks():
        print(f"{c}- {task}")
        c+=1
    while True:
        finp= input("\nselect a task from the list above to remove(ENTER the number next to the task or ENTER 0 to cancel): ")
        try:
            if int(finp) in range(len(tlists[aclist].tasks())+1):
                finp= int(finp)
                break
            else:
                print ("invalid input. try again.\n" \
                "you can only ENTER the number of the task in the list")
        except:
            print ("invalid input. try again.\n" \
            "you can only ENTER the number of the task in the list")
    
    if finp==0:
        print("canceled")
        input("press ENTER to continue")
    else:
        tlists[aclist].remove_task(tlists[aclist].tasks()[finp-1])
        print("removed successfully")
        input("press ENTER to continue")

def savetocsv():
    print(f"active list: {aclist}")
    finp= input("\ntype the path to save your csv file to (leave empty for default): ")
    if finp=="":
        finp=f"{aclist}.csv"
    elif not ".csv" in finp:
        finp=f"{finp}.csv"
    tlists[aclist].save_to_csv(finp)
    print(f"saved to {finp} successfully")
    input("press ENTER to continue")

def viewlists():
    print("available lists:")
    c=1
    for i in tlists.keys():
        print(f"{c}- {i}")
        c+=1
    while True:
        finp= input("\ntype the number of the list you want to activate: ")
        try:
            if int(finp)-1 in range(len(tlists.keys())):
                finp= int(finp)
                break
            else:
                print ("invalid input. try again.\n" \
                "you can only ENTER the number of the list in the list")
        except:
            print ("invalid input. try again.\n" \
            "you can only ENTER the number of the list in the list")
    global aclist
    aclist= list(tlists.keys())[finp-1]
    print(f"{aclist} activated")
    input("press ENTER to continue")



tlists= dict()
aclist= None

def main():
    print("to-do list app")
    while True:
        inp=menue()
        if aclist==None and not inp in (1,2,6,8):
            print ("no active list detected. create a list or import one first so you can do actions on it.")
            input("press ENTER to continue")
            continue
        if inp==1:
            createlist()
        if inp==2:
            importfromcsv()
        if inp==3:
            addtolist()
        if inp==4:
            removefromlist()
        if inp==5:
            savetocsv()
        if inp==6:
            viewlists()
        if inp==7:
            tlists[aclist].sortbyprio()
            print("sorted by priority successfully")
            input("press ENTER to continue")
        if inp==8:
            input("bye! press ENTER for the window to close")
            break

if __name__ == "__main__":
    main()
