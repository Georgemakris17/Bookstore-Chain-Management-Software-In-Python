import pandas as pd
import random
import numpy as np
import ast
head = ['id', 'title', 'author', 'publisher','categories','cost','shipping_cost','availability','copies','bookstores']
# Χρησιμοποιούμε τον χαρακτήρα ";" ως διαχωριστικό στο αρχείο CSV
books_df = pd.read_csv('books.csv', names=head, header=None, sep=';')
def book_fount(list_of_favorites):
   
   list_of_favorites = [int(id_book) for id_book in list_of_favorites]
   for id_book in list_of_favorites:
       if (id_book-1)<len(books_df):
           if books_df['availability'][id_book-1]==1:
               print("the book is available and the cost is:", books_df['cost'][id_book-1],"with id:",id_book)
           else:
              print("the book is unavailable with id:",id_book) 
       else:
           print("the book is unavailable with id:",id_book)
#book_fount([1,10])

def book_cost(list_of_books):
    list_of_books = [int(id_book) for id_book in list_of_books]
    cost_of_books=0
    ###################################################3
    for id_book in list_of_books:
        if (id_book-1)<len(books_df):
            cost_of_books+=(books_df['cost'][id_book-1]+books_df['shipping_cost'][id_book-1])
        
    
    #print(cost_of_books)
    return cost_of_books

def available_book(list_of_books):
    list_of_books = [int(id_book) for id_book in list_of_books]
    available_books_list = []
    for id_book in list_of_books:
        if (id_book-1)<len(books_df):
            if books_df['availability'][id_book-1]>0:
                available_books_list.append(str(id_book))
        
    #print(available_books_list)       
    return available_books_list

def change_copies(list_of_books,choice):
    list_of_books = [int(id_book) for id_book in list_of_books]
    
    for id_book in list_of_books:
        copies=books_df['copies'][id_book-1]
        if choice==1:
            copies+=1
        elif choice ==2:
            copies-=1
        #print(copies)
        books_df.loc[id_book-1,"copies"]=copies
        books_df.to_csv('books.csv',index=False,header=None,sep=';')
    change_available(list_of_books)
    
def change_available(list_of_books):
    list_of_books = [int(id_book) for id_book in list_of_books]
    for id_book in list_of_books:
        if books_df['copies'][id_book-1]>0:
            books_df.loc[id_book-1,"availability"]=1
        else:
            books_df.loc[id_book-1,"availability"]=0
        books_df.to_csv('books.csv',index=False,header=None,sep=';')
def has_common_elements(list1, list2):
    set1 = set(list1)
    set2 = set(list2)
    return len(set1.intersection(set2)) >0
def book_name(list_of_books):
    list_of_books = [int(id_book) for id_book in list_of_books]
    for id_book in list_of_books:
        print("suggest the book/books:",books_df['title'][id_book-1])
def suggestion_books(list_of_books):
    list_of_books = [int(id_book) for id_book in list_of_books]
    list_of_categories = []
    for id_book in list_of_books:
        if (id_book-1)<len(books_df):
            list_of_categories.append(books_df['categories'][id_book-1])
    
    most_common=max(set(list_of_categories),key=list_of_categories.count)
    print(list_of_books)
    print(most_common)
    select_stories = books_df[books_df['categories'].str.contains(most_common, case=False, na=False)]
    print(select_stories['id'].tolist())
    random_books=list(random.sample(select_stories['id'].tolist(), 3))
    print(random_books)
    
    while has_common_elements((random_books), (list_of_books))!=False :
        #print("mpika")
        random_books=list(random.sample(select_stories['id'].tolist(), 3))
    print(random_books)
    book_name(random_books)
    
def find_book_with_name(name_of_book):
    book_name = []
    # Μετατροπή του ονόματος του βιβλίου σε πεζά για σύγκριση
    name_of_book_lower = name_of_book.lower()
    
    # Έλεγχος αν το όνομα του βιβλίου υπάρχει (αγνοώντας κεφαλαία/πεζά)
    if name_of_book_lower in books_df['title'].str.lower().tolist():
        # Εύρεση όλων των βιβλίων που περιέχουν το όνομα (αγνοώντας κεφαλαία/πεζά)
        book = books_df[books_df['title'].str.lower().str.contains(name_of_book_lower, na=False)]
        book_name = book['id'].tolist()
        print(book_name)
    else:
        print("Το βιβλίο δεν είναι διαθέσιμο")
    
    return book_name

