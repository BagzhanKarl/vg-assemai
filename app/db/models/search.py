from app.db import db, Default

class SearchData(Default):
    __tablename__ = 'search_data'

    id = db.Column(db.Integer, primary_key=True)
    query = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)

    