from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from forms import MembershipForm
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///members.db'
app.config['UPLOAD_FOLDER'] = 'static/images/uploads'
db = SQLAlchemy(app)

class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    father_name = db.Column(db.String(50), nullable=False)
    cnic = db.Column(db.String(13), nullable=False, unique=True)
    phone = db.Column(db.String(15), nullable=False)
    cnic_pic = db.Column(db.String(100), nullable=False)
    profile_pic = db.Column(db.String(100), nullable=False)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/membership', methods=['GET', 'POST'])
def membership():
    form = MembershipForm()
    if form.validate_on_submit():
        # Save the uploaded images
        cnic_pic_filename = secure_filename(form.cnic_pic.data.filename)
        profile_pic_filename = secure_filename(form.profile_pic.data.filename)
        form.cnic_pic.data.save(os.path.join(app.config['UPLOAD_FOLDER'], cnic_pic_filename))
        form.profile_pic.data.save(os.path.join(app.config['UPLOAD_FOLDER'], profile_pic_filename))
        
        # Create and save member info in a .txt file
        user_info_filename = os.path.join(app.config['UPLOAD_FOLDER'], f"{form.name.data}.txt")
        with open(user_info_filename, 'w') as f:
            f.write(f"Name: {form.name.data}\n")
            f.write(f"Father's Name: {form.father_name.data}\n")
            f.write(f"CNIC: {form.cnic.data}\n")
            f.write(f"Phone: {form.phone.data}\n")
        
        # Save the member's details to the database
        new_member = Member(
            name=form.name.data,
            father_name=form.father_name.data,
            cnic=form.cnic.data,
            phone=form.phone.data,
            cnic_pic=cnic_pic_filename,
            profile_pic=profile_pic_filename
        )
        db.session.add(new_member)
        db.session.commit()
        flash('Membership form submitted successfully!', 'success')
        return redirect(url_for('membership'))
    return render_template('membership.html', form=form)

@app.route('/dashboard')
def dashboard():
    members = Member.query.all()
    return render_template('dashboard.html', members=members)

if __name__ == '__main__':
    # Create the database tables
    with app.app_context():
        db.create_all()
    
    app.run()
