#!/usr/bin/env python3
"""
ConnectScript HTTP API Server
Serveur API pour le compilateur ConnectScript
Permet à la frontend IDE de compiler directement sans utiliser le simple parser JS
"""

import json
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import os

# Add compiler directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from compiler import compile_script


class ConnectScriptHandler(BaseHTTPRequestHandler):
    """Handler pour les requêtes HTTP"""
    
    def do_OPTIONS(self):
        """Gérer les requêtes CORS OPTIONS"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_POST(self):
        """Traiter les requêtes POST"""
        path = urlparse(self.path).path
        
        # Route: /api/compile
        if path == '/api/compile':
            self.handle_compile()
        else:
            self.send_error(404, "Route not found")
    
    def do_GET(self):
        """Traiter les requêtes GET"""
        path = urlparse(self.path).path
        
        # Route: /api/status
        if path == '/api/status':
            self.handle_status()
        # Route: /api/version
        elif path == '/api/version':
            self.handle_version()
        else:
            self.send_error(404, "Route not found")
    
    def handle_compile(self):
        """Handle POST /api/compile
        
        Request body (JSON):
        {
            "code": "page Home..."
        }
        
        Response (JSON):
        {
            "success": true,
            "code": "// generated javascript",
            "ast": { ... },
            "errors": [],
            "warnings": []
        }
        """
        try:
            # Lire le body
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            
            # Parser JSON
            request_data = json.loads(body.decode('utf-8'))
            code = request_data.get('code', '')
            
            # Compiler
            result = compile_script(code)
            
            # Répondre
            response = {
                'success': result['success'],
                'javascript': result['javascript'],
                'ast': result['ast'],
                'errors': result['errors'],
                'warnings': result['warnings']
            }
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
            
        except json.JSONDecodeError:
            self.send_error(400, "Invalid JSON")
        except Exception as e:
            self.send_error(500, f"Internal server error: {str(e)}")
    
    def handle_status(self):
        """Handle GET /api/status
        
        Retourne le statut du serveur
        """
        response = {
            'status': 'online',
            'service': 'ConnectScript Compiler API',
            'version': '1.0.0',
            'endpoints': {
                'POST /api/compile': 'Compiler du code ConnectScript',
                'GET /api/status': 'Statut serveur',
                'GET /api/version': 'Numéro de version'
            }
        }
        
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
    
    def handle_version(self):
        """Handle GET /api/version"""
        response = {
            'version': '1.0.0',
            'compiler_version': '1.0.0',
            'api_version': '1.0',
            'language': 'ConnectScript',
            'description': 'Professional Compiler for ConnectScript'
        }
        
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
    
    def log_message(self, format, *args):
        """Override pour personnaliser les logs"""
        path = urlparse(self.path).path
        method = self.command
        print(f'[{self.client_address[0]}] {method} {path}')


def run_server(port=5001):
    """Lance le serveur HTTP"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, ConnectScriptHandler)
    
    print(f"\n╔{'='*68}╗")
    print(f"║  🚀 ConnectScript Compiler API Server{'':29}║")
    print(f"╚{'='*68}╝\n")
    
    print(f"📡 Serveur démarré sur: http://localhost:{port}/")
    print(f"📍 Point de terminaison: POST http://localhost:{port}/api/compile")
    print(f"\n📊 Vous pouvez maintenant:")
    print(f"  1. Compiler du code via POST /api/compile")
    print(f"  2. Vérifier le statut via GET /api/status")
    print(f"  3. Voir la version via GET /api/version")
    print(f"\n💾 Exemple de requête POST:")
    print(f"""
curl -X POST http://localhost:{port}/api/compile \\
  -H "Content-Type: application/json" \\
  -d '{{"code":"page Home\\n-background\\n--color blue"}}'
""")
    print(f"\n⌨️  Appuyez sur Ctrl+C pour arrêter le serveur...\n")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n✋ Serveur arrêté.")
        httpd.server_close()


if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5001
    run_server(port)
