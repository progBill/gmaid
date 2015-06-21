import MySQLdb

class Database:

    def __init__(self):
        self.connect()

    def _check_connection(func):
        def checker(self, *args, **kwargs):
            try:
                self.cur.execute("SELECT 1")
            except:
                self.connect()
            finally:
                return func(self, *args, **kwargs)
        return checker

    def connect(self):
        self.db = MySQLdb.connect(user='bill',db='gmtools')
        self.cur = self.db.cursor()

    @_check_connection
    def get_npc_base(self, params=[]):
        """gets the fundamentals for an NPC"""

        sql = """
            SELECT a.first, a.last, a.sex, b.name
            FROM gmtools.names a
            INNER JOIN gmtools.culture b
            ON a.culture = b.id
        """

        self.cur.execute(sql)
        return self.cur.fetchall()

    @_check_connection
    def get_all_professions(self):
        """gets professions based on parameters"""
        sql = """
            SELECT occupation, description, category, rarity, id
            FROM gmtools.professions
        """
        self.cur.execute(sql)
        return self.cur.fetchall()

    @_check_connection
    def get_all_traits(self):
        """gets all personality traits"""
        sql = """
            SELECT name 
            FROM gmtools.traits
        """

        self.cur.execute(sql)
        return self.cur.fetchall()

    @_check_connection
    def save_name(self, names):
        """Saved an NPC name in the DB"""
        sql = "INSERT INTO names (first, last, sex) VALUES('%s','',3)"
        for name in names:
            name = name.replace('\n', '')
            self.cur.execute(sql % name)
            self.db.commit()

    @_check_connection
    def get_all_places(self):
        """get's a town name"""
        sql = """
            SELECT name 
            FROM places
        """
        self.cur.execute(sql)
        return self.cur.fetchall()

if __name__ == '__main__':
    db = Database()
    print db.get_npc_base()

#    with open('/home/bill/Documents/gaming/names') as f:
#        names = f.readlines()

#    save_name(names)

