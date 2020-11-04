# Starting influx, creating an admin user for influx
# Iterating over data directory and populating database with all the data in the directory
service influxdb start && \
sleep 5 && \
curl -XPOST "http://localhost:8086/query" --data-urlencode "q=CREATE USER admin WITH PASSWORD 'teamfox' WITH ALL PRIVILEGES" && \
curl -XPOST "http://localhost:8086/query" -u admin:teamfox --data-urlencode "q=CREATE DATABASE iiwari_org" && \
curl -G http://localhost:8086/query -u admin:teamfox --data-urlencode "q=SHOW DATABASES" && \
for file in ./data/*; do
        python3 csv-to-influxdb.py --user admin --password teamfox --dbname iiwari_org -m SensorData -tf "%Y-%m-%d %H:%M:%S.%f+00:00" --input "$file" --tagcolumns node_id --fieldcolumns x,y,z,q -b 200000
done