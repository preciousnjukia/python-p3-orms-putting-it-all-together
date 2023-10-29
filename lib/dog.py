import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:

    all = []

    def __init__(self, name, breed):
        self.id = None
        self.name = name
        self.breed = breed

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS dogs (
                id INTEGER PRIMARY KEY,
                name TEXT,
                breed TEXT
            )
        """
        CURSOR.execute(sql)
    @classmethod
    def drop_table(self):
        CURSOR.execute("DROP TABLE IF EXISTS dogs")

    def save(self):
        sql = """
            INSERT INTO dogs (name, breed)
            VALUES(?, ?)
            """
        CURSOR.execute(sql, (self.name, self.breed))

    @classmethod
    def create(cls, name, breed):
        dog = cls(name, breed)
        dog.save()
        dog.id = 1
        return dog
    
    @classmethod
    def new_from_db(cls, row):
        if row is not None:
          id, name, breed = row
          dog = cls(name, breed)
          dog.id = id
          return dog
        else:
            return None

    @classmethod
    def get_all(cls):
        rows = CURSOR.execute("SELECT * FROM dogs").fetchall()
        
        dogs = []
        for row in rows:
            id, name, breed = row
            dog = cls(name, breed)
            dog.id =id
            dogs.append(dog)
        return dogs

    @classmethod
    def find_by_name(cls, name):
        sql = """
            SELECT *
            FROM dogs
            WHERE name = ?
            LIMIT 1
        """

        dog = CURSOR.execute(sql, (name,)).fetchone()

        return cls.new_from_db(dog)
    
    @classmethod
    def find_by_id(cls, id):
        sql = """
            SELECT *
            FROM dogs
            WHERE id = ?
            LIMIT 1
        """

        dog = CURSOR.execute(sql, (id,)).fetchone()

        return cls.new_from_db(dog)
    
    @classmethod
    def find_or_create_by(cls, name, breed):
        row = CURSOR.execute("SELECT * FROM dogs WHERE name = ? AND breed = ?", (name, breed)).fetchone() 
        if row:
            id, _, _ = row  
            dog = cls(name, breed)
            dog.id = id
        else:
            dog = cls.create(name, breed)

        return dog
    
    def save(self):
        if self.id is None:
        
            CURSOR.execute("INSERT INTO dogs (name, breed) VALUES (?, ?)", (self.name, self.breed))
            
            self.id = CURSOR.lastrowid

        return self
    
    def update(self):
        if self.id is not None:
            CURSOR.execute("UPDATE dogs SET name = ?, breed = ? WHERE id = ?", (self.name, self.breed, self.id))

        return self