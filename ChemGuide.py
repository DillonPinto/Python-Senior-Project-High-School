#Disclaimer: This program and it's name does not intentionally bear likness to any other
#            application or product. Any likeness to another program or product is
#            coincidental.


#Import everything from the peewee module for the database.
#This module will be used to make tables to store user data in.
from peewee import *

#Used to generate random integers for algorithms used in this program.
import random


"""Import the periodictable module to retrieve information on all chemical elements.
   This module will be used to to proivde information and be used to
   cross-reference information. For example, finding the name of a chemical element
   by its atomic number, etc."""
import periodictable as PT

#Import all UI widgets and tools from the Kivy module.
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView

#Note: Break functions have been used in while loops because bugs in Python version 3.4.x won't allow
#      a loop to break even if the condition to break has been met.


#Instance of peewee.sqlitedatabase class that stores the datbase location and type.
ChemGuide_Database=SqliteDatabase("ChemGuide.db")


#Relational database class
"""This class stores the login details of every user who registers in a relational database.
   It has 4 fields that store a user's First name, last name, username and password.
   Username has the "unique" attribute which means 2 usernames cannot be the same or it will
   produce an integrity error. In my program, this is fixed by prompting the user to change
   his/her password."""
class StudentLogins(Model):
    FirstName=CharField(max_length=40)
    LastName=CharField(max_length=40)
    username=CharField(max_length=250,unique=True)
    password=CharField(max_length=60)
    points=IntegerField()

    #Links the class/model to the database.
    class Meta:
        database=ChemGuide_Database

def initialise():
    """Create the table and database if they don't exist"""
    ChemGuide_Database.connect()
    ChemGuide_Database.create_tables([StudentLogins],safe=True)


#Sources
"""
http://archlinux.me/dusty/2013/06/29/creating-an-application-in-kivy-part-3/
kivy.org
youtube.com
stackoverflow.com
inclem.net
"""


