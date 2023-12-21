import warnings
warnings.filterwarnings('ignore', category=FutureWarning)
from flask import (abort, render_template, Flask)
import db

APP = Flask(__name__)

# -----------------------------------------------------------------------------------------------

"""
      # ---- #
      | Home |
      # ---- #
"""

@APP.route('/')
def home():
  return render_template('home.html')

# -----------------------------------------------------------------------------------------------

"""
      # ------ #
      | Genres |
      # ------ #
"""

# Genres - Listing

@APP.route('/genres/')
def list_genres():
  genres = db.execute(
    '''
    SELECT g.genre_id, g.name
    FROM Genre g
    ORDER BY g.name;
    '''
  ).fetchall()
  return render_template('list_genres.html',
                         n_genres=len(genres),
                         genres=genres)

# Genres - Movies/TvShows that have a certain genre

@APP.route('/genres/<int:id>')
def get_shows_genre(id):

  genre = db.execute(
    '''
    SELECT g.name
    FROM Genre g
    WHERE g.genre_id = ?
    ''', [id]).fetchone()

  movies_genre = db.execute(
    '''
    SELECT s.show_id, s.title, s.release_year, s.duration
    FROM Show s JOIN Show_Genre sg JOIN Genre g JOIN Type t
    ON (s.show_id = sg.show_id AND sg.genre_id = g.genre_id AND s.type_id = t.type_id)
    WHERE t.type = 'Movie' AND g.genre_id = ?
    ORDER BY s.title;
    ''', [id]).fetchall()
  
  tvshows_genre = db.execute(
    '''
    SELECT s.show_id, s.title, s.release_year, s.duration
    FROM Show s JOIN Show_Genre sg JOIN Genre g JOIN Type t
    ON (s.show_id = sg.show_id AND sg.genre_id = g.genre_id AND s.type_id = t.type_id)
    WHERE t.type = 'TV Show' AND g.genre_id = ?
    ORDER BY s.title;
    ''', [id]).fetchall()

  return render_template('genre.html',
                         genre_name=genre['name'],
                         n_movies_genre = len(movies_genre),
                         movies_genre=movies_genre,
                         n_tvshows_genre = len(tvshows_genre),
                         tvshows_genre=tvshows_genre,
                         n_results=(len(movies_genre) + len(tvshows_genre)))

# -----------------------------------------------------------------------------------------------

"""
      # --------- #
      | Countries |
      # --------- #
"""

# Countries - Listing

@APP.route('/countries/')
def list_countries():
  countries = db.execute(
    '''
    SELECT c.country_id, c.name
    FROM Country c
    ORDER BY c.name;
    ''').fetchall()
  
  return render_template('list_countries.html',
                         n_countries=len(countries),
                         countries=countries)

# Countries - Movies/TvShows Recorded in a certain country

@APP.route('/countries/<int:id>')
def get_shows_countries(id):
  country = db.execute(
    '''
    SELECT c.name
    FROM Country c
    WHERE c.country_id = ?;
    ''', [id]).fetchone()

  movies_countries = db.execute(
    '''
    SELECT s.show_id, s.title, s.release_year, s.duration
    FROM SHOW s JOIN Country c JOIN Show_Country sc JOIN Type t
    ON (s.show_id=sc.show_id AND sc.country_id=c.country_id AND s.type_id=t.type_id)
    WHERE c.country_id = ? AND t.type = 'Movie'
    ORDER BY s.title;
    ''', [id]).fetchall()
  
  tvshows_countries = db.execute(
    '''
    SELECT s.show_id, s.title, s.release_year, s.duration
    FROM SHOW s JOIN Country c JOIN Show_Country sc JOIN Type t
    ON (s.show_id=sc.show_id AND sc.country_id=c.country_id AND s.type_id=t.type_id)
    WHERE c.country_id = ? AND t.type = 'TV Show'
    ORDER BY s.title;
    ''', [id]).fetchall()

  return render_template('country.html',
                         n_results=(len(movies_countries) + len(tvshows_countries)),
                         country_name=country['name'],
                         n_movies_country=len(movies_countries),
                         movies_countries=movies_countries,
                         n_tvshows_country=len(tvshows_countries),
                         tvshows_countries=tvshows_countries)


