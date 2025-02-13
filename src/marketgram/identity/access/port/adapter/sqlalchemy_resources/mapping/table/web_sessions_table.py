from sqlalchemy import UUID, Column, DateTime, ForeignKey, Integer, String, Table, text

from marketgram.common.sqlalchemy_metadata import metadata


web_session_table = Table(
    'web_session',
    metadata,
    Column(
        'id', 
        UUID, 
        primary_key=True, 
        nullable=False, 
        server_default=text("gen_random_uuid()")
    ),
    Column('session_id', UUID, nullable=False),
    Column('user_id', UUID, ForeignKey('users.user_id'), nullable=False),
    Column('created_at', DateTime(timezone=True), nullable=False),
    Column('expires_in', DateTime(timezone=True), nullable=False),
    Column('device', String, nullable=False),
    Column('version_id', Integer, nullable=False)
)