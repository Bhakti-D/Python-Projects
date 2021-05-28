# doing necessary imports

from flask import Flask, render_template, request,jsonify
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq

app = Flask(__name__)  # initialising the flask app with the name 'app'

@app.route('/', methods=['GET'])
def homepage():
    return render_template('index.html')

# base url + /
#http://localhost:8000 + /
@app.route('/scrap',methods=['POST']) # route with allowed methods as POST and GET
def index():
    if request.method == 'POST':
        searchString = request.form['content'].replace(" ","") # obtaining the search string entered in the form
        try:
            flipkart_url = "https://www.flipkart.com/search?q=" + searchString # preparing the URL to search the product on flipkart
            uClient = uReq(flipkart_url) # requesting the webpage from the internet
            flipkartPage = uClient.read() # reading the webpage
            uClient.close() # closing the connection to the web server
            flipkart_html = bs(flipkartPage, "html.parser") # parsing the webpage as HTML
            bigboxes = flipkart_html.findAll("div", {"class": "_1AtVbE col-12-12"}) # seacrhing for appropriate tag to redirect to the product link
            del bigboxes[0:3] # the first 3 members of the list do not contain relevant information, hence deleting them.
            box = bigboxes[0] #  taking the first iteration (for demo)
            productLink = "https://www.flipkart.com" + box.div.div.div.a['href'] # extracting the actual product link
            prodRes = requests.get(productLink) # getting the product page from server
            prod_html = bs(prodRes.text, "html.parser") # parsing the product page as HTML
            commentboxes = prod_html.find_all('div', {'class': "col _2wzgFH"}) # finding the HTML section containing the customer comments

 
            reviews = [] # initializing an empty list for reviews
            #  iterating over the comment section to get the details of customer and their comments
            for commentbox in commentboxes:
                try:
                    name_extracted = commentbox.find("p", class_="_2sc7ZR _2V5EHH")
                    name = name_extracted.text

                except:
                    name = 'No Name'

                try:
                    rating_extracted = commentbox.find("div", class_="_3LWZlK _1BLPMq")
                    rating = rating_extracted.text


                except:
                    rating = 'No Rating'

                try:
                    commentHead_extracted = commentbox.find("p", class_="_2-N8zT")
                    commentHead = commentHead_extracted.text

                except:
                    commentHead = 'No Comment Heading'
                try:
                    comtag = commentbox.find("div", class_="t-ZTKy")
                    custComment = comtag.text

                except:
                    custComment = 'No Customer Comment'
                
                mydict = {"Product": searchString, "Name": name, "Rating": rating, "CommentHead": commentHead,
                          "Comment": custComment} # saving that detail to a dictionary
                
                reviews.append(mydict) #  appending the comments to the review list
            return render_template('results.html', reviews=reviews) # showing the review to the user
        except:
            return 'something is wrong'



if __name__ == "__main__":
    app.run(port=8000,debug=True) # running the app on the local machine on port 8000
