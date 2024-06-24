ESWIN邮箱配置

```config
[sendemail]
	smtpencryption = tls
	smtpserver = smtp.eswincomputing.com
	smtpuser = zhangdongdong@eswincomputing.com
	smtpserverport = 25
	from = zhangdongdong@eswincomputing.com
	smtppass = siyuan
	cc = zhangdongdong@eswincomputing.com
```

QQ 邮箱配置：

```.config
[sendemail]
	smtpencryption = tls
    smtpserver = smtp.qq.com
    smtpuser = dominic_riscx@qq.com
	smtpserverport = 587
    from = dominic_riscx@qq.com
	smtppass = siyuan
	cc = zhangdongdong@eswincomputing.com
	#to = opensbi@lists.infradead.org
```

```
git format-patch -o update_gitignore/  HEAD^

git format-patch --cover-letter -o update_gitignore/ --base=auto  update_gitignore@{u}..update_gitignore
git send-email --to=target@example.com update_gitignore/*.patch
git format-patch -v2 --cover-letter -o update_gitignore/   master..update_gitignore-v1
git commit --amend --author="<FirstName> <LastName> <xxx@xxx.com>" --no-edit
git format-patch -o ../patch/opensbi HEAD^

git send-email --to zhangdongdong@eswincomputing.com 
                 --in-reply-to="<foo.12345.author@example.com>" 
               update_gitignore/v2-*.patch 

git send-email --to=zhuwenjun@eswincomputing.com --cc=qinhaijun@eswincomputing.com,zhangleizheng@eswincomputing.com
git send-email --to=jinyanjiang@eswincomputing.com --cc=zhuwenjun@eswincomputing.com,zhengyu@eswincomputing.com

# OpenSBI 社区
git send-email --to=opensbi@lists.infradead.org  /home/user/ips-workspace/patch/opensbi/

```