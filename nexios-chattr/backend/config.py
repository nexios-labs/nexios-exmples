from nexios.config import MakeConfig




test_config = MakeConfig({
    "secret_key":"nexios-chattr",
    "cors":{
        "allow_origins":["*"]
    }
})


db_config = {
    "connections": {"default": "sqlite://db.sqlite3"},  # Change to your DB
    "apps": {
        "models": {
            "models": ["DBEntities", "aerich.models"],
            "default_connection": "default",
        },
    },
}