def calculate_total_cost():
    # Φιλτράρισμα για διαθέσιμα βιβλία
    available_books = books_df[books_df['availability'] == 1]
    
    choice = int(input("total cost with:\n1.publisher\n2.author\n3.total\n: "))
    
    if choice == 1:
        # Υπολογισμός κόστους ανά εκδότη για διαθέσιμα βιβλία
        total_cost = available_books.groupby('publisher')['cost'].sum()
        total_cost+=available_books.groupby('publisher')['shipping_cost'].sum()
        print("Συνολικό κόστος διαθέσιμων βιβλίων ανά εκδότη:")
        for publisher, cost in total_cost.items():
            print(f"{publisher}: {cost:.2f}")
        
    elif choice == 2:
        # Υπολογισμός κόστους ανά συγγραφέα για διαθέσιμα βιβλία
        total_cost = available_books.groupby('author')['cost'].sum()
        total_cost += available_books.groupby('author')['shipping_cost'].sum()
        print("Συνολικό κόστος διαθέσιμων βιβλίων ανά συγγραφέα:")
        for author, cost in total_cost.items():
            print(f"{author}: {cost:.2f}")
        
    elif choice == 3:
        # Υπολογισμός συνολικού κόστους για διαθέσιμα βιβλία
        total_cost = available_books['cost'].sum()
        total_cost += available_books['shipping_cost'].sum()
        print(f"Συνολικό κόστος όλων των διαθέσιμων βιβλίων: {total_cost:.2f}")
    
    else:
        print("Μη έγκυρη επιλογή.")
def check_book_availability(book_title, bookstores):
    # Εύρεση του βιβλίου με βάση τον τίτλο
    books_df['bookstores'] = books_df['bookstores'].apply(ast.literal_eval)

    book = books_df[books_df['title'].str.lower() == book_title.lower()]
    
    if book.empty:
        print(f"Το βιβλίο '{book_title}' δεν βρέθηκε.")
        return
    
    # Απόκτηση του λεξικού με τα καταστήματα και τις ποσότητες
    book_stores_dict = book['bookstores'].iloc[0]
    
    # Φιλτράρισμα των αποτελεσμάτων για τα συγκεκριμένα καταστήματα
    filtered_stores = {store: copies for store, copies in book_stores_dict.items() if store in bookstores}
    
    # Εμφάνιση των αποτελεσμάτων
    if not filtered_stores:
        print(f"Το βιβλίο '{book_title}' δεν είναι διαθέσιμο στα καταστήματα {bookstores}.")
    else:
        print(f"Διαθεσιμότητα του βιβλίου '{book_title}' στα καταστήματα {bookstores}: {filtered_stores}")
