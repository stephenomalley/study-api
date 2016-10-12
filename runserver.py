from studies_api import app
import os

os.environ["MONGOHQ_URL"] = "mongodb://localhost:27017/studies_api"
app.run(debug=True)