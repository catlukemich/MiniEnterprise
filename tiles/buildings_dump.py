

datas = [
    {"path" : "assets/buildings/building1.png" , "name" : "NWL Block"               , "population": 20},
    {"path" : "assets/buildings/building2.png" , "name" : "NWL Block South"         , "population": 20},
    {"path" : "assets/buildings/building3.png" , "name" : "Small House"             , "population":4},
    {"path" : "assets/buildings/building4.png" , "name" : "Medium Block"            , "population":35},
    {"path" : "assets/buildings/building5.png" , "name" : "Medium Block 2"          , "population":35},
    {"path" : "assets/buildings/building6.png" , "name" : "Big Block"               , "population":60},
    {"path" : "assets/buildings/building7.png" , "name" : "Mini House"              , "population":4},
    {"path" : "assets/buildings/building8.png" , "name" : "House South"             , "population":5},
    {"path" : "assets/buildings/building9.png" , "name" : "House Black Roof"        , "population":6},
    {"path" : "assets/buildings/building10.png", "name" : "House With Inbuild"      , "population":6},
    {"path" : "assets/buildings/building11.png", "name" : "Small Block"             , "population":10},
    {"path" : "assets/buildings/building12.png", "name" : "Small Block"             , "population":35}, # TODO Duplicat
    {"path" : "assets/buildings/building13.png", "name" : "L Block"                 , "population":25},
    {"path" : "assets/buildings/building14.png", "name" : "Small House"             , "population":4},
    {"path" : "assets/buildings/building15.png", "name" : "Small House"             , "population":4},
    {"path" : "assets/buildings/building16.png", "name" : "Living House"            , "population":5},
    {"path" : "assets/buildings/building17.png", "name" : "Living House"            , "population":6},
    {"path" : "assets/buildings/building18.png", "name" : "Small Apartaments"       , "population":10},
    {"path" : "assets/buildings/building19.png", "name" : "Small Apartaments"       , "population":10},
    {"path" : "assets/buildings/building20.png", "name" : "Big House"               , "population":6},
    {"path" : "assets/buildings/building21.png", "name" : "Medium Apartaments"      , "population":11},
    {"path" : "assets/buildings/building22.png", "name" : "Medium Apartaments"      , "population":12},
    {"path" : "assets/buildings/building23.png", "name" : "Medium Apartaments"      , "population":13},
    {"path" : "assets/buildings/building24.png", "name" : "Small Skyscraper"        , "population":80},
    {"path" : "assets/buildings/building25.png", "name" : "Small Skyscraper 2"      , "population":86},
    {"path" : "assets/buildings/building26.png", "name" : "Shopping Mall"           , "population":20},
    {"path" : "assets/buildings/park.png"      , "name" : "Park"                    , "population":2},
]


def dump_to_json():
    import json 
    return json.dumps(datas, indent=4)


if __name__ == "__main__":
    print(dump_to_json())
    