#!/usr/bin/env python3
import http.server
import socketserver
import os
import sys

# เปลี่ยน directory ไปยังโฟลเดอร์ hotspot
os.chdir('/Users/mansuangpawong/Code/hotspot')

PORT = 8000

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # เพิ่ม headers เพื่อป้องกัน caching
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

    def do_GET(self):
        # ถ้าเข้าหน้า root ให้ redirect ไป login.html
        if self.path == '/':
            self.send_response(302)
            self.send_header('Location', '/login.html')
            self.end_headers()
            return
        
        # ถ้าเป็นไฟล์ที่ไม่มีอยู่ ให้แสดง login.html
        if not os.path.exists(self.path[1:]):
            self.path = '/login.html'
        
        return super().do_GET()

if __name__ == "__main__":
    try:
        with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
            print(f"🚀 Server กำลังรันที่ http://localhost:{PORT}")
            print(f"📱 เปิดเบราว์เซอร์ไปที่ http://localhost:{PORT}")
            print("🛑 กด Ctrl+C เพื่อหยุด server")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Server หยุดทำงานแล้ว")
        sys.exit(0)
    except OSError as e:
        if e.errno == 48:  # Address already in use
            print(f"❌ Port {PORT} ถูกใช้งานอยู่แล้ว")
            print(f"💡 ลองใช้ port อื่น: python3 server.py {PORT + 1}")
        else:
            print(f"❌ เกิดข้อผิดพลาด: {e}")
        sys.exit(1)
