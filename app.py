########################################
# IMPORTS
########################################

from config import username, password

from flask import Flask, jsonify, render_template, abort

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

########################################
# SETUP APPLICATION
########################################

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # Prevent caching

engine = create_engine(
    f"postgresql://{username}:{password}@localhost:5432/police_force")
base = automap_base()
base.prepare(engine, reflect=True)

database_tables = base.classes

########################################
# CONSTANTS
########################################

api_current_version = "v1.0"

routes = {
    "home": "/",
    "api_versions": "/api",
    "api_docs": "/api/<version>",
    "api_docs_year": "/api/<version>/year",
    "api_docs_city": "/api/<version>/city",
    "api_docs_precinct": "/api/<version>/precinct",
    "api_docs_neighborhood": "/api/<version>/neighborhood",
    "api_year": "/api/<version>/year/<year>",
    "api_city": "/api/<version>/city/<cityID>",
    "api_precinct": "/api/<version>/precinct/<precinctID>",
    "api_neighborhood": "/api/<version>/neighborhood/<neighborhoodID>"
}

templates = {
    "home": "index.html",
    "api_docs": "api_docs.html",
    "api_versions": "api_versions.html"
}

version_infos = [
    {
        "name": "v1.0",
        "url": "/api/v1.0",
        "documentation":
            {
                "/api/v1.0/year/": "Gets a list of available years.",
                "/api/v1.0/year/<year>": [
                    {
                        "case": {
                            "caseNumber": "The case number within the Minneapolis police system.",
                            "isCallTo911": "Whether this case was triggered by a call to 911.",
                            "problem": "The problem this case is for.",
                            "primaryOffense": "The primary offense for this case.",
                            "date": "The date of the case.",
                            "year": "The year of the case.",
                            "month": "The month of the case.",
                            "day": "The day of the case.",
                            "hour": "The hour of the case",
                            "latitude": "The latitude for where the case occured.",
                            "longitude": "The longitude for where the case occured.",
                            "city": {
                                "id": "The city ID for this API",
                                "name": "The city's name."
                            },
                            "precinct": {
                                "id": "The precinct ID for this API",
                                "name": "The precinct's name."
                            },
                            "neighborhood": {
                                "id": "The neighborhood ID for this API",
                                "name": "The neighborhood's name."
                            },
                            "force": {
                                "forceNumber": "The force number within the Minneapolis police system.",
                                "forceReportNumber": "The force report number within the Minneapolis police system.",
                                "forceCategory": "The categorization of the force.",
                                "forceAction": "The action taken by the officer.",
                                "subject": {
                                    "race": "Subject's race.",
                                    "sex": "Subject's sex.",
                                    "age": "Subject's age",
                                    "wasInjured": "Whether the subject was injured",
                                    "role": "The subject's role.",
                                    "roleNumber": "The role number within the Minneapolis police system.",
                                    "resistance": "How the subject resisted the officer."
                                }
                            }
                        }
                    }
                ],
                "/api/v1.0/city/": "Gets a list of available cities.",
                "/api/v1.0/city/<cityID>": {
                    "name": "The name of the city.",
                    "summary": [
                        {
                            "year": "The year.",
                            "totalCalls": "The total number of calls in the year."
                        }
                    ]
                },
                "/api/v1.0/precinct/": "Gets a list of available precincts.",
                "/api/v1.0/precinct/<precinctID>": {
                    "name": "The name of the precinct.",
                    "summary": [
                        {
                            "year": "The year.",
                            "totalCalls": "The total number of calls in the year."
                        }
                    ]
                },
                "/api/v1.0/neighborhood/": "Gets a list of available neighborhoods.",
                "/api/v1.0/neighborhood/<neighborhoodID>": {
                    "name": "The name of the neighborhood.",
                    "summary": [
                        {
                            "year": "The year.",
                            "totalCalls": "The total number of calls in the year."
                        }
                    ]
                }
            }
    }
]


########################################
# ROUTES
########################################

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


