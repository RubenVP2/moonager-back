import tmdb


def get_movie_info(movie: tmdb.TMDBMovieInfo):
    movie.progress = 45
    return movie