# -----------------------------------------------------------------------------------------------

"""
      # ------- #
      | Ratings |
      # ------- #
"""

# Ratings - Listing

@APP.route('/ratings/')
def list_ratings():
  ratings = db.execute(
    '''
    SELECT r.rating_id, r.acronym, r.description
    FROM Rating r
    ORDER BY r.rating_id;
    ''').fetchall()
  return render_template('list_ratings.html',
                         ratings=ratings)

# Ratings - Shows that match a certain Rating

@APP.route('/ratings/<int:id>')
def get_shows_ratings(id):
  
  rating_acr = db.execute(
    '''
    SELECT r.acronym
    FROM Rating r
    WHERE r.rating_id = ?
    ''', [id]).fetchone()

  movies_rating = db.execute(
    '''
    SELECT s.show_id, s.title, s.release_year, s.duration
    FROM Show s JOIN Type t
    ON (s.type_id = t.type_id)
    WHERE s.rating_id = ? AND t.type = 'Movie'
    ORDER BY s.title;
    ''', [id]).fetchall()
  
  tvshows_rating = db.execute(
    '''
    SELECT s.show_id, s.title, s.release_year, s.duration
    FROM Show s JOIN Type t
    ON (s.type_id = t.type_id)
    WHERE s.rating_id = ? AND t.type = 'TV Show'
    ORDER BY s.title;
    ''', [id]).fetchall()

  return render_template('rating.html',
                         rating_acr=rating_acr['acronym'],
                         n_movies_rating=len(movies_rating),
                         movies_rating=movies_rating,
                         n_tvshows_rating=len(tvshows_rating),
                         tvshows_rating=tvshows_rating,
                         n_results=(len(movies_rating) + len(tvshows_rating)))

# -----------------------------------------------------------------------------------------------

"""
      # ------ #
      | Movies |
      # ------ #
"""

# Movies - Listing all entries

@APP.route('/movies/P<int:page_number>')
def list_movies(page_number):
  size = 1000
  start_limit = (page_number - 1) * size
  end_limit = (page_number) * size
  
  movies = db.execute(
    '''
    SELECT s.show_id, s.title, s.release_year, s.duration
    FROM Show s NATURAL JOIN Type t
    WHERE t.type = 'Movie'
    ORDER by s.title
    LIMIT ?, ?;
    ''', [start_limit, end_limit]).fetchall()
  
  return render_template('list_movies.html', movies=movies)

# Movies - People who were involved in a certain Movie

@APP.route('/movies/<int:id>')
def get_movie(id):
  movie = db.execute('''
  SELECT s.show_id, s.title, s.release_year, s.duration, s.description
  FROM Show s NATURAL JOIN Type t
  WHERE t.type = 'Movie' AND s.show_id = ?
  ORDER by s.show_id;
  ''', [id]).fetchone()

  if (movie is None):
    abort(404, 'Show id {} does not exist.'.format(id))

  rating = db.execute('''
    SELECT r.acronym
    FROM Show s JOIN Rating r
    ON (s.rating_id=r.rating_id)
    WHERE s.show_id = ?
    ''', [id]).fetchone()

  if (rating is None):
    abort(404, 'Show id {} does not have a rating.'.format(id))

  genres = db.execute('''
  SELECT g.name
  FROM Show s JOIN Show_Genre sg JOIN Genre g
  ON (s.show_id = sg.show_id AND sg.genre_id=g.genre_id)
  WHERE s.show_id = ?
  ORDER BY g.name;
  ''', [id]).fetchall()

  if (genres is None):
    abort(404, 'Show id {} does not have genres.'.format(id))

  countries = db.execute('''
  SELECT c.name
  FROM Show s JOIN Show_Country sc JOIN Country c
  ON (s.show_id = sc.show_id AND sc.country_id=c.country_id)
  WHERE s.show_id = ?
  ORDER BY c.name;
  ''', [id]).fetchall()

  if (countries is None):
    abort(404, 'Show id {} does not have countries.'.format(id))

  actors = db.execute('''
  SELECT p.person_id, p.name
  FROM Show_Person_Job spj JOIN Job j JOIN Person p JOIN Show s JOIN Type t
  ON (spj.person_id = p.person_id AND spj.job_id = j.job_id AND spj.show_id = s.show_id AND s.type_id = t.type_id)
  WHERE t.type = 'Movie' AND spj.show_id = ? AND j.name = 'cast'
  ORDER by p.name;
  ''', [id]).fetchall()

  if (actors is None):
    abort(404, 'Show id {} does not have actors.'.format(id))
  
  directors = db.execute('''
  SELECT p.person_id, p.name
  FROM Show_Person_Job spj JOIN Job j JOIN Person p JOIN Show s JOIN Type t
  ON (spj.person_id = p.person_id AND spj.job_id = j.job_id AND spj.show_id = s.show_id AND s.type_id = t.type_id)
  WHERE t.type = 'Movie' AND spj.show_id = ? AND j.name = 'director'
  ORDER by p.name;
  ''', [id]).fetchall()

  if (directors is None):
    abort(404, 'Show id {} does not have directors.'.format(id))

  return render_template('movie.html',
                         movie=movie,
                         rating=rating,
                         n_genres=len(genres),
                         genres=genres,
                         n_countries=len(countries),
                         countries=countries,
                         n_actors = len(actors),
                         actors=actors,
                         n_directors=len(directors),
                         directors=directors)