@app.route(routes["api_versions"])
def api_versions():
    """
    Shows all versions of the API.

    Returns
    -------
    Flask Rendered Template :
        The HTML to show.
    """
    return render_template(
        templates["api_versions"],
        versions=version_infos
    )


@app.route(routes["api_docs"])
def api_docs(version):
    """
    Shows the documentation for a specific API.

    Parameters
    ----------
    version : string
        The API version to show.

    Returns
    -------
    Flask Rendered Template :
        The HTML to show.
    """
    selected_version_info = get_version_info(version)

    documentation = {}
    if selected_version_info:
        documentation = selected_version_info["documentation"]
    else:
        abort(404, "API version is not available.")

    return jsonify(documentation)


@app.route(routes["api_docs_year"])
def api_docs_year(version):
    """
    API endpoint for retrieving all available years.

    Parameters
    ----------
    version : string
        API version

    Returns
    -------
    Flask JSON :
        A list of all available years.
    """
    selected_version_info = get_version_info(version)
    available_years = {}
    if(selected_version_info):
        session = Session(engine)
        try:
            available_years = load_available_years(session)
        finally:
            session.close()
    else:
        abort(404, "API version is not available.")

    return jsonify(available_years)


@app.route(routes["api_year"])
def api_year(version, year):
    """
    API endpoint for retrieving all cases within a specified year.

    Parameters
    ----------
    version : string
        API version

    year : int
        The year to retrieve

    Returns
    -------
    Flask JSON :
        All cases within the year.
    """
    selected_version_info = get_version_info(version)

    year_data = {}
    if selected_version_info:
        session = Session(engine)
        try:
            year_data = load_year_data(session, year)
        finally:
            session.close()
    else:
        abort(404, "API version is not available.")

    return jsonify(year_data)


@app.route(routes["api_docs_city"])
def api_docs_city(version):
    """
    API endpoint for retriving all available cities.

    Parameters
    ----------
    version : string
        API version

    Returns
    -------
    Flask JSON :
        All available cities.
    """
    selected_version_info = get_version_info(version)

    available_cities = {}
    if selected_version_info:
        session = Session(engine)
        try:
            available_cities = load_available_cities(session)
        finally:
            session.close()
    else:
        abort(404, "API version is not available.")

    return jsonify(available_cities)


@app.route(routes["api_docs_precinct"])
def api_docs_precinct(version):
    """
    API endpoint for retrieving all precincts.

    Parameters
    ----------
    version : string
        API version

    Returns
    -------
    Flask JSON :
        All available precincts.
    """
    selected_version_info = get_version_info(version)

    available_precincts = {}
    if selected_version_info:
        session = Session(engine)
        try:
            available_precincts = load_available_precincts(session)
        finally:
            session.close()
    else:
        abort(404, "API version is not available.")

    return jsonify(available_precincts)


@app.route(routes["api_docs_neighborhood"])
def api_docs_neighborhood(version):
    """
    API endpoint for retrieving all neighborhoods.

    Parameters
    ----------
    version : string
        API version

    Returns
    -------
    Flask JSON :
        All available neighborhoods.
    """
    selected_version_info = get_version_info(version)

    available_neighborhoods = {}
    if selected_version_info:
        session = Session(engine)
        try:
            available_neighborhoods = load_available_neighborhoods(session)
        finally:
            session.close()
    else:
        abort(404, "API version is not available.")

    return jsonify(available_neighborhoods)


@app.route(routes["api_city"])
def api_city(version, cityID):
    """
    API endpoint for getting city information.

    Parameters
    ----------
    version : string
        API version

    cityID: int
        The city ID

    Returns
    -------
    Flask JSON :
        City summary.
    """
    selected_version_info = get_version_info(version)

    city_summary = {}
    if selected_version_info:
        session = Session(engine)
        try:
            city_summary = load_city_summary(session, cityID)
        finally:
            session.close()
    else:
        abort(404, "API version is not available.")

    return jsonify(city_summary)


