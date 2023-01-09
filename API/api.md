# API

## Get list of containers

`GET /containers`

Response

```
HTTP/1.1 405 METHOD NOT ALLOWED
Allow: GET, HEAD, OPTIONS
Connection: close
Content-Length: 153
Content-Type: text/html; charset=utf-8
Date: Sun, 08 Jan 2023 20:49:21 GMT
Server: Werkzeug/2.2.2 Python/3.10.8
        },
        {
            "id": "c6110b8c1922ce94046318581ca67f754f02ad58cd16a084c8fc826b50d7c843"
        },
        {
            "id": "9b0ca4b2513daba9ae59a4ea36c9293628dbbe236eec11cbe5d8bfa582da5f73"
        },
        {
            "id": "d92ca7846eb0b61e67870dc9235d04548cd2d3d95903f6cda20667e8cd4ee4d2"
        }
    ]
}
```

## Get container info

`GET /container/<container_id>`

Response
using `httpie`

```
http 127.0.0.1:5000/container/9b
```
```
Connection: close
Content-Length: 247
Content-Type: application/json
Date: Sun, 08 Jan 2023 20:50:29 GMT
Server: Werkzeug/2.2.2 Python/3.10.8

{
    "id": "9b0ca4b2513daba9ae59a4ea36c9293628dbbe236eec11cbe5d8bfa582da5f73",
    "name": "magical_hofstadter",
    "port": {
        "8128/tcp": [
            {
                "HostIp": "0.0.0.0",
                "HostPort": "8001"
            }
        ]
    },
    "status": "running"
}
```

## POST config

`POST /config`

Using `httpie`

```
http --form 127.0.0.1:5000/config file@vpnext-UDP4-1197-config.ovpn
```

Response

```
HTTP/1.1 201 CREATED
Connection: close
Content-Length: 34
Content-Type: application/json
Date: Sun, 08 Jan 2023 20:51:54 GMT
Server: Werkzeug/2.2.2 Python/3.10.8

{
    "message": "Config created"
}
```


## GET configs

`GET /configs`

```
HTTP/1.1 200 OK
Connection: close
Content-Length: 167
Content-Type: application/json
Date: Sun, 08 Jan 2023 20:52:19 GMT
Server: Werkzeug/2.2.2 Python/3.10.8

{
    "configs": [
        "vpnext-UDP4-1197-config.ovpn",
        "vpngate_public-vpn-192.opengw.net_udp_1195.ovpn",
        "vpngate_public-vpn-224.opengw.net_tcp_443.ovpn"
    ]
}
```

## RUN container

`POST /container/`

using `httpie`

```
http POST 127.0.0.1:5000/container config=vpnext-UDP4-1197-config.ovpn
```

Response

```
HTTP/1.1 201 CREATED
Connection: close
Content-Length: 37
Content-Type: application/json
Date: Sun, 08 Jan 2023 20:42:38 GMT
Server: Werkzeug/2.2.2 Python/3.10.8

{
    "message": "Container created"
}
```