# -----------------------------------------------------------------------------------------------

"""
      # -------- #
      | TV Shows |
      # -------- #
"""

# TV Shows - Listing all entries

@APP.route('/tvshows/') # AMOUNT OF RESULTS CHANGED -> WAY TOO MANY DATA
def list_tvshows():
  tvshows = db.execute(
    '''
    SELECT s.show_id, s.title, s.release_year, s.duration
    FROM Show s NATURAL JOIN Type t
    WHERE t.type = 'TV Show'
    ORDER by s.title
    LIMIT 1000;
    ''').fetchall()

  # ADD EXTRA INFO TO THE TV SHOW
  
  return render_template('list_tvshows.html', tvshows=tvshows)

# TV Shows - People who were involved in a certain TvShow

@APP.route('/tvshows/<int:id>')
def get_tvshow(id):
  tvshow = db.execute('''
  SELECT s.show_id, s.title, s.release_year, s.duration, s.description
  FROM Show s NATURAL JOIN Type t
  WHERE t.type = 'TV Show' AND s.show_id = ?
  ORDER by s.show_id;
  ''', [id]).fetchone()

  if (tvshow is None):
      abort(404, 'TV Show id {} does not exist.'.format(id))

  rating = db.execute('''
    SELECT r.acronym
    FROM Show s JOIN Rating r
    ON (s.rating_id=r.rating_id)
    WHERE s.show_id = ?
    ''', [id]).fetchone()

  if (rating is None):
    abort(404, 'Show id {} does not have a rating.'.format(id))

  genres = db.execute('''
  SELECT g.name
  FROM Show s JOIN Show_Genre sg JOIN Genre g
  ON (s.show_id = sg.show_id AND sg.genre_id=g.genre_id)
  WHERE s.show_id = ?
  ORDER BY g.name;
  ''', [id]).fetchall()

  if (genres is None):
    abort(404, 'Show id {} does not have genres.'.format(id))

  countries = db.execute('''
  SELECT c.name
  FROM Show s JOIN Show_Country sc JOIN Country c
  ON (s.show_id = sc.show_id AND sc.country_id=c.country_id)
  WHERE s.show_id = ?
  ORDER BY c.name;
  ''', [id]).fetchall()

  if (countries is None):
    abort(404, 'Show id {} does not have countries.'.format(id))


  actors = db.execute('''
  SELECT p.person_id, p.name
  FROM Show_Person_Job spj JOIN Job j JOIN Person p JOIN Show s JOIN Type t
  ON (spj.person_id = p.person_id AND spj.job_id = j.job_id AND spj.show_id = s.show_id AND s.type_id = t.type_id)
  WHERE t.type = 'TV Show' AND spj.show_id = ? AND j.name = 'cast'
  ORDER by p.name;
  ''', [id]).fetchall()

  if (actors is None):
    abort(404, 'TV Show id {} does not have actors.'.format(id))
  
  directors = db.execute('''
  SELECT p.person_id, p.name
  FROM Show_Person_Job spj JOIN Job j JOIN Person p JOIN Show s JOIN Type t
  ON (spj.person_id = p.person_id AND spj.job_id = j.job_id AND spj.show_id = s.show_id AND s.type_id = t.type_id)
  WHERE t.type = 'TV Show' AND spj.show_id = ? AND j.name = 'director'
  ORDER by p.name;
  ''', [id]).fetchall()

  if (directors is None):
    abort(404, 'TV Show id {} does not have directors.'.format(id))

  return render_template('tvshow.html',
                         tvshow=tvshow,
                         rating=rating,
                         genres=genres,
                         countries=countries,
                         n_actors=len(actors),
                         actors=actors,
                         n_directors=len(directors),
                         directors=directors)

