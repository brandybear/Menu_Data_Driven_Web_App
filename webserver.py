__author__ = 'Brandybear'

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

# import CRUD operations from Lesson 1
from database_setup import Base, Restaurant, MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# create session and connect to DB
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith('/restaurants'):
                restaurants = session.query(Restaurant).all()
                self.send_response(200)
                self.send_header('content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "<a href = 'restaurants/new'>Make a new restaurant here</a>"
                output += "</br></br>"
                for restaurant in restaurants:
                    output += restaurant.name
                    output += "</br>"
                    output += "<a href = '/%s/edit'>Edit</a>" % restaurant.id
                    output += "</br>"
                    output += "<a href = '/%s/delete'>Delete</a>" % restaurant.id
                    output += "</br></br></br>"

                output += "</body></html>"
                self.wfile.write(output)
                return

            if self.path.endswith('/new'):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()


                output = ""
                output += "<html><body>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants'>
                    <h2> Make a new restaurant here </h2>
                    <input name ='restaurant' type='text'>
                    <input type ='submit' value='Create'>
                    </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                return

            if self.path.endswith('/edit'):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                restaurantIDPath = self.path.split("/")[1]
                myRestaurant = session.query(Restaurant).filter_by(id=restaurantIDPath).one()

                output = ""
                output += "<html><body>"
                output += '''<form method='POST' enctype='multipart/form-data' action='%(1)s/edit'>
                    <h2> Edit %(2)s here </h2>
                    <input name ='newRestaurantName' type='text'>
                    <input type ='submit' value='Rename'>
                    </form>''' % {"1": myRestaurant.id, "2": myRestaurant.name}
                output += "</body></html>"
                self.wfile.write(output)
                return

            if self.path.endswith('/delete'):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                restaurantIDPath = self.path.split("/")[1]
                myRestaurant = session.query(Restaurant).filter_by(id=restaurantIDPath).one()

                output = ""
                output += "<html><body>"
                output += '''<form method='POST' enctype='multipart/form-data' action='%(1)s/delete'>
                    <h2> Are you sure you want to delete %(2)s? </h2>
                    <input type ='submit' value='Delete'>
                    ''' % {"1": myRestaurant.id, "2": myRestaurant.name}
                output += "</form><a href='/restaurants'><button>Cancel</button></a>"
                output += "</body></html>"
                self.wfile.write(output)
                return

            if self.path.endswith('/hello'):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "Hello!"
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'>
                    <h2>What would you like me to say?</h2>
                    <input name='message' type='text'>
                    <input type='submit' value='Submit'>
                    </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith('/hola'):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body> &#161 Hola !"
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'>
                    <h2>What would you like me to say?</h2>
                    <input name='message' type='text'>
                    <input type='submit' value='Submit'>
                    </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

        except IOError:
            self.send_error(404, "File Not Found %s" % self.path)

    def do_POST(self):
        try:

            if self.path.endswith('/restaurants'):
                ctype, pdict = cgi.parse_header(self.headers.getheader('Content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)

                    new_name = fields.get('restaurant')[0] # TODO: checkfor length of array

                    new_restaurant = Restaurant(name=new_name)

                    session.add(new_restaurant)

                    session.commit()

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()

            if self.path.endswith('/edit'):
                ctype, pdict = cgi.parse_header(self.headers.getheader('Content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)

                    rename = fields.get('newRestaurantName')[0]
                    restaurantIDPath = self.path.split("/")[1]

                    myRestaurantQuery = session.query(Restaurant).filter_by(id = restaurantIDPath).one()

                    myRestaurantQuery.name = rename

                    session.add(myRestaurantQuery)

                    session.commit()

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()


            if self.path.endswith('/delete'):
                ctype, pdict = cgi.parse_header(self.headers.getheader('Content-type'))
                if ctype == 'multipart/form-data':

                    restaurantIDPath = self.path.split("/")[1]

                    myRestaurantQuery = session.query(Restaurant).filter_by(id = restaurantIDPath).one()

                    session.delete(myRestaurantQuery)
                    session.commit()

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()

        except IOError:
            pass


    # def do_POST(self):
    #     try:
    #         self.send_response(301)
    #         self.end_headers()
    #
    #         ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
    #         if ctype == 'multipart/form-data':
    #             fields = cgi.parse_multipart(self.rfile, pdict)
    #             messagecontent = fields.get('message')
    #
    #         output = ""
    #         output += "<html><body>"
    #         output += "<h2> Okay, how about this: </h2>"
    #         output += "<h1> %s </h1>" % messagecontent[0]
    #
    #         output += '''<form method='POST' enctype='multipart/form-data' action='/hello'>
    #                 <h2>What would you like me to say?</h2>
    #                 <input name='message' type='text'>
    #                 <input type='submit' value='Submit'>
    #                 </form>'''
    #         output += "</body></html>"
    #         self.wfile.write(output)
    #         print output
    #
    #     except IOError:
    #         pass

def main():

    try:
        port = 8080
        server = HTTPServer(('',port), webserverHandler)
        print "Web server running on port %s" % port
        server.serve_forever()

    except KeyboardInterrupt:
        print "^C entered, stopping web server..."
        server.socket.close()

if __name__ == '__main__':
        main()