#import library flask and flask restful
from flask import Flask,jsonify
from flask_restful import reqparse,Resource,Api
from flaskext.mysql import MySQL

#instance object of MySQL as mysql
mysql=MySQL()
#instance object of Flask as app
app = Flask(__name__)

#configure database server
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'example_students'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
#configure output json to not order asc
app.config['JSON_SORT_KEYS']=False

#initialitaion
mysql.init_app(app)
api=Api(app)

#this default method or index main in this program
@app.route('/')
def main():
    return "Welcome To REST API Using Flask RESTful Python"

#declare class as resource
class Students(Resource):

    #get method for read from database server
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id')
        args = parser.parse_args()
        if args['id'] is not None:
            _id=args['id']
            sql_query = "select id,name,DATE_FORMAT(date_of_birth,'%d-%m-%Y') as date_of_birth,address from students where id='{}'".format(_id)
        else:
            sql_query = "select id,name,DATE_FORMAT(date_of_birth,'%d-%m-%Y') as date_of_birth,address from students"
        conn=mysql.connect()
        cursor=conn.cursor()
        cursor.execute(sql_query)
        row_header=[x[0] for x in cursor.description]
        rv=cursor.fetchall()
        json_data=[]
        #make a json data
        for result in rv:
            json_data.append(dict(zip(row_header,result)))
        cursor.close()
        conn.close()
        return jsonify(json_data)

    #post method for insert data students
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('date_of_birth', type=str)
        parser.add_argument('address', type=str)
        args = parser.parse_args()
        print(args)
        _Name = args['name']
        _dateBirth = args['date_of_birth']
        _Address=args['address']
        if _Name is not None and _dateBirth is not None and _Address is not None:
            sql_query = """INSERT INTO students (id, name, date_of_birth, address) VALUES (NULL, '{}', '{}', '{}')""".format(_Name,_dateBirth,_Address)
            conn=mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql_query)
            conn.commit()
            cursor.close()
            conn.close()
            return jsonify({
                'message': 'Data Students Has Been Created',
                'status': True
            })
        else:
            return jsonify({
                'message': "Check your input",
                'status': False
            })

    # put method for update data students
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=str)
        parser.add_argument('name', type=str)
        parser.add_argument('date_of_birth', type=str)
        parser.add_argument('address', type=str)
        args = parser.parse_args()
        _Id = args['id']
        _Name = args['name']
        _dateBirth = args['date_of_birth']
        _Address = args['address']
        sql_query="""UPDATE students SET name = '{}', date_of_birth = '{}', address = '{}' WHERE id = {}""".format(_Name,_dateBirth,_Address,_Id)
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql_query)
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({
            'message': 'Data Students Has Been Updated',
            'status': True
        })

    #delete method for delete data students
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id')
        args = parser.parse_args()
        _id = args['id']
        if _id is None:
            return jsonify({
                'message' : 'ID Required',
                'status' : False
            })
        else:
            try:
                sql_query="""DELETE FROM students WHERE id='{}'""".format(_id)
                conn = mysql.connect()
                cursor=conn.cursor()
                cursor.execute(sql_query)
                conn.commit()
                cursor.close()
                conn.close()
                return jsonify({
                    'message': 'Data Students Has Been Deleted',
                    'status': True
                })
            except Exception as e:
                return jsonify({
                    'message': e,
                    'status': False
                })

#add route to resource
api.add_resource(Students,'/students')

if __name__ == "__main__":
    app.run(debug=True)