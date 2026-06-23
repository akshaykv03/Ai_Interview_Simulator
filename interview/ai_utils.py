from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer(
    'all-MiniLM-L6-v2'
)

def calculate_similarity(
        correct_answer,
        user_answer
):

    embeddings = model.encode([
        correct_answer,
        user_answer
    ])

    similarity =cosine_similarity(
        [embeddings[0]],
        [embeddings[1]]
    )[0][0]

    return round(similarity * 100, 2)


def calculate_marks(
        similarity,
        total_marks
):

    if similarity >= 70:

        return total_marks

    elif similarity >= 50:

        return total_marks * 0.7

    elif similarity >= 30:

        return total_marks * 0.5

    elif similarity >= 15:

        return total_marks * 0.3

    else:

        return 0

    if similarity >= 80:

        return total_marks

    elif similarity >= 60:

        return total_marks * 0.7

    elif similarity >= 40:

        return total_marks * 0.5

    else:

        return 0