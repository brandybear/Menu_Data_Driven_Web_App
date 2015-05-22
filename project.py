__author__ = 'Brandybear'

from flask import Flask, render_template, url_for, request, redirect
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)
    return render_template('menu.html', restaurant=restaurant, items=items)

    # output = ''
    # for i in items:
    #     output += i.name
    #     output += '</br>'
    #     output += i.price
    #     output += '</br>'
    #     output += i.description
    #     output += '</br></br></br>'
    # return output

#Task 1: Create route for newMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/add_item/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        newItem = MenuItem(name = request.form['name'], restaurant_id = restaurant_id)
        session.add(newItem)
        session.commit()
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))

    else:
        return render_template('add_item.html', restaurant_id=restaurant_id)

    #return "page to create a new menu item.  Task 1 complete!"

#Task 2: Create route for editMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/edit_item/<int:menu_id>/', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    editedItem = session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        session.add(editedItem)
        session.commit()
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))

    else:
        return render_template('edit_item.html', restaurant_id=restaurant_id, menu_id=menu_id, item=editedItem)

    #return "page to edit a new menu item.  Task 2 complete!"

#Task 3: Create a route for deleteMenuItem, function here
@app.route('/restaurants/<int:restaurant_id>/delete_item/<int:menu_id>/')
def deleteMenuItem(restaurant_id, menu_id):
    return "page to delete menu item.  Task 3 complete!"


if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port=5000)
