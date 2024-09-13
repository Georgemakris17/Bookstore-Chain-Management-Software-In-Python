from user import new_user,login_user,menu_user
from admin import admin_login,menu_admin


def Menu():
    choice =int(input("1:user\n2:admin\n0:exit\n:"))
    if choice==1:
        print("hello user\n")
        choice =int(input("1:new user\n2:login\n0:exit\n:"))
        if choice==1:
            print("New user\n")
            username, password=new_user()
            #menu_user(username,password)
        elif choice==2:
            print("login user\n")
            username, password= login_user()
            menu_user(username,password)
            
        
    elif choice==2:
        print("hello admin\n")
        choice =int(input("1:login\n0:exit\n:"))
        if choice==1:
           username,password= admin_login()
           menu_admin(username, password)
        
    elif choice==0 :
        print("exit")
        
        
    
    
if __name__ == "__main__":
    Menu()