echo ""

echo "Testing static file output:"
wrk -t2 -c2 -d1s http://127.0.0.1:80/
echo ""

echo "Testing proxy service:"
wrk -t2 -c2 -d10s http://127.0.0.1:81/
echo ""
