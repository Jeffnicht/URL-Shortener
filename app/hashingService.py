
import hashlib
import string

def hash_url_to_base62(url, length=8):
   
    # Base62 alphabet: 0-9, A-Z, a-z (62 characters total)
    alphabet = string.digits + string.ascii_uppercase + string.ascii_lowercase
    base = len(alphabet)  # 62
    
    # Create SHA-256 hash of the URL
    hash_bytes = hashlib.sha256(url.encode('utf-8')).digest()
    
    # Convert first 8 bytes to integer (plenty of entropy)
    hash_int = int.from_bytes(hash_bytes[:8], byteorder='big')
    
    # Convert to base62
    if hash_int == 0:
        return alphabet[0] * length
    
    encoded = []
    while hash_int > 0 and len(encoded) < length:
        hash_int, remainder = divmod(hash_int, base)
        encoded.append(alphabet[remainder])
    
    # Reverse to get correct order and ensure we have the desired length
    result = ''.join(reversed(encoded))
    
    # If result is shorter than desired length, take more bytes from hash
    if len(result) < length:
        # Use more bytes from the original hash
        extended_int = int.from_bytes(hash_bytes, byteorder='big')
        extended_encoded = []
        
        while extended_int > 0 and len(extended_encoded) < length:
            extended_int, remainder = divmod(extended_int, base)
            extended_encoded.append(alphabet[remainder])
        
        result = ''.join(reversed(extended_encoded))[:length]
    
    # Ensure we return exactly the requested length
    return result[:length]