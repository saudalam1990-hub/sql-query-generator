from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

history = []

@app.route("/", methods=["GET", "POST"])
def home():

    query = ""

    if request.method == "POST":

        table = request.form['table']
        action = request.form['action']
        columns = request.form['columns']
        values = request.form['values']
        condition = request.form['condition']
        datatype = request.form.get("datatype")

        excel_data = request.form.get("excel_data")

        file = request.files.get("file")

        # INSERT
        if action == "INSERT":

            # Excel File Upload
            if file and file.filename != "":

                df = pd.read_excel(file)

                queries = []

                for _, row in df.iterrows():

                    vals = []

                    for v in row:

                        if isinstance(v, str):
                            vals.append(f"'{v}'")
                        else:
                            vals.append(str(v))

                    q = f"INSERT INTO {table} VALUES ({', '.join(vals)});"

                    queries.append(q)

                query = "\n".join(queries)

            # Excel Paste
            elif excel_data:

                rows = excel_data.strip().split("\n")

                queries = []

                for row in rows:

                    vals = row.split()

                    formatted = []

                    for v in vals:

                        if v.isdigit():
                            formatted.append(v)
                        else:
                            formatted.append(f"'{v}'")

                    q = f"INSERT INTO {table} VALUES ({', '.join(formatted)});"

                    queries.append(q)

                query = "\n".join(queries)

            # Manual Insert
            else:

                query = f"INSERT INTO {table} ({columns}) VALUES ({values});"

        # UPDATE
        elif action == "UPDATE":

            query = f"UPDATE {table} SET {values} WHERE {condition};"

        # DELETE
        elif action == "DELETE":

            query = f"DELETE FROM {table} WHERE {condition};"

        # SELECT
        elif action == "SELECT":

            query = f"SELECT {columns} FROM {table} WHERE {condition};"

        # CREATE TABLE
        elif action == "CREATE":

            cols = columns.split(",")
            types = datatype.split(",")

            final_cols = []

            for c, t in zip(cols, types):

                final_cols.append(f"{c.strip()} {t.strip()}")

            query = f"CREATE TABLE {table} (\n" + ",\n".join(final_cols) + "\n);"

        if query:
            history.insert(0, query)

    history_data = history[:5]

    return render_template(
        "index.html",
        query=query,
        history=history_data
    )

if __name__ == "__main__":
    app.run(debug=True)