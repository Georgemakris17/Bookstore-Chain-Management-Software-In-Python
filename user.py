import pandas as pd
import time
from books import book_fount, book_cost, available_book,change_copies,suggestion_books
from reviews import load_reviews,user_review_book
head = ['id', 'username', 'password', 'address','city','orders','favorites','balance']
# Χρησιμοποιούμε τον χαρακτήρα ";" ως διαχωριστικό στο αρχείο CSV
user_df = pd.read_csv('user.csv', names=head, header=None, sep=';')

favorites_df =pd.read_csv('favorites.csv', names=['id','zero'], header=None, sep=';')
def menu_user(username,password):
    position=found_line(username,password)
    
    choice = int(input("1.μεταφορτωση βιβλίων\n2.prosthiki entry\n3.τροποποίηση στοιχίων\n4.αφαίρεση βιβλίων απο την λιστα favorites\n5.ελεγχος υπολοίπου\n6.διαθεσιμοτιτα και τιμη βιβλίων.\n7.προβολ΄ή παραγγελιών και τροποποίηση\n8.προτάσεις βιβλίων\n9.review\n:"))
    if choice==1:
       favorites_change(position)
    elif choice==2:
        add_favorites(position)
    elif choice ==3:
        modification_of_personal_details(position)
    elif choice==4:
        delete_favorites(position)
    elif choice==5:
        balance(position)
    elif choice==6:
        favorites_books(position)
    elif choice == 7:
        modification_of_orders(position)  
    elif choice == 8:
        suggestions(position)
    elif choice ==9:
        review(position)
    elif choice ==0:
        print("exit")
        
        
def contains_special_character(s):
    special_characters = set("!@#$%^&*()-_+=<>?/|\\{}[]~`")
    return any(char in special_characters for char in s)
def new_user():
    head = ['id', 'username', 'password', 'address', 'city', 'orders', 'favorites', 'balance']
    # Χρησιμοποιούμε τον χαρακτήρα ";" ως διαχωριστικό στο αρχείο CSV
    user_df = pd.read_csv('user.csv', names=head, header=None, sep=';')
    
    username = input("Please give me your name: ")
    password = input("Please give me your password: ")
    while not contains_special_character(password) or len(password) < 8:
        print("Your password needs to have a special character and be at least 8 characters long.")
        password = input("Please give me your password: ")
    
    address = input("Please give me your address: ")
    city = input("Please give me your city: ")
    favorites = input("Please give me your favorites: ")
    balance = input("Please give me your balance: ")
    
    new_data = {'id': len(user_df) + 1, 'username': username, 'password': password, 
                'address': address, 'city': city, 'orders': '', 'favorites': favorites, 
                'balance': balance}
    
    new_df = pd.DataFrame([new_data])  # Δημιουργία DataFrame με τα νέα δεδομένα
    
    user_df = pd.concat([user_df, new_df], ignore_index=True)  # Συνένωση του user_df με το new_df
    
    user_df.to_csv('user.csv', sep=';', index=False, header=False, mode='w')
    return username, password
def login_user():
    counter=0
    head = ['id', 'username', 'password', 'address','city','orders','favorites','balance']
    # Χρησιμοποιούμε τον χαρακτήρα ";" ως διαχωριστικό στο αρχείο CSV
    user_df = pd.read_csv('user.csv', names=head, header=None, sep=';')
    
    # print(user_df['favorites'][3])
    # favorites_list = (user_df['favorites'][3].split(','))
    # print(favorites_list)
    while(counter<3):
        username = input("Hello user\npleace give your username:")
        password = input("pleace give your password:")
        if username in user_df['username'].tolist() and password in user_df['password'].tolist():
            
            #print(user_df)
            print("login is good")
            counter=5
        else:
            print("login fail")
            counter+=1
            if(counter==3):
                counter=0
                time.sleep(10)
    return username, password
def found_line(username, password):

    # Συνδυάζουμε τις συνθήκες για το username και το password
    founder_combined = user_df.loc[(user_df['username'] == username) & (user_df['password'] == password)]
    print(founder_combined)
    
    # Ελέγχουμε αν υπάρχει τουλάχιστον μία γραμμή που να πληροί τις συνθήκες
    if not founder_combined.empty:
        # Παίρνουμε τη θέση της πρώτης γραμμής που πληροί τις συνθήκες
        position = founder_combined.index[0]
    else:
        # Αν δεν υπάρχει γραμμή που να πληροί τις συνθήκες, επιστρέφουμε None
        position = None
    
    print(position)
    return position
    