#Builder enables the kivy language (UI language) to be written on the same file instead of
#2 different linked files containing python and kivy, respectively.
#Almost all of the UI has been developed in kivy language.
Builder.load_string("""
#: import sm kivy.uix.screenmanager
<MenuScreen>:
    FloatLayout:
        canvas.before:
            Color:
                rgba: 0, 0, 0, 1
            Rectangle:
                # self here refers to the widget i.e BoxLayout
                pos: self.pos
                size: self.size

        Label:
            font_size: '82sp'
            text: "[b]Chem[color=2AFF1D][/color][color=3333ff][b]Guide[/color]"
            markup:True
            pos_hint: {'x':0,'y':.2}

        Button:
            text: "Login"
            pos_hint: {'x':0.25,'y':.2}
            size_hint: .2,.1
            background_color: 0, 0, 3, 1

            on_press:
                root.manager.transition.direction = 'right'
                root.manager.current = 'login'

        Button:
            text:"[color=fffff]Register[/color]"
            markup:True
            size_hint: .2,.1
            pos_hint: {'x':0.5,'y':.2}
            background_color:3,3,3,1
            on_press:
                root.manager.transition.direction = 'left'
                root.manager.current = 'registration'      
<LoginScreen>:
    login_username: username
    login_password: password
    FloatLayout:
        Button:
            text:"Go to menu"
            markup:True
            background_color: 0, 0, 3, 1
            pos_hint: {'x':0.25,'y':.2}
            size_hint: .2,.1           
            on_press:
                root.manager.transition.direction = 'left'
                root.manager.current = 'menu'
            valign: "middle"
            halign:"center"
            text_size: self.size
        Button:
            text: "[color=fffff]Login[/color]"
            markup:True
            background_color:3,3,3,1
            pos_hint: {'x':0.5,'y':.2}
            size_hint: .2,.1
            on_press:
                root.login()
            


        Label:
            text:"[b]Log[color=2AFF1D][/color][color=3333ff][b]in[/color]"
            markup:True
            pos_hint: {'x':0,'y':.2}
            font_size: "50sp"
            
        Label:
            text: "Username:"
            size_hint: .2,.05
            pos_hint: {'x':0.235,'y':.5}
        Label:
            text: "Password:"
            size_hint: .2,.05
            pos_hint: {'x':0.235,'y':.418}
           
        TextInput:
            id: username
            size_hint: .2,.05
            pos_hint: {'x':0.405,'y':.5}
            multiline:False
        TextInput:
            id: password
            size_hint: .2,.05
            pos_hint: {'x':0.405,'y':.418}
            password:True
            multiline:False

<RegistrationScreen>:
    r_first_name: first_name
    r_last_name: last_name
    r_username: username
    r_password: password
    r_password_reenter: reenter
    FloatLayout:
        Button:
            text:"Go to menu"
            background_color: 0, 0, 3, 1
            markup:True
            pos_hint: {'x':.25,'y':.2}
            size_hint: .2,.1            
            on_press:
                root.manager.transition.direction = 'right'
                root.manager.current="menu"
            valign: "middle"
            halign:"center"
            text_size: self.size
            
        Button:
            text:"[color=fffff]Register[/color]"
            markup:True
            background_color:3,3,3,1
            pos_hint: {'x':0.5,'y':.2}
            size_hint: .2,.1
            on_press:root.register()

        Label:
            text:"[b]Regi[color=2AFF1D][/color][color=3333ff][b]ster[/color]"
            markup:True
            pos_hint: {'x':0,'y':.3}
            font_size: "50sp"
        Label:
            text:"First name:"
            pos_hint: {'x':0.23,'y':.668}
            size_hint: .2,.05
        Label:
            text:"Last name:"
            pos_hint: {'x':0.23,'y':.58}
            size_hint: .2,.05
        Label:
            text:"Username:"
            pos_hint: {'x':0.23,'y':.492}
            size_hint: .2,.05
            
        Label:
            text:"Password:"
            pos_hint: {'x':0.23,'y':.414}
            size_hint: .2,.05
        Label:
            text:"Re-enter password:"
            pos_hint: {'x':0.21,'y':.33}
            size_hint: .2,.05

        TextInput:
            id: first_name
            size_hint: .2,.05
            pos_hint: {'x':0.41,'y':.668}
            multiline:False
        TextInput:
            id: last_name
            size_hint: .2,.05
            pos_hint: {'x':0.41,'y':.58}
            multiline:False
        TextInput:
            id: username
            size_hint: .2,.05
            pos_hint: {'x':0.41,'y':.492}
            multiline:False

        TextInput:
            id: password
            size_hint: .2,.05
            pos_hint: {'x':0.41,'y':.414}
            password:True
            multiline:False
        TextInput:
            id: reenter
            size_hint: .2,.05
            pos_hint: {'x':0.41,'y':.33}
            password:True
            multiline:False

<RevisionScreen>:
    subshell_calc: calculate
    FloatLayout:
        Label:
            text:"[b]Rev[color=2AFF1D][/color][color=3333ff][b]ise[/color]"
            markup:True
            pos_hint: {'x':0,'y':.4}
            font_size: "50sp"

        ScrollableLabel:
            size_hint: (1, 0.65)
            pos_hint: {'x':0,'y':.17}
            
        
            Label:
                size_hint_y: None
                height: self.texture_size[1]
                text_size: self.width, None
                text: root.ScrollableLabel().Description
                

        TextInput:
            id: calculate
            size_hint: .2,.05
            pos_hint: {'x':0.405,'y':.15}
            multiline:False

        Button:
            text:"[color=fffff]Calculate[/color]"
            markup:True
            pos_hint: {'x':0.405,'y':.02}
            background_color:3,3,3,1
            size_hint: .2,.1
            on_press:
                root.calculate_subshells()

        Button:
            pos_hint: {'x':0.63,'y':.02}
            text:"Back"
            background_color:0,0,3,1
            markup:True
            size_hint: .2,.1
            on_press:
                root.manager.transition.direction = 'right'
                root.manager.current='welcome'
                

<WelcomeScreen>:
    FloatLayout:
        Label:
            text:"[b]Wel[color=2AFF1D][/color][color=3333ff][b]come[/color]"
            markup:True
            pos_hint: {'x':-.08,'y':.4}
            font_size: "50sp"


        Label:
            text:"Would you like to: "
            markup:True
            pos_hint: {'x':-.1,'y':.215}
            font_size: "30sp"

        Label:
            text:"Or"
            markup:True
            pos_hint: {'x':-.1,'y':.12}
            font_size: "40sp"

        Label:
            text:"Would you like to: "
            markup:True
            pos_hint: {'x':-.1,'y':.01}
            font_size: "30sp"

        Label:
            text:"Or"
            markup:True
            pos_hint: {'x':-.1,'y':-.1}
            font_size: "40sp"

        Label:
            text:"Would you like to: "
            markup:True
            pos_hint: {'x':-.1,'y':-0.2}
            font_size: "30sp"

        Button:
            pos_hint: {'x':0.63,'y':.465}
            text:"[color=fffff]Quiz yourself[/color]"
            background_color:3,3,3,1
            markup:True
            size_hint: .2,.1
            on_press:
                root.manager.transition.direction = 'right'
                root.manager.current='quiz'

        Button:
            text:"Revise"
            pos_hint: {'x':0.63,'y':.663}
            background_color:0,0,3,1
            size_hint: .2,.1
            on_press:
                root.manager.transition.direction = 'left'
                root.manager.current="revise"

        Button:
            text:"View Leaderboard"
            pos_hint: {'x':0.63,'y':.25}
            background_color:0,0,3,1
            size_hint: .2,.1
            on_press:
                root.manager.transition.direction = 'left'
                root.manager.current="leaderboard"


        Button:
            text:"[color=fffff]Logout[/color]"
            background_color:3,3,3,1
            markup:True
            pos_hint: {'x':0.30,'y':.035}
            size_hint: .2,.1
            on_press:
                root.manager.transition.direction = 'left'
                root.manager.current="menu"

<QuizScreen>:
    question1_input:q1
    question2_input:q2
    question3_input:q3
    FloatLayout:
        Label:
            text:"[b]Qu[color=2AFF1D][/color][color=3333ff][b]iz[/color]"
            markup:True
            pos_hint: {'x':0,'y':.4}
            font_size: "50sp"

        Button:
            pos_hint: {'x':0.4,'y':.685}
            text:"Instructions"
            background_color:0,0,3,1
            markup:True
            size_hint: .2,.1
            on_press:
                root.Quiz_instructions.open()

        Label:
            text:"Please view instructions before you begin."
            pos_hint: {'x':0,'y':.32}
            font_size: "20sp"
        
        Label:
            text:root.Question1
            pos_hint: {'x':0,'y':.15}
            font_size: "20sp"

        TextInput:
            id: q1
            size_hint: .3,.05
            pos_hint: {'x':0.35,'y':.55}
            multiline:False

        Label:
            text:root.Question2
            pos_hint: {'x':0,'y':0}
            font_size: "20sp"

        TextInput:
            id: q2
            size_hint: .3,.05
            pos_hint: {'x':0.35,'y':.40}
            multiline:False

        Label:
            text:root.Question3
            pos_hint: {'x':0,'y':-.15}
            font_size: "20sp"

        TextInput:
            id: q3
            size_hint: .3,.05
            pos_hint: {'x':0.35,'y':.25}
            multiline:False

        Button:
            pos_hint: {'x':0.23,'y':.05}
            text:"Mark"
            background_color:0,0,3,1
            markup:True
            size_hint: .2,.1
            on_press:
                root.Mark()
                

        Button:
            pos_hint: {'x':0.63,'y':.05}
            text:"[color=fffff]Back[/color]"
            background_color:3,3,3,1
            markup:True
            size_hint: .2,.1
            on_press:
                root.refresh_labels()
                root.manager.transition.direction = 'left'
                root.manager.current='welcome'

<LeaderboardScreen>:

    Label:
        text:"[b]Leader[color=2AFF1D][/color][color=3333ff][b]Board[/color]"
        markup:True
        pos_hint: {'x':0,'y':.4}
        font_size: "50sp"
    
    Button:
        pos_hint: {'x':0.5,'y':.05}
        text:"[color=fffff]Back[/color]"
        background_color:3,3,3,1
        markup:True
        size_hint: .2,.1
        on_press:
            root.manager.transition.direction = 'right'
            root.manager.current='welcome'#refresh_leaderboard
    Button:
        pos_hint: {'x':0.2,'y':.05}
        text:"Refresh Leaderboard"
        background_color:0,0,3,1
        markup:True
        size_hint: .2,.1
        on_press:
            root.clear()
            root.refresh_leaderboard()

""")

