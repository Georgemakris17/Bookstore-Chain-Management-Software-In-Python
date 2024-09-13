import pandas as pd
import matplotlib.pyplot as plt
import ast

def plots():
    # Ανάγνωση των CSV αρχείων με τις κατάλληλες κεφαλίδες
    user_head = ['id', 'username', 'password', 'address', 'city', 'orders', 'favorites', 'balance']
    user_df = pd.read_csv('user.csv', names=user_head, header=None, sep=';')
    
    admin_head = ['id', 'username', 'password', 'bookstores']
    admin_df = pd.read_csv('admin.csv', names=admin_head, header=None, sep=';')
    
    books_head = ['id', 'title', 'author', 'publisher', 'categories', 'cost', 'shipping_cost', 'availability', 'copies', 'bookstores']
    books_df = pd.read_csv('books.csv', names=books_head, header=None, sep=';')
    choice = int(input("1. Αριθμός βιβλίων ανά εκδότη (λαμβάνοντας υπόψη τα αντίτυπα)\n2.Αριθμός βιβλίων ανά εκδότη (μη λαμβάνοντας υπόψη τα αντίτυπα).\n3.Αριθμός βιβλίων ανά συγγραφέα (λαμβάνοντας υπόψη τα αντίτυπα).\n4.Αριθμός βιβλίων ανά συγγραφέα (μη λαμβάνοντας υπόψη τα αντίτυπα)\n5.Αριθμός βιβλίων ανά κατηγορία (μη λαμβάνοντας υπόψη τα αντίτυπα).\n6.Αριθμός βιβλίων ανά κατάστημα (λαμβάνοντας υπόψη τα αντίτυπα).\n7.Κατανομή κόστους διαθέσιμων βιβλίων.\n8.Αριθμός χρηστών ανά πόλη.\n:"))
    if choice==1:
    # Μετατροπή των στηλών από string σε κατάλληλους τύπους δεδομένων (λίστες και λεξικά)
        publisher_copies = books_df.groupby('publisher')['copies'].sum()
        publisher_copies.plot(kind='bar', title='Αριθμός βιβλίων ανά εκδότη (λαμβάνοντας υπόψη τα αντίτυπα)')
        plt.xlabel('Εκδότης')
        plt.ylabel('Αριθμός Βιβλίων')
        plt.show() 
    elif choice ==2:
        publisher_count = books_df['publisher'].value_counts()
        publisher_count.plot(kind='bar', title='Αριθμός βιβλίων ανά εκδότη (μη λαμβάνοντας υπόψη τα αντίτυπα)')
        plt.xlabel('Εκδότης')
        plt.ylabel('Αριθμός Βιβλίων')
        plt.show()
    elif choice ==3:
        author_copies = books_df.groupby('author')['copies'].sum()
        author_copies.plot(kind='bar', title='Αριθμός βιβλίων ανά συγγραφέα (λαμβάνοντας υπόψη τα αντίτυπα)')
        plt.xlabel('Συγγραφέας')
        plt.ylabel('Αριθμός Βιβλίων')
        plt.show()
    elif choice ==4:
        author_count = books_df['author'].value_counts()
        author_count.plot(kind='bar', title='Αριθμός βιβλίων ανά συγγραφέα (μη λαμβάνοντας υπόψη τα αντίτυπα)')
        plt.xlabel('Συγγραφέας')
        plt.ylabel('Αριθμός Βιβλίων')
        plt.show()
    elif choice ==5:
        categories = books_df.explode('categories')
        category_count = categories['categories'].value_counts()
        category_count.plot(kind='bar', title='Αριθμός βιβλίων ανά κατηγορία (μη λαμβάνοντας υπόψη τα αντίτυπα)')
        plt.xlabel('Κατηγορία')
        plt.ylabel('Αριθμός Βιβλίων')
        plt.show()
    elif choice ==6:
        # Μετατροπή του πεδίου 'bookstores' από string σε λεξικό
        books_df['bookstores'] = books_df['bookstores'].apply(ast.literal_eval)
        
        # Δημιουργία λεξικού για αποθήκευση του συνολικού αριθμού βιβλίων ανά κατάστημα
        store_totals = {}
        
        # Υπολογισμός του συνολικού αριθμού βιβλίων για κάθε κατάστημα
        for _, row in books_df.iterrows():
            for store, copies in row['bookstores'].items():
                store_totals[store] = store_totals.get(store, 0) + copies
        
        # Ταξινόμηση των καταστημάτων με βάση τον αριθμό των βιβλίων
        sorted_stores = sorted(store_totals.items(), key=lambda x: x[1], reverse=True)
        
        # Διαχωρισμός των δεδομένων για το γράφημα
        stores = [item[0] for item in sorted_stores]
        book_counts = [item[1] for item in sorted_stores]
        
        # Δημιουργία του γραφήματος
        plt.figure(figsize=(12, 6))
        plt.bar(stores, book_counts)
        plt.title('Αριθμός Βιβλίων ανά Κατάστημα')
        plt.xlabel('Κατάστημα')
        plt.ylabel('Αριθμός Βιβλίων')
        plt.xticks(rotation=45)
        
        # Προσθήκη ετικετών με τον ακριβή αριθμό βιβλίων πάνω από κάθε μπάρα
        for i, v in enumerate(book_counts):
            plt.text(i, v, str(v), ha='center', va='bottom')
        
        plt.tight_layout()
        plt.show()
    elif choice ==7:
        available_books = books_df[books_df['availability']==1]
        available_books['cost'].plot(kind='hist', bins=20, title='Κατανομή κόστους διαθέσιμων βιβλίων')
        plt.xlabel('Κόστος')
        plt.ylabel('Συχνότητα')
        plt.show()
    elif choice ==8:
        city_count = user_df['city'].value_counts()
        city_count.plot(kind='bar', title='Αριθμός χρηστών ανά πόλη')
        plt.xlabel('Πόλη')
        plt.ylabel('Αριθμός Χρηστών')
        plt.show()
    




