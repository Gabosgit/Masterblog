from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
    {"id": 3, "title": "Zapatillas", "content": "Zapatos, zapatillas"},
    {"id": 4, "title": "Sombreros", "content": "Gorros y sombreros"},
]


def generate_new_id(list_posts):
    id_list = []
    for post in list_posts:
        id_list.append(post["id"])
    greater_id = max(id_list)
    for new_id in range(1, greater_id+1):
        if new_id not in id_list:
            return new_id
    return greater_id + 1


def check_new_post(post):
    """ If any field is missing return a json message + a status 400 """
    if post['title'] == '' and post['content'] == '':
        return jsonify("Missing Fields 'text and 'content'"), 400
    if post['title'] == '':
        return jsonify("Missing Field 'title'"), 400
    if post['content'] == '':
        return jsonify("Missing Field 'content'"), 400


@app.route('/api/posts', methods=['GET', 'POST'])
def get_posts():
    if request.method == 'POST':
        new_post = request.get_json()
        if check_new_post(new_post):
            return check_new_post(new_post)
        new_id = generate_new_id(POSTS)
        new_post['id'] = new_id
        POSTS.append(new_post)
        return new_post, 201

    sort = request.args.get('sort')
    direction = request.args.get('direction')

    if direction and sort:
        if direction == 'asc':
            direction = False
        elif direction == 'desc':
            direction = True
        else:
            return jsonify("direction key have to be asc or desc")
        try:
            sorted_posts = sorted(POSTS, key=lambda x: x[sort], reverse=direction)
        except KeyError as e:
            return jsonify("sort key have to be title or content")
        return jsonify(sorted_posts)
    return jsonify(POSTS)


def fetch_post_by_id(post_id):
    """ Returns the dictionary of the post containing the given id (post_id) """
    for post in POSTS:
        if post['id'] == post_id:
            return post
    return False


@app.route('/api/posts/<int:post_id>', methods=["DELETE"])
def delete(post_id):
    if request.method == 'DELETE':
        post = fetch_post_by_id(post_id)
        if not post:
            return jsonify("Post was not found"), 404
        POSTS.remove(post)
        return jsonify(f'"message": "Post with id {post_id} has been deleted successfully."'), 200


@app.route('/api/posts/<int:post_id>', methods=["PUT"])
def update(post_id):
    if request.method == 'PUT':
        update_post = request.get_json()
        post = fetch_post_by_id(post_id)
        print(post)
        if not post:
            return jsonify("Post was not found UPDATE"), 404
        if update_post['title']:
            post['title'] = update_post['title']
        if update_post['content']:
            post['content'] = update_post['content']
        id_post_in_list = POSTS.index(post)
        POSTS[id_post_in_list] = post
        return jsonify(post), 200

@app.route('/api/posts/search', methods=["GET"])
def search():
    """ GET Requests for 'title' and 'content'
        If gets a variable iterate in the list searching for the value
    """
    if request.method == 'GET':
        list_found = []
        search_in_title = request.args.get('title')
        search_in_content = request.args.get('content')
        for post in POSTS:
            for key, value in post.items():
                if key == 'title' and search_in_title:
                    if search_in_title.lower() in value.lower():
                        list_found.append(post)
                if key == 'content' and search_in_content:
                    if search_in_content.lower() in value.lower():
                        list_found.append(post)
        return list_found


@app.errorhandler(400)
def bad_request():
    """ Render '404.html' """
    return jsonify("Field missing"), 400


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