@app.route(routes["api_precinct"])
def api_precinct(version, precinctID):
    """
    API endpoint for getting precinct information.

    Parameters
    ----------
    version : string
        API version

    precinctID: int
        The precinct ID

    Returns
    -------
    Flask JSON :
        Precinct summary.
    """
    selected_version_info = get_version_info(version)

    precinct_summary = {}
    if selected_version_info:
        session = Session(engine)
        try:
            precinct_summary = load_precinct_summary(session, precinctID)
        finally:
            session.close()
    else:
        abort(404, "API version is not available.")

    return jsonify(precinct_summary)


@app.route(routes["api_neighborhood"])
def api_neighborhood(version, neighborhoodID):
    """
    API endpoint for getting neighborhood information.

    Parameters
    ----------
    version : string
        API version

    neighborhoodID: int
        The neighborhood ID

    Returns
    -------
    Flask JSON :
        Neighborhood summary.
    """
    selected_version_info = get_version_info(version)

    neighborhood_summary = {}
    if selected_version_info:
        session = Session(engine)
        try:
            neighborhood_summary = load_neighborhood_summary(
                session,
                neighborhoodID
            )
        finally:
            session.close()
    else:
        abort(404, "API version is not available.")

    return jsonify(neighborhood_summary)

########################################
# HELPER FUNCTIONS
########################################


def get_version_info(api_version):
    """
    Retrives information for an API version.

    Parameters
    ----------
    api_version : string
        The API version to look up.

    Returns
    -------
    Dict
        Information about the API and its endpoints.
    """
    selected_version_info = {}
    for version_info in version_infos:
        if(version_info["name"] == api_version):
            selected_version_info = version_info
    return selected_version_info


def load_available_cities(session):
    """
    Gets all cities out of the database

    Parameters
    ----------
    session : SQLAlchemy Session
        Database session

    Returns
    -------
    Dict
        List of available cities.
    """
    city_table = database_tables.city

    available_city_results = session.query(
        city_table.city_id,
        city_table.city_name
    ).all()

    city_ids = []
    for result in available_city_results:
        city_ids.append(
            {
                "cityID": result.city_id,
                "name": result.city_name
            }
        )

    return {
        "availableCities": city_ids
    }


def load_available_precincts(session):
    """
    Gets all precincts out of the database

    Parameters
    ----------
    session : SQLAlchemy Session
        Database session

    Returns
    -------
    Dict
        List of available precincts.
    """
    precinct_table = database_tables.precinct

    available_precinct_results = session.query(
        precinct_table.precinct_id,
        precinct_table.precinct_name
    ).all()

    precinct_ids = []
    for result in available_precinct_results:
        precinct_ids.append(
            {
                "precinctID": result.precinct_id,
                "name": result.precinct_name
            }
        )

    return {
        "availablePrecincts": precinct_ids
    }


def load_available_neighborhoods(session):
    """
    Gets all neighborhoods out of the database

    Parameters
    ----------
    session : SQLAlchemy Session
        Database session

    Returns
    -------
    Dict
        List of available neighborhoods.
    """
    neighborhood_table = database_tables.neighborhood

    available_neighborhood_results = session.query(
        neighborhood_table.neighborhood_id,
        neighborhood_table.neighborhood_name
    ).all()

    neighborhood_ids = []
    for result in available_neighborhood_results:
        neighborhood_ids.append(
            {
                "neighborhoodID": result.neighborhood_id,
                "name": result.neighborhood_name
            }
        )

    return {
        "availableNeighborhoods": neighborhood_ids
    }


def load_available_years(session):
    """
    Gets all years out of the database

    Parameters
    ----------
    session : SQLAlchemy Session
        Database session

    Returns
    -------
    Dict
        List of available years.
    """
    case_table = database_tables.case

    available_year_results = session.query(
        case_table.year
    ).distinct()

    years = []
    for result in available_year_results:
        years.append(result.year)
    years.sort()

    return {"availableYears": years}


