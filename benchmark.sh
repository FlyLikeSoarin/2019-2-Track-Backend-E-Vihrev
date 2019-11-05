echo ""

echo "Testing static file output:"
wrk -t2 -c64 -d10s http://127.0.0.1:80/
echo ""

echo "Testing proxy service:"
wrk -t2 -c64 -d10s http://127.0.0.1:81/
echo ""
