from flask import Blueprint, render_template, request, render_template, redirect, url_for,flash, jsonify
from . import redis_service as r
from .redis_service import getUrl,setUrl
from flask import request,render_template
from .calcStringtoSeconds import convert_to_seconds
import os

maxUrlLen = 800
shortener = Blueprint('shortener', __name__)

def normalize_url(url):
    """Add protocol if missing, defaulting to https://"""
    if not url:
        return url
    
    # Remove any leading/trailing whitespace
    url = url.strip()
    
    # If no protocol is specified, add https:// as default
    
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    return url

@shortener.route("/", methods=["GET"])
@shortener.route("/index", methods=["GET"])
def index():
    return render_template("index.html")

@shortener.route("/<string:short_code>")
def redirect_short_url(short_code):
    try:
        original_url = r.getUrl(short_code, is_url=False)
        if isinstance(original_url, tuple) or original_url is None:
            flash("URL not found or invalid short code")
            return redirect(url_for("shortener.index"))
        if original_url and not original_url.startswith("The shortened url you provided is not registered"):
            # decode if bytes
            url = original_url.decode('utf-8') if isinstance(original_url, bytes) else original_url
            return redirect(url)
        else:
            flash("URL not found or invalid short code")
            return redirect(url_for("shortener.index"))
    except RuntimeError:
        return redirect(url_for("shortener.error_page"))
    except Exception as e:
        flash("Unexpected error occurred")
        return redirect(url_for("shortener.index"))

@shortener.route("/shorten", methods=["POST"])
def shorten_url():
    try:
        raw_url = request.form.get("url")
        if len(raw_url) > maxUrlLen:
            return render_template("index.html", url_too_long=True)
        
        url = normalize_url(raw_url)  # Add protocol if missing
        
        retain = request.form.get("retain", "")
        print(f"retain from page : {retain}")
        short_code = r.setUrl(url, retain=retain, is_url=True)
        if not short_code or isinstance(short_code, str) and short_code.startswith("Couldn't insert"):
            flash("Failed to shorten URL")
            return redirect(url_for("shortener.index"))
        
        base_url = request.host_url
        shortened_url = f"{base_url}{short_code}"

        saved_chars = len(url) - len(shortened_url)
        compression_ratio = round((saved_chars / len(url)) * 100, 2) if len(url) > 0 else 0

        return render_template("index.html",
                               shortened_url=shortened_url,
                               original_url=url,
                               saved_chars=saved_chars,
                               compression_ratio=compression_ratio,
                               retain=retain)
    except RuntimeError:
        return redirect(url_for("shortener.error_page"))
    

@shortener.route("/error")
def error_page():
    return render_template("error.html")

@shortener.route('/api/shorten', methods=['POST'])
def handle_json():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()
    
    raw_url = data.get('url')
    if not raw_url:
        return jsonify({"error": "Missing required field: 'url'"}), 400



    if len(raw_url) > maxUrlLen:
        return jsonify({
            "error": f"URL too long. Maximum allowed length is {maxUrlLen} characters."
        }), 400

    url = normalize_url(raw_url)  # Add protocol if missing
    
    retain = data.get('retain', "1H")
    print(retain, url)
    short_code = r.setUrl(url, retain=retain, is_url=True)

    if not short_code or (isinstance(short_code, str) and short_code.startswith("Couldn't insert")):
        return jsonify({
            "error": "Couldn't insert data into the database",
            "details": "The request was either invalid or there are internal server errors"
        }), 500

    
    base_url = os.getenv("BASE_URL", request.host_url)
    shortened_url = f"{base_url}{short_code}"


    saved_chars = len(url) - len(shortened_url)
    compression_ratio = round((saved_chars / len(url)) * 100, 2) if len(url) > 0 else 0

    return jsonify({
    "shortened_url": shortened_url,
    "short_code": short_code,
    "original_url": url,
    "retain": retain,
    "saved_characters": saved_chars,
    "compression_ratio_percent": compression_ratio
        }), 200

@shortener.route('/api/<string:hash>', methods=['GET'])
def api_getUrl(hash):
    try:
        original_url = r.getUrl(hash, is_url=False)

        if isinstance(original_url, tuple) or original_url is None:
            return jsonify({
                "error": "URL not found or invalid short code"
            }), 404

        if original_url and not str(original_url).startswith("The shortened url you provided is not registered"):
            url = original_url.decode('utf-8') if isinstance(original_url, bytes) else original_url
            return jsonify({
                "short_code": hash,
                "original_url": url
            }), 200
        else:
            return jsonify({
                "error": "Short code not registered"
            }), 404

    except RuntimeError:
        return jsonify({
            "error": "Internal server error (runtime)"
        }), 500

    except Exception as e:
        return jsonify({
            "error": "Unexpected error occurred",
        }), 500

def register_routes(app):
    app.register_blueprint(shortener)
