from flask import Flask,render_template,request,redirect, flash
from flask.signals import request_tearing_down
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField
from wtforms.validators import InputRequired,Email,Length
from flask_bootstrap import Bootstrap

from sqlalchemy.orm import backref

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)
app.config['SECRET_KEY'] = '40928745c948f3f1e67703b23b49b9c5'
Bootstrap(app)





class User(db.Model):
    id =db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(200),unique=True)
    password=db.Column(db.String(200),unique=True)
    email=db.Column(db.String(200),unique=True)

class LoginForm(FlaskForm):
    username=StringField('username',validators=[InputRequired(), Length(min=4, max=15)])
    password=StringField('password',validators=[InputRequired(), Length(min=8, max=80)])
    remember=BooleanField('remember me')

class RegistrationForm(FlaskForm):
    email=StringField('email' , validators=[InputRequired(), Email(message='Invalid email'),Length(max=50)])
    username=StringField('username',validators=[InputRequired(), Length(min=4, max=15)])
    password=StringField('password',validators=[InputRequired(), Length(min=8, max=80)])

class Customer(db.Model):
    customer_ID=db.Column(db.Integer , primary_key=True)
    customer_name=db.Column(db.String(200) , nullable=False)
    Address=db.Column(db.Text , nullable=False)
    Membership_category=db.Column(db.String(10) , nullable=False)
    Painting_info=db.Column(db.Integer , nullable=False)
    Payment_details=db.Column(db.Integer , nullable=False)
 
    def __repr__(self):
        return str(self.customer_ID)

class Discount(db.Model):
    id=db.Column(db.Integer , primary_key=True)
    customer_ID=db.Column(db.Integer , db.ForeignKey('customer.customer_ID'))
    Membership_category=db.Column(db.String(10) , nullable=False)
    discount=db.Column(db.Integer , nullable=False)
    
    def __repr__(self):
        return str(self.id)    
        
class Owner_info(db.Model):
    owner_ID=db.Column(db.Integer , primary_key=True)
    owner_name=db.Column(db.String(200) , nullable=False)
    Address=db.Column(db.Text , nullable=False)
    Submitted=db.Column(db.Integer , nullable=False)
    Returned=db.Column(db.Integer , nullable=False)

    def __repr__(self):
        return str(self.owner_ID)   

class employee(db.Model):
    emp_ID=db.Column(db.Integer , primary_key=True)
    emp_name=db.Column(db.String(200) , nullable=False)
    Address=db.Column(db.Text , nullable=False)
    Position=db.Column(db.Integer , nullable=False)

    def __repr__(self):
        return str(self.emp_ID)
    

with app.app_context():
    db.create_all()


@app.route('/', methods=['GET','POST'])
def Login():
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(username=form.username.data).first()
        if user:
            if user.password==form.password.data:
                return redirect('/home')
        flash("Invalid Email or Password")
        return render_template('Login.html',form=form)    

    return render_template('Login.html',form=form)    

@app.route('/signup', methods=['GET','POST'])
def Signup():
    form=RegistrationForm()
    if form.validate_on_submit():
        new_user=User(username=form.username.data, password=form.password.data, email=form.email.data)
        db.session.add(new_user)
        db.session.commit()
        flash("Signup Success")
        return redirect("/")
    return render_template('signup.html',form=form)        

@app.route('/home')
def home():
    return render_template('home.html')                             

@app.route('/customer',methods=['GET','POST'])
def customer():

    if request.method=='POST':
        c_id=request.form['cust_id']
        c_name=request.form['name']
        c_add=request.form['address']
        mem_cat=request.form['member']
        paint_info=request.form['info']
        pay=request.form['details']
        post=Customer(customer_ID=c_id,customer_name=c_name,Address=c_add,Membership_category=mem_cat,Painting_info=paint_info,Payment_details=pay)
        db.session.add(post)
        db.session.commit()
        return redirect('/customer')

    else:
        all_posts= Customer.query.all()
        return render_template('Customer.html',posts=all_posts) 

