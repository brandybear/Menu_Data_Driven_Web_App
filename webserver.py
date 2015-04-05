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
                    output += "<a href = '#'>Edit</a>"
                    output += "</br>"
                    output += "<a href = '#'>Delete</a>"
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
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
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