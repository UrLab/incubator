import requests

TOKEN = "EAACEdEose0cBAEPUFZAd2zp4wZAMZAqh5XB2mcCZA58c7NnzEsNhl8k6WWWl9ppZAUZASbJkVZCinCCJpvwFy5oZAI7CjWWRvDx2Ya9IU9yAgYluqX9x090u6eTZARdKp16qAXX1kTbQ9q0zn0k3zsM912DZBxO51Y2rypoHJSkQkIGRZAQT0xseEljlqX5N22m408aBj7xpvmZAewZDZD"


def post_to_group(group_id, token, message, link=None):
    """
    Doc : https://developers.facebook.com/docs/graph-api/reference/v2.9/group/feed#publish
    """
    data = {
        'message': message,
        'access_token': token,
    }
    if link:
        data["link"] = link

    response = requests.post('https://graph.facebook.com/v2.9/%s/feed' % group_id, data=data)
    assert response.code == 200

    return response.json()["id"]


def post_to_page(page_id, token, message):
    """
    Doc : https://developers.facebook.com/docs/graph-api/reference/v2.9/page/feed#publish
    """
    pass
