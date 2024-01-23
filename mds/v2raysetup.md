---
title: نحوه راه اندازی تحریم شکن با پروکسی
date: 2023-10-31 13:18
tldr: وی تو ری با انجین ایکس، یه سرور ایران و یه سرور خارج هم نیاز دارید، وایر پروکسی هم استفاده میکنیم تا بعضی از سایتای حساس به آیپی مثل اسپاتیفای رو بفرستیم برا وارپ
draft: false
---
شما یه سرور خارج نیاز دارید از هرجا خواستید میتونید بگیرید من از [رک نرد](https://www.racknerd.com/) گرفتم چون تو آفر خیلی ارزون بود.  
برای سرور داخل کشور هم میتونید از هر جا که خواستید بگیرید البته مواظب باشید پورت سرور یه گیگ باشه.  

اول از همه رو سرور لینوکس خارج از کشورتون [v2ray](https://github.com/v2fly/v2ray-core) نصب کنید، البته میتونید از همینایی که با اسکریپت نصب میشه هم استفاده کنید ولی من چون بهشون آشنا نیستم.   

بعد از اینکه از ریلیز پیج دانلود کردید و محتویات توش رو هم اکسترکت کردید باید اول  v2ray.service تو پوشه سرویس رو کپی کنید تو مسیر زیر.

```
/etc/systemd/system   
```
 
طبق خود همون v2ray.service باینری v2ray و config.json رو به ترتیب به مسیرای زیر منتقل کنید  

```
/usr/bin   
/usr/local/etc/v2ray  
```

وی تو ری تو کانفیگش inbound و outbound داره اینجا من تو inbound از وی مس با ترنسپورت وبسوکت استفاده میکنم که رو پورت ۱۰۸۶ لیسن میکنه دلیل استفاده از وب سوکت اینه که اون اوایل فیلترینگ داخل کشور سنگین بود و آیپی هارو پشت سرهم بلاک میکردن واسه همین از ریورس پروکسی کلاود فلر استفاده میکردیم و وب سوکت تنها ترنسپورتی بود که وی تو ری داشت که کلاود فلرم ازش پشتیبانی میکرد. پورت رو هم میتونید به ۸۰ تغییر بدید اگه نمیخواید از nginx استفاده کنید.

```
$ cat /usr/local/etc/config.json 

{
    "stats": {},
    "api": {
        "tag": "api",
        "services": [
            "StatsService"
        ]
    },
    "policy": {
        "levels": {
            "0": {
                "statsUserUplink": true,
                "statsUserDownlink": true
            }
        },
        "system": {
            "statsInboundUplink": true,
            "statsInboundDownlink": true
        }
    },
    "inbounds": [
        {
            "port": 1086,
            "protocol": "vmess",
            "settings": {
                "clients": [
                    {
                        "email": "uuid1",
                        "id": "",
                        "level": 0
                    },
                    {
                        "email": "uuidfabe9f",
                        "id": "",
                        "level": 0
                    },
                    {
                        "email": "uuid1dc11",
                        "id": "",
                        "level": 0
                    }
                ]
            },
            "streamSettings": {
                "network": "ws",
                "wsSettings": {
                    "path": "/ws/"
                },
                "security": "none"
            }
        },
        {
            "listen": "127.0.0.1",
            "port": 8080,
            "protocol": "dokodemo-door",
            "settings": {
                "address": "127.0.0.1"
            },
            "tag": "api"
        }
    ],
    "outbounds": [
        {
            "tag": "direct",
            "protocol": "freedom",
            "settings": {}
        },
        {
            "tag": "warp",
            "protocol": "socks",
            "settings": {
                "servers": [
                    {
                        "address": "127.0.0.1",
                        "port": 4040
                    }
                ]
            }
        }
    ],
    "routing": {
        "rules": [
            {
                "inboundTag": [
                    "api"
                ],
                "outboundTag": "api",
                "type": "field"
            },
            {
                "domain": [
                    "bard.google.com",
                    "open.spotify.com",
                    "rateyourmusic.com"
                ],
                "outboundTag": "warp",
                "type": "field"
            }
        ],
        "domainStrategy": "AsIs"
    }
}

```

تو کانفیگ بالا باید بخش clients رو خودتون ادیت کنید فک نکنم نیاز به توضیح باشه یه uuid جنریت کنید میتونید گوگل کنید ببینید چجوری اینکارو میکنن.   

تو کانفیگ بالا ما دو تا outbound داریم یکیش همون freedom و یکی دیگه پروکسی ساکس با تگ warp، تو routing rules هم مشخصه که مثلا اسپاتیفای و rym رو فرستادیم رو تگ warp.   

وایر پروکسی ای که من استفاده کردم رو پورت ۴۰۴۰ لیسن میکنه میتونید عوضش کنید به هر چی که میخواید.   
به کانفیگ وایرگارد warp نیاز دارید، برای پیدا کردن warp plus هم میتونید سرچ کنید یه ربات تلگرامه ولی از اونجا که قانونی نیست از [wgcf](https://github.com/ViRb3/wgcf) برای جنریت کردن کانفیگ وایرگارد وارپ استفاده کنید.  
بعدش باید [wireproxy](https://github.com/pufferffish/wireproxy) رو دانلود کنید رو سرورتون این کانفیگ وایرگارد رو میگیره جای اینکه یه اینترفیس باشه  فقط یه پروکسی ساکس میده. فقط یه بدی ای که داره اینه که udp ساپورت نمیکنه.

```
WGConfig =/path/to/wg/config/config.conf

[Socks5]
BindAddress = 127.0.0.1:4040

```


برای ریورس پروکسی هم باید nginx رو نصب کنید اگه از اوبونتو یا دبیان استفاده میکنید میتونید با همون apt نصبش کنید بعد از نصب کانفیگش رو جوری ادیت کنید تا هر ریکویستی که رو پورت ۸۰ میاد رو بفرسته به وی تو ری، طبق کانفیگ وی توری ما که وب سوکت بود رو پورت 1086 و مسیر /ws  
بود کافیگ باید اینجوری باشه.

```
$ cat /etc/nginx/nginx.conf

user www-data;
worker_processes auto;
pid /run/nginx.pid;
include /etc/nginx/modules-enabled/*.conf;

events {
    worker_connections 768;
    # multi_accept on;
}

http {

    ##
    # Basic Settings
    ##

    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;
    # server_tokens off;

    # server_names_hash_bucket_size 64;
    # server_name_in_redirect off;

    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    # Helper variable for proxying websockets.
	 map $http_upgrade $connection_upgrade {
		default upgrade;
		'' close;
	}

    ##
    # Logging Settings
    ##
    access_log /var/log/nginx/access.log;
    error_log /var/log/nginx/error.log;

    ##
    # Gzip Settings
    ##

    gzip on;

    server {
        listen 80 default_server;
        listen [::]:80 default_server;


        root /var/www/html;

        # Add index.php to the list if you are using PHP
        index index.html index.htm index.nginx-debian.html;

        server_name _;

        location / {
            # First attempt to serve request as file, then
            # as directory, then fall back to displaying a 404.
            try_files $uri $uri/ =404;
		}

        location /ws {
            proxy_pass http://localhost:1086;
            proxy_http_version 1.1;
            proxy_pass_request_headers      on;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection $connection_upgrade;
		} 
    }


}

```

اگه بخواید تو این مرحله میتونید ssl هم اضافه کنید باید .acme.sh هم نصب کنید باهاش سرتیفیکیت جنریت کنید که از نظر من کار اضافیه.    
اگه دامنتون رو بردید کلاود فلر و ریورس پروکسی رو فعال کردید میتونید بدون تنظیمات اضافی رو پورت 443 اس اس ال بگیرید.   


الان سرورتون آمادس میتونید ازش استفاده کنید ولی از اونجا که اینترنت همراه توسط معاندین مورد سو استفاده واقع میگردد و از لبه تیز چاقوی تحریم شکن برای کارای خاک برسری و متزلزل ساختن پایه های نظام مقدس جمهوری اسلامی استفاده میکنند (aka فیلتر شکن ) دسترسی به سرورتون رو اپراتورا با اختلال مواجه میشه و به یه سرور داخل هم نیاز دارید.     

بعد از اینکه سرور داخل تهیه کردید باید از سرور خارج بهش وصل بشید.   
راه های زیادی برای تونل کردن سرور وجود داره ولی طبق تجربه من وقتی اینترنتا ملی میشه دسترسی ها فقط از داخل قطع میشه ولی یکی از آلمان یا آمریکا میتونه به داخل کشور ریکویست بده 
واسه همین من از ssh tunnel استفاده میکنم به این صورت که شما با ssh پورت داخلی v2ray رو رو سرور ایرانتون اکسپوز میکنید و بعد با انجین ایکس رو سرور ایرانتون همه ترافیک رو میفرستید به سمت تونل ssh 
```
	client ---> nginx ---> ssh tunnel ---> v2ray 
```

من از autossh استفاده میکنم و جای یه تونل 10 تا تونل درست میکنم چون ظرفیت هر تونل خیلی کمه و پهنای باند کل سرور رو پوشش نمیده و بعد با یه کرون جاب هر سی دقیقه این تونلارو میکشم و یکی دوباره از اول درست میکنم.  
قبلشم حتما کلید اس اس اچ جنریت کنید و ssh-copy-id رو انجام بدید تا دیگه رمز نخواد.

```
$ cat tunnel.sh

pkill autossh &&\
 autossh -M 0 -o "ServerAliveInterval 30" -o "ServerAliveCountMax 3" -N -f -R 2000:localhost:1086 user@iranserverip &&\
 autossh -M 0 -o "ServerAliveInterval 30" -o "ServerAliveCountMax 3" -N -f -R 2001:localhost:1086 user@iranserverip  &&\
 autossh -M 0 -o "ServerAliveInterval 30" -o "ServerAliveCountMax 3" -N -f -R 2002:localhost:1086 user@iranserverip  &&\
 autossh -M 0 -o "ServerAliveInterval 30" -o "ServerAliveCountMax 3" -N -f -R 2003:localhost:1086 user@iranserverip  &&\
 autossh -M 0 -o "ServerAliveInterval 30" -o "ServerAliveCountMax 3" -N -f -R 2004:localhost:1086 user@iranserverip  &&\
 autossh -M 0 -o "ServerAliveInterval 30" -o "ServerAliveCountMax 3" -N -f -R 2005:localhost:1086 user@iranserverip  &&\
 autossh -M 0 -o "ServerAliveInterval 30" -o "ServerAliveCountMax 3" -N -f -R 2006:localhost:1086 user@iranserverip  &&\
 autossh -M 0 -o "ServerAliveInterval 30" -o "ServerAliveCountMax 3" -N -f -R 2007:localhost:1086 user@iranserverip  &&\
 autossh -M 0 -o "ServerAliveInterval 30" -o "ServerAliveCountMax 3" -N -f -R 2008:localhost:1086 user@iranserverip  &&\
 autossh -M 0 -o "ServerAliveInterval 30" -o "ServerAliveCountMax 3" -N -f -R 2009:localhost:1086 user@iranserverip  &&\
 autossh -M 0 -o "ServerAliveInterval 30" -o "ServerAliveCountMax 3" -N -f -R 2010:localhost:1086 user@iranserverip 
```



رو سرور ایرانتون هم از کانفیگ  nginx زیر استفاده کنید اینجا هم میتونید ssl تنظیم کنید ولی ضروری نیست.   

بلاک upstream درواقع آدرس همون تونلاس که خود انجین ایکس اوتوماتیک بینشون لود بالانس میکنه. 


```
$ cat /etc/nginx/nginx.conf

user www-data;
worker_processes auto;
pid /run/nginx.pid;
include /etc/nginx/modules-enabled/*.conf;

events
{
	worker_connections 768;
	# multi_accept on;
}

http
{

	##
	# Basic Settings
	##

	sendfile on;
	tcp_nopush on;
	tcp_nodelay on;
	keepalive_timeout 65;
	types_hash_max_size 2048;
	# server_tokens off;

	# server_names_hash_bucket_size 64;
	# server_name_in_redirect off;

	include /etc/nginx/mime.types;
	default_type application/octet-stream;

	# Helper variable for proxying websockets.
	map $http_upgrade $connection_upgrade
	{
		default upgrade;
		'' close;
	}

	##
	# Logging Settings
	##
	access_log /var/log/nginx/access.log;
	error_log /var/log/nginx/error.log;

	##
	# Gzip Settings
	##

	gzip on;


	upstream bck
	{
		server localhost:2000;
		server localhost:2001;
		server localhost:2002;
		server localhost:2003;
		server localhost:2004;
		server localhost:2005;
		server localhost:2006;
		server localhost:2007;
		server localhost:2008;
		server localhost:2009;
		server localhost:2010;
	}
	server
	{
		listen 80 default_server;
		listen [::]:80 default_server;


		root /var/www/html;

		# Add index.php to the list if you are using PHP
		index index.html index.htm index.nginx-debian.html;

		server_name _;


		location /ws
		{
			proxy_pass http://bck;
			proxy_http_version 1.1;
			proxy_pass_request_headers on;
			proxy_set_header Upgrade $http_upgrade;
			proxy_set_header Connection $connection_upgrade;
		}

		# location /api {
		#     proxy_pass http://localhost:4050;
		# }
	}

}
```


موفق و پیروز باشید.