# Declare screens
class MenuScreen(Screen):
    pass

                   
class LoginScreen(Screen):
    login_username= ObjectProperty()
    login_password= ObjectProperty()

    #Stores the username of the current user
    Current_user=[]
    def login(self):
        
        complete_entryboxes=True
        #Stores string text from entryboxes in these 2 variables.
        login_username2=self.login_username.text
        login_password2=self.login_password.text
############################################################################################################################
        Success_LoginComplete=Popup(title='Success',
                                    content=Label(text='Congratulations!\n Login successful.'),
                                    size_hint=(None, None), size=(400, 200))
        Error_EmptyBoxes=Popup(title='Error',
                               content=Label(text='Please fill in all entry boxes'),
                               size_hint=(None, None), size=(400, 200))
        Error_incorrect_password=Popup(title='Error',
                                       content=Label(text="Incorrect password.\nPlease re-enter your password"),
                                       size_hint=(None, None), size=(400, 200))
        Error_username_nonexistant=Popup(title='Error',
                                       content=Label(text="Username does not exist.\nPlease re-enter your an existing username\nor register with an another username."),
                                       size_hint=(None, None), size=(400, 200))

############################################################################################################################




        """This while loop checks if the entry boxes have been filled in.
           It does this by checking if the variables "login_username2"
           and "login_password2" contain data.
           If not complete_entryboxes evaluates to False so the rest of code doesn't execute.
           Popup messages display the error to the user so they can fix it to continue logging in.
           """
        while complete_entryboxes==True:
            if login_username2:
                    pass                
            else:
                Error_EmptyBoxes.open()
                complete_entryboxes=False

            if login_password2:
                break
                
            else:
                Error_EmptyBoxes.open()
                complete_entryboxes=False


        
        #Boolean values to check if password and username exist and match.
        password_check=bool
        username_check=bool
        """This checks if "complete_entryboxes" is still true after the check, if so
           the code can continue, if not the login function won't run.
           The "Student_pool" variable stores all the records in the "StudentLogins".
           Next a for loop looks reads through every record in the database and checks
           if the any of the students usernames match the username typed into the
           entrybox.
           If so, any items in the Current_user list will be deleted so the program
           knows that the previous user isn't still loggged in.
           Username_check evaluates to True and then checks if the password
           corresponds to the username inputted. If this is true the password_check
           evaluates to True and the students username is appended to the list."""
        if complete_entryboxes==True:
            Student_pool=StudentLogins.select()
            for studs in Student_pool:
                if studs.username==self.login_username.text.lower():
                    del LoginScreen.Current_user[:]
                    username_check=True
                    if  username_check==True:
                        if studs.password==login_password2:
                            password_check=True
                            LoginScreen.Current_user.append(studs.username)
                            break

            """Part of the same if statement that checks if """
            if username_check==True:
                if password_check==True:
                    Success_LoginComplete.open()
                    self.login_username.text=""
                    self.login_password.text=""
                    Screens.transition.direction = 'left'
                    Screens.current = 'welcome'
                else:
                    Error_incorrect_password.open()
            else:
                Error_username_nonexistant.open()


        #Previous code for login that produced a bug that has been commented out
        """#If complete_entryboxes is still true
        if complete_entryboxes==True:
            Student_pool=StudentLogins.select()#.order_by(StudentLogins.FirstName.desc())
            for studs in Student_pool:
                if studs.username==self.login_username.text.lower():
                    if studs.password==login_password2:
                        Success_LoginComplete.open()
                        self.login_username.text=""
                        self.login_password.text=""
                        Screens.transition.direction = 'left'
                        Screens.current = 'revise'
                        break
                    else:
                        Error_incorrect_password.open()
                else:
                    Error_username_nonexistant.open()"""


class RegistrationScreen(Screen):
    r_first_name= ObjectProperty()
    r_last_name= ObjectProperty()
    r_username= ObjectProperty()
    r_password= ObjectProperty()
    r_password_reenter=ObjectProperty()


    
    def register(self):
        """Create variables to hold the text inputted from the entry
           boxes."""
        rf_first_name= self.r_first_name.text
        rf_last_name=  self.r_last_name.text
        rf_username=self.r_username.text
        rf_password=self.r_password.text
        rf_password_reenter=self.r_password_reenter.text

        #Booleans for validation
        complete_entryboxes=True
        is_not_alpha=False