def favorites_books(position):
    choice =int(input("1:do you want to see all books\n2:or some of them\n0:exit\n:"))
    if choice ==1:
       
        favorites_str = user_df['favorites'][position]
        favorites_list = favorites_str.split(',')
        print(favorites_list)
        book_fount(favorites_list)
    elif choice == 2:
        
        
        favorites_str = user_df['favorites'][position]
        favorites_list = favorites_str.split(',')
        print(favorites_list)
        myopinion=input("choice of list favorites with(,):")
        mylist= myopinion.split(',')
        print(mylist)
        book_fount(mylist)
def favorites_change(position):
    
    favorites_str = user_df['favorites'][position]
    favorites_list = favorites_str.split(',')
    print("Τα βιβλία που έχετε στα αγαπημένα (με ,):", favorites_list)
    
    favorites_change_str = favorites_df['id'][0]
    favorites_change_list = favorites_change_str.split(',')
    
    # Αφαίρεση διπλότυπων χρησιμοποιώντας set
    unique_favorites = list(set(favorites_list + favorites_change_list))
    
    # Αφαίρεση τυχόν κενών στοιχείων
    unique_favorites = [fav.strip() for fav in unique_favorites if fav.strip()]
    
    favorites_change_str = ','.join(unique_favorites)
    user_df.loc[position, "favorites"] = favorites_change_str
    user_df.to_csv('user.csv', index=False, header=None, sep=';')
    print("ok\n")

def balance(position):
    
    print("your balance is: ",user_df['balance'][position])
    
def delete_favorites(position):
    
    favorites_str = user_df['favorites'][position]
    favorites_list =  favorites_str.split(',')
    print("the books you have in favorites:",favorites_list)
    favorites_change_str= input("enter your books who you whould like to delete: ")
    favorites_change_list = favorites_change_str.split(',')
    
    favorites_change_list = list(set(favorites_list)-set(favorites_change_list))
    favorites_change_str = ','.join(favorites_change_list)
    user_df.loc[position, "favorites"]=favorites_change_str
    user_df.to_csv('user.csv',index=False,header=None,sep=';')
def modification_of_personal_details(position):
    
    
    choice = int(input("1.modification of username\n2.modification of password\n3.modification of address\n4.modification of city\n5.modification of balance\n:"))
    if choice == 1:
        modification = input("give me your new username: ")
        user_df.loc[position, "username"]=modification
        user_df.to_csv('user.csv',index=False,header=None,sep=';')
    elif choice ==2:
        modification = input("give me your new password: ")
        while not contains_special_character(modification) or len(modification) < 8:
            print("Your password needs to have a special character and be at least 8 characters long.")
            modification = input("Please give me your password: ")
        user_df.loc[position, "password"]=modification
        user_df.to_csv('user.csv',index=False,header=None,sep=';')
    elif choice == 3:
        modification = input("give me your new address: ")
        user_df.loc[position, "address"]=modification
        user_df.to_csv('user.csv',index=False,header=None,sep=';')
    elif choice == 4:
        modification = input("give me your new city: ")
        user_df.loc[position, "city"]=modification
        user_df.to_csv('user.csv',index=False,header=None,sep=';')
    elif choice == 5:
        modification = float(input("give me your new balance: "))
        user_df.loc[position, "balance"]=modification
        user_df.to_csv('user.csv',index=False,header=None,sep=';')
    print("\nthe change is finish\n")
