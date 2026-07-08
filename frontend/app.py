# Database connection with fallback to a JSON-backed mock DB
@st.cache_resource
def init_db():
    db = Database(
        host=os.getenv('MYSQL_HOST', 'localhost'),
        user=os.getenv('MYSQL_USER', 'root'),
        password=os.getenv('MYSQL_PASSWORD', ''),
        database=os.getenv('MYSQL_DATABASE', 'nextstep_ai')
    )
    # Try connecting to real MySQL
    try:
        if db.connect():
            db.create_tables()
            return db
    except Exception:
        pass

    # Fallback: use MockDatabase (file-based) so frontend continues working
    try:
        from src.database.mock_db import MockDatabase
        mock_db = MockDatabase(file_path=os.path.join("data", "mock_db.json"))
        return mock_db
    except Exception:
        return None
