import psycopg2
conn = psycopg2.connect(database="BD",
                                     user="postgres",
                                     password=" ",
                                     host="localhost",
                                     port="5432")
cursor = conn.cursor()
def find_schools_in_distr(cursor,distr):
    cursor.execute(f'Select school_name from schools where iddistr = {distr}')
    return [ans[0] for ans in cursor.fetchall()]

print(find_schools_in_distr(cursor,1))