# import model
# import app

# model.connect_to_db(app.app)

# with app.app.app_context():
#     model.db.create_all()


# with open("data/movies.json") as f:
#     movie_data=json.loads(f.read())

# print(movie_data)
# Create movies, store them in list so we can use them
# to create fake ratings later
# movies_in_db = []

# for movie in movie_data:
    # TODO: get the title, overview, and poster_path from the movie
    # dictionary. Then, get the release_date and convert it to a
    # datetime object with datetime.strptime
    # TODO: create a movie here and append it to movies_in_db
    # date=datetime.strptime(movie['release_date'],"%Y-%m-%d")
    # mov=crud.create_movie(movie['overview'],movie['poster_path'],date,movie['title'])
    # movies_in_db.append(mov)

# model.db.session.add_all(movies_in_db)
# model.db.session.commit()

# for n in range(10):
#     email=f"usera{n}@abc.com"
#     password="test"

#     user=crud.create_user(email,password)
#     model.db.session.add(user)
#     model.db.session.commit()

#     for _ in range(10):
#         random_movie = choice(movies_in_db)
#         score = randint(1, 5)

#         rating = crud.create_rating(user, random_movie, score)
#         model.db.session.add(rating)
#         model.db.session.commit()