def update_books_df(existing_csv, new_csv):
    # Ορισμός των επικεφαλίδων
    head = ['id', 'title', 'author', 'publisher', 'categories', 'cost', 'shipping_cost', 'availability', 'copies', 'bookstores']
    
    # Ανάγνωση του υπάρχοντος CSV
    existing_df = pd.read_csv(existing_csv, names=head, header=None, sep=';', dtype={'id': str})
    
    # Ανάγνωση του νέου CSV
    new_df = pd.read_csv(new_csv, names=head, header=None, sep=';', dtype={'id': str})
    
    # Δημιουργία ενός dictionary με τα νέα δεδομένα, χρησιμοποιώντας το 'id' ως κλειδί
    new_data_dict = new_df.set_index('id').to_dict('index')
    
    # Ενημέρωση του υπάρχοντος dataframe
    for index, row in existing_df.iterrows():
        if row['id'] in new_data_dict:
            existing_df.loc[index] = new_data_dict[row['id']]
    
    # Προσθήκη νέων βιβλίων που δεν υπάρχουν στο υπάρχον dataframe
    new_books = new_df[~new_df['id'].isin(existing_df['id'])]
    updated_df = pd.concat([existing_df, new_books]).reset_index(drop=True)
    
    # Μετατροπή του 'id' σε ακέραιο αριθμό για σωστή ταξινόμηση
    updated_df['id'] = pd.to_numeric(updated_df['id'], errors='coerce').astype('Int64')
    
    # Αφαίρεση γραμμών με NaN στη στήλη 'id'
    updated_df = updated_df.dropna(subset=['id'])
    
    # Ταξινόμηση με βάση το ID
    updated_df = updated_df.sort_values('id')
    
    # Μετατροπή του 'id' σε string χωρίς δεκαδικά ψηφία
    updated_df['id'] = updated_df['id'].astype(str).str.replace('.0', '', regex=False)
    
    # Επαναφορά του index
    updated_df = updated_df.reset_index(drop=True)
    
    # Αφαίρεση κενών τιμών από το ID
    updated_df['id'] = updated_df['id'].str.strip()
    updated_df = updated_df[updated_df['id'] != '']
    
    # Αποθήκευση του ενημερωμένου dataframe πίσω στο αρχικό CSV
    updated_df.to_csv(existing_csv, index=False, header=False, sep=';')
    
    print(f"Το αρχείο {existing_csv} ενημερώθηκε επιτυχώς.")
    print(f"Συνολικός αριθμός βιβλίων μετά την ενημέρωση: {len(updated_df)}")
def update_books_df_manual(existing_csv):
    # Ορισμός των επικεφαλίδων
    head = ['id', 'title', 'author', 'publisher', 'categories', 'cost', 'shipping_cost', 'availability', 'copies', 'bookstores']
    
    # Ορισμός των τύπων δεδομένων για κάθε στήλη
    dtypes = {
        'id': 'Int64',  # Χρησιμοποιούμε 'Int64' αντί για str
        'title': str,
        'author': str,
        'publisher': str,
        'categories': str,
        'cost': float,
        'shipping_cost': float,
        'availability': str,
        'copies': int,
        'bookstores': str
    }
    
    # Ανάγνωση του υπάρχοντος CSV με τους καθορισμένους τύπους δεδομένων
    existing_df = pd.read_csv(existing_csv, names=head, header=None, sep=';', dtype=dtypes)
    
 
    print("\nΕισάγετε τα στοιχεία του νέου βιβλίου:")
    new_book = {}
    for column in head:
        value = input(f"{column}: ").strip()
        # Μετατροπή της τιμής στον σωστό τύπο δεδομένων
        try:
            if column == 'id':
                new_book[column] = int(value)  # Μετατροπή του ID σε ακέραιο
            else:
                new_book[column] = dtypes[column](value)
        except ValueError:
            print(f"Μη έγκυρη τιμή για {column}. Χρησιμοποιείται κενή τιμή.")
            new_book[column] = None
    
    # Έλεγχος αν το ID υπάρχει ήδη
    if new_book['id'] in existing_df['id'].values:
        print(f"Το βιβλίο με ID {new_book['id']} υπάρχει ήδη. Θα ενημερωθούν τα στοιχεία του.")
        for column in head:
            existing_df.loc[existing_df['id'] == new_book['id'], column] = new_book[column]
    else:
        existing_df = pd.concat([existing_df, pd.DataFrame([new_book])], ignore_index=True)
        print(f"Το βιβλίο με ID {new_book['id']} προστέθηκε επιτυχώς.")
    

# Μετατροπή του 'id' σε ακέραιο αριθμό για σωστή ταξινόμηση
    existing_df['id'] = pd.to_numeric(existing_df['id'], errors='coerce').astype('Int64')

# Αφαίρεση γραμμών με NaN στη στήλη 'id'
    existing_df = existing_df.dropna(subset=['id'])

# Ταξινόμηση με βάση το ID
    existing_df = existing_df.sort_values('id')

# Επαναφορά του index
    existing_df = existing_df.reset_index(drop=True)

# Μετατροπή του 'id' σε string χωρίς δεκαδικά ψηφία
    existing_df['id'] = existing_df['id'].astype(str).str.replace('.0', '', regex=False)

