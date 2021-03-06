from app import db
from sqlalchemy.orm import backref

class Client(db.Model):
    id = db.Column(db.Text, primary_key=True, autoincrement=False) # this gets generated by Firestore
    email = db.Column(db.String, unique=True, nullable=False)
    display_name = db.Column(db.Text)
    decks = db.relationship("Deck", backref="client", lazy=True)

    def to_json(self):
        return {
            "displayName": self.display_name,
            "id": self.id,
            "email": self.email
        }  
