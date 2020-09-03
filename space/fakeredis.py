def get_redis():
    return None


def get_mac(client):
    mac = "50:7b:9d:09:51:b6,b4:b6:76:03:17:9a,00:22:b0:ba:64:91,00:24:1d:1e:63:3d,00:27:10:aa:dc:78,00:30:05:c5:da:82,28:b2:bd:d0:2a:ff,fc:f8:ae:5b:aa:63,54:be:f7:11:93:14,54:be:f7:11:93:14,28:ba:b5:4b:51:ef,f8:e0:79:5f:d5:90,a4:9a:58:d6:ae:92,00:de:ad:00:be:ef"

    if mac == "":
        return 35, []

    return 35, mac.split(',')


def get_hostnames(client):
    return {
        "00:de:ad:00:be:ef": "this-is-a-hostname"
    }


def set_space_open(client, is_open):
    f = open('/tmp/spacestatus', 'w')
    f.write(str(is_open))
    f.close()


def space_is_open(client):
    try:
        with open('/tmp/spacestatus', 'r') as f:
            return f.read().strip() == "True"
    except Exception:
        return False