#######################################################################################################

        #Popup widgets for various messages that need to be displayed.
        Success_RegComplete=Popup(title='Success',
                    content=Label(text='Congratulations!\nRegistration successful.'),
                    size_hint=(None, None), size=(400, 200))
        Error_EmptyBoxes=Popup(title='Error',
                    content=Label(text='Please fill in all entry boxes'),
                    size_hint=(None, None), size=(400, 200))
        Error_mismatch=Popup(title='Error',
                             content=Label(text="Passwords don't match.\nPlease re-enter your password"),
                             size_hint=(None, None), size=(400, 200))
        Error_isnotalpha=Popup(title='Error',
                             content=Label(text="Invalid character(s).\nNames can only contain letters.\nNumbers and special characters are not allowed.\nPlease re-enter the textfield with text only."),
                             size_hint=(.66, .5))
        Integrity_Error=Popup(title='Error',
                             content=Label(text="Username already exists.\nPlease try again."),
                             size_hint=(None, None), size=(400, 200))


        
########################################################################################################

        """Checks if all textinputs have text in the same way as the login function in the login class.
           The first and last name entryboxes are checked for if they're contain only letters
           A previous implementation made the use of a for loop to check all the variables that contain
           the data from the entry boxes but it gave errors due to bugs in python. So I had to create a
           longer and less efficient algorithm to enable it to work without any bugs. """ 
        while complete_entryboxes==True:
            if rf_first_name:
                if not rf_first_name.isalpha():
                    is_not_alpha=True
                    Error_isnotalpha.open()
                    break
            else:
                Error_EmptyBoxes.open()
                complete_entryboxes=False
                break

            if rf_last_name:
                if not rf_last_name.isalpha():
                    is_not_alpha=True
                    Error_isnotalpha.open()
                    break                
            else:
                Error_EmptyBoxes.open()
                complete_entryboxes=False
                break
            
            if rf_username:
                pass
            
            else:
                Error_EmptyBoxes.open()
                complete_entryboxes=False
                break

            if rf_password:
                pass                
            else:
                Error_EmptyBoxes.open()
                complete_entryboxes=False
                break
            
            #Last if statement in the for loop, so a break function was required.
            if rf_password_reenter:
                break
                
            else:
                Error_EmptyBoxes.open()
                complete_entryboxes=False
                break
            
        """Here "complete_entryboxes" and "is_not_alpha" is checked for if the entryboxes
           were filled and all of the inputs were alphabetical only then the rest of the code executes.
           If the password is exactly the same as the password re-entered in the second password box
           then the next part of the code can be executed, if not a popup is displayed.
           I had to insert the try and except into a while loop because python wasn't reading the try
           and except or the function that I had originally created.
           
           The while function run's while "IntegError==False". A new record is created for the four attributes
           of the StudentLogins class/table. Once this code has exectuded successfully, a popup appears saying
           registration is successful, all the text in the entryboxes are deleted and the screen transitions to
           the login page and the while loop breaks.

           The except condition runs if there is an integrity error, which is caused by the username already
           existing in the database. In this case, an error popup is displayed prompting the user to re-enter
           a new username because it already exists and the loop breaks."""  
        if (complete_entryboxes==True) and (is_not_alpha==False):
            if rf_password==rf_password_reenter:
                IntegError=False
                while IntegError==False:
                    try:
                        StudentLogins.create(FirstName=rf_first_name,
                                             LastName=rf_last_name,
                                             username=rf_username.lower(),
                                             password=rf_password,
                                             points=0)
                        Success_RegComplete.open()
                        

                        #Delete all text in all entryboxes and transitions to the login page.
                        self.r_first_name.text=""
                        self.r_last_name.text=""
                        self.r_username.text=""
                        self.r_password.text=""
                        self.r_password_reenter.text=""
                        Screens.transition.direction = 'right'
                        Screens.current = 'login'
                        break
                    

                    except IntegrityError:
                        Integrity_Error.open()
                        IntegError=True
                        break                  
                    
            else:
                Error_mismatch.open()


class WelcomeScreen(Screen):
    #Only stores design widgets.
    pass

