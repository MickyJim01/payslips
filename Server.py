"""Server Module"""


class Server:
    """Server Class

    Available functions:
    - connect() - > establish a connection to the database via ssh then psycopg2
    - disconnect() -> disconnect from the database
    - version() -> return version of the connected databse using SQL
    - execute(command) -> equivelant to execute() from psycopg2
    - fetch() -> equivelant to fetchall() from psycopg2
    - print_fetch() -> instead of returning results as str, prints the results
    """

    import psycopg2
    from sshtunnel import SSHTunnelForwarder
    import json

    def __init__(self, database: str = "payslipsdb"):
        """Initialize Server object

        If using WITH a context manager, I.E. a 'with' statement,
        the cursor object from psycopg2 is returned.

        If using WITHOUT context manager, must use:
        - execute()
        - fetch()
        - print_fetch()
        """
        self.database: str = database
        pass

    def __enter__(self):
        """Create and return a cursor object."""
        self.connect(self.database)
        self.cur = self.conn.cursor()
        return self.cur

    def __exit__(self, *args):
        """Close the Server."""
        self.disconnect()

    def connect(self) -> None:
        """Connect to the server."""
        try:
            # Load the login details
            with open("./secrets/login.json", "r") as file:
                self.login = self.json.load(file)
            self.user = self.login["login"]["user"]
            self.password = self.login["login"]["password"]

            self.server = self.SSHTunnelForwarder(
                ("10.0.0.200", 22),
                # ssh_private_key="</path/to/private/ssh/key>",
                ### in my case, I used a password instead of a private key
                ssh_username=self.user,
                ssh_password=self.password,
                remote_bind_address=("localhost", 5432),
            )

            self.server.start()
            print("Server connected")

            params: dict = {
                "database": self.database,
                "user": self.user,
                "password": self.password,
                "host": "localhost",
                "port": self.server.local_bind_port,
            }

            self.conn = self.psycopg2.connect(**params)
            self.cur = self.conn.cursor()
            print("Connected to database:", self.database)

        except:
            print("Connection Failed")
            exit()

    def disconnect(self) -> None:
        try:
            self.cur.close()
            self.conn.close()
            self.server.stop()
            print("Disconnected from server")
        except:
            print("Something went wrong when disconnecting")

    def version(self):
        self.cur.execute("SELECT version();")
        result = self.cur.fetchall()
        print(result)

    def execute(self, command: str) -> None:
        self.cur.execute(command)
        self.cur.fetchall()

    def fetch(self) -> str:
        self.cur.fetchall()

    def print_fetch(self) -> None:
        result = self.fetch()
        print(result)