@app.route('/customer/delete/<int:id>')
def delete(id):
    b=Customer.query.get_or_404(id)
    db.session.delete(b)
    db.session.commit()
    return redirect('/customer')

@app.route('/customer/update/<int:id>',methods=['GET','POST'])
def update(id):
    post=Customer.query.get_or_404(id)
    if request.method == 'POST': 
        post.customer_name=request.form['name']
        post.Address=request.form['address']
        post.Membership_category=request.form['member']
        post.Painting_info=request.form['info']
        post.Payment_details=request.form['details']
        db.session.commit()
        return redirect('/customer')
    else:
        return render_template('edit.html',post=post)    


@app.route('/discount',methods=['GET','POST'])
def discount():

    if request.method=='POST':
        c_id=request.form['id']
        mem_cat=request.form['category']
        Dis=request.form['discount']
        Customer_Name=request.form['name']
        dis= Discount(id=c_id,customer_ID=Customer_Name,Membership_category=mem_cat,discount=Dis)
        db.session.add(dis)
        db.session.commit()
        return redirect('/discount')

    else:
        all_posts= Discount.query.all()
        return render_template('Discount.html',posts=all_posts)   

@app.route('/discount/delete/<int:id>')
def Delete(id):
    b=Discount.query.get_or_404(id)
    db.session.delete(b)
    db.session.commit()
    return redirect('/discount')         

@app.route('/discount/update/<int:id>',methods=['GET','POST'])
def updateDiscount(id):
    post=Discount.query.get_or_404(id)
    if request.method == 'POST': 
        post.Membership_category=request.form['category']
        post.discount=request.form['discount']
        db.session.commit()
        return redirect('/discount')
    else:
        return render_template('editDiscount.html',post=post)

@app.route('/owner',methods=['GET','POST'])
def owner():

    if request.method=='POST':
        c_id=request.form['o_id']
        name=request.form['name']
        Address=request.form['address']
        submit=request.form['s']
        returned=request.form['r']
        post=Owner_info(owner_ID=c_id,owner_name=name,Address=Address,Submitted=submit,Returned=returned)
        db.session.add(post)
        db.session.commit()
        return redirect('/owner')

    else:
        all_posts= Owner_info.query.all()
        return render_template('Owner.html',posts=all_posts)       

@app.route('/owner/delete/<int:id>')
def Delete_owner(id):
    b=Owner_info.query.get_or_404(id)
    db.session.delete(b)
    db.session.commit()
    return redirect('/owner')  

@app.route('/owner/update/<int:id>',methods=['GET','POST'])
def Ownerupdate(id):
    post=Owner_info.query.get_or_404(id)
    if request.method == 'POST': 
        post.owner_name=request.form['name']
        post.Address=request.form['address']
        post.Submitted=request.form['s']
        post.Returned=request.form['r']
        db.session.commit()
        return redirect('/owner')
    else:
        return render_template('editOwner.html',post=post)   

@app.route('/employee',methods=['GET','POST'])
def Employee():

    if request.method=='POST':
        id=request.form['e_id']
        e_name=request.form['name']
        e_add=request.form['address']
        pos=request.form['pos']
        post=employee(emp_ID=id,emp_name=e_name,Address=e_add,Position=pos)
        db.session.add(post)
        db.session.commit()
        return redirect('/employee')

    else:
        all_posts= employee.query.all()
        return render_template('employee.html',posts=all_posts) 

@app.route('/employee/delete/<int:id>')
def deleteEmployee(id):
    b=employee.query.get_or_404(id)
    db.session.delete(b)
    db.session.commit()
    return redirect('/employee') 

@app.route('/employee/update/<int:id>',methods=['GET','POST'])
def employeeupdate(id):
    post=employee.query.get_or_404(id)
    if request.method == 'POST': 
        post.Address=request.form['address']
        post.Position=request.form['pos']
        db.session.commit()
        return redirect('/employee')
    else:
        return render_template('editEmployee.html',post=post)                       

  
if __name__=='__main__':
    app.run(debug=True)         

