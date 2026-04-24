# models/models.py
from model import db
from datetime import datetime


class Division(db.Model):
    __tablename__ = "division"

    id           = db.Column(db.Integer, primary_key=True)
    name         = db.Column(db.String(80), nullable=False, unique=True)
    div_capacity = db.Column(db.Integer, nullable=False)  # total participants in this division
    per_session  = db.Column(db.Integer, nullable=False)  # max allowed per session

    # One division has many participants
    participants = db.relationship("Participant", back_populates="division", lazy=True)

    def __repr__(self):
        return f"<Division {self.name}>"


class Session(db.Model):
    __tablename__ = "session"

    id           = db.Column(db.Integer, primary_key=True)
    session_name = db.Column(db.String(120), nullable=False, unique=True)
    max_capacity = db.Column(db.Integer, nullable=False, default=20)
    start_time   = db.Column(db.Time, nullable=False)   # Time only — not full DateTime
    end_time     = db.Column(db.Time, nullable=False)



    # Convenience — how many seats remain
    def remaining_seats(self):
        return self.max_capacity - self.allocated_count()

    # Convenience — is this session full?
    def is_full(self):
        return self.allocated_count() >= self.max_capacity

    def __repr__(self):
        return f"<Session {self.session_name}>"
   
class Coordinator(db.Model):
    """
    Admin user who manages the system.
    Does NOT get allocated to sessions 
    """
    __tablename__ = "coordinator"

    id          = db.Column(db.Integer, primary_key=True)
    username    = db.Column(db.String(80), nullable=False, unique=True)
    email       = db.Column(db.String(120), nullable=False, unique=True)
    password    = db.Column(db.String(256), nullable=False)  # store hashed — never plaintext

    def __repr__(self):
        return f"<Coordinator {self.username}>"