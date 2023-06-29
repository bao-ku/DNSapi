from flask import Flask, request, jsonify
import dns.resolver

app = Flask(__name__)

@app.route('/dns_query', methods=['GET'])
def dns_query():
    domain = request.args.get('domain')

    if not domain:
        return jsonify({'error': 'Domain parameter is missing.'}), 400

    resolver = dns.resolver.Resolver()
    resolver.nameservers = ['119.29.29.29', '114.114.114.114']  # 设置外部 DNS 服务器

    try:
        answers = resolver.query(domain, 'A')
        ip_addresses = [str(rdata) for rdata in answers]
        return jsonify({'domain': domain, 'ip_addresses': ip_addresses}), 200
    except dns.resolver.NXDOMAIN:
        return jsonify({'error': 'Domain does not exist.'}), 404
    except dns.resolver.NoAnswer:
        return jsonify({'error': 'No A records found for the domain.'}), 404
    except dns.resolver.Timeout:
        return jsonify({'error': 'DNS query timed out.'}), 500
    except dns.exception.DNSException:
        return jsonify({'error': 'DNS query failed.'}), 500

if __name__ == '__main__':
    app.run()
