from flask import Flask
from src.services.search_drug_name import drug

app = Flask(__name__)
app.register_blueprint(drug)
