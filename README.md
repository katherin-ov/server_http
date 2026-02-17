
Установка зависимостей:
```
poetry install
```

Запуск проекта:
```
python src/server/httpd.py -w 8
```

Тесты:
```commandline
pytest tests/httptest.py 
```

Результаты нагрузочного тестирования:
```text
❯ docker build -t http-server-test .  
❯ docker run http-server-test  
This is ApacheBench, Version 2.3 <$Revision: 1903618 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking 127.0.0.1 (be patient)
Completed 5000 requests
Completed 10000 requests
Completed 15000 requests
Completed 20000 requests
Completed 25000 requests
Completed 30000 requests
Completed 35000 requests
Completed 40000 requests
Completed 45000 requests
Completed 50000 requests
Finished 50000 requests


Server Software:        HTTPServer
Server Hostname:        127.0.0.1
Server Port:            8080

Document Path:          /httptest/wikipedia_russia.html
Document Length:        954824 bytes

Concurrency Level:      100
Time taken for tests:   95.226 seconds
Complete requests:      50000
Failed requests:        0
Total transferred:      47748400000 bytes
HTML transferred:       47741200000 bytes
Requests per second:    525.07 [#/sec] (mean)
Time per request:       190.452 [ms] (mean)
Time per request:       1.905 [ms] (mean, across all concurrent requests)
Transfer rate:          489670.46 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0  145 1299.4      0   19564
Processing:     0   30  72.6     25    2107
Waiting:        0   29  71.5     24    2105
Total:          1  176 1300.3     26   19588

Percentage of the requests served within a certain time (ms)
  50%     26
  66%     30
  75%     38
  80%     41
  90%     50
  95%     73
  98%    328
  99%   6709
 100%  19588 (longest request)
```
