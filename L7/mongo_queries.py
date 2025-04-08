from pymongo import MongoClient

QUERY_CIRCUITS_FRANCE = { "country": "France" }
QUERY_REMOVE_DRIVERS_NULL_CODE = {
    "code": None
}
AGGREGATE_OLDEST_DRIVERS = [
    {
        "$addFields": {
            "dob_parsed": {
                "$dateFromString": {
                    "dateString": "$dob",
                    "format": "%d/%m/%Y",
                    "onError": None,
                    "onNull": None
                }
            }
        }
    },
    { "$match": { "dob_parsed": { "$ne": None } } },
    { "$sort": { "dob_parsed": 1 } },
    { "$limit": 1 }
]
AGGREGATE_FIRST_SEASON = [
    {
        "$group": {
            "_id": None,
            "min_year": { "$min": "$year" }
        }
    },
    {
        "$lookup": {
            "from": "seasons",
            "let": { "minYear": "$min_year" },
            "pipeline": [
                { "$match": { "$expr": { "$eq": [ "$year", "$$minYear" ] } } }
            ],
            "as": "first_seasons"
        }
    },
    { "$unwind": "$first_seasons" },
    { "$replaceRoot": { "newRoot": "$first_seasons" } }
]
NEW_SEASON_2019 = {
    "year": 2019,
    "url": "https://en.wikipedia.org/wiki/2019_Formula_One_World_Championship"
}
AGGREGATE_RACE_COUNT_PER_YEAR = [
    {
        "$group": {
            "_id": "$year",
            "race_count": { "$sum": 1 }
        }
    },
    { "$sort": { "_id": 1 } },
    {
        "$project": {
            "_id": 0,
            "year": "$_id",
            "race_count": 1
        }
    }
]
AGGREGATE_RACE_RESULTS_2010 = [
    {
        "$lookup": {
            "from": "races",
            "localField": "raceId",
            "foreignField": "raceId",
            "as": "race"
        }
    },
    { "$unwind": "$race" },
    {
        "$lookup": {
            "from": "drivers",
            "localField": "driverId",
            "foreignField": "driverId",
            "as": "driver"
        }
    },
    { "$unwind": "$driver" },
    {
        "$lookup": {
            "from": "constructors",
            "localField": "constructorId",
            "foreignField": "constructorId",
            "as": "constructor"
        }
    },
    { "$unwind": "$constructor" },
    {
        "$match": { "race.year": 2010 }
    },
    {
        "$project": {
            "_id": 0,
            "resultId": 1,
            "raceId": 1,
            "race_name": "$race.name",
            "driver_name": {
                "$concat": ["$driver.forename", " ", "$driver.surname"]
            },
            "constructor_name": "$constructor.name",
            "position": 1,
            "points": 1,
            "year": "$race.year"
        }
    },
    {
        "$sort": { "race_name": 1, "position": 1 }
    }
]
AGGREGATE_DRIVER_MOST_POINTS = [
    {
        "$facet": {
            "maxPoints": [
                {
                    "$group": {
                        "_id": None,
                        "max_points": { "$max": "$points" }
                    }
                }
            ],
            "allResults": [
                {
                    "$lookup": {
                        "from": "drivers",
                        "localField": "driverId",
                        "foreignField": "driverId",
                        "as": "driver"
                    }
                },
                { "$unwind": "$driver" },
                {
                    "$lookup": {
                        "from": "races",
                        "localField": "raceId",
                        "foreignField": "raceId",
                        "as": "race"
                    }
                },
                { "$unwind": "$race" }
            ]
        }
    },
    {
        "$project": {
            "max_points": { "$arrayElemAt": ["$maxPoints.max_points", 0] },
            "allResults": 1
        }
    },
    { "$unwind": "$allResults" },
    {
        "$replaceRoot": {
            "newRoot": {
                "$mergeObjects": [
                    "$allResults",
                    { "max_points": "$max_points" }
                ]
            }
        }
    },
    {
        "$match": {
            "$expr": {
                "$eq": ["$points", "$max_points"]
            }
        }
    },
    {
        "$project": {
            "_id": 0,
            "driverId": 1,
            "driver_name": {
                "$concat": ["$driver.forename", " ", "$driver.surname"]
            },
            "race_name": "$race.name",
            "race_year": "$race.year",
            "points": 1
        }
    },
    {
        "$sort": {
            "race_year": 1,
            "race_name": 1,
            "driver_name": 1
        }
    }
]
QUERY_REMOVE_NULL_RESULTS = {
    "$or": [
        { "raceId": None },
        { "driverId": None },
        { "constructorId": None },
        { "number": None },
        { "grid": None },
        { "position": None },
        { "positionText": None },
        { "positionOrder": None },
        { "points": None },
        { "laps": None },
        { "time": None },
        { "milliseconds": None },
        { "fastestLap": None },
        { "rank": None },
        { "fastestLapTime": None },
        { "fastestLapSpeed": None },
        { "statusId": None }
    ]
}
AGGREGATE_FASTEST_PITSTOP = [
    {
        "$match": { "duration": { "$ne": None } }
    },
    {
        "$group": {
            "_id": None,
            "min_duration": { "$min": "$duration" }
        }
    },
    {
        "$lookup": {
            "from": "pitstops",
            "let": { "minDuration": "$min_duration" },
            "pipeline": [
                {
                    "$match": {
                        "$expr": { "$eq": ["$duration", "$$minDuration"] }
                    }
                },
                {
                    "$lookup": {
                        "from": "drivers",
                        "localField": "driverId",
                        "foreignField": "driverId",
                        "as": "driver"
                    }
                },
                { "$unwind": "$driver" },
                {
                    "$lookup": {
                        "from": "races",
                        "localField": "raceId",
                        "foreignField": "raceId",
                        "as": "race"
                    }
                },
                { "$unwind": "$race" },
                {
                    "$project": {
                        "_id": 0,
                        "driver_name": {
                            "$concat": [
                                "$driver.forename", " ",
                                "$driver.surname", " (",
                                { "$toString": "$driver.number" }, ")"
                            ]
                        },
                        "lap": 1,
                        "duration": 1,
                        "race_name": "$race.name",
                        "race_year": "$race.year"
                    }
                },
                {
                    "$sort": { "race_year": 1, "race_name": 1 }
                }
            ],
            "as": "fastest"
        }
    },
    { "$unwind": "$fastest" },
    { "$replaceRoot": { "newRoot": "$fastest" } }
]


