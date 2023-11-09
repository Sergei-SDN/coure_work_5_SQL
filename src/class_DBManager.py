import psycopg2
from pprint import pprint


class DBManager:
    """
    Этот класс для создания и управления базой данных
    """

    def __init__(self, database_name: str, params: dict):
        self.name = database_name
        self.params = params
        self.create_database()
        self.create_table_companies()
        self.create_table_vacancies()

    def create_database(self):
        """
        Этот метод создания базы данных
        """
        conn = psycopg2.connect(**self.params)
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute(f"DROP DATABASE IF EXISTS {self.name}")
        cur.execute(f'CREATE DATABASE {self.name}')

        conn.close()

        self.params.update({'dbname': self.name})

    def create_table_companies(self):
        """
        Этот метод создания таблицы компаний
        """
        conn = psycopg2.connect(**self.params)
        cur = conn.cursor()
        cur.execute('''CREATE TABLE companies (
            company_id_hh integer PRIMARY KEY,
            company_name varchar(150),
            employer_url varchar(150)
        )''')
        conn.commit()

        cur.close()
        conn.close()

    def create_table_vacancies(self):
        """
        Этот метод создания таблицы вакансий
        """
        conn = psycopg2.connect(**self.params)
        cur = conn.cursor()
        cur.execute('''CREATE TABLE vacancies (
            vacancy_id_hh integer PRIMARY KEY,
            company_id_hh integer,
            vacancy_name varchar(150),
            data_published date,
            salary_average integer,
            area varchar(150),
            url varchar(150),
            requirement varchar(500),
            experience varchar(150),
            employment varchar(150),

            CONSTRAINT fk_hh_vacancies_vacancies FOREIGN KEY(company_id_hh) REFERENCES companies(company_id_hh)
        )''')
        conn.commit()

        cur.close()
        conn.close()

    def insert_data_company(self, data: dict):
        """
        Этот метод вставки данных в таблицу компаний
        """
        conn = psycopg2.connect(**self.params)
        cur = conn.cursor()

        cur.execute("INSERT INTO companies VALUES (%s, %s, %s)",
                    (int(data["employer"]["id"]), data["employer"]["name"], data["employer"]["alternate_url"]))

        conn.commit()

        cur.close()
        conn.close()

    def insert_data_vacancy(self, vacancies: list):
        """
        Этот метод вставки данных в таблицу вакансий
        """
        conn = psycopg2.connect(**self.params)
        cur = conn.cursor()
        for vacancy in vacancies:
            cur.execute("INSERT INTO vacancies VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                        (vacancy.id,
                         vacancy.employer_id,
                         vacancy.name,
                         vacancy.data_published,
                         vacancy.salary_average,
                         vacancy.area,
                         vacancy.url,
                         vacancy.requirement,
                         vacancy.experience,
                         vacancy.employment))

        conn.commit()

        cur.close()
        conn.close()

    def get_companies_and_vacancies_count(self):
        """
        Этот метод получения компаний с количеством вакансий
        """
        conn = psycopg2.connect(**self.params)
        cur = conn.cursor()
        cur.execute('''SELECT company_name, COUNT(*)
        FROM vacancies
        JOIN companies USING (company_id_hh)
        GROUP BY company_name''')
        pprint(cur.fetchall())
        cur.close()
        conn.close()

    def get_all_vacancies(self):
        """
        Этот метод получения всех вакансий
        """
        conn = psycopg2.connect(**self.params)
        cur = conn.cursor()
        cur.execute('''SELECT company_name, vacancy_name, salary_average, url
        FROM vacancies
        JOIN companies USING (company_id_hh)''')
        pprint(cur.fetchall())
        cur.close()
        conn.close()

    def get_avg_salary(self):
        """
        Этот метод получения средней зарплаты по вакансиям
        """
        conn = psycopg2.connect(**self.params)
        cur = conn.cursor()
        cur.execute('''SELECT AVG(salary_average)
        FROM vacancies
        WHERE salary_average > 0''')
        pprint(cur.fetchall())
        cur.close()
        conn.close()

    def get_vacancies_with_higher_salary(self):
        """
        Этот метод получения вакансий с зарплатой выше средней зарплаты по вакансиям.
        """
        conn = psycopg2.connect(**self.params)
        cur = conn.cursor()
        cur.execute('''SELECT company_name, vacancy_name, salary_average, url
        FROM vacancies
        JOIN companies USING (company_id_hh)
        WHERE salary_average > (SELECT AVG(salary_average)
        FROM vacancies
        WHERE salary_average > 0)
        ORDER BY salary_average DESC''')
        pprint(cur.fetchall())
        cur.close()
        conn.close()

    def get_vacancies_with_keyword(self, word: str):
        """
        Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python
        """
        conn = psycopg2.connect(**self.params)
        cur = conn.cursor()
        cur.execute(f'''SELECT company_name, vacancy_name, salary_average, url
        FROM vacancies
        JOIN companies USING (company_id_hh)
        WHERE vacancy_name LIKE '%{word.lower()}%' OR vacancy_name LIKE '%{word.title()}%' OR vacancy_name LIKE '%{word.upper()}%';''')
        pprint(cur.fetchall())
        cur.close()
        conn.close()
