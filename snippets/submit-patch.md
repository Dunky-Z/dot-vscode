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
git format-patch -o ../patch/opensbi HEAD^

git send-email --to zhangdongdong@eswincomputing.com 
                 --in-reply-to="<foo.12345.author@example.com>" 
               update_gitignore/v2-*.patch 

git send-email --to=zhuwenjun@eswincomputing.com --cc=qinhaijun@eswincomputing.com,zhangleizheng@eswincomputing.com
git send-email --to=jinyanjiang@eswincomputing.com --cc=zhuwenjun@eswincomputing.com,zhengyu@eswincomputing.com

# OpenSBI 社区
git format-patch --cover-letter -o ../patch/opensbi HEAD^
git send-email --to=opensbi@lists.infradead.org  /home/user/ips-workspace/patch/opensbi/

```


OpenSBI v1.4-130-g87d099e
   ____                    _____ ____ _____
  / __ \                  / ____|  _ \_   _|
 | |  | |_ __   ___ _ __ | (___ | |_) || |
 | |  | | '_ \ / _ \ '_ \ \___ \|  _ < | |
 | |__| | |_) |  __/ | | |____) | |_) || |_
  \____/| .__/ \___|_| |_|_____/|____/_____|
        | |
        |_|

Platform Name             : riscv-virtio,qemu
Platform Features         : medeleg
Platform HART Count       : 1
Platform IPI Device       : aclint-mswi
Platform Timer Device     : aclint-mtimer @ 10000000Hz
Platform Console Device   : uart8250
Platform HSM Device       : ---
Platform PMU Device       : ---
Platform Reboot Device    : syscon-reboot
Platform Shutdown Device  : syscon-poweroff
Platform Suspend Device   : ---
Platform CPPC Device      : ---
Firmware Base             : 0x80000000
Firmware Size             : 327 KB
Firmware RW Offset        : 0x40000
Firmware RW Size          : 71 KB
Firmware Heap Offset      : 0x49000
Firmware Heap Size        : 35 KB (total), 2 KB (reserved), 11 KB (used), 21 KB (free)
Firmware Scratch Size     : 4096 B (total), 416 B (used), 3680 B (free)
Runtime SBI Version       : 2.0

Domain0 Name              : root
Domain0 Boot HART         : 0
Domain0 HARTs             : 0*
Domain0 Region00          : 0x0000000000100000-0x0000000000100fff M: (I,R,W) S/U: (R,W)
Domain0 Region01          : 0x0000000010000000-0x0000000010000fff M: (I,R,W) S/U: (R,W)
Domain0 Region02          : 0x0000000002000000-0x000000000200ffff M: (I,R,W) S/U: ()
Domain0 Region03          : 0x0000000080040000-0x000000008005ffff M: (R,W) S/U: ()
Domain0 Region04          : 0x0000000080000000-0x000000008003ffff M: (R,X) S/U: ()
Domain0 Region05          : 0x000000000c400000-0x000000000c5fffff M: (I,R,W) S/U: (R,W)
Domain0 Region06          : 0x000000000c000000-0x000000000c3fffff M: (I,R,W) S/U: (R,W)
Domain0 Region07          : 0x0000000000000000-0xffffffffffffffff M: () S/U: (R,W,X)
Domain0 Next Address      : 0x0000000080200000
Domain0 Next Arg1         : 0x0000000082200000
Domain0 Next Mode         : S-mode
Domain0 SysReset          : yes
Domain0 SysSuspend        : yes

Boot HART ID              : 0
Boot HART Domain          : root
Boot HART Priv Version    : v1.12
Boot HART Base ISA        : rv64imafdch
Boot HART ISA Extensions  : sstc,zicntr,zihpm,zicboz,zicbom,sdtrig,svadu
Boot HART PMP Count       : 16
Boot HART PMP Granularity : 2 bits
Boot HART PMP Address Bits: 54
Boot HART MHPM Info       : 16 (0x0007fff8)
Boot HART Debug Triggers  : 2 triggers
Boot HART MIDELEG         : 0x0000000000001666
Boot HART MEDELEG         : 0x0000000000f0b509

# Running SBIUNIT tests #
## Running test suite: bitmap_test_suite
[PASSED] bitmap_and_test
[PASSED] bitmap_or_test
[PASSED] bitmap_xor_test
3 PASSED / 0 FAILED / 3 TOTAL
## Running test suite: console_test_suite
[PASSED] putc_test
[PASSED] puts_test
[PASSED] printf_test
3 PASSED / 0 FAILED / 3 TOTAL
## Running test suite: atomic_test_suite
[PASSED] atomic_rw_test
[PASSED] add_return_test
[PASSED] sub_return_test
[PASSED] cmpxchg_test
[PASSED] atomic_xchg_test
[PASSED] atomic_raw_set_bit_test
[PASSED] atomic_raw_clear_bit_test
[PASSED] atomic_set_bit_test
[PASSED] atomic_clear_bit_test
9 PASSED / 0 FAILED / 9 TOTAL
## Running test suite: locks_test_suite
[PASSED] spin_lock_test
[PASSED] spin_trylock_fail
[PASSED] spin_trylock_success
3 PASSED / 0 FAILED / 3 TOTAL
## Running test suite: math_test_suite
[PASSED] log2roundup_test
1 PASSED / 0 FAILED / 1 TOTAL

Test payload running