import heapq
from collections import Counter


def counter_nbest(text, k): 
    # Tokenize text
    tokens = text.split()
    # Count token frequencies
    token_counts = Counter(tokens)
    # Extract top k tokens
    top_tokens = token_counts.most_common(k)
    # Print top k tokens
    print(f"Top {k} tokens:", top_tokens)
    
    

def heap_nbest(text, k): 
    # Tokenize text
    tokens = text.split()
    # Count token frequencies
    token_counts = Counter(tokens)
    # Create a min-heap to store the top two tokens
    heap = []
    # Iterate through the token frequency dictionary and maintain the min-heap
    for token, count in token_counts.items():
        if len(heap) < k:
            heapq.heappush(heap, (count, token))
        else:
            if count > heap[0][0]:
                heapq.heappop(heap)
                heapq.heappush(heap, (count, token))
    # Extract top k tokens
    top_tokens = [heapq.heappop(heap)[1] for _ in range(len(heap))]
    # Reverse the order to get the top token first
    top_tokens.reverse()
    # Print top k tokens
    print(f"Top {k} tokens:", top_tokens)
    
    