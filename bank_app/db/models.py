from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Bank(db.Model):
    """
    model for the database.
    """
    __tablename__ = 'banks'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    
    def __init__(self, name, location):
        self.name = name
        self.location = location
    
    def __repr__(self):
        return f"<Bank {self.name} at {self.location}>"
    
    def to_dict(self):
        """
        bank object to dictionary
        """
        return {
            'id': self.id,
            'name': self.name,
            'location': self.location
        }
