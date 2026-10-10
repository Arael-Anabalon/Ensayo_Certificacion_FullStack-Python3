from flask_app.config.pymysqlconnection import connectToMySQL

class Peluche:
    def __init__(self, data):
        self.id_peluche = data['id_peluche']
        self.nombre = data['nombre']
        self.descripcion = data['descripcion']
        self.creador_id = data['creador_id']
        self.adoptador_id = data['adoptador_id']
        self.vistas = data['vistas']
        self.creador_nombre = data.get('creador_nombre', '')
        self.adoptador_nombre = data.get('adoptador_nombre', '')

    @classmethod
    def guardar(cls, data):
        query = """
            INSERT INTO peluches (nombre, descripcion, creador_id, created_by)
            VALUES (%(nombre)s, %(descripcion)s, %(creador_id)s, %(created_by)s);
        """
        return connectToMySQL().query_db(query, data)

    @classmethod
    def obtener_todos_con_usuarios(cls):
        query = """
            SELECT p.*, 
                   CONCAT(u1.nombre, ' ', u1.apellido) AS creador_nombre,
                   CONCAT(u2.nombre, ' ', u2.apellido) AS adoptador_nombre
            FROM peluches p
            JOIN usuarios u1 ON p.creador_id = u1.id_usuario
            LEFT JOIN usuarios u2 ON p.adoptador_id = u2.id_usuario
            WHERE p.deleted = 0;
        """
        resultados = connectToMySQL().query_db(query)
        return [cls(fila) for fila in resultados] if resultados else []

    @classmethod
    def obtener_por_id_con_usuarios(cls, id_peluche):
        query = """
            SELECT p.*, 
                   CONCAT(u1.nombre, ' ', u1.apellido) AS creador_nombre,
                   CONCAT(u2.nombre, ' ', u2.apellido) AS adoptador_nombre
            FROM peluches p
            JOIN usuarios u1 ON p.creador_id = u1.id_usuario
            LEFT JOIN usuarios u2 ON p.adoptador_id = u2.id_usuario
            WHERE p.id_peluche = %(id)s AND p.deleted = 0;
        """
        data = {'id': id_peluche}
        resultados = connectToMySQL().query_db(query, data)
        return cls(resultados[0]) if resultados else None

    @classmethod
    def validar_nombre_unico(cls, nombre, id_peluche=None):
        if id_peluche:
            query = "SELECT id_peluche FROM peluches WHERE nombre = %(nombre)s AND id_peluche != %(id)s AND deleted = 0;"
            data = {'nombre': nombre, 'id': id_peluche}
        else:
            query = "SELECT id_peluche FROM peluches WHERE nombre = %(nombre)s AND deleted = 0;"
            data = {'nombre': nombre}
        resultado = connectToMySQL().query_db(query, data)
        return len(resultado) == 0

    @classmethod
    def incrementar_vista(cls, id_peluche):
        query = "UPDATE peluches SET vistas = vistas + 1 WHERE id_peluche = %(id)s;"
        return connectToMySQL().query_db(query, {'id': id_peluche})

    @classmethod
    def adoptar(cls, data):
        query = "UPDATE peluches SET adoptador_id = %(adoptador_id)s WHERE id_peluche = %(id_peluche)s;"
        return connectToMySQL().query_db(query, data)

    @classmethod
    def actualizar(cls, data):
        query = """
            UPDATE peluches 
            SET nombre = %(nombre)s, descripcion = %(descripcion)s, updated_by = %(updated_by)s
            WHERE id_peluche = %(id_peluche)s;
        """
        return connectToMySQL().query_db(query, data)

    @classmethod
    def eliminar(cls, id_peluche):
        query = "UPDATE peluches SET deleted = 1 WHERE id_peluche = %(id)s;"
        return connectToMySQL().query_db(query, {'id': id_peluche})