# Αφαίρεση κενών τιμών από το ID
    existing_df['id'] = existing_df['id'].str.strip()
    existing_df = existing_df[existing_df['id'] != '']

# Αποθήκευση του ενημερωμένου dataframe πίσω στο αρχικό CSV
    existing_df.to_csv(existing_csv, index=False, header=False, sep=';')

    print(f"Το αρχείο {existing_csv} ενημερώθηκε επιτυχώς.")
    print(f"Συνολικός αριθμός βιβλίων μετά την ενημέρωση: {len(existing_df)}")

def update_book_details( book_title, user_bookstores):
    def safe_eval_bookstores(bookstores_str):
        if pd.isna(bookstores_str) or bookstores_str == '':
            return {}
        try:
            return ast.literal_eval(bookstores_str)
        except (ValueError, SyntaxError):
            print(f"Προειδοποίηση: Μη έγκυρη τιμή bookstores: {bookstores_str}")
            return {}

# Εύρεση του βιβλίου
    book_index = books_df.index[books_df['title'].str.lower() == book_title.lower()].tolist()
    
    if not book_index:
        print(f"Το βιβλίο '{book_title}' δεν βρέθηκε.")
        return books_df
    
    book_index = book_index[0]
    book = books_df.loc[book_index]
    
    # Ασφαλής μετατροπή του πεδίου 'bookstores' σε λεξικό
    book_stores_dict = safe_eval_bookstores(book['bookstores'])
    
    print(f"Τρέχουσες πληροφορίες του βιβλίου '{book_title}':")
    print(book[['title', 'author', 'publisher', 'categories', 'cost', 'shipping_cost', 'availability', 'copies']])
    print(f"Bookstores: {book_stores_dict}")
    
    # Λίστα των πεδίων που μπορούν να τροποποιηθούν
    fields = ['title', 'author', 'publisher', 'categories', 'cost', 'shipping_cost', 'availability', 'copies']
    
    for field in fields:
        new_value = input(f"Εισάγετε νέα τιμή για {field} (ή πατήστε Enter για να μην αλλάξει): ")
        if new_value:
            if field in ['cost', 'shipping_cost']:
                try:
                    books_df.at[book_index, field] = float(new_value)
                except ValueError:
                    print(f"Μη έγκυρη τιμή για {field}. Παρακαλώ εισάγετε έναν αριθμό.")
                    continue
            elif field in ['copies', 'availability']:
                try:
                    books_df.at[book_index, field] = int(new_value)
                except ValueError:
                    print(f"Μη έγκυρη τιμή για {field}. Παρακαλώ εισάγετε έναν ακέραιο αριθμό.")
                    continue
            else:
                books_df.at[book_index, field] = new_value

# Ενημέρωση του πεδίου 'bookstores'
    print("\nΕνημέρωση αντιτύπων για τα βιβλιοπωλεία:")
    for store in list(book_stores_dict.keys()):  # Χρησιμοποιούμε list() για να αποφύγουμε το RuntimeError
        if int(store) in user_bookstores:
            new_copies = input(f"Εισάγετε νέο αριθμό αντιτύπων για το κατάστημα {store} (τρέχον: {book_stores_dict[store]}, ή πατήστε Enter για να μην αλλάξει): ")
            if new_copies:
                try:
                    book_stores_dict[store] = int(new_copies)
                except ValueError:
                    print(f"Μη έγκυρη τιμή. Ο αριθμός αντιτύπων παραμένει {book_stores_dict[store]}.")
        else:
            print(f"Κατάστημα {store}: {book_stores_dict[store]} αντίτυπα (δεν έχετε πρόσβαση για αλλαγή)")
    
    # Αποθήκευση του ενημερωμένου λεξικού πίσω στο DataFrame ως string
    books_df.at[book_index, 'bookstores'] = str(book_stores_dict)
   

    print("\nΟι πληροφορίες του βιβλίου ενημερώθηκαν επιτυχώς.")
    
    # Εκτύπωση των ενημερωμένων πληροφοριών για επαλήθευση
    print("\nΕνημερωμένες πληροφορίες του βιβλίου:")
    print(books_df.loc[book_index])

    # Αποθήκευση των αλλαγών στο CSV αρχείο
    try:
        books_df.to_csv('books.csv', index=False, header=False, sep=';')
        print("\nΟι αλλαγές αποθηκεύτηκαν επιτυχώς στο αρχείο 'books.csv'.")
    except Exception as e:
        print(f"\nΣφάλμα κατά την αποθήκευση στο CSV: {e}")
    