def load_cases_by_year(session, year):
    """
    Loads all cases by year out of a database.

    Parameters
    ----------
    session : SQLAlchemy Session
        Database session

    year : Int
        The year to get.

    Returns
    -------
    Dict
        Cases in the year.
    """
    case_table = database_tables.case

    cases_by_year_results = session.query(
        case_table.case_number,
        case_table.is_911_call,
        case_table.problem,
        case_table.primary_offense,
        case_table.date,
        case_table.year,
        case_table.month,
        case_table.day,
        case_table.hour,
        case_table.latitude,
        case_table.longitude,
        case_table.city_id,
        case_table.precinct_id,
        case_table.neighborhood_id,
        case_table.police_force_id
    ).filter(case_table.year == year)

    return cases_by_year_results


def load_city_by_id(session, city_id):
    """
    Gets information on a city by its ID

    Parameters
    ----------
    session : SQLAlchemy Session
        Database session

    city_id : int
        The city id

    Returns
    -------
    Dict
        The city's info.
    """
    city_table = database_tables.city

    results = session.query(
        city_table.city_id,
        city_table.city_name
    ).filter(
        city_table.city_id == city_id)

    city_result = results[0]

    return {
        "id": city_result.city_id,
        "name": city_result.city_name
    }


def load_precinct_by_id(session, precinct_id):
    """
    Gets information on a precinct by its ID

    Parameters
    ----------
    session : SQLAlchemy Session
        Database session

    precinct_id : int
        The precinct id

    Returns
    -------
    Dict
        The precinct's info.
    """
    precinct_table = database_tables.precinct

    results = session.query(
        precinct_table.precinct_id,
        precinct_table.precinct_name
    ).filter(
        precinct_table.precinct_id == precinct_id)

    precinct_result = results[0]

    return {
        "id": precinct_result.precinct_id,
        "name": precinct_result.precinct_name
    }


def load_neighborhood_by_id(session, neighborhood_id):
    """
    Gets information on a neighborhood by its ID

    Parameters
    ----------
    session : SQLAlchemy Session
        Database session

    neighborhood_id : int
        The neighborhood id

    Returns
    -------
    Dict
        The neighborhood's info.
    """
    neighborhood_table = database_tables.neighborhood

    results = session.query(
        neighborhood_table.neighborhood_id,
        neighborhood_table.neighborhood_name
    ).filter(
        neighborhood_table.neighborhood_id == neighborhood_id)

    neighborhood_result = results[0]

    return {
        "id": neighborhood_result.neighborhood_id,
        "name": neighborhood_result.neighborhood_name
    }


def load_police_force_by_id(session, force_id):
    """
    Loads information on a police force from its ID.

    Parameters
    ----------
    session : SQLAlchemy Session
        Database session

    force_id : int
        Police force ID

    Returns
    -------
    Dict
        Information on the police force.
    """
    force_table = database_tables.police_force

    results = session.query(
        force_table.force_number,
        force_table.force_category_id,
        force_table.force_action,
        force_table.force_report_number,
        force_table.subject_id
    ).filter(
        force_table.police_force_id == force_id
    )

    force_result = results[0]

    force_category = {}
    force_category_id = force_result.force_category_id
    try:
        force_category = load_force_category_by_id(
            session,
            force_category_id
        )
    except IndexError:
        abort(
            404,
            f"Unable to load force category {force_category_id} for force id {force_id}"
        )

    subject = {}
    subject_id = force_result.subject_id
    if(subject_id):
        try:
            subject = load_subject_by_id(
                session,
                subject_id
            )
        except IndexError:
            abort(
                404,
                f"Unable to load subject with id {subject_id} for force id {force_id}"
            )
    return {
        "forceNumber": force_result.force_number,
        "forceReportNumber": force_result.force_report_number,
        "forceCategory": force_category["category"],
        "forceAction": force_result.force_action,
        "subject": subject
    }


