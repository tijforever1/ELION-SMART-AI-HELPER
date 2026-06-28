import http.server, socketserver, hashlib

_exp_upper_hash = '3763FCF7D04E64492C2A2832DD17E32A960B44562C5332D1714BA37DB5EB8945'

PORT = 8000
Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving on port {PORT}")
    httpd.serve_forever()




