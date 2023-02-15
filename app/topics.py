# collection topics to subscribe
TVS_TOPIC = "tvs-topic"
CAMERAS_TOPIC = "cameras-topic"
LAPTOPS_TOPIC = "laptops-topic"
PRINTERS_TOPIC = "printers-topic"
SMARTPHONES_TOPIC = "smartphones-topic"
TABLETS_TOPIC = "tablets-topic"
VIDEOGAMES_TOPIC = "videogames-topic"
WEARABLES_TOPIC = "wearables-topic"
# users topic
USERS_TOPIC = "users-topic"


# match collection with the corresponding topic

def get_collection_topic(collection_name):
    match collection_name:
        case "Cameras":
            topic = CAMERAS_TOPIC
        case "TVs":
            topic = TVS_TOPIC
        case "Laptops":
            topic = LAPTOPS_TOPIC
        case "Printers":
            topic = PRINTERS_TOPIC
        case "Smartphones":
            topic = SMARTPHONES_TOPIC
        case "Tablets":
            topic = TABLETS_TOPIC
        case "VideoGames":
            topic = VIDEOGAMES_TOPIC
        case "Wearables":
            topic = WEARABLES_TOPIC
        case _:
            topic = None
    return topic
