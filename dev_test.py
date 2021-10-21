import feedparser
import requests
import re
import json
from jsonToTable.core.extent_table import ExtentTable
from jsonToTable.core.table_maker import TableMaker
test = {}
response = requests.get(
    "https://api.themoviedb.org/3/movie/500?api_key=569760ff55e24c593b9cf89e8503decd").json()
test[0] = [
    {
        "adult": "false",
        "backdrop_path": "/g6R1OT7ETBLGLeUJOE0pOiAFHcI.jpg",
        "belongs_to_collection": None,
        "budget": 1200000,
        "genres": [
            {
                "id": 80,
                "name": "Crime"
            },
            {
                "id": 53,
                "name": "Thriller"
            }
        ],
        "homepage": "",
        "id": 500,
        "imdb_id": "tt0105236",
        "original_language": "en",
        "original_title": "Reservoir Dogs",
        "overview": "Après un hold‐up manqué, des cambrioleurs de haut vol font leurs comptes dans une confrontation violente, pour découvrir lequel d’entre eux les a trahis.",
        "popularity": 30.021,
        "poster_path": "/p61wwD0jWfgbhg9Ja9uoDZdS8YE.jpg",
        "production_companies": [
            {
                "id": 285,
                "logo_path": "null",
                "name": "Live Entertainment",
                "origin_country": ""
            },
            {
                "id": 26198,
                "logo_path": "null",
                "name": "Dog Eat Dog Productions",
                "origin_country": ""
            }
        ],
        "production_countries": [
            {
                "iso_3166_1": "US",
                "name": "United States of America"
            }
        ],
        "release_date": "1992-09-02",
        "revenue": 2859750,
        "runtime": 95,
        "spoken_languages": [
            {
                "english_name": "English",
                "iso_639_1": "en",
                "name": "English"
            }
        ],
        "status": "Released",
        "tagline": "Qui les a balancé ?",
        "title": "Reservoir Dogs",
        "video": False,
        "vote_average": 8.2,
        "vote_count": 11089
    }
]

test[1] = [
    {
        "adult": "false",
        "backdrop_path": "/znyf0hylb3hj7UQaJAnXS1N4mHP.jpg",
        "belongs_to_collection": {
            "id": 718511,
            "name": "Le Gendarme - Saga",
            "poster_path": "/p0aqUJRHKxQYbJp4SWz2EEvYtdn.jpg",
            "backdrop_path": "/9vDc4bbrkcYsxHtYAvijSnnIMUk.jpg"
        },
        "budget": 0,
        "genres": [
            {
                "id": 35,
                "name": "Comédie"
            }
        ],
        "homepage": "",
        "id": 11915,
        "imdb_id": "tt0083996",
        "original_language": "fr",
        "original_title": "Le gendarme et les gendarmettes",
        "overview": "Dans ses locaux flambant neufs, la brigade de Saint-Tropez est chargée d'accueillir, de prendre soin et de former un contingent de quatre jeunes femmes en uniforme. Un spécialiste de l'espionnage informatique enlève, l'une après l'autre, les nouvelles recrues. L'existence de la brigade étant mise en danger par ces enlèvements dont la raison semble inexplicable, nos gendarmes déploieront au péril de leur vie, des trésors d'ingéniosité pour retrouver ces femmes dont ils avaient la garde.",
        "popularity": 9.958,
        "poster_path": "/aMRRaX48RpSGp7RJxwkIJUndtdJ.jpg",
        "production_companies": [
            {
                "id": 249,
                "logo_path": "null",
                "name": "Société Nouvelle de Cinématographie",
                "origin_country": ""
            },
            {
                "id": 2902,
                "logo_path": "/nSPZ1BNASeC2dxJKB8AF6dJCx5q.png",
                "name": "SND",
                "origin_country": "FR"
            }
        ],
        "production_countries": [
            {
                "iso_3166_1": "FR",
                "name": "France"
            }
        ],
        "release_date": "1982-10-03",
        "revenue": 0,
        "runtime": 100,
        "spoken_languages": [
            {
                "english_name": "French",
                "iso_639_1": "fr",
                "name": "Français"
            }
        ],
        "status": "Released",
        "tagline": "",
        "title": "Le Gendarme et les Gendarmettes",
        "video": "false",
        "vote_average": 6,
        "vote_count": 410
    }
]

print(response)

# # Creates an extent table object that manages all the tables
extent_table = ExtentTable()


# # Pass the extent table object to the table maker
table_maker = TableMaker(extent_table)


# # Below is the name of the objects you are trying to convert. In our case, we are dealing with automobiles hence the "root" name will be automobiles
root_table_name = "movie"


table_maker.convert_json_objects_to_tables(response, root_table_name)


# # num_elements is the max number of elements to show when printing the tables
# table_maker.show_tables()

extent_table.save_extent_table_state()

extent_table = ExtentTable()

table_maker = TableMaker(extent_table)

extent_table.load_extent_table_state()

# Continue adding objects. We are basically just saving the info twice for the sake of example.

table_maker.convert_json_objects_to_tables(response, root_table_name)

table_maker.show_tables()
