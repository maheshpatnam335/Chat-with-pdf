from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection
from sentence_transformers import SentenceTransformer
import fitz
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename


app = Flask(__name__)

def milvus_setup():
    connections.connect("default", host="localhost", port="19350")
    
    fields=[
        FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
        FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=768)
    ]

    schema= CollectionSchema(fields, "PDF Text Embeddings")

    collection = Collection(name="pdf_collection", schema=schema)


    model = SentenceTransformer('all-MiniLM-L6-v2')
    return collection, model

def pdf_to_text(file_path):
    doc = fitz.open(file_path)
    text=""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text += page.get_text()
    return text

def store_embeddings(file_path):
    text=pdf_to_text(file_path=file_path)

    collection, model = milvus_setup()
    embeddings =  model.encode([text])[0]
    collection.insert([[embeddings]])


def search(query):

    collection, model = milvus_setup()
    query_embedding = model.encode([query])[0]
    results = collection.search(data=[query_embedding], anns_field="embedding", param={"metric_type":"L2"}, limit=10)
    return results

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    results = search(query)
    return jsonify(results)


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    if file:
        # filename = secure_filename(file.filename)
        file_path = "E:\Work\Documents\Complaints\comp-pr2019-140- Facebook.pdf"
        file.save(file_path)
        store_embeddings(file_path)
        return 'File uploaded and processed', 200

if __name__ == '__main__':
    app.run(debug=True)

# results = search("search term")
# for result in results:
#     print(result.id, result.distance)