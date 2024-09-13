import pandas as pd
import time
from books import find_book_with_name,book_fount,book_cost,calculate_total_cost,check_book_availability,update_books_df,update_books_df_manual,update_book_details,delete_book_data,update_book_df
from user import delete_user_menu
from plots import plots
from reviews import load_reviews,admin_manage_reviews

head = ['id', 'username', 'password', 'bookstores']
# Χρησιμοποιούμε τον χαρακτήρα ";" ως διαχωριστικό στο αρχείο CSV
admin_df = pd.read_csv('admin.csv', names=head, header=None, sep=';')
def menu_admin(username,password):
    position=found_line(username, password)
    print(position)
    choice = int(input("1.μεταφόρτωση ενός csv με βιβλία\n2.προσθήκη βιβλιου\n3.τροποποίηση των βιβλίων\n4.διαγραφή στοιχείων απο βιβ΄λία\n5.εξαγωγη csv\n6.ελεγχος βιβλιου(διαθεσιμοτιτα)βάση τίτλου\n7.ελεγχος διαθεσιμότητας ενος βιβλίου σε συγκεκριμένα βιβλιοπωλεία\n8.κόστος ενος βιβλίου\n9.συνολικο κόστος διαθέσιμων βιβλίων\n10.διαγραφή user\n11.plots\n12.reviews\n:"))
    if choice==1:
        existing_csv = 'books.csv'
        new_csv = 'updatebook.csv'
        update_books_df(existing_csv, new_csv)
    elif choice ==2:
        update_books_df_manual('books.csv')
    elif choice == 3:
        name_of_book=input("give me the name of book:")
        bookstore_str = admin_df['bookstores'][position]
        bookstore = list(map(int, bookstore_str.split(',')))
        print(bookstore)
        update_book_details(name_of_book,bookstore)
    elif choice ==4:
        name_of_book=input("give me the name of book:")
        bookstore_str = admin_df['bookstores'][position]
        bookstore = list(map(int, bookstore_str.split(',')))
        print(bookstore)
        delete_book_data(name_of_book,bookstore)
    elif choice ==5:
        update_book_df()
    elif choice == 6:
        name_of_book=input("give me the name of book:")
        id_of_book=find_book_with_name(name_of_book)
        book_fount(id_of_book)
    elif choice == 7:
        name_of_book=input("give me the name of book:")
        bookstore_str = admin_df['bookstores'][position]
        bookstore = list(map(int, bookstore_str.split(',')))
        print(bookstore)
        check_book_availability(name_of_book,bookstore)
    elif choice == 8:
        choice= int(input("1.with id\n2.with title\n:"))
        if choice ==1:
            id_of_book=int(input("give me the id of book:"))
            id_of_book = [id_of_book]
            print("the cost is:",book_cost(id_of_book))
        elif choice ==2:
            name_of_book=input("give me the name of book:")
            id_of_book=find_book_with_name(name_of_book)
            print("the cost is:",book_cost(id_of_book))
    elif choice ==9:
        calculate_total_cost()
    elif choice == 10:
        delete_user_menu()
    elif choice ==11:
        plots()
    elif choice ==12:
        reviews(position)
        
    #print(position)
def admin_login():
    counter=0
    
    
    print(admin_df['bookstores'].tolist())
    while(counter<3):
        username = input("Hello admin\n pleace give your username:")
        password = input("pleace give your password:")
        if username in admin_df['username'].tolist() and password in admin_df['password'].tolist():
            print("login is good")
            counter=5
        else:
            print("login fail")
            counter+=1
            if(counter==3):
                counter=0
                time.sleep(10)
                
    return username,password

def found_line(username, password):

    # Συνδυάζουμε τις συνθήκες για το username και το password
    founder_combined = admin_df.loc[(admin_df['username'] == username) & (admin_df['password'] == password)]
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
def reviews(position):
    reviews_df=load_reviews()
    admin_id = admin_df['id'][position]
    admin_manage_reviews(admin_id,reviews_df)

#admin_login()