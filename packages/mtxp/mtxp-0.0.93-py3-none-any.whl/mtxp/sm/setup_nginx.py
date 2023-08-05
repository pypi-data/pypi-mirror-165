from subprocess import CompletedProcess
import sys
from pathlib import Path
from mtlibs import process_helper
from dotenv import load_dotenv, find_dotenv
from mtlibs.docker_helper import isInContainer
# from .consts import SM_API_ROOT,HTML_ROOT_DIR
# STATIC_ROOT="/var/www/html"
def setup_nginx(htmlRoot:str, smApiPrefix:str):
    nginx_conf = """user nginx;
worker_processes auto;

error_log /var/log/nginx/error.log notice;
pid /var/run/nginx.pid;

events {
  worker_connections 1024;
}

http {
  upstream smirror {
    server 127.0.0.1:3456 weight=100 max_fails=12 fail_timeout=60s;
  }
  upstream default_backend {
    server 127.0.0.1:3000 weight=150 max_fails=12 fail_timeout=60s;
  }
  upstream mtx {
    server 127.0.0.1:8000 weight=200 max_fails=12 fail_timeout=60s;
  }
  include /etc/nginx/mime.types;
  default_type application/octet-stream;

  log_format main '$remote_addr - $remote_user [$time_local] "$request" '
  '$status $body_bytes_sent "$http_referer" '
  '"$http_user_agent" "$http_x_forwarded_for"';

  access_log /var/log/nginx/access.log main;

  sendfile on;
  #tcp_nopush     on;
  keepalive_timeout 65;
  gzip on;
  types_hash_max_size 2048;
  include /etc/nginx/conf.d/*.conf;
}
"""
    # print("nginx 配置信息", nginx_conf)
    nginx_default_site = """
server {
  listen 80;
  server_name 127.0.0.1;
  #access_log  /var/log/nginx/host.access.log  main;
  # location / {
  #   root /app/static;
  #   index index.html index.htm;
  # }
  index index.php;
  # access_log /etc/nginx/conf.d/log/access.log;
  # error_log /etc/nginx/conf.d/log/error.log;
  # location / {
  #   add_header X-Powered-By 'PHP';
  #   root /var/www/html;
  #   index index.php index.html index.htm;
  #   # try_files @sm $uri $uri/;
  #   # try_files $uri /index.php?$args $uri/index.html $uri.html @default_backend;
  #   try_files $uri $uri/index.html $uri.html @default_backend;

  #   # # proxy_pass http://default_backend;
  #   # # autoindex on;
  #   # proxy_http_version 1.1;
  #   # index index.html index.htm;
  #   # proxy_set_header Upgrade $http_upgrade;
  #   # proxy_set_header Connection "Upgrade";
  #   # proxy_set_header Host $host;
  #   # proxy_set_header Host $host;
  #   # proxy_set_header X-Real-IP $remote_addr;
  #   # proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
  # }
  root @@STATIC_DIR@@;
  location / {
    autoindex on;
    index index.php index.html index.htm;
    try_files $uri $uri/ /index.php?$args @mtx default_backend;
    # try_files $uri $uri/ /index.php?$args;
    # proxy_pass http://mtx;
  }

  location ^~ /smirror {
    add_header X-Powered-By 'PHP';
    # root /app/static;
    # try_files @nextfront $uri $uri/;
    proxy_pass http://smirror; 
    # autoindex on;
    # index index.html index.htm;
  }

  location ^~ /mtxcms/ {
    add_header X-Powered-By 'PHP';
    # root /app/static;
    # try_files @nextfront $uri $uri/;
    proxy_pass http://default_backend;
    # autoindex on;
    # index index.html index.htm;
  }
  
  location ^~ @@SM_API@@/ {
    add_header X-Powered-By 'PHP';
    # root /app/static;
    # try_files @nextfront $uri $uri/;
    proxy_pass http://default_backend;
    # autoindex on;
    # index index.html index.htm;
  }

  location ^~ /admin/ {
    add_header X-Powered-By 'PHP';
    # try_files @nextfront $uri $uri/;
    proxy_pass http://mtx;
    # autoindex on;
    # index index.html index.htm;
  }

  error_page 500 502 503 504 /50x.html;
  location = /50x.html {
    root /usr/share/nginx/html;
  }

  location /baidu {
    try_files /baidu.html
    $uri $uri/index.html $uri.html
    @fallback1;
  }
  #跳转到百度页面
  location @fallback {
    # rewrite ^/(.*)$ http://www.baidu.com;
    proxy_pass http://smirror;
  }

  location @default_backend {
    proxy_pass http://default_backend;
  }
  location @mtx {
    proxy_pass http://mtx;
  }


  # deny access to .htaccess files, if Apache's document root
  # concurs with nginx's one
  location ~ /\.ht {
    deny all;
  }
  # proxy the PHP scripts to Apache listening on 127.0.0.1:80
  #
  #location ~ \.php$ {
  #    proxy_pass   http://127.0.0.1;
  #}

  # pass the PHP scripts to FastCGI server listening on 127.0.0.1:9000
  #
  #location ~ \.php$ {
  #    root           html;
  #    fastcgi_pass   127.0.0.1:9000;
  #    fastcgi_index  index.php;
  #    fastcgi_param  SCRIPT_FILENAME  /scripts$fastcgi_script_name;
  #    include        fastcgi_params;
  #}
  location ~ \.php$ {
    root /var/www/html;
    # try_files $uri =404;
    fastcgi_pass 127.0.0.1:9000;
    # fastcgi_pass /run/php/php7.4-fpm.sock;
    # 设置nginx的默认首页文件(上面已经设置过了，可以删除)
    fastcgi_index index.php;
    fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
    include fastcgi_params;
  }
  location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
    expires max;
    log_not_found off;
  }
  # #ignored: “-” thing used or unknown variable in regex/rew
  # rewrite ^/([_0-9a-zA-Z-]+/)?wp-admin$ /$1wp-admin/ permanent;

  # if (-f $request_filename) {
  #   set $rule_2 1;
  # }
  # if (-d $request_filename) {
  #   set $rule_2 1;
  # }
  # if ($rule_2 = "1") {
  #   #ignored: “-” thing used or unknown variable in regex/rew
  # }
  # rewrite ^/([_0-9a-zA-Z-]+/)?(wp-(content|admin|includes).*) /$2 last;
  # rewrite ^/([_0-9a-zA-Z-]+/)?(.*.php)$ /$2 last;
  # rewrite /. /index.php last;

  # deny access to .htaccess files, if Apache's document root
  # concurs with nginx's one
  #
  location ~ /\.ht {
    deny all;
  }
  location ~* \.(xml|yaml|cmd|cfg|yml|tmp|sh|bat|txt|ts|tsx|jsx|lock)$ {
    # 禁用某些后缀名文件访问。
    deny all;
  }
  location ~ (README\.md|ockerfile.*|package.*\.json|.*config.js|.*prisma.*)$ {
    deny all;
  }
  location ^~ /(configs|build|log|logs)/ {
    #禁用某些目录访问
    deny all;
  }
  location ^~ /. {
    # 禁止以.开始的文件访问
    # 匹配任何以 /. 开头的地址，匹配符合以后，停止往下搜索正则，采用这一条。
    deny all;
  }

  location = /some2.html {
    rewrite ^/some2.html$ /test/2.html break;
  }
}


"""    
    with open("/etc/nginx/nginx.conf", "w") as f:
        f.write(nginx_conf)


    if not Path(htmlRoot).exists():
      Path(htmlRoot).mkdir(parents=True,mode=0o700,exist_ok=True)
      
    nginx_default_site = nginx_default_site.replace("@@STATIC_DIR@@",htmlRoot)
    nginx_default_site = nginx_default_site.replace("@@SM_API@@",smApiPrefix)
    

    with open("/etc/nginx/conf.d/default.conf", "w") as f:
        f.write(nginx_default_site)
        
    cp: CompletedProcess = process_helper.exec("nginx -t")
    if cp.returncode != 0:
        print("nginx 配置信息不正确")
        print(cp.stderr + cp.stdout)
        return
    nginx_cp= process_helper.exec("nginx -s reload", check=False)
    nginx_cp= process_helper.exec("nginx", check=False)
    if nginx_cp.returncode == 0:
        print("nginx 成功启动")