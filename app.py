import joblib
import pandas as pd
from flask import Flask, render_template, request
import numpy as np

# Load top_60_books using joblib
top_60_books = joblib.load('topbooks(60).pkl')

# Load df_books using joblib
df_books = joblib.load('book_dataset.pkl')

# Load final_dataset using joblib
final_dataset = joblib.load('final_dataset.pkl')

# Load similarity_score using joblib
similatrity_score = joblib.load('sim_score.pkl')


# except Exception as e:
#     print(f"Error loading pickled file: {e}")


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html',
                           top_60_books=top_60_books,
                           book_name=list(top_60_books['Book-Title'].values),
                           rating=list(top_60_books['Book-Rating'].values),
                           avg_rating=list(top_60_books['avg_rating'].values),
                           author=list(top_60_books['Book-Author'].values),
                           publisher=list(top_60_books['Publisher'].values),
                           img=list(top_60_books['Image-URL-M'].values)
                           )


@app.route('/recommandation')
def recomaded():
    return render_template('recommandation.html')

@app.route('/recom_value',methods=['POST'] )
def similar_show():


                user_input = request.form.get('user_book')

                index = np.where(final_dataset.index == user_input)[0][0]
                similar_item = sorted(list(enumerate(similatrity_score[index])), key=lambda x: x[1], reverse=True)[1:5]

                data = []
                for i in similar_item:
                    items = []
                    # print(pivot.index[i[0]])
                    temp_var = df_books[df_books['Book-Title'] == final_dataset.index[i[0]]]
                    items.extend(list(temp_var.drop_duplicates('Book-Title')['Book-Title'].values))
                    items.extend(list(temp_var.drop_duplicates('Book-Title')['Book-Author'].values))
                    items.extend(list(temp_var.drop_duplicates('Book-Title')['Image-URL-M'].values))
                    data.append(items)
                print(data)
                # return data
                return render_template('recommandation.html',data=data)

            # return render_template('recommandation.html')

        #




if __name__ == '__main__':
    app.run(debug=True)
