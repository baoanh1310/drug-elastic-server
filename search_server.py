from src.services.search_service import app
from src.database.elastic_search_client import *

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1999, debug=False)