# -----------------------------------------------------------------------------------------------

"""
      # ------ #
      | Actors |
      # ------ #
"""

# Actors - Listing all entries

@APP.route('/actors/')
def list_actors(): # AMOUNT OF RESULTS CHANGED -> WAY TOO MANY DATA
  actors = db.execute('''
  SELECT DISTINCT p.person_id, p.name
  FROM Show_Person_Job spj JOIN Person p JOIN Job j
  ON (spj.person_id = p.person_id AND spj.job_id = j.job_id)
  WHERE j.name = 'cast'
  ORDER by p.name
  LIMIT 100;
  ''').fetchall()

  return render_template('list_actors.html',
                         actors=actors)

# Actors - Productions that a certain actor was involved in

@APP.route('/actors/<int:id>')
def get_actor(id):
  actor = db.execute('''
  SELECT DISTINCT p.person_id, p.name
  FROM Show_Person_Job spj JOIN Person p JOIN Job j
  ON (spj.person_id=p.person_id AND spj.job_id=j.job_id)
  WHERE j.name = 'cast' AND p.person_id = ?
  ORDER by p.name;            
  ''', [id]).fetchone()

  if (actor is None):
    abort(404, 'Actor id {} does not exit.'.format(id))

  productions_movies = db.execute('''
  SELECT DISTINCT s.show_id, s.title, s.release_year, s.duration
  FROM Show s JOIN Type t JOIN Show_Person_Job spj JOIN Job j JOIN Person p
  ON (spj.show_id = s.show_id AND spj.person_id = p.person_id AND spj.job_id = j.job_id AND s.type_id = t.type_id)
  WHERE p.person_id = ? AND t.type = 'Movie'
  ORDER by s.title;      
  ''', [id]).fetchall()

  productions_tvshows = db.execute('''
  SELECT DISTINCT s.show_id, s.title, s.release_year, s.duration
  FROM Show s JOIN Type t JOIN Show_Person_Job spj JOIN Job j JOIN Person p
  ON (spj.show_id = s.show_id AND spj.person_id = p.person_id AND spj.job_id = j.job_id AND s.type_id = t.type_id)
  WHERE p.person_id = ? AND t.type = 'TV Show'
  ORDER by s.title;
  ''', [id]).fetchall()

  return render_template('actor.html',
                         actor=actor,
                         n_movies=len(productions_movies),
                         productions_movies=productions_movies,
                         n_tvshows=len(productions_tvshows),
                         productions_tvshows=productions_tvshows,
                         n_results=len(productions_movies) + len(productions_tvshows))

# -----------------------------------------------------------------------------------------------

"""
      # --------- #
      | Directors |
      # --------- #
"""

# Directors - Listing all entries

@APP.route('/directors/')
def list_directors(): # AMOUNT OF RESULTS CHANGED -> WAY TOO MANY DATA
  directors = db.execute('''
  SELECT DISTINCT p.person_id, p.name
  FROM Show_Person_Job spj JOIN Person p JOIN Job j
  ON (spj.person_id = p.person_id AND spj.job_id = j.job_id)
  WHERE j.name = 'director'
  ORDER by p.name
  LIMIT 100;
  ''').fetchall()

  return render_template('list_directors.html',
                         directors=directors)

# Directors - Productions that a certain director was involved in