class QuizScreen(Screen):
    Question1=StringProperty()
    Question2=StringProperty()
    Question3=StringProperty()
    
    question1_input=ObjectProperty()
    question2_input=ObjectProperty()
    question3_input=ObjectProperty()

    #Stores random atomic numbers created for the quiz.
    AN_list=[]
    
    #Popup that displays quiz instructions
    Quiz_instructions=Popup(title='Instructions',
                               content=Label(text='Please fill in all entry boxes using subshell notation for the '+
                                             "atomic\n numbers given. You should use commas to seperate each subshell.\n"+
                                             "e.g 1s2,2s2...\n10 points are awarded for every correct subshell."),
                               size_hint=(None, None), size=(500, 300))

    def __init__(self, **kwargs):
        super(QuizScreen, self).__init__(**kwargs)
        #This page dynamically creates questions for the user
        #everytime the user visits the page.


        #Stores names of the three elements generated for the quiz.
        self.Elemental_trio=[]
        #Generates random atomic number for three questions.

        """The first random atomic number between 1 and 30 is
           generated outside the loop. Inside the while loop
           a second random number is generated and if the second
           number is equal to the first a new number will be generated
           and will keep generating until they are not equal. The
           process is the same for the third number, a number is generated
           and if it isn't equal to the previous 2 numbers then it will be
           stored in the list like the previous 2.
           """
        Randcheck=True
        self.random_AN1=random.randint(1,30)
        self.AN_list.append(self.random_AN1)
        while Randcheck:
            self.random_AN2=random.randint(1,30)
            if self.random_AN2 != self.random_AN1:
                self.AN_list.append(self.random_AN2)
                self.random_AN3=random.randint(1,30)
                if self.random_AN3 != self.random_AN2 and (self.random_AN3 != self.random_AN1):
                    self.AN_list.append(self.random_AN3)
                    break

        #Finds symbol for random elements
        self.Random_Element1=PT.elements[self.random_AN1]
        self.Random_Element2=PT.elements[self.random_AN2]
        self.Random_Element3=PT.elements[self.random_AN3]

        #Stores random element symbols
        self.Element_list=[self.Random_Element1,self.Random_Element2,self.Random_Element3]

        """The part of the function that finds the name of
           the element using the symbols of the atomic number, since
           there wasn't a direct method to do this in the module.

           The for loop looks through all the atomic elements in the periodictable
           module and matches them with the elements in the "self.Element_list" list.
           When it finds a match, it will generate a name for the symbol the element
           produced. For example, it will find the symbol "H" for Hydrogen or "O" for
           oxygen and append the "Hydrogen" or "Oxygen" to the list after the text has
           been formatted.
           """
        for RandEl in self.Element_list:
            for el in PT.elements:
                if el==RandEl:
                    self.Element_name=str(el.name)
                    self.Element_name=(self.Element_name[0].upper()+self.Element_name[1:])
                    self.Elemental_trio.append(self.Element_name)
                    break

        #Stores the strings for three questions on the quiz page.
        self.Question1=self.Elemental_trio[0]+"  --  (Atomic number: "+str(self.AN_list[0])+")"
        self.Question2=self.Elemental_trio[1]+"  --  (Atomic number: "+str(self.AN_list[1])+")"
        self.Question3=self.Elemental_trio[2]+"  --  (Atomic number: "+str(self.AN_list[2])+")"

    def refresh_labels(self):
        #Identical to the previous procedure, used to refresh labels. the questions and answers.

        self.Elemental_trio=[]

        #Generates random atomic number for three questions
        Randcheck=True
        self.random_AN1=random.randint(1,30)
        self.AN_list[0]=self.random_AN1
        while Randcheck:  
            self.random_AN2=random.randint(1,30)
            if self.random_AN2 != self.random_AN1:
                self.AN_list[1]=self.random_AN2
                self.random_AN3=random.randint(1,30)
                if self.random_AN3 != self.random_AN2 and (self.random_AN3 != self.random_AN1):
                    self.AN_list[2]=self.random_AN3
                    break
        

        #Finds symbol for random elements
        self.Random_Element1=PT.elements[self.random_AN1]
        self.Random_Element2=PT.elements[self.random_AN2]
        self.Random_Element3=PT.elements[self.random_AN3]

        #Stores random element symbols
        self.Element_list=[self.Random_Element1,self.Random_Element2,self.Random_Element3]

        """The part of the function that finds the name of
           the element using the symbols of the atomic number, since
           there wasn't a direct method to do this in the module.
           """
        for RandEl in self.Element_list:
            for el in PT.elements:
                if el==RandEl:
                    self.Element_name=str(el.name)
                    self.Element_name=(self.Element_name[0].upper()+self.Element_name[1:])
                    self.Elemental_trio.append(self.Element_name)
                    break

        self.Question1=self.Elemental_trio[0]+"  --  (Atomic number: "+str(self.AN_list[0])+")"
        self.Question2=self.Elemental_trio[1]+"  --  (Atomic number: "+str(self.AN_list[1])+")"
        self.Question3=self.Elemental_trio[2]+"  --  (Atomic number: "+str(self.AN_list[2])+")"

    
    def Mark(self):
        #The marking function.

        #Text from the entrybox is stripped of spaces and all characters before each
        #comma become strings and then items in a list. E.g 1s2,2s2 --> ['1s2','2s2']
        Question1_inputed=self.question1_input.text.strip().split(",")
        Question2_inputed=self.question2_input.text.strip().split(",")
        Question3_inputed=self.question3_input.text.strip().split(",")

        #The answers that the program generates from the questions are
        #stored in this list.
        self.answers=[]

        #Variable that stores the points the user gains in each test.
        #Starts with 0 everytime.
        quiz_points=0


        #Empty entryboxes popup
        Error_EmptyBoxes=Popup(title='Error',
                               content=Label(text='Please fill in all entry boxes'),
                               size_hint=(None, None), size=(400, 200))

        
        #Instance of the complete_entryboxes variable being reused, along with the
        #procedure to check if entryboxes have been filled (contain data).
        #Identical to previous procedures in the registration and login classes.
        complete_entryboxes=True

        while complete_entryboxes==True:
            if self.question1_input.text:
                pass
            
            else:
                Error_EmptyBoxes.open()
                complete_entryboxes=False
                break

            if self.question1_input.text:
                pass
            
            
            else:
                Error_EmptyBoxes.open()
                complete_entryboxes=False
                break

            if self.question1_input.text:
                break

            else:
                Error_EmptyBoxes.open()
                complete_entryboxes=False
                break

        if complete_entryboxes==True:
            for AN in self.AN_list:
                #AN stands for atomic number.
                
                #Automated version of the calcualtion on the revision page.

                #The answer for each question that the program calculates is stored in the ouput variable
                #while the loop is running and then appended to the self.answers list.
                output=[]

                #Stores the original atomic number.
                original_AN=AN
                #Declares the count variable and sets the count to 0 before the loop executes.
                count=0
                while AN>0:
                    
                    """This calculation is the same as the one on the revision page except for the
                       the exception to the general rule, while the other calculation algorithm
                       handled the 2 exceptions using their string names, this one uses the
                       original atomic number to handle them. Another difference between the 2
                       is the this loop is nested inside a for loop that loops 3 times, because
                       of the 3 answers that need to be calculate for."""
                    count=count+1
                    if AN>=2:
                        output.append(str(count)+"s"+"2")
                        AN=AN-2
                        if AN==0:
                            break
                    else:
                        output.append(str(count)+"s"+"1")
                        AN=AN-1
                        if AN==0:
                            break
                        
                    if count==1:
                        pass
                    else:
                        if AN>=6:
                            output.append(str(count)+"p"+"6")
                            AN=AN-6
                            if AN==0:
                                break
                        else:
                            p=str(AN)
                            output.append(str(count)+"p"+str(p))
                            break
                        
                        if count==3:
                            if (original_AN==24) or (original_AN==29):
                                if AN>=10:
                                    output.append(str(count)+"d"+"10")
                                    AN=AN-10
                                    if AN==2:
                                        output.append(str(count+1)+"s"+"2")
                                        AN=AN-2
                                        if AN==0:
                                            break
                                    
                                else:
                                    d=5
                                    AN=AN-d
                                    output.append(str(count)+"d"+str(d))
                                    if AN==1:
                                        output.append(str(count+1)+"s"+"1")
                                        AN=AN-1
                                        if AN==0:
                                            break


                            else:
                                #4s subshell
                                if AN>=2:
                                    output.append(str(count+1)+"s"+"2")
                                    AN=AN-2
                                    if AN==0:
                                        break
                                else:
                                    output.append(str(count+1)+"s"+"1")
                                    AN=AN-1
                                    if AN==0:
                                        break

                                #3d subshell
                                if AN>=10:
                                    output.append(str(count)+"d"+"10")
                                    AN=AN-10
                                    if AN==0:
                                        break
                                else:
                                    d=str(AN)
                                    output.append(str(count)+"d"+d)
                                    break

                """For each of the 3 times that the for loop, loops it takes
                   the output list and appends the "output" list into the answers
                   list. This is so the "self.answers" list contains 3 lists inside it,
                   those 3 lists will be used in the marking process."""
                self.answers.append(output)


            """Each of the 3 marking algorithms contain their
               respective output lists from the "self.answers" list.
               The next variable holds the number of items in the
               list.
               This is used so the for loops know how many items to
               check. It then checks each item in both lists starting
               with the 0 index position until the end of either list.
               If the users answer is not complete the for loop will mark
               it up to the point that the user has completed it to.
               10 points are awarded for every subshell the user gets
               right.

               The same process is done for the next 2 questions to be
               marked."""
                            
            actual_answer1=self.answers[0]
            actual_answer1_length=len(actual_answer1)
            try:
                for i in range(0,actual_answer1_length):
                    if Question1_inputed[i]==actual_answer1[i]:
                        quiz_points=quiz_points+10
                    else:
                        pass
            except IndexError:
                pass

            actual_answer2=self.answers[1]
            actual_answer2_length=len(actual_answer2)
            try:
                for i in range(0,actual_answer2_length):
                    if Question2_inputed[i]==actual_answer2[i]:
                        quiz_points=quiz_points+10
                    else:
                        pass
            except IndexError:
                pass

            actual_answer3=self.answers[2]
            actual_answer3_length=len(actual_answer3)
            try:
                for i in range(0,actual_answer3_length):
                    if Question3_inputed[i]==actual_answer3[i]:
                        quiz_points=quiz_points+10
                    else:
                        pass
            except IndexError:
                pass

            
            #Finds which user is currently logged in from the login screen "Current_uers" list.
            #This doesn't produce an error if the list is emptu because python doesn't check code
            #this deep or indented into a function.By the time this part of the code is executed, the
            #"Current_user" list will have an item in the 0 index.
            Logged_in_user=LoginScreen().Current_user[0]

            #Finds the total points available by finding the length of all items in the 3 lists
            #and multiplying them by 10(points).
            points_available=(actual_answer1_length+actual_answer2_length+actual_answer3_length)*10

            """This if-else statement makes sure the user has gained any points.
               If not the remaining code doesn't serve any pupose so the else
               statement gives the pass command to do nothing.

               If the user gained points then the Student_pool variable is used
               again to store all records in the database. The for loop reads
               through all records in database/Student_pool variable.
               It then looks for the user that's logged, searching by username
               since the username is the unique/primary key in the database
               . Once the user is found then the the points gained from this
               quiz is added to the user's already existing score
               (could be an exising score of 0). Then it brings up the records
               just found to update it with the new score and saves the updated
               record."""
            if quiz_points>0:
    
                Student_pool=StudentLogins.select()
                for studs in Student_pool:
                    if Logged_in_user==studs.username:
                        new_points=studs.points+quiz_points
                        Get_logged_in_user=StudentLogins.get(username=Logged_in_user)
                        Get_logged_in_user.points=new_points
                        Get_logged_in_user.save()
                        break                       
            else:
                pass
            
            #A popup is then defined and opened with the quiz results.
            Quiz_results=Popup(title='Results',
                               content=Label(text="You got "+str(quiz_points)+" out of "+str(points_available)+"."),
                               size_hint=(None, None), size=(400, 200))

            Quiz_results.open()

            
            #Clears out text from entry boxes, refreshes labels and questions and then transitions to the welcome screen.
            self.question1_input.text=""
            self.question2_input.text=""
            self.question3_input.text=""
            self.refresh_labels()
            Screens.transition.direction = 'left'
            Screens.current = 'welcome'
    


