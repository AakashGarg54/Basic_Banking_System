from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///datebase.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class customer_details(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500), nullable=False)
    emailid = db.Column(db.String(500), nullable=False)
    balance = db.Column(db.Integer, nullable=False)

    def __repr__(self) -> str:
        return f"{self.balance}"


class transfer_history(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    transfer_from = db.Column(db.String(500), nullable=False)
    transfer_to = db.Column(db.String(500), nullable=False)
    amount = db.Column(db.Integer, nullable=False)

    def __repr__(self) -> str:
        return f"{self.transfer_from} to {self.transfer_to} amount = {self.amount}"


@app.route("/transfer/<string:name>", methods=['GET', 'POST'])
def transfer(name):
    row = transfer_history.query.filter_by(transfer_from=name).first()
    allrows = transfer_history.query.filter_by(transfer_from=name).all()
    if row == None:
        return render_template("error-404.html")
    return render_template('transfer.html', cst=row, allrows=allrows)


@app.route("/transfer")
def transfers():
    allrows = transfer_history.query.all()
    return render_template('transfer.html', allrows=allrows, cst="")


@app.route("/customers/<string:name>", methods=['GET', 'POST'])
def customer(name):
    row = customer_details.query.filter_by(name=name).first()
    allrows = customer_details.query.all()
    if request.method == 'POST':
        sno = int(request.form['sno'])
        transfer_to = customer_details.query.filter_by(sno=sno).first()
        amount = int(request.form['Amount'])
        credit = transfer_to.balance + amount
        transfer_to.balance = credit
        transfer_from = row.balance
        debit = transfer_from - amount
        row.balance = debit
        newrow = transfer_history(
            transfer_from=name, transfer_to=transfer_to.name, amount=amount)
        print(newrow)
        db.session.add(newrow)
        db.session.commit()
    return render_template('customer.html', cst=row, allrows=allrows)


@app.route("/customers")
def customers():
    allrows = customer_details.query.all()
    print(allrows)
    return render_template('customers.html', allrows=allrows)


@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/")
def homepage():
    return render_template('homepage.html')


if __name__ == '__main__':
    app.run(debug=True)
