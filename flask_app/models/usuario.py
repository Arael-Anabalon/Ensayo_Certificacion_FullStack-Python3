from flask_app.config.pymysqlconnection import connectToMySQL

class Usuario:
    def __init__(self, data):
        self.id_usuario = data['id_usuario']
        self.nombre = data['nombre']
        self.apellido = data['apellido']
        self.email = data['email']
        self.contrasena = data['contrasena']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def registrar(cls, data):
        query = """
            INSERT INTO usuarios (nombre, apellido, email, contrasena, created_by)
            VALUES (%(nombre)s, %(apellido)s, %(email)s, %(contrasena)s, 'Registro');
        """
        return connectToMySQL().query_db(query, data)

    @classmethod
    def obtener_por_email(cls, email):
        query = "SELECT * FROM usuarios WHERE email = %(email)s AND deleted = 0;"
        data = {'email': email}
        resultados = connectToMySQL().query_db(query, data)
        if resultados:
            return cls(resultados[0])
        return None
