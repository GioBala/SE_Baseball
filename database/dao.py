from database.DB_connect import DBConnect
from model.team import Team

class DAO:
    @staticmethod
    def query_esempio():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT * FROM esempio """

        cursor.execute(query)

        for row in cursor:
            result.append(row)

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_anni():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor()
        query = """ SELECT DISTINCT year FROM `team` WHERE year>=1980; """
        cursor.execute(query)
        for row in cursor:
            result.append(row[0])
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_teams():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """ SELECT team.*,0 as salario FROM team WHERE (team.year<1985 AND team.year>=1980) OR team.year>2016  GROUP BY team.id; """
        cursor.execute(query)
        for row in cursor:
            result.append(Team(**row))
        query = """ SELECT team.*,SUM(salary.salary) as salario FROM team JOIN salary ON salary.team_id=team.id WHERE salary.year=team.year GROUP BY team.id """
        cursor.execute(query)
        for row in cursor:
            result.append(Team(**row))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_team_by_year(year):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        if 1984 < year < 2017:
            query = """ SELECT team.*,SUM(salary.salary) as salario FROM team JOIN salary ON salary.team_id=team.id WHERE salary.year=team.year AND team.year=%s GROUP BY team.id; """
        else:
            query="SELECT team.*,0 as salario FROM team WHERE team.year=%s GROUP BY team.id;"
        cursor.execute(query, (year,))
        for row in cursor:
            result.append(Team(**row))
        cursor.close()
        conn.close()
        return result