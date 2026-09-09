from database.DB_connect import DBConnect
from model.airport import Airport
from model.tratta import Tratta


class DAO():

    @staticmethod
    def getAllAirports():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT * from airports a order by a.AIRPORT asc"""

        cursor.execute(query)

        for row in cursor:
            result.append(Airport(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllNodes(n, idMapA):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ select t.ID, t.IATA_CODE, count(*) as N
                    from(select a.ID, a.IATA_CODE, f.AIRLINE_ID 
                    from airports a, flights f 
                    where a.ID =f.ORIGIN_AIRPORT_ID or a.ID=f.DESTINATION_AIRPORT_ID 
                    group by a.ID, a.IATA_CODE, f.AIRLINE_ID
                    ) t
                    group by t.ID, t.IATA_CODE
                    having N>=%s
                    order by N asc"""

        cursor.execute(query,(n,))

        for row in cursor:
            result.append(idMapA[row['ID']])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdgesV1( idMapA):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID, count(*) as peso
                    FROM flights f
                    group by f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID 
                    ORDER BY f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID  """

        cursor.execute(query)

        for row in cursor:
           # result.append(idMapA[row['ORIGIN_AIRPORT_ID']],
                        #  idMapA[row['DESTINATION_AIRPORT_ID']],
                             #  row['peso'])
        #OPPURE USO L'OGGETTO TRATTA
            result.append(Tratta(idMapA[row['ORIGIN_AIRPORT_ID']],
                                 idMapA[row['DESTINATION_AIRPORT_ID']],
                                 row['peso']))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdgesV2(idMapA):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT t1.ORIGIN_AIRPORT_ID, t1.DESTINATION_AIRPORT_ID, coalesce (t1.n,0)+coalesce (t2.n,0) as peso
                    FROM( 
                    SELECT f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID, count(*) as n
                    FROM flights f
                    group by f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID 
                    ORDER BY f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID) t1 
                     LEFT JOIN (
                    SELECT f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID, count(*) as n
                    FROM flights f
                    group by f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID 
                    ORDER BY f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID) t2
                    ON t1.ORIGIN_AIRPORT_ID=t2.DESTINATION_AIRPORT_ID AND t1.DESTINATION_AIRPORT_ID=t2.ORIGIN_AIRPORT_ID
                    where t1.ORIGIN_AIRPORT_ID<t1.DESTINATION_AIRPORT_ID  or t2.ORIGIN_AIRPORT_ID is Null
                    """

        cursor.execute(query)

        for row in cursor:

            result.append(Tratta(idMapA[row['ORIGIN_AIRPORT_ID']],
                                 idMapA[row['DESTINATION_AIRPORT_ID']],
                                 row['peso']))

        cursor.close()
        conn.close()
        return result