def modification_of_orders(position):
      
       order_str = str(user_df['orders'][position])
       order_list = order_str.split(',')
       print("the books you have in orders: ",order_list)
       choice = int(input("you want to:\n1.delete a book and refound\n2.add a book"))
       if choice == 1:
           modification = input("enter book/books you would like to delete(with , ): ")
           modification_list = modification.split(',')
           order_list=set(order_list)
           modification_list = set(modification_list)
           
           modification_list = modification_list.intersection(order_list)
           modification_list = list(modification_list)
           print(modification_list)
           change_copies(modification_list, 1)
           cost=book_cost(modification_list)
           balance = user_df['balance'][position]
           balance+=cost
           print(balance)
           user_df.loc[position,"balance"]=balance
           user_df.to_csv('user.csv',index=False,header=None,sep=';')
           order_list = list(order_list-set(modification_list))
           print(order_list)
           order_str = ','.join(order_list)
           user_df.loc[position,"orders"]=order_str
           user_df.to_csv('user.csv',index=False,header=None,sep=';')
       elif choice==2:
            modification = input("Enter book/books you would like to add (with , ): ")
            modification_list = [book.strip() for book in modification.split(',') if book.strip()]
            
            # Καθαρίζουμε την order_list από 'nan' και κενές συμβολοσειρές
            order_list = [book for book in order_list if book and book != 'nan']
            
            order_set = set(order_list)
            modification_set = set(modification_list)
            
            common_books = order_set.intersection(modification_set)
            print("Common books:", common_books)
            
            modification_list = [book for book in modification_list if book not in common_books]
            print("Books to add:", modification_list)
            
            modification_list = available_book(modification_list)
            cost = book_cost(modification_list)
            balance = user_df['balance'][position]
            balance -= cost
            
            if balance > 0:
                change_copies(modification_list, 2)
                print("Final books to add:", modification_list)
                order_list.extend(modification_list)
                print("Updated order list:", order_list)
                order_str = ','.join(order_list)
                user_df.loc[position, "orders"] = order_str
                user_df.loc[position, "balance"] = balance
                user_df.to_csv('user.csv', index=False, header=None, sep=';')
            else:
                print("Insufficient balance to add these books.")
def add_favorites(position):
   
    favorites_str = str(user_df['favorites'][position])
    favorites_list = favorites_str.split(',')
    print("the books you have in favorites: ",favorites_list)
    modification = input("enter book/books you would like to favorite(with , ): ")
    modification_list = modification.split(',')
    favorites_list=set(favorites_list)
    modification_list = set(modification_list)
    common_books=favorites_list.intersection(modification_list)
    print("koina",common_books)
    modification_list=[book for book in modification_list if book not in common_books]
    modification_list=list(modification_list)
    print(modification_list)
    favorites_list = list(favorites_list)+(modification_list)
    print(favorites_list)
    favorites_list = ','.join(favorites_list)
    user_df.loc[position,"favorites"]=favorites_list
    user_df.to_csv('user.csv',index=False,header=None,sep=';')
def suggestions(position):
    
    favorites_str = str(user_df['favorites'][position])
    favorites_list = [item.strip() for item in favorites_str.split(',') if item.strip() and item.strip() != 'nan']
    orders_str = str(user_df['orders'][position])
    orders_list = [item.strip() for item in orders_str.split(',') if item.strip() and item.strip() != 'nan']
    
    favorites_list=set(favorites_list)
    print("favorites",favorites_list)
    orders_list = set(orders_list)
    print("orders",orders_list)
    common_books=favorites_list.intersection(orders_list)
    books_for_send=[book for book in orders_list if book not in common_books]
    books_for_send=list(books_for_send)
    books_for_send = books_for_send+list(favorites_list)
    print("book for send",books_for_send)
    suggestion_books(books_for_send)
    
def delete_user(user_df, username):
    #global user_df  # Δηλώνουμε ότι θέλουμε να χρησιμοποιήσουμε την global μεταβλητή
    
    # Ελέγχουμε αν ο χρήστης υπάρχει
    if username not in user_df['username'].values:
        print(f"Ο χρήστης '{username}' δεν βρέθηκε.")
        return
    
    # Διαγραφή του χρήστη
    user_df = user_df[user_df['username'] != username]
    print(f"Ο χρήστης '{username}' διαγράφηκε επιτυχώς.")
    
    # Επαναφορά του index του DataFrame
    user_df = user_df.reset_index(drop=True)
    
    # Αποθήκευση των αλλαγών στο CSV αρχείο
    user_df.to_csv('user.csv', index=False, header=False, sep=';')
    print("Το αρχείο ενημερώθηκε επιτυχώς.")

def delete_user_menu():
    #global user_df  # Δηλώνουμε ότι θέλουμε να χρησιμοποιήσουμε την global μεταβλητή
    
    while True:
        username = input("Εισάγετε το username του χρήστη που θέλετε να διαγράψετε (ή 'q' για έξοδο): ")
        if username.lower() == 'q':
            break
        
        delete_user(user_df, username)
        
def review(position):
    orders_str = str(user_df['orders'][position])
    print("your orders:",orders_str)
    choice = int(input("choice a book:"))
    reviews_df= load_reviews()
    id_user=int(user_df['id'][position])
    user_review_book(id_user,choice,reviews_df)
    
    
        
    
    
    
    
    
    
                
            
            
            
        
        
        
     