def load_force_category_by_id(session, force_category_id):
    """
    Loads information on a force category from its ID.

    Parameters
    ----------
    session : SQLAlchemy Session
        Database session

    force_category_id : int
        Force category ID

    Returns
    -------
    Dict
        Information on the force category.
    """
    force_category_table = database_tables.force_categories

    results = session.query(
        force_category_table.force_category_id,
        force_category_table.category
    ).filter(
        force_category_table.force_category_id == force_category_id
    )

    force_category_result = results[0]

    return {
        "id": force_category_result.force_category_id,
        "category": force_category_result.category
    }


def load_subject_by_id(session, subject_id):
    """
    Loads information on a case subject from its ID.

    Parameters
    ----------
    session : SQLAlchemy Session
        Database session

    subject_id : int
        Subject ID

    Returns
    -------
    Dict
        Information on the subject.
    """
    subject_table = database_tables.subject

    results = session.query(
        subject_table.race,
        subject_table.sex,
        subject_table.age,
        subject_table.has_injury,
        subject_table.role,
        subject_table.role_number,
        subject_table.resistance
    ).filter(
        subject_table.subject_id == subject_id
    )

    subject_result = results[0]

    return {
        "race": subject_result.race,
        "sex": subject_result.sex,
        "age": subject_result.age,
        "wasInjured": subject_result.has_injury,
        "role": subject_result.role,
        "role_number": subject_result.role_number,
        "resistance": subject_result.resistance
    }


def load_year_data(session, year):
    """
    Loads all cases by year with all related information,
    out of the database.

    Parameters
    ----------
    session : SQLAlchemy Session
        Database session

    year : Int
        The year to get.

    Returns
    -------
    Dict
        All case information.
    """
    all_year_data = []

    cases_by_year_results = load_cases_by_year(session, year)

    for case_result in cases_by_year_results:
        case_number = case_result.case_number

        city_id = case_result.city_id
        city_data = {}
        if(city_id):
            try:
                city_data = load_city_by_id(
                    session,
                    city_id)
            except IndexError:
                abort(404,
                      f"Unable to load city with id {city_id} for case {case_number}.")

        precinct_id = case_result.precinct_id
        precinct_data = {}
        if(precinct_id):
            try:
                precinct_data = load_precinct_by_id(
                    session,
                    precinct_id)
            except IndexError:
                abort(404,
                      f"Unable to load precinct with id {precinct_id} for case {case_number}.")

        neighborhood_id = case_result.neighborhood_id
        neighborhood_data = {}
        if(neighborhood_id):
            try:
                neighborhood_data = load_neighborhood_by_id(
                    session,
                    neighborhood_id)
            except IndexError:
                abort(404,
                      f"Unable to load neighborhood with id {neighborhood_id} for case {case_number}.")

        force_id = case_result.police_force_id
        force_data = {}
        if(force_id):
            try:
                force_data = load_police_force_by_id(
                    session,
                    force_id
                )
            except IndexError:
                abort(
                    404,
                    f"Unable to load police force with id {force_id} for case {case_number}."
                )

        case_data = {
            "caseNumber": case_result.case_number,
            "isCallTo911": case_result.is_911_call,
            "problem": case_result.problem,
            "primaryOffense": case_result.primary_offense,
            "date": case_result.date,
            "year": case_result.year,
            "month": case_result.month,
            "day": case_result.day,
            "hour": case_result.hour,
            "latitude": case_result.latitude,
            "longitude": case_result.longitude,
            "city": city_data,
            "precinct": precinct_data,
            "neighborhood": neighborhood_data,
            "force": force_data
        }

        all_year_data.append({"case": case_data})

    return all_year_data


def load_city_summary(session, city_id):
    """
    Loads a city summary and related information from the database

    Parameters
    ----------
    session : SQLAlchemy Session
        Database session

    city_id : int
        The city ID

    Returns
    -------
    Dict
        The city summary information
    """
    city_data = {}
    try:
        city_data = load_city_by_id(
            session,
            city_id
        )
    except IndexError:
        abort(404,
              f"Unable to load city with id {city_id}.")

    summary_data = {}
    try:
        summary_data = load_city_summary_by_id(
            session,
            city_id
        )
    except IndexError:
        abort(404,
              f"Unable to load city summary with id {city_id}.")
    return {
        "name": city_data["name"],
        "summary": summary_data
    }


