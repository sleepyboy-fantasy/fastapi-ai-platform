from sentence_transformers import SentenceTransformer


_model = None


def get_embedding_model():

    global _model

    if _model is None:

        _model = SentenceTransformer(
            "/app/models/bge-small-zh-v1.5"
        )

    return _model


def generate_embedding(text: str):

    model = get_embedding_model()

    vector = model.encode(
        text,
        normalize_embeddings=True
    )

    return vector.tolist()