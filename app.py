from flask import Flask, request, jsonify
from flask_cors import CORS
import dns.resolver
import time
import mysql.connector
import datetime

app = Flask(__name__)
CORS(app, origins='https://hosts.3dweb.ltd')
cache = {}
CACHE_EXPIRATION_TIME = 60
DNS_SERVERS = ['119.29.29.29', '114.114.114.114']

db_config = {
    'host': '127.0.0.1',
    'user': 'baoziapikey',
    'password': 'ARTe7prRe3HwJ47a',
    'database': 'apikey'
}

def resolve_dns(domain):
    if domain in cache:
        cached_data = cache[domain]
        if time.time() - cached_data['timestamp'] < CACHE_EXPIRATION_TIME:
            return cached_data['ip_addresses']
    try:
        resolver = dns.resolver.Resolver()
        resolver.nameservers = DNS_SERVERS
        answer = resolver.query(domain, 'A')
        ip_addresses = [str(rdata) for rdata in answer]
        cache[domain] = {
            'ip_addresses': ip_addresses,
            'timestamp': time.time()
        }
        return ip_addresses
    except:
        return None

def authenticate(func):
    def wrapper(*args, **kwargs):
        api_key = request.args.get('key')
        if validate_key(api_key):
            return func(*args, **kwargs)
        else:
            return jsonify({'error': '身份验证失败。'}), 401
    return wrapper

def validate_key(api_key):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        query = "SELECT * FROM keys_table WHERE key_value = %s"
        cursor.execute(query, (api_key,))
        result = cursor.fetchone()
        if result:
            is_active = result[2]
            activation_date = result[3]
            expiration_days = result[4]
            if is_active == 0:
                update_query = "UPDATE keys_table SET is_active = 1, activation_date = NOW() WHERE key_value = %s"
                cursor.execute(update_query, (api_key,))
                conn.commit()
                activation_date = datetime.datetime.now()
            current_date = datetime.datetime.now()
            expiration_date = activation_date + datetime.timedelta(days=expiration_days)
            remaining_days = (expiration_date - current_date).days
            update_expiration_query = "UPDATE keys_table SET expiration_date = %s WHERE key_value = %s"
            cursor.execute(update_expiration_query, (remaining_days, api_key))
            conn.commit()
            if remaining_days >= 0:
                return True
            else:
                return False
        else:
            return False
    except:
        return False
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/dns_query', methods=['GET'])
@authenticate
def dns_query():
    try:
        domain = request.args.get('domain')
        if not domain:
            return jsonify({'error': '缺少域名参数。'}), 400
        ip_addresses = resolve_dns(domain)
        if ip_addresses:
            api_key = request.args.get('key')
            expiration_date = get_expiration_date(api_key)
            if expiration_date is not None:
                return jsonify({'domain': domain, 'ip_addresses': ip_addresses, 'KEY_date': expiration_date}), 200
            else:
                return jsonify({'error': '无法获取到有效期日期。'}), 500
        else:
            return jsonify({'error': '无法解析域名。'}), 500
    except:
        return jsonify({'error': '发生错误。'}), 500

def get_expiration_date(api_key):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        query = "SELECT expiration_date FROM keys_table WHERE key_value = %s"
        cursor.execute(query, (api_key,))
        result = cursor.fetchone()
        if result:
            expiration_date = result[0]
            return expiration_date
        else:
            return None
    except:
        return None
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


if __name__ == '__main__':
    app.run()
