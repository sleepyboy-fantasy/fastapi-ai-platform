from app.database import SessionLocal

from app.models.document import Document

from app.services.hash_service import calculate_file_hash


db = SessionLocal()


documents = (
    db.query(Document)
    .filter(
        Document.file_hash == None
    )
    .all()
)


for doc in documents:

    file_hash = calculate_file_hash(
        doc.file_path
    )

    doc.file_hash = file_hash

    print(
        doc.id,
        doc.filename,
        file_hash
    )


db.commit()

db.close()