@APP.route('/directors/<int:id>')
def get_director(id):
  director = db.execute('''
  SELECT DISTINCT p.person_id, p.name
  FROM Show_Person_Job spj JOIN Person p JOIN Job j
  ON (spj.person_id = p.person_id AND spj.job_id = j.job_id)
  WHERE j.name = 'director' AND p.person_id = ?
  ORDER by p.name;            
  ''', [id]).fetchone()

  if (director is None):
    abort(404, 'Director id {} does not exit.'.format(id))

  productions_movies = db.execute('''
  SELECT DISTINCT s.show_id, s.title, s.release_year, s.duration
  FROM Show s JOIN Person p JOIN Type t JOIN Show_Person_Job spj
  ON (s.type_id = t.type_id AND spj.person_id = p.person_id AND spj.show_id = s.show_id)
  WHERE p.person_id = ? AND t.type = 'Movie'
  ORDER by s.title;      
  ''', [id]).fetchall()

  productions_tvshows = db.execute('''
  SELECT DISTINCT s.show_id, s.title, s.release_year, s.duration
  FROM Show s JOIN Person p JOIN Type t JOIN Show_Person_Job spj
  ON (s.type_id = t.type_id AND spj.person_id = p.person_id AND spj.show_id = s.show_id)
  WHERE p.person_id = ? AND t.type = 'TV Show'
  ORDER by s.title;
  ''', [id]).fetchall()

  return render_template('director.html',
                         director=director,
                         n_movies=len(productions_movies),
                         productions_movies=productions_movies,
                         n_tvshows=len(productions_tvshows),
                         productions_tvshows=productions_tvshows,
                         n_results=(len(productions_movies) + len(productions_tvshows)))

# -----------------------------------------------------------------------------------------------

"""
  # ------------ #
  | Search Motor |
  # ------------ #
"""

@APP.route('/search/<string:input_search>')
def search(input_search):
  
  input_search_with_wildcards = f"%{input_search}%"

  # Query to Search the Movies
  movies_query = '''
          SELECT s.show_id, s.title, s.release_year, s.duration
          FROM Show s JOIN Type t on (s.type_id = t.type_id)
          WHERE s.title LIKE :search_term AND t.type='Movie'
          ORDER BY s.title;
          '''
  
  movies_results = db.execute(movies_query, {"search_term": input_search_with_wildcards}).fetchall()

  # Query to Search the TV Shows
  tvshow_query = '''
          SELECT s.show_id, s.title, s.release_year, s.duration
          FROM Show s JOIN Type t on (s.type_id = t.type_id)
          WHERE s.title LIKE :search_term AND t.type='TV Show'
          ORDER BY s.title;
          '''

  tvshows_results = db.execute(tvshow_query, {"search_term": input_search_with_wildcards}).fetchall()

  # Query to Search the Actors
  actor_query = '''
          SELECT p.person_id, p.name
          FROM Person p JOIN Show_Person_Job spj JOIN Job j
          ON (p.person_id=spj.person_id AND spj.job_id=j.job_id)
          WHERE p.name LIKE :search_term AND j.name='cast'
          ORDER BY p.name;'''
  
  actors_results = db.execute(actor_query, {"search_term": input_search_with_wildcards}).fetchall()
  
  # Query to Search the Directors
  director_query = '''
          SELECT p.person_id, p.name
          FROM Person p JOIN Show_Person_Job spj JOIN Job j
          ON (p.person_id=spj.person_id AND spj.job_id=j.job_id)
          WHERE p.name LIKE :search_term AND j.name='director'
          ORDER BY p.name;'''
  
  directors_results = db.execute(director_query, {"search_term": input_search_with_wildcards}).fetchall()

  return render_template('search.html',
                         input_search=input_search,
                         n_movies=len(movies_results),
                         movies_results=movies_results,
                         n_tvshows=len(tvshows_results),
                         tvshows_results=tvshows_results,
                         n_actors=len(actors_results),
                         actors_results=actors_results,
                         n_directors=len(directors_results),
                         directors_results=directors_results,
                         n_results=(len(movies_results) + 
                                    len(tvshows_results) + 
                                    len(actors_results) + 
                                    len(directors_results)))