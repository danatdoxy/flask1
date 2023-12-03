from llama_hub.youtube_transcript import YoutubeTranscriptReader
from llama_index import VectorStoreIndex
reader = YoutubeTranscriptReader()
transcript = reader.load_data(['https://www.youtube.com/watch?v=R-Geamq9xc0'])


print(transcript[0].text)
# We'll embed and vector store the documents using pinecone
pinecone_index = VectorStoreIndex()