class RevisionScreen(Screen):
    subshell_calc= ObjectProperty()
    class ScrollableLabel(ScrollView):
        #Stores the text for the description/explanation on the revision page, this text is then put into a label
        Description=StringProperty('')
        Description=("Electron subshell notation follows a specific pattern.\n\n"+
                     "The first character is used to denote the shell's 'Principal quantum number'. "+
                     "The smaller the principal quantum number is, the closer it is to the nucleus. For example, "+
                     "the 1s orbital is the closest to the nucleus."
                     "The first orbital can only hold 2 electrons before filling up completely. "+
                     "This is denoted by 1s2. '1' is the prinicipal quantum number, 's' is the type of subshell and "+
                     "2 is the amount of electrons it can hold. All 's' subhells can only hold 2 electrons.\n\n"+
                     "The second orbital has a prinicipal quantum number of 2 and contains 2 subshells: the 's' and 'p' "+
                     "subshells. The 'p' subshell can hold a maximum of 6 electrons. e.g 1s2,2s2,2p6\n\n"+
                     "The third orbital like the first and second contain as many subshells as its prinicpal"+
                     "quantum shell's value: 's','p' and 'd'.\n\n"+
                     "Lastly, for the A-level Chemistry syllabus, sutdents are only required to notate up to"+
                     "the 4s subshell, which because it's an 's' subshell contains a maximum of only 2 electrons.\n"+
                     "An important point to note is the the 4s subshell fills before the 3d subshell. "+
                     "e.g 1s2,2s2,2p6,3s2,3p6,4s2,3d10. "+
                     "However there are 2 exceptions to this rule: Chromium (atomic number 24) and Copper (atomic number 29). "+
                     "These 2 elements have their 3d subshells fill up before the 4s subshell.\n\n"+
                     "Enter their atomic numbers in the box below to see how they fill their orbitals and enter atomic numbers"+
                     " for other elements between 1-30 to compare them against each other.")
    
    def calculate_subshells(self):
        #AN stands for atomic number.
        
        subshell_calc=self.subshell_calc.text

        Value_Error=Popup(title='Error',
                          content=Label(text="Atomic number can only be a (positive) integer.\nPlease try again."),
                          size_hint=(None, None), size=(400, 200))

        AN_check=Popup(title='Error',
                          content=Label(text="For the AS syllabus only elements with atomic\nnumbers 1-30 are required.\nPlease input an atomic number in this range."),
                          size_hint=(None, None), size=(500, 200))

        try:
            output=[]            
            
            AN=int(subshell_calc)
            #Declares the count variable and sets the count to 0 before the loop executes.
            count=0

            """Neutron exception, since it isn't an element in the periodic table but is outputted if AN==0 in
               the periodictable module.So I've given it an output in this case."""
            if AN==0:
                output.append("Neutron")
            
            #If the atomic number is greater than 30, which isn't on the syllabus a message displays
            #and the loop below does not run.
            elif AN>30:
                AN_check.open()

            else:

                """Finds the elements name in the periodic table, since the module doesn't provide a direct way to do this."""
                Element=PT.elements[AN]
                for el in PT.elements:
                    if el==Element:
                        Element_name=str(el.name)
                        #change
                        Element_name=(Element_name[0].upper()+Element_name[1:])
                        



                """Everytime the loop, loops it adds 1 to the count.
                       Which represents the "principal quantum shell" explained in the
                       revision page.

                       If the Atomic number is 2 or greater it will add 2 "electrons" to the
                       first 's' subshell. If not the only other number it could be is 1,
                       since the loop did is set to break at 0. The else statement will
                       append 1s1 to the list. 2 is subtracted from the atomic number (AN)
                       so as the loop progresses the program knows how many electrons there
                       are left. This is the same for other if-else statements in the loop,
                       except for the fact that the other ones will subtract up to 6 or even
                       10 instead of 2.

                       Next the loop checks if count equals 1, if so, it doesn't continue with the
                       rest of the loop and starts again.
                       After it restarts, count is equal to 2 and goes through the first if-else
                       statements again.

                       The next if-else statements do the same as the first 2, but instead of
                       writing 2 or 1, in the p subshell they would only have 6 or less.
                       If they have 6 or more, they will be appended to the output list with
                       #p6 or #p(#<6), e.g 2p6 or 2p3.
                       If the number is less than 6, it's safe to say that after this number is
                       subtracted, the atomic number will be 0. So the loop breaks after appending
                       the number.

                       If the count variable is on 3 and passed through the 's' and 'p'
                       if-else statements prior to the "if count==3" statement then
                       the "if count==3" statement will check for the 2 exceptions to
                       the general subshell calculation rule, which are the elements
                       copper and chromium.

                       If it's either one of these 2 elements, then the loop follows
                       a different path, that corresponds to those 2 elements.

                       The loop continues to the 4s and/or 3d subshells in all other cases
                       with atomic numbers big enough.

                       
                       """
                
                while AN>0:

                    count=count+1
                    if AN>=2:
                        output.append(str(count)+"s"+"2")
                        AN=AN-2
                        if AN==0:
                            break
                    else:
                        output.append(str(count)+"s"+"1")
                        AN=AN-1
                        if AN==0:
                            break
                        
                    if count==1:
                        pass
                    else:
                        if AN>=6:
                            output.append(str(count)+"p"+"6")
                            AN=AN-6
                            if AN==0:
                                break
                        else:
                            p=str(AN)
                            output.append(str(count)+"p"+str(p))
                            break
                        
                        if count==3:
                            if (Element_name=="Copper") or (Element_name=="Chromium"):
                                if AN>=10:
                                    output.append(str(count)+"d"+"10")
                                    AN=AN-10
                                    if AN==2:
                                        output.append(str(count+1)+"s"+"2")
                                        AN=AN-2
                                        if AN==0:
                                            break
                                    
                                else:
                                    d=5
                                    AN=AN-d
                                    output.append(str(count)+"d"+str(d))
                                    if AN==1:
                                        output.append(str(count+1)+"s"+"1")
                                        AN=AN-1
                                        if AN==0:
                                            break


                            else:
                                #4s subshell
                                if AN>=2:
                                    output.append(str(count+1)+"s"+"2")
                                    AN=AN-2
                                    if AN==0:
                                        break
                                else:
                                    output.append(str(count+1)+"s"+"1")
                                    AN=AN-1
                                    if AN==0:
                                        break

                                #3d subshell
                                if AN>=10:
                                    output.append(str(count)+"d"+"10")
                                    AN=AN-10
                                    if AN==0:
                                        break
                                else:
                                    d=str(AN)
                                    output.append(str(count)+"d"+d)
                                    break

                        
                """The first line clears out the entrybox's text.
                   A popup widget is defined and opened, containing all the information
                   needed to be outputted from the calculation."""
                self.subshell_calc.text=""
                subshell_output=Popup(title='Subshell',
                                      content=Label(text=("Element name: "+Element_name+"\n"+
                                                          "Element Symbol: "+str(Element)+"\n"+
                                                          "Electron configuration: "+str(output))),
                                      size_hint=(None, None), size=(500, 250),halign="center", valign="middle")
                subshell_output.open()
                
        #Stops execution if anything but positive numbers are inputted.
        except (ValueError, KeyError) as error:
            Value_Error.open()
            self.subshell_calc.text=""



