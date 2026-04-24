from model import Participant, Session, Allocation
from database import db

SESSION_ORDER = ["morning", "midday", "afternoon"]

dept_limits = {
    "A": 8,
    "B": 6,
    "C": 6
}


def allocate_participant(participant_id):

    participant = Participant.query.get(participant_id)

    if participant.assigned:
        return {"status": "failed", "reason": "Already assigned"}

    for session_name in SESSION_ORDER:

        session = Session.query.filter_by(name=session_name).first()

        # count session usage
        current_count = Allocation.query.filter_by(session_name=session_name).count()

        if current_count >= 20:
            continue

        dept_count = Allocation.query.filter_by(
            session_name=session_name,
            participant_id=participant_id
        ).count()

        if dept_count >= dept_limits[participant.department]:
            continue

        # assign
        allocation = Allocation(
            participant_id=participant.id,
            session_name=session_name
        )

        participant.assigned = True
        participant.session = session_name

        db.session.add(allocation)
        db.session.commit()

        return {
            "status": "success",
            "session": session_name
        }

    return {
        "status": "failed",
        "reason": "No available session"
    }