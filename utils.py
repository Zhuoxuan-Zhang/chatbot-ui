import uuid

def generate_session_id():
    return f"session-{uuid.uuid4()}"
