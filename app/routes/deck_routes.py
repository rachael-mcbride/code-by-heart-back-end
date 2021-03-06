from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.flashcard import Flashcard
from app.models.deck import Deck
from datetime import datetime

decks_bp = Blueprint("decks_bp", __name__, url_prefix="/decks")

# Get a particular client's decks 
@decks_bp.route("/<owner_id>", methods=["GET"])
def get_deck(owner_id):
    decks = Deck.query.filter_by(owner_id=owner_id)
    decks_response = [deck.to_json() for deck in decks]
    return jsonify(decks_response), 200


# Add a deck to client's decks
@decks_bp.route("/<owner_id>", methods=["POST"])
def add_deck(owner_id):
    request_data = request.get_json()

    new_deck = Deck(
        deck_name=request_data["deck_name"],
        owner_id=owner_id
    )

    db.session.add(new_deck)
    db.session.commit()

    return new_deck.to_json(), 200


# Add a flashcard to a particular deck
@decks_bp.route("/<deck_id>/flashcards", methods=["POST"])
def add_flashcard_to_deck(deck_id):
    request_data = request.get_json()

    flashcard = Flashcard(
        front = request_data['front'],
        back = request_data['back'],
        language = request_data['language'],
        deck_id = int(deck_id),
        difficulty_level = 0,
        previous_repetitions = 0,
        previous_ease_factor = 2.5,
        interval = 0,
        date_to_review = datetime.now(),
        total_times_reviewed = 0
    )

    db.session.add(flashcard)
    db.session.commit()

    return flashcard.to_json(), 200


# Delete a deck 
@decks_bp.route("/<deck_id>", methods=["DELETE"])
def delete_deck(deck_id):
    deck = Deck.query.get(deck_id)
    if not deck: 
        return make_response("deck not found", 404)

    db.session.delete(deck)
    db.session.commit()
    return make_response("deck deleted", 200)


# Get all flashcards by deck id 
@decks_bp.route("/<deck_id>/flashcards", methods=["GET"]) 
def get_flashcards_by_deck(deck_id):
    if not deck_id:
        return jsonify({"message" : "The user hasn't selected a deck yet."})

    flashcards = Flashcard.query.filter_by(deck_id=deck_id)
    if flashcards.count() > 1:
        flashcards = flashcards.order_by(Flashcard.id)
    flashcards_response = [flashcard.to_json() for flashcard in flashcards]
    return jsonify(flashcards_response), 200


# Get all flashcards by deck id that have a review date of now or earlier (in JSON format)
@decks_bp.route("/<deck_id>/flashcards_to_review", methods=["GET"]) 
def get_flashcards_to_review_by_deck(deck_id):
    flashcards = Flashcard.query.filter_by(deck_id=deck_id)
    
    up_for_review = []
    for card in flashcards:
        if card.date_to_review <= datetime.today():
            up_for_review.append(card.to_json())
    
    return jsonify(up_for_review), 200
