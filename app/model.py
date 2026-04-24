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
    # back_populates = "division" -> matches the field name in Participant
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

    # One session has many allocations
    allocations  = db.relationship("Allocation", back_populates="session", lazy=True)

    # Convenience — how many seats are taken
    def allocated_count(self):
        return len(self.allocations)

    # Convenience — how many seats remain
    def remaining_seats(self):
        return self.max_capacity - self.allocated_count()

    # Convenience — is this session full?
    def is_full(self):
        return self.allocated_count() >= self.max_capacity

    def __repr__(self):
        return f"<Session {self.session_name}>"


class Participant(db.Model):
    __tablename__ = "participant"

    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(80), nullable=False)
    email       = db.Column(db.String(120), nullable=False, unique=True)

    # FK → division table
    # This is the owning side — the foreign key column lives here
    division_id = db.Column(db.Integer, db.ForeignKey("division.id"), nullable=False)

    # Relationship — lets you do participant.division to get the Division object
    # back_populates = "participants" → matches the field name in Division
    division    = db.relationship("Division", back_populates="participants")

    # One participant has at most one allocation
    # uselist=False → treat this as a single object, not a list
    allocation  = db.relationship("Allocation", back_populates="participant",
                                  uselist=False)

    # Convenience — has this participant been assigned yet?
    def is_allocated(self):
        return self.allocation is not None

    def __repr__(self):
        return f"<Participant {self.name}>"


class Allocation(db.Model):
    __tablename__ = "allocation"

    id           = db.Column(db.Integer, primary_key=True)
    allocated_at = db.Column(db.DateTime, default=datetime.utcnow)

    # FK -> participant — unique=True enforces one allocation per participant
    # This is constraint 2: a participant can only be assigned to one session
    participant_id = db.Column(db.Integer, db.ForeignKey("participant.id"),
                                nullable=False, unique=True)

    # FK -> session
    session_id     = db.Column(db.Integer, db.ForeignKey("session.id"),
                                nullable=False)

    # Relationships
    participant = db.relationship("Participant", back_populates="allocation")
    session     = db.relationship("Session", back_populates="allocations")

    def __repr__(self):
        return f"<Allocation participant={self.participant_id} session={self.session_id}>"


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