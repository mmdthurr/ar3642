---
title: پیام رسان سلف هاستبل با قابلیت تماس تصویری
date: 2023-10-31 18:53
tldr: یه سرور اکس ام پی پی با کوترن
draft: false
---

 چرا باید سلف هاست کنید؟ در حال حاضر همه پیام رسانای خارجی فیلتره هیچکدومشون کار نمیکنه، پیام رسانای داخلی هم کیفیت مناسبی ندارن.  
 دو تا گزینه هست ماتریکس و xmpp   
 ماتریکس ایمپلمنتیشن اصلیش به پایتونه که خیلی کنده و سنگینم هست.  
 تو خود سایت ماتریکس [conduit](https://conduit.rs/) پیدا کردم ولی مشکل اصلی سرور نبود کلاینت اندرویدش element به طرز غیر قابل تحملی مضخرف بود.   
 
### نحوه راه اندازی xmpp 

 باید [prosody](https://prosody.im/) رو نصب کنید تو سایت خودش گفته چجور نصب کنید. اگه سروتون دبیانه اول همونطور که گفته apt رو آپدیت کنید.  
 بعد اینکه نصب کردید میتونید با prosodyctl بهش یوزر اضافه کنید یا حذف کنید.     
 برای استفاده از xmpp نیاز به سرتیفیکیت دارید من پیشنهاد میکنم از [ .acme.sh](https://github.com/acmesh-official/acme.sh) استفاده کنید.   
 دو تا دی انس رکورد xmpp.domain.com و turn.domain.com درست کنید  
 اگه نمیخواید تماس تصویری داشته باشید turn.domain.com رو اضافه نکنید      

```
.acme.sh/acme.sh --issue -d 'xmpp.domain.com' --server letsencrypt --standalone 
```



حالا باید سرتیفیکتاتون رو کپی کنید یه جا دیگه و مالکیتش رو با chown بدید به prosody 

```
chown prosody:prosody /path/to/fullchain.cer &&\
chown prosody:prosody /path/to/xmpp.domain.com.key
```

بعد از اینکه اس اس ال گرفتید باید کانفیگ prosody رو ادیت کنید و ویرچوال هاست رو اضافه کنید.    

```
$ vi /etc/prosody/prosody.cfg.lua
```

```
VirtualHost "xmpp.domain.com"
  ssl = {
    certificate = "/var/lib/prosody/xmpp.domain.com_ecc/fullchain.cer";
    key = "/var/lib/prosody/xmpp.domain.com_ecc/xmpp.domain.com.key";
  } 
```

حالا اگه میخواید تماس تصویری یا  صوتی هم داشته باشید باید یه سرور turn داشته باشید   
کوترن رو نصب کنید کانفیگشم ادیت کنید و اینو توش بنویسید سعی کنید secret رو یه چیز سخت انتخاب کنید که قابل حدس زدن نباشه.(برا اینم میتونید ssl اضافه کنید گوگل کنید البته به نظر من واجب نیست در کل اضافه هم نکنید تاثیری رو امنیت تماس تصویریتون نداره)

```
vi /etc/turnserver.conf
```

```
use-auth-secret
static-auth-secret=somestrongAuthKeykdi3kdkd
realm=turn.domain.com
```

بعدش که سرویس coturn رو ری استارت کردید(یادتون نره enable اش کنید )، کانفیگ prosody رو هم ادیت کنید که از سرور coturn استفاده کنه.   
باید turn_external رو تو لیست modules_enabled اضافه کنید (فک کنم بتونید فقط کامنتش رو بردارید) این دو خطم به کانفیگ بر اساس همون کانفیگ coturn اضافه کنید.  

```
turn_external_host = "turn.domain.com"
turn_external_secret = "somestrongAuthKeykdi3kdkd"
```

برای اضافه کردن یوزرم مثل زیر از adduser استفاده کنید بعدشم باید پسورد اینا هم اضافه کنید.    
```
prosodyctl adduser user@xmpp.domain.com
```


 خیلی کلاینت وجود داره رو اندروید میتونید از [Conversations](https://f-droid.org/en/packages/eu.siacs.conversations/) استفاده کنید خودمم از همین استفاده میکنم.    
اگه خواستید میتونید لیست ماژولارم نگاه کنید تا یخورده مثل تلگرامش کنید مثلا یه سرور جدا برای آپلود فایل یا مثلا هیستوری رو نگه داره یا یه سرور برای گروه زدن و از اینجور چیزا من فقط میخواستم با مامانم تماس تصویری بگیرم.   