def delete_book_data(book_title, user_bookstores):
    global books_df  # βεβαιωθείτε ότι το books_df είναι προσβάσιμο μέσα στη συνάρτηση
    
    # Μετατροπή του πεδίου 'bookstores' από string σε λεξικό
    def safe_literal_eval(val):
        if pd.isna(val):
            return {}
        try:
            return ast.literal_eval(val)
        except (ValueError, SyntaxError):
            return {}

    books_df['bookstores'] = books_df['bookstores'].apply(safe_literal_eval)
    
    book_index = books_df.index[books_df['title'].str.lower() == book_title.lower()].tolist()
    
    if not book_index:
        print(f"Το βιβλίο '{book_title}' δεν βρέθηκε.")
        return books_df
    
    book_index = book_index[0]
    book = books_df.loc[book_index]
    book_stores_dict = book['bookstores']
    
    # Έλεγχος αν ο χρήστης έχει πρόσβαση σε όλα τα βιβλιοπωλεία του βιβλίου
    book_stores = set(map(int, book_stores_dict.keys()))
    user_stores = set(user_bookstores)
    
    if not book_stores.issubset(user_stores):
        print(f"Δεν έχετε πρόσβαση σε όλα τα βιβλιοπωλεία για το βιβλίο '{book_title}'.")
        print(f"Βιβλιοπωλεία βιβλίου: {book_stores}")
        print(f"Βιβλιοπωλεία admin: {user_stores}")
        return books_df
    
    # Εμφάνιση πληροφοριών βιβλίου πριν τη διαγραφή των δεδομένων
    print(f"Πληροφορίες του βιβλίου '{book_title}' προς διαγραφή:")
    print(book[['id', 'title', 'author', 'publisher', 'categories', 'cost', 'shipping_cost', 'availability', 'copies']])
    print(f"Bookstores: {book_stores_dict}")
    
    # Επιβεβαίωση διαγραφής
    confirm = input("Είστε σίγουροι ότι θέλετε να διαγράψετε τα δεδομένα αυτού του βιβλίου; (ναι/όχι): ")
    
    if confirm.lower() == 'ναι':
        # Διατήρηση μόνο του id και καθαρισμός των υπόλοιπων πεδίων
        books_df.at[book_index, 'title'] = ''
        books_df.at[book_index, 'author'] = ''
        books_df.at[book_index, 'publisher'] = ''
        books_df.at[book_index, 'categories'] = ''
        books_df.at[book_index, 'cost'] = 0.0
        books_df.at[book_index, 'shipping_cost'] = 0.0
        books_df.at[book_index, 'availability'] = np.nan
        books_df.at[book_index, 'copies'] = 0
        books_df.at[book_index, 'bookstores'] = '{}'
        
        print(f"Τα δεδομένα του βιβλίου με ID {book['id']} διαγράφηκαν επιτυχώς.")
    else:
        print("Η διαγραφή ακυρώθηκε.")
    books_df.to_csv('books.csv', index=False, header=False, sep=';')
    
    return books_df


def update_book_df():
    books_df.to_csv('updated_books.csv', index=False, header=False, sep=';')
# Παράδειγμα χρήσης:
# Ανάγνωση του CSV αρχείου
# Κλήση της συνάρτησης
#user_bookstores = [1, 2, 3]  # Τα βιβλιοπωλεία στα οποία έχει πρόσβαση ο χρήστης
#update_book_details("bat man", user_bookstores)

# Αποθήκευση των αλλαγών πίσω στο CSV αρχείο


# Αποθήκευση των αλλαγών πίσω στο CSV αρχείο
     


#check_book_availability("oneira1", [1,10])  
#available_book([1,10])
#change_copies([1,10],1)
#suggestion_books([1,2,60])
#calculate_total_cost()