# ─── Сниппет для долгоживущих прокси (XHTTP / WebSocket) ─
(xhttp-ws-proxy) {
    reverse_proxy {args[0]} {
        header_up Host {host}
        header_up X-Real-IP {remote_host}
        header_up X-Forwarded-For {http.request.header.X-Forwarded-For}, {remote_host}
        header_up X-Forwarded-Proto {scheme}
        flush_interval -1
        transport http {
            read_timeout 86400s
            write_timeout 86400s
        }
    }
}

# ─── HTTP → HTTPS ────────────────────────────────────────
http://servers-nl-coffee-3.tech {
    redir https://{host}{uri} 301
}

# ═══════════════════════════════════════════════════════════
# Единый порт 443: gRPC, XHTTP, WebSocket, редирект остального
# ═══════════════════════════════════════════════════════════
servers-nl-coffee-3.tech:443 {

	tls /etc/caddy/certs/servers-nl-coffee-3.tech/fullchain.pem \
		/etc/caddy/certs/servers-nl-coffee-3.tech/privkey.pem

    # 1) gRPC – маскировка под браузер
    handle /grpc.health.v1.api {
        @grpc {
            header Content-Type application/grpc
        }
        reverse_proxy @grpc 127.0.0.1:10001 {
            transport http {
                versions h2c
            }
            header_up Host {host}
            header_up X-Real-IP {remote_host}
            header_up User-Agent "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
            header_up Accept "application/grpc-web, application/grpc, */*"
            header_up Accept-Language "en-US,en;q=0.5"
            header_up Cache-Control "no-cache"
            header_up Pragma "no-cache"
            header_up Grpc-Timeout "5S"
        }
        respond 415 "grpc-only"
    }

    # 2) XHTTP
    handle /xhttp.health.v1.api {
        import xhttp-ws-proxy 127.0.0.1:10002
    }

    # 3) WebSocket
    handle /ws.health.v1.api {
        import xhttp-ws-proxy 127.0.0.1:10003
    }

    # 4) Редирект всего остального
    redir https://my.hostes.io{uri}
}
