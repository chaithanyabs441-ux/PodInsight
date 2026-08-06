import json
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss

class PodcastSearchIndex:
    def __init__(self, segments_file='segments.json'):
        self.segments_file = segments_file
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.segments = []
        self.index = None
        
    def load_segments(self):
        """Load segments from file"""
        with open(self.segments_file, 'r', encoding='utf-8') as f:
            self.segments = json.load(f)
        print(f"Loaded {len(self.segments)} segments")
        
    def build_index(self):
        """Build FAISS index from segment embeddings"""
        print("Building search index...")
        
        # Get embeddings for all segments
        texts = [seg['text'] for seg in self.segments]
        embeddings = self.model.encode(texts, show_progress_bar=True)
        
        # Normalize embeddings for cosine similarity
        embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)
        
        # Build FAISS index
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dimension)  # Inner product for cosine similarity
        self.index.add(embeddings.astype('float32'))
        
        # Save index
        faiss.write_index(self.index, 'podcast_index.faiss')
        
        print("Index built and saved!")
        
    def search(self, query, top_k=3):
        """Search for most relevant segments"""
        if self.index is None:
            self.load_index()
        
        # Encode query
        query_embedding = self.model.encode([query])
        query_embedding = query_embedding / np.linalg.norm(query_embedding)
        
        # Search
        scores, indices = self.index.search(query_embedding.astype('float32'), top_k)
        
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < len(self.segments):
                segment = self.segments[idx].copy()
                segment['relevance_score'] = float(score)
                results.append(segment)
        
        return results
    
    def load_index(self):
        """Load pre-built index"""
        self.load_segments()
        self.index = faiss.read_index('podcast_index.faiss')

# Build the index
if __name__ == "__main__":
    search_index = PodcastSearchIndex()
    search_index.load_segments()
    search_index.build_index()
    
    # Test search
    query = "What is first-principles thinking?"
    results = search_index.search(query)
    
    for i, result in enumerate(results):
        print(f"\nResult {i+1}:")
        print(f"Time: {result['start_formatted']} - {result['end_formatted']}")
        print(f"Text: {result['text'][:200]}...")
        print(f"Relevance: {result['relevance_score']:.3f}")