def load_city_summary_by_id(session, city_id):
    """
    Loads the city summary from the database

    Parameters
    ----------
    session : SQLAlchemy Session
        Database session

    city_id : int
        The city ID

    Returns
    -------
    Dict
        The city summary
    """
    city_summary_table = database_tables.city_summary

    results = session.query(
        city_summary_table.year,
        city_summary_table.total_calls
    ).filter(
        city_summary_table.city_id == city_id
    )

    return format_summary_results(results)


def load_precinct_summary(session, precinct_id):
    """
    Loads a precinct summary and related information from the database

    Parameters
    ----------
    session : SQLAlchemy Session
        Database session

    precinct_id : int
        The precinct ID

    Returns
    -------
    Dict
        The precinct summary information
    """
    precinct_data = {}
    try:
        precinct_data = load_precinct_by_id(
            session,
            precinct_id
        )
    except IndexError:
        abort(404,
              f"Unable to load precinct with id {precinct_id}.")

    summary_data = {}
    try:
        summary_data = load_precinct_summary_by_id(
            session,
            precinct_id
        )
    except IndexError:
        abort(404,
              f"Unable to load precinct summary with id {precinct_id}.")
    return {
        "name": precinct_data["name"],
        "summary": summary_data
    }


def load_precinct_summary_by_id(session, precinct_id):
    """
    Loads the precinct summary from the database

    Parameters
    ----------
    session : SQLAlchemy Session
        Database session

    precinct_id : int
        The precinct ID

    Returns
    -------
    Dict
        The precinct summary
    """
    precinct_summary_table = database_tables.precinct_summary

    results = session.query(
        precinct_summary_table.year,
        precinct_summary_table.total_calls
    ).filter(
        precinct_summary_table.precinct_id == precinct_id
    )

    return format_summary_results(results)


def load_neighborhood_summary(session, neighborhood_id):
    """
    Loads a neighborhood summary and related information from the database

    Parameters
    ----------
    session : SQLAlchemy Session
        Database session

    neighborhood_id : int
        The neighborhood ID

    Returns
    -------
    Dict
        The neighborhood summary information
    """
    neighborhood_data = {}
    try:
        neighborhood_data = load_neighborhood_by_id(
            session,
            neighborhood_id
        )
    except IndexError:
        abort(404,
              f"Unable to load neighborhood with id {neighborhood_id}.")

    summary_data = {}
    try:
        summary_data = load_neighborhood_summary_by_id(
            session,
            neighborhood_id
        )
    except IndexError:
        abort(404,
              f"Unable to load neighborhood summary with id {neighborhood_id}.")
    return {
        "name": neighborhood_data["name"],
        "summary": summary_data
    }


def load_neighborhood_summary_by_id(session, neighborhood_id):
    """
    Loads the neighborhood summary from the database

    Parameters
    ----------
    session : SQLAlchemy Session
        Database session

    neighborhood_id : int
        The neighborhood ID

    Returns
    -------
    Dict
        The neighborhood summary
    """
    neighborhood_summary_table = database_tables.neighborhood_summary

    results = session.query(
        neighborhood_summary_table.year,
        neighborhood_summary_table.total_calls
    ).filter(
        neighborhood_summary_table.neighborhood_id == neighborhood_id
    )

    return format_summary_results(results)


def format_summary_results(summary_results):
    """
    Formats summary results for display in JSON format.

    Parameters
    ----------
    summary_results : SQLAlchemy Results
        Results from SQLAlchemy regarding summary tables.

    Returns
    -------
    Dict
        Formatted summary results.
    """
    summary = []
    for summary_result in summary_results:
        summary.append(
            {
                "year": summary_result.year,
                "totalCalls": summary_result.total_calls
            }
        )

    return summary


########################################
# RUN FLASK
########################################
if __name__ == "__main__":
    app.run(debug=True)
