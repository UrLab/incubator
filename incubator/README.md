Le routeur crossbar doit avoir un truc du genre dans sa config :

"paths": {
    ...
    "publish": {
        "type": "publisher",
        "realm": "realm1",
        "role": "anonymous",
        "options": {
           "secret": "Vairy secrette",
           "key": "Much key"
        }
    }
}
