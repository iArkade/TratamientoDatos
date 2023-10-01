from flask import Flask
from mongo import MongoConnection
from flask import render_template
from flask import request



app = Flask(__name__, template_folder='views')

# Creamos la conexión con la base de datos
db_client = MongoConnection().client
db = db_client['MercadoLibre']
col = db["laptops"]



@app.route("/", methods=["GET"])
def index():
    laptops = col.find()

    return render_template("index.html", laptops=laptops)


@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("query")
    query = str(query)

    laptops = col.find({
        "$or": [
            {"titulo": {"$regex": query, "$options": "i"}},
            {"precio": {"$regex": query, "$options": "i"}},
            {"descripcion": {"$regex": query, "$options": "i"}}
        ]
    })

    laptops_list = list(laptops)
    if laptops_list:
        return render_template("search.html", laptops=laptops_list)
    else:
        return render_template("search.html", error="No se encontraron resultados")


if __name__ == "__main__":
    app.run(debug=True)