def get_collection(mongo_client, db_name, collection_name):
    client = MongoClient(mongo_client)
    db = client[db_name]
    return db[collection_name]

def get_france_circuits(mongo_client, db_name):
    collection = get_collection(mongo_client, db_name, "circuits")

    # Execute and print results
    results = collection.find(QUERY_CIRCUITS_FRANCE)

    print("Mongo france circuits query result:")
    for doc in results:
        print(doc)

def remove_null_code_drivers(mongo_client, db_name):
    collection = get_collection(mongo_client, db_name, "drivers")

    # Execute and print results
    result = collection.delete_many(QUERY_REMOVE_DRIVERS_NULL_CODE)

    print("Mongo Remove null code drivers query result:")
    print(f"Deleted {result.deleted_count} documents.")

def get_oldest_drivers(mongo_client, db_name):
    collection = get_collection(mongo_client, db_name, "drivers")
    results = collection.aggregate(AGGREGATE_OLDEST_DRIVERS)

    print("Mongo oldest drivers query result:")
    for driver in results:
        print(driver)

def get_first_season(mongo_client, db_name):
    collection = get_collection(mongo_client, db_name, "seasons")
    results = collection.aggregate(AGGREGATE_FIRST_SEASON)

    print("Mongo first season query result:")
    for driver in results:
        print(driver)

def add_new_season(mongo_client, db_name):
    collection = get_collection(mongo_client, db_name, "seasons")
    result = collection.insert_one(NEW_SEASON_2019)

    print("Mongo Add new season query result:")
    print(f"Inserted ID: {result.inserted_id}")

def get_race_count_per_year(mongo_client, db_name):
    collection = get_collection(mongo_client, db_name, "races")
    results = collection.aggregate(AGGREGATE_RACE_COUNT_PER_YEAR)

    print("Mongo races per year query result:")
    for year_stat in results:
        print(year_stat)

def get_race_results_for_year(mongo_client, db_name):
    collection = get_collection(mongo_client, db_name, "results")
    results = collection.aggregate(AGGREGATE_RACE_RESULTS_2010)

    print("Mongo races results for year 2010 query result:")
    for doc  in results:
        print(doc )

def get_driver_with_most_points(mongo_client, db_name):
    collection = get_collection(mongo_client, db_name, "driver_standings")
    results = collection.aggregate(AGGREGATE_DRIVER_MOST_POINTS)

    print("Mongo driver with most points query result:")
    for doc  in results:
        print(doc)

def remove_null_results(mongo_client, db_name):
    collection = get_collection(mongo_client, db_name, "results")
    result = collection.delete_many(QUERY_REMOVE_NULL_RESULTS)

    print("Mongo Remove null results query result:")
    print(f"Deleted {result.deleted_count} documents.")

def get_fastest_pitstop(mongo_client, db_name):
    collection = get_collection(mongo_client, db_name, "pitstops")
    results = collection.aggregate(AGGREGATE_FASTEST_PITSTOP)

    print("Mongo fastest pitstop query result:")
    for doc  in results:
        print(doc)