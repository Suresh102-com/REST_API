from flask import Flask, request, jsonify

managedata = Flask(__name__)

# Simple in-memory store for users
users = {}
next_user_id = 1  # to auto-increment user IDs

# Get all users
@managedata.route('/users', methods=['GET'])
def get_all_users():
    return jsonify(users)

# Get a single user by ID
@managedata.route('/users/<int:user_id>', methods=['GET'])
def get_single_user(user_id):
    user = users.get(user_id)
    if user:
        return jsonify({user_id: user})
    return jsonify({"error": "User not found"}), 404

# Create a new user
@managedata.route('/users', methods=['POST'])
def create_user():
    global next_user_id
    data = request.get_json()
    # Check if required fields are present
    if not data or 'name' not in data or 'email' not in data:
        return jsonify({"error": "Please provide name and email"}), 400
    # Create and store the user
    users[next_user_id] = {
        "name": data['name'],
        "email": data['email']
    }
    # Respond with the created user
    created_user = {next_user_id: users[next_user_id]}
    next_user_id += 1
    return jsonify(created_user), 201

# Update a user
@managedata.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = users.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()

    # Update fields if provided
    user['name'] = data.get('name', user['name'])
    user['email'] = data.get('email', user['email'])

    return jsonify({user_id: user})

# Delete a user
@managedata.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if user_id in users:
        deleted = users.pop(user_id)
        return jsonify({"message": "User deleted", "user": deleted})
    return jsonify({"error": "User not found"}), 404

if __name__ == '__main__':
    managedata.run(debug=True)