class LeaderboardScreen(Screen):

    def __init__(self, **kwargs):
        super(LeaderboardScreen, self).__init__(**kwargs)

        #Define the layout widgets.
        self.Grid = GridLayout(cols=5, padding=60, spacing=10,size_hint=(1, None), width=900)
        self.Grid.bind(minimum_height=self.Grid.setter('height'))
        self.ScrollviewLayout = ScrollView(size_hint=(1, None), size=(900, 320),
                pos_hint={'center_x': .5, 'center_y': .5}
                , do_scroll_x=False)

        """Note: This has been put into exception handlers because running when this file runs
           for the first time, a database file for it will not exist and will cause an
           OperationalError within the peewee module since the database only initialises
           at the end of the code. Originally this caused elements from
           the UI to disappear but rearragning the code fixed that problem.

           The "Student_pool" variable has been used again but arranges all records in the
           database in descending order in terms of points. So, the user with the highest
           score is first and the user with the lowest score is last/at the bottom.

           The rank variable is placed outside the loop and set to 0. The for loop
           will go throught every record in the database starting with the user
           with the highest score (to the user with the lowest score) the rank variable
           adds 1 to itself for every student starting with the first so as it goes
           through every record and the increasing number will show their rank.
           The leaderboard_details variable stores all the text information required
           for each user in the leaderboard and is used as the text for the button
           it'll be placed in.
           A button is then created for each user with the leaderboard_details as its
           text and added to the grid layout widget.
           After all the buttons have been added for each user, the grid layout
           is added to the Scrollview layout which in turn is added to the
           main screen (LeaderboardScreen).
           """
        try:
            Student_pool=StudentLogins.select().order_by(StudentLogins.points.desc())
            rank=0
            for studs in Student_pool:
                rank=rank+1
                leaderboard_details=(("#"+str(rank)+"\n"+studs.FirstName+" "+studs.LastName+
                                     "\n"+"Points:"+str(studs.points)))
                self.btn = Button(text=leaderboard_details,
                             size=(480, 100),
                             size_hint=(1, None),
                             halign='center',
                             valign='middle')
                self.Grid.add_widget(self.btn)

        except OperationalError:
            pass
            
        self.ScrollviewLayout.add_widget(self.Grid)
        self.add_widget(self.ScrollviewLayout)
        

    def clear(self):
        """Used to clear contents of the leaderboard widgets, i.e the
           table that stores buttons for every user. The scrollview as
           mentioned contains all the widgets in the table."""
                                     
        for i in range(1):
            self.remove_widget(self.ScrollviewLayout)
        

            
    def refresh_leaderboard(self):
        #Refer to the original procedure, since this is identical. It serves to
        #add all the widgets back as updated versions after being cleared out.
        self.Grid = GridLayout(cols=5, padding=60, spacing=10,size_hint=(1, None), width=900)
        self.Grid.bind(minimum_height=self.Grid.setter('height'))

        self.ScrollviewLayout = ScrollView(size_hint=(1, None), size=(900, 320),
                pos_hint={'center_x': .5, 'center_y': .5}
                , do_scroll_x=False)

        
        Student_pool=StudentLogins.select().order_by(StudentLogins.points.desc())   
        try:
            
            rank=0
            for studs in Student_pool:
                rank=rank+1
                leaderboard_details=("#"+str(rank)+"\n"+studs.FirstName+" "+studs.LastName+
                                     "\n"+"Points:"+str(studs.points))
                self.btn = Button(text=leaderboard_details,
                             size=(480, 100),
                             size_hint=(1, None))
                self.Grid.add_widget(self.btn)


        except OperationalError:
            pass
        
        self.ScrollviewLayout.add_widget(self.Grid)
        self.add_widget(self.ScrollviewLayout)
        



# Create the screen manager
####################################################################
#Add all the other screens to the main ScreenManager class("Screens").
Screens = ScreenManager()
Screens.add_widget(MenuScreen(name='menu'))
Screens.add_widget(LoginScreen(name='login'))
Screens.add_widget(RegistrationScreen(name='registration'))
Screens.add_widget(RevisionScreen(name='revise'))
Screens.add_widget(WelcomeScreen(name='welcome'))
Screens.add_widget(QuizScreen(name='quiz'))
Screens.add_widget(LeaderboardScreen(name='leaderboard'))
###################################################################


#The App class builds and runs the program.
class ChemGuideApp(App):
    def build(self):
        return Screens

if __name__ == '__main__':
    initialise()
    ChemGuideApp().run()
                                     
