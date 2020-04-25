import json
import requests
import os
import sqlite3
import matplotlib
import matplotlib.pyplot as plt


#sets up database
def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn


#calculates the average rating for each author
#only include books that have a rating (some books don't have that information available)
#author_averageRating is a list of (author,average rating) tuples
#returns a sorted list of tuples from highest average rating to lowest average rating
def calculation(cur):
    cur.execute("SELECT id,name FROM Authors")
    author_info = cur.fetchall()
    author_averageRating = []

    for author in author_info:
        ID = author[0]
        name = author[1]
        cur.execute("SELECT rating FROM Books WHERE author_id = ?", (ID, ))
        ratings = cur.fetchall()
        book_ratings = 0.0
        num_books = 0

        for rating in ratings:
            rating = rating[0]
            if rating != 'NA':
                num_books += 1
                book_ratings += float(rating)
                average_rating = round(book_ratings/num_books,1)
        t = (name,average_rating)
        author_averageRating.append(t)

    book_data = sorted(author_averageRating, key = lambda x : x[1], reverse = True)

    return book_data


#write the calculations into a file
def writeToFile(data):
    dir = os.path.dirname(__file__)
    f = open(os.path.join(dir, "average_rating_calculations.csv"), "w")
    f.write('Author,Average Rating\n')
    for pair in data:
        f.write(pair[0] + ", " + str(pair[1]))
        f.write('\n')
    f.close()
    

#VISUALIZATION
def visualization(data):
    figsize = (13, 5)
    fig = plt.figure(figsize=figsize,dpi=100)
    fig.suptitle('NYT Best Sellers Fiction Authors')

    #plot for top 5 authors
    ax1 = fig.add_subplot(121)
    lst1 = []
    lst1_val = []
    colors = ['blue','yellow','pink','red','green']
    i = 0
    for pair in data[:5]:
        ax1.barh(pair[0], pair[1], color=colors[i])
        #adds author names to list
        lst1.append(pair[0])
        #adds average ratings to a list
        lst1_val.append(pair[1])
        i += 1

    #plot for bottom 5 authors 
    ax2 = fig.add_subplot(122)
    lst2 = []
    lst2_val = []
    i = 0
    for pair in data[-5:]:
        ax2.barh(pair[0], pair[1], color=colors[i])
        #adds author names to list
        lst2.append(pair[0])
        #adds average ratings to a list
        lst2_val.append(pair[1])
        i += 1

    ax1.set_yticklabels((lst1[0],lst1[1],lst1[2],lst1[3],lst1[4]))
    ax2.set_yticklabels((lst2[0],lst2[1],lst2[2],lst2[3],lst2[4]))

    #adds text to the individual bars to show value
    for index, value in enumerate(lst1_val):
        ax1.text(value, index, str(value))
    for index, value in enumerate(lst2_val):
        ax2.text(value, index, str(value))

    #scale for x axis
    ax1.set(xlim=(0.0, 5.0))
    ax2.set(xlim=(0.0, 5.0))

    # set the x and y axis labels and the title
    ax1.set(ylabel='Author', xlabel='Average Rating', title='Top 5 Authors')
    ax2.set(ylabel='Author', xlabel='Average Rating', title='Bottom 5 Authors')

    #adjusting the layout for the bar graphs 
    fig.subplots_adjust(left=.15, bottom=.11, right=.98, top=.88, wspace=.52, hspace=.2)
 
    # save the figure
    fig.savefig("authors.png",dpi=300)
    plt.show()

#run main to write calculations to a file and display a plot
def main():
    cur, conn = setUpDatabase("masterDB.db")
    result = calculation(cur)
    writeToFile(result)
    visualization(result)


if __name__ == "__main__":
    main()