import json
import requests
import sqlite3
import os

#nytimes API (used to get a list of authors that will be used as a parameter for the google books API url)
#creates and returns a list of authors from the nytimes best sellers fiction list
def getAuthors():
    nytimes_API_KEY = "TT4lVTDwP83jPzu8lNVSclqZFuGFVN97"

    nytimes_url = "https://api.nytimes.com/svc/books/v3/lists/current/hardcover-fiction.json?api-key=" + nytimes_API_KEY 
    nytimes_response = requests.get(nytimes_url)
    nytimes = json.loads(nytimes_response.text)          

    nytimes_authors_list = []
    if len(nytimes) > 0:
        nytimes_dict = nytimes.get("results", None)
        for book in nytimes_dict['books']:
            author = book['author']
            #some books had two authors
            if ' and ' in author:
                a = author.split(" and ")
                for i in a:
                    if i not in nytimes_authors_list:
                        nytimes_authors_list.append(i)
            else:
                if author not in nytimes_authors_list:
                    nytimes_authors_list.append(author)

    #nytimes_authors_list = ['Delia Owens', 'Elizabeth Wetmore', 'Jeanine Cummins', 'Harlan Coben', 'James Patterson', 'Andrew Bourelle', 'Alex Michaelides', 'Emily St John Mandel', 'Hilary Mantel', 'Jojo Moyes', 'Louise Erdrich', 'Ann Patchett', 'Terry McMillan', 'Rebecca Serle', 'Kiley Reid', 'James O Born']   
    return nytimes_authors_list


#google books API
#function takes in 1 parameter: a list of authors that will be returned by getAuthors()
#returns google_dic, which will consists of information for each author (the books and their individual average ratings)
def getBooks(authors):
    google_API_KEY = "AIzaSyDbbi5i8xygn2zpnJL4uQUhAu2xzwzWGmI"

    google_dic = {}
    for author in authors:
        author_books = {}
        google_url = "https://www.googleapis.com/books/v1/volumes?q=inauthor:" + author + "&key=" + google_API_KEY
        google_response = requests.get(google_url)
        google = json.loads(google_response.text)
        g_dict = google.get("items", None)
        for book_list in g_dict:
            book = book_list['volumeInfo']['title']
            if 'averageRating' in book_list['volumeInfo']:
                book_rating = book_list['volumeInfo']['averageRating']
            else:
                #some books did not have a rating
                book_rating = "NA"
            ratingAndId = {}
            ratingAndId['id'] = book_list['id']
            ratingAndId['rating'] = book_rating
            author_books[book] = ratingAndId
        google_dic[author] = author_books
    return google_dic


#set up database
def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn


#create an Authors table of authors and the author's id
#create the Books table
def createTables(cur):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Authors (
            id INTEGER PRIMARY KEY, 
            name TEXT
        )
        """)
     
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Books (
        id TEXT PRIMARY KEY, 
        author_id INTEGER,
        book TEXT,
        rating INTEGER
    )
    """)


#function takes in 1 parameter: a list of authors that will be returned by getAuthors()
#inserts the item into the table only if it is not already found in the table  
def addToAuthorsTable(authors,cur,conn):
    a_id = 0
    for author in authors:
        if a_id >= 20:
            print('Retrieved 20 authors, restart to retrieve more')
            break
        cur.execute("SELECT id FROM Authors WHERE name = ?", (author, ))
        try:
            data = cur.fetchone()[0]
            continue
        except:
            pass
        cur.execute('INSERT INTO Authors (id,name) VALUES (?,?)', (a_id,author))
        a_id += 1 
    
    conn.commit()


#parameter is a dictionary that consists of information for each author (the books and their individual average ratings)
#count keeps track of the number of items that are being inserted into the database
#inserts 20 items at a time into the database
#inserts the item into the table only if it is not already found in the table
#selects author id from the Authors table
def addToBooksTable(data,cur,conn):
    count = 0
    for author in data:
        if count >= 20:
            print('Retrieved 20 books, restart to retrieve more')
            break
        for title in data[author]:
            if count >= 20:
                break
            book = title
            bookID = data[author][title]['id']

            cur.execute("SELECT id FROM Books WHERE book = ?", (book, ))
            try:
                info = cur.fetchone()[0]
                continue
            except:
                pass

            bookRating = data[author][title]['rating']
            cur.execute('SELECT id FROM Authors WHERE name = ? ', (author, ))
            author_id = cur.fetchone()[0]
            cur.execute('INSERT INTO Books (id,author_id,book,rating) VALUES (?,?,?,?)', (bookID,author_id,book,bookRating))
            count += 1

    conn.commit()


#run main until there is no output shown 
def main():
    authors = getAuthors()
    google_dic = getBooks(authors)
    cur, conn = setUpDatabase('masterDB.db')
    createTables(cur)
    addToAuthorsTable(authors,cur,conn)
    addToBooksTable(google_dic,cur,conn)

if __name__ == "__main__":
    main()