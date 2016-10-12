from studies_api import app
import os

if "MONGOHQ_URL" not in os.environ:
    os.environ["MONGOHQ_URL"] = "mongodb://localhost:27017/studies_api"

port = int(os.environ.get("PORT", 5000))
app.run(host='0.0.0.0', port=port)