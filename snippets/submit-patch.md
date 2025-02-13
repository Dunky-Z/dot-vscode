ESWIN邮箱配置

```config
[sendemail]
	smtpencryption = tls
	smtpserver = smtp.eswincomputing.com
	smtpuser = zhangdongdong@eswincomputing.com
	smtpserverport = 25
	from = zhangdongdong@eswincomputing.com
	smtppass = 
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
	smtppass = 
	cc = zhangdongdong@eswincomputing.com
	#to = opensbi@lists.infradead.org
```

```
git format-patch -o update_gitignore/  HEAD^

git format-patch --cover-letter -o update_gitignore/ --base=auto  update_gitignore@{u}..update_gitignore
git send-email --to=target@example.com update_gitignore/*.patch
git format-patch -v2 --cover-letter -o update_gitignore/   master..update_gitignore-v1
git commit --amend --author="<FirstName> <LastName> <xxx@xxx.com>" --no-edit
git format-patch -o ~/patch/opensbi HEAD^

git send-email --to zhangdongdong@eswincomputing.com 
                 --in-reply-to="<foo.12345.author@example.com>" 
               update_gitignore/v2-*.patch 

git send-email --to=zhuwenjun@eswincomputing.com --cc=qinhaijun@eswincomputing.com,zhangleizheng@eswincomputing.com
git send-email --to=jinyanjiang@eswincomputing.com --cc=zhuwenjun@eswincomputing.com,zhengyu@eswincomputing.com

# OpenSBI 社区
# commit 标题需要在冒号后加空格如lib: src: 
git format-patch -o ~/patch/opensbi HEAD^
git format-patch --cover-letter -o ~/patch/opensbi/test-math HEAD^
git send-email --to=opensbi@lists.infradead.org  /home/user/ips-workspace/patch/opensbi/

# Buildroot 社区
git format-patch --cover-letter -o ~/patch/buildroot HEAD^
git format-patch -v2 --cover-letter -o ~/patch/buildroot/add-github-action-v2 add-github-action..add-github-action-v2 
git format-patch -o ~/patch/buildroot HEAD^
# 获取需要抄送的开发者
./utils/get-developers /home/user/ips-workspace/patch/buildroot/
git send-email --to=buildroot@buildroot.org --cc=bonet@grenoble.cnrs.fr,arnout@mind.be
```

# Linux Kernel 社区

```bash
git format-patch -o ~/patch/linux HEAD^
./scripts/get_maintainer.pl ~/patch/linux/xxx.patch
```

测试发送邮件：

```bash
git send-email --to="alex.williamson@redhat.com" \
               --cc="bhelgaas@google.com" \
               --cc="zhangdongdong@eswincomputing.com" \
               --cc="yishaih@nvidia.com" \
               --cc="avihaih@nvidia.com" \
               --cc="yi.l.liu@intel.com" \
               --cc="ankita@nvidia.com" \
               --cc="kvm@vger.kernel.org" \
               --cc="linux-kernel@vger.kernel.org" \
               --cc="linux-pci@vger.kernel.org" \
               --dry-run 0001-some-feature-fix.patch
```
