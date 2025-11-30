#!/bin/bash

# Get local IP address
IP=$(ifconfig | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}' | head -1)

echo "=========================================="
echo "TYC Islamic Finance Advisor"
echo "=========================================="
echo ""
echo "Your web application is running!"
echo ""
echo "Local access:"
echo "  http://localhost:5000"
echo ""
echo "Share this link with friends on the same WiFi:"
echo "  http://$IP:5000"
echo ""
echo "=========================================="
echo ""
echo "To stop the server, press Ctrl+C in the terminal where app.py is running"
echo ""

