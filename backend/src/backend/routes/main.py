from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..services import knowledge_base, search, feeds, clustering
from datetime import datetime

main_bp = Blueprint('main', __name__)

@main_bp.route('/documents', methods=['GET'])
@jwt_required()
def get_documents():
    user_id = get_jwt_identity()
    doc_type = request.args.get('type')
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')

    start_date = None
    if start_date_str:
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        except ValueError:
            return jsonify({"msg": "Invalid start_date format. Use YYYY-MM-DD."}), 400

    end_date = None
    if end_date_str:
        try:
            end_date = datetime.strptime(end_date_str + " 23:59:59", '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return jsonify({"msg": "Invalid end_date format. Use YYYY-MM-DD."}), 400
    
    docs = knowledge_base.get_user_documents(user_id, doc_type, start_date, end_date)
    return jsonify(docs)

@main_bp.route('/documents', methods=['POST'])
@jwt_required()
def upload_document():
    if 'file' not in request.files:
        return jsonify({"msg": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"msg": "No selected file"}), 400
    
    user_id = get_jwt_identity()
    doc = knowledge_base.add_document(user_id, file)
    if doc:
        return jsonify({"msg": "File uploaded successfully"}), 201
    return jsonify({"msg": "File type not supported"}), 400

@main_bp.route('/documents/<int:doc_id>', methods=['DELETE'])
@jwt_required()
def delete_document(doc_id):
    user_id = get_jwt_identity()
    if knowledge_base.delete_document(user_id, doc_id):
        return jsonify({"msg": "Document deleted successfully"})
    return jsonify({"msg": "Document not found"}), 404

@main_bp.route('/documents/batch_delete', methods=['POST'])
@jwt_required()
def batch_delete_documents():
    user_id = get_jwt_identity()
    doc_ids = request.json.get('doc_ids', [])
    if not doc_ids:
        return jsonify({"msg": "No document IDs provided"}), 400
    
    deleted_count = knowledge_base.batch_delete_documents(user_id, doc_ids)
    return jsonify({"msg": f"{deleted_count} documents deleted successfully"})

@main_bp.route('/documents/<int:doc_id>', methods=['PUT'])
@jwt_required()
def edit_document(doc_id):
    user_id = get_jwt_identity()
    data = request.get_json()
    tags = data.get('tags')
    source = data.get('source')

    if knowledge_base.edit_document_metadata(user_id, doc_id, tags, source):
        return jsonify({"msg": "Document updated successfully"})
    return jsonify({"msg": "Document not found"}), 404

@main_bp.route('/search', methods=['POST'])
@jwt_required()
def search_documents():
    query = request.json.get('query')
    if not query:
        return jsonify({"msg": "Query is required"}), 400
    user_id = get_jwt_identity()
    results = search.perform_search(user_id, query)
    return jsonify(results)

@main_bp.route('/report/keywords', methods=['GET'])
@jwt_required()
def keyword_report():
    user_id = get_jwt_identity()
    report = search.generate_keyword_report(user_id)
    return jsonify(report)

@main_bp.route('/report/clustering', methods=['GET'])
@jwt_required()
def clustering_report():
    user_id = get_jwt_identity()
    report = clustering.generate_cluster_report(user_id)
    return jsonify(report)

@main_bp.route('/feeds', methods=['GET'])
@jwt_required()
def get_feeds():
    user_id = get_jwt_identity()
    user_feeds = feeds.get_user_feeds(user_id)
    return jsonify(user_feeds)

@main_bp.route('/feeds', methods=['POST'])
@jwt_required()
def add_feed():
    url = request.json.get('url')
    if not url:
        return jsonify({"msg": "URL is required"}), 400
    user_id = get_jwt_identity()
    feed = feeds.add_feed(user_id, url)
    if feed:
        return jsonify({"id": feed.id, "url": feed.url}), 201
    return jsonify({"msg": "Feed already exists"}), 400

@main_bp.route('/feeds/<int:feed_id>', methods=['DELETE'])
@jwt_required()
def delete_feed(feed_id):
    user_id = get_jwt_identity()
    if feeds.delete_feed(user_id, feed_id):
        return jsonify({"msg": "Feed deleted successfully"})
    return jsonify({"msg": "Feed not found"}), 404
