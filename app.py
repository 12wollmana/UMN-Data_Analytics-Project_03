########################################
# region IMPORTS

# from config import username, password

from flask import Flask, jsonify, render_template, abort

# from sqlalchemy.ext.automap import automap_base
# from sqlalchemy.orm import Session
# from sqlalchemy import create_engine

# endregion

########################################
# region SETUP APPLICATION

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # Prevent caching

# engine = create_engine(
#     f"postgresql://{username}:{password}@localhost:5432/police_force")
# base = automap_base()
# base.prepare(engine, reflect=True)

# database_tables = base.classes

# endregion

########################################
# region CONSTANTS

routes = {
    "home": "/",
    "gallery": "/gallery"
}

templates = {
    "home": "index.html",
    "gallery": "gallary.html"
}

# endregion

########################################
# region ROUTES


@app.route(routes["home"])
def home():
    """
    The homepage.

    Returns
    -------
    Flask Rendered Template :
        The HTML to show.
    """

    return render_template(templates["home"])


@app.route(routes["gallery"])
def gallery():
    """
    The gallery.

    Returns
    -------
    Flask Rendered Template :
        The HTML to show.
    """

    return render_template(templates["gallery"])
# endregion

########################################
# region HELPER FUNCTIONS

# endregion

########################################
# region FLASK


if __name__ == "__main__":
    app.run(debug=True)

# endregion
