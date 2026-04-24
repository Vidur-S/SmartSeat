# models/user.py
from model import db
from datetime import datetime


class Division(db.Model):
    __tablename__ = "Division"
 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
 
    # Total number of employees in this division
    div_capacity = db.Column(db.Integer, nullable=False)
 
    # Max number of people from this division that can be assigned to a single session
    per_session = db.Column(db.Integer, nullable=False)
 
    # One division can have many coordinators
    coordinators = db.relationship("Coordinators", back_populates="division", lazy=True)
 
    def __repr__(self):
        return f"<Division {self.name}>"
    
class Sessions(db.Model):
    __tablename__ = "Sessions"
 
    id = db.Column(db.Integer, primary_key=True)
    session_name = db.Column(db.String(120), nullable=False, unique=True)
 
    # Fixed business rule: a session holds at most 20 people total
    max_capacity = db.Column(db.Integer, nullable=False, default=20)
 
    start_time   = db.Column(db.DateTime, nullable=False)
    end_time     = db.Column(db.DateTime, nullable=False)
 
    # Max number of participants allowed from any single division in this session
    max_per_division = db.Column(db.Integer, nullable=False)
 
    # One session can have many coordinators assigned to it
    coordinators = db.relationship("Coordinators", back_populates="session", lazy=True)
 
    def __repr__(self):
        return f"<Session {self.session_name}>"   
    
    
class Coordinators(db.Model):
    __tablename__ = "Coordinators"
 
    id          = db.Column(db.Integer, primary_key=True)
    username    = db.Column(db.String(80), nullable=False, unique=True)
    email       = db.Column(db.String(120), nullable=False, unique=True)
    password    = db.Column(db.String(256), nullable=False)  # Always store hashed, never plaintext
 
    # employee_id is just a reference number — it doesn't FK into another table unless you have an Employee model
    employee_id = db.Column(db.Integer, nullable=False, unique=True)
 
    # Foreign keys — these store the actual id values linking to Division and Sessions
    division_id = db.Column(db.Integer, db.ForeignKey("Division.id"), nullable=False)
    session_id  = db.Column(db.Integer, db.ForeignKey("Sessions.id"), nullable=True)  # nullable: coordinator may not be assigned yet
 
    # Relationships — lets you do coordinator.division or coordinator.session directly in code
    division = db.relationship("Division", back_populates="coordinators")
    session  = db.relationship("Sessions", back_populates="coordinators")
 
    def __repr__(self):
        return f"<Coordinator {self.username}>"
    
   