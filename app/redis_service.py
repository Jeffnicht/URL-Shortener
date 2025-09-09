from .extensions import redis_client
from .hashingService import hash_url_to_base62
from urllib.parse import urlparse
from .calcStringtoSeconds import convert_to_seconds
from flask import Blueprint, render_template, request, render_template, redirect, url_for,flash
def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def keyExists(func):
    def wrapper(key_or_url, *args, retain="1H", is_url=True, **kwargs):
        if key_or_url is None:
            return "Nothing was Provided"

        if is_url:
            if not is_valid_url(key_or_url):
                return "Invalid URL format"
            try:
                hash = hash_url_to_base62(key_or_url)
                fetchedUrl = redis_client.get(hash)
                if not fetchedUrl:
                    return func(hash, key_or_url, retain=retain)
                else:
                    return hash
            except Exception as e:
                print("Error while hashing or reaching redis:", e)
                # Instead of redirect, raise error or return None
                raise RuntimeError("Redis connection error")

        else:
            try:
                fetchedUrl = redis_client.get(key_or_url)
                if not fetchedUrl:
                    return "The shortened url you provided is not registered"
                else:
                    return func(fetchedUrl)
            except Exception as e:
                print("Error can't reach redis:", e)
                raise RuntimeError("Redis connection error")

    return wrapper


@keyExists
def getUrl(url):
    return url
 

@keyExists
def setUrl(hash, url,retain="1H"):
    try:
        redis_client.set(hash, url,ex=convert_to_seconds(retain))
        return hash  
    except Exception as e:
        print(f"Error while inserting values in redis: {e}")
        return "Couldn't insert your value"
