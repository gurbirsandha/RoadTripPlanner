from flask import Flask, render_template, url_for, request, redirect
# hello
from flask_sqlalchemy import SQLAlchemy

from map import distance, mappyboi
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///maps.db'
db = SQLAlchemy(app)

class Destination(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dest = db.Column(db.String(200), nullable=False)
    index = db.Column(db.Integer, default=0)
    # distance = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return '<Destination %r>' % self.id

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        destination = request.form['destination']
        destinations = Destination.query.order_by(Destination.index).all()
        # distances = []
        if len(destinations) >= 1:
            # for dest in destinations:
            #     dist_left = distance(dest, destinations[-1])
            #     dest.distance = dist_left
            new_ind = destinations[-1].index + 1
            new_dest = Destination(dest=destination, index=new_ind)
        else:
            new_dest = Destination(dest=destination)
        try:
            db.session.add(new_dest)
            db.session.commit()
            return redirect('/')
        except:
            return 'issue adding dest'
    else:
        destinations = Destination.query.order_by(Destination.index).all()
        
        return render_template('index.html', dests=destinations)

@app.route('/delete/<int:id>', methods = ['GET', 'POST'])
def delete(id):
    dest_delete = Destination.query.get_or_404(id)
    destinations = Destination.query.order_by(Destination.index).all()
    for dest in destinations:
        if dest.index > dest_delete.index:
            dest.index = dest.index - 1
    try:
        db.session.delete(dest_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'there was an issue deleting this destination'

@app.route('/update/<int:id>', methods = ['GET', 'POST'])
def update(id):
    dest_update = Destination.query.get_or_404(id)
    if request.method == 'POST':
        dest_update.dest = request.form['destination']
        try:
            db.session.commit()
            return redirect('/')
        except:
            "issue updating the destination"
    else:
        return render_template('update.html', dest=dest_update)

@app.route('/moveDown/<int:id>', methods = ['GET', 'POST'])
def moveDown(id):
    dest_down = Destination.query.get_or_404(id)
    destinations = Destination.query.order_by(Destination.index).all()
    for dest in destinations:
        if dest.index == dest_down.index + 1:
            dest.index = dest.index - 1
            dest_down.index = dest_down.index + 1
            break
    try:
        db.session.commit()
        return redirect('/')
    except:
        "issue moveDowning the destination"

@app.route('/moveUp/<int:id>', methods = ['GET', 'POST'])
def moveUp(id):
    dest_up = Destination.query.get_or_404(id)
    destinations = Destination.query.order_by(Destination.index).all()
    for dest in destinations:
        if dest.index == dest_up.index - 1:
            dest.index = dest.index + 1
            dest_up.index = dest_up.index - 1
    try:
        db.session.commit()
        return redirect('/')
    except:
        "issue moveUpping the destination"

@app.route('/seeMap', methods = ['GET', 'POST'])
def seeMap():
    destinations = Destination.query.order_by(Destination.index).all()
    if len(destinations) == 0:
        return "You have no destinations yet."
    mappyboi(destinations)
    return render_template('map.html')



if __name__ == '__main__':
    app.run(debug=True)