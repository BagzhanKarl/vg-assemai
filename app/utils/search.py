from sentence_transformers import SentenceTransformer
import pickle
import torch


class SemanticBot:
    def __init__(self):
        self.model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-mpnet-base-v2')
        self.document_sections = []
        self.embeddings = None

    def semantic_search(self, query, top_k=2):
        query_embedding = self.model.encode(query, convert_to_tensor=True)
        cos_scores = torch.nn.functional.cosine_similarity(query_embedding, self.embeddings)
        top_results = torch.topk(cos_scores, k=min(top_k, len(self.document_sections)))

        results = []
        for score, idx in zip(top_results.values, top_results.indices):
            if score > 0.3:
                results.append({
                    'content': self.document_sections[idx],
                    'score': float(score)
                })
        return results

    def generate_response(self, query):
        results = self.semantic_search(query)
        if not results:
            return "Извините, я не нашел релевантной информации по вашему запросу."
        relevant_sections = [r['content'] for r in sorted(results, key=lambda x: x['score'], reverse=True)]
        return "\n".join(relevant_sections)

    def load_model(self, file_path):
        with open(file_path, 'rb') as f:
            data = pickle.load(f)
        self.document_sections = data['document_sections']
        self.embeddings = data['embeddings']


def create_semantic_response(query, model_path='app/utils/semantic_model.pkl'):
    bot = SemanticBot()
    bot.load_model(model_path)
    context = bot.generate_response(query)

    prompt = f"""ТОП-2 ответа который мог бы подойти к вашему вопросу. \n\n

    {context}

    """

    return prompt