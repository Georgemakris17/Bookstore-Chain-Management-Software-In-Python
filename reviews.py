import pandas as pd
import ast
import os

# Φόρτωση των DataFrames
books_df = pd.read_csv('books.csv', names=['id', 'title', 'author', 'publisher', 'categories', 'cost', 'shipping_cost', 'availability', 'copies', 'bookstores'], header=None, sep=';')
admin_df = pd.read_csv('admin.csv', names=['id', 'username', 'password', 'bookstores'], header=None, sep=';')
user_df = pd.read_csv('user.csv', names=['id', 'username', 'password', 'address', 'city', 'orders', 'favorites', 'balance'], header=None, sep=';')

# Φόρτωση ή δημιουργία του DataFrame για τις αξιολογήσεις
def load_reviews():
    try:
        reviews_df = pd.read_csv('book_reviews.csv', sep=';', dtype={
            'book_id': int,
            'user_id': int,
            'rating': float,
            'comment': str
        })
        if reviews_df.empty:
            reviews_df = pd.DataFrame(columns=['book_id', 'user_id', 'rating', 'comment'])
    except (pd.errors.EmptyDataError, FileNotFoundError):
        reviews_df = pd.DataFrame(columns=['book_id', 'user_id', 'rating', 'comment'])
    return reviews_df

def save_reviews(reviews_df):
    reviews_df.to_csv('book_reviews.csv', index=False, sep=';')

def user_review_book(user_id, book_id, reviews_df):
    # Έλεγχος αν ο χρήστης έχει το βιβλίο στις παραγγελίες του
    user_orders = user_df.loc[user_df['id'] == user_id, 'orders'].iloc[0]
    
    if pd.isna(user_orders):
        print("Δεν έχετε καμία παραγγελία.")
        return reviews_df
    
    if isinstance(user_orders, str):
        try:
            user_orders = ast.literal_eval(user_orders)
        except (ValueError, SyntaxError):
            print("Σφάλμα στη μορφή των παραγγελιών.")
            return reviews_df
    
    if not isinstance(user_orders, (list, tuple)):
        print("Μη έγκυρη μορφή παραγγελιών.")
        return reviews_df
    
    if book_id not in user_orders:
        print("Δεν μπορείτε να αξιολογήσετε αυτό το βιβλίο καθώς δεν το έχετε παραγγείλει.")
        return reviews_df

    # Έλεγχος αν υπάρχει ήδη αξιολόγηση από τον ίδιο χρήστη για το ίδιο βιβλίο
    existing_review = reviews_df[(reviews_df['user_id'] == user_id) & (reviews_df['book_id'] == book_id)]
    
    # Λήψη βαθμολογίας και σχολίων
    while True:
        try:
            rating = float(input("Δώστε τη βαθμολογία σας (1-5): "))
            if 1 <= rating <= 5:
                break
            else:
                print("Η βαθμολογία πρέπει να είναι μεταξύ 1 και 5.")
        except ValueError:
            print("Παρακαλώ εισάγετε έναν έγκυρο αριθμό.")
    comment = input("Προσθέστε τα σχόλιά σας (προαιρετικά): ")
    
    if not existing_review.empty:
        # Ενημέρωση υπάρχουσας αξιολόγησης
        index = existing_review.index[0]
        reviews_df.loc[index, 'rating'] = rating
        reviews_df['comment'] = reviews_df['comment'].astype(object)  # Μετατροπή σε object
        reviews_df.loc[index, 'comment'] = comment
        print("Η προηγούμενη αξιολόγησή σας ενημερώθηκε επιτυχώς.")
    else:
        # Προσθήκη νέας αξιολόγησης
        new_index = len(reviews_df)
        reviews_df.loc[new_index] = [book_id, user_id, rating, comment]
        print("Η νέα αξιολόγησή σας καταχωρήθηκε επιτυχώς.")
    
    save_reviews(reviews_df)
    return reviews_df

def admin_manage_reviews(admin_id, reviews_df):
    # Έλεγχος αν ο χρήστης είναι admin
    if admin_id not in admin_df['id'].values:
        print("Δεν έχετε δικαιώματα διαχειριστή.")
        return reviews_df

    # Εμφάνιση όλων των αξιολογήσεων
    for index, book in books_df.iterrows():
        book_reviews = reviews_df[reviews_df['book_id'] == book['id']]
        
        print(f"Βιβλίο: {book['title']} (ID: {book['id']})")
        for index, review in book_reviews.iterrows():
            print(f"  Αξιολόγηση {index}:")
            print(f"    Χρήστης: {review['user_id']}")
            print(f"    Βαθμολογία: {review['rating']}")
            print(f"    Σχόλια: {review['comment']}")
        print()

    # Επιλογή αξιολόγησης για διαγραφή
    book_id = int(input("Εισάγετε το ID του βιβλίου για διαχείριση αξιολογήσεων: "))
    review_index = int(input("Εισάγετε τον αριθμό της αξιολόγησης για διαγραφή: "))

    if review_index in reviews_df.index and reviews_df.loc[review_index, 'book_id'] == book_id:
        reviews_df = reviews_df.drop(review_index)
        print("Η αξιολόγηση διαγράφηκε επιτυχώς.")
        save_reviews(reviews_df)
    else:
        print("Μη έγκυρος αριθμός αξιολόγησης.")

    return reviews_df

#reviews_df =load_reviews()
#user_review_book(2,15,reviews_df)
#admin_manage_reviews(1, reviews_df)