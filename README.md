# dot-vscode(.vscode)

.vscode 目录下的文件一般是用来配置 vscode 的，比如配置调试、配置任务、配置插件等等。本项目保存了一些常用的配置，方便以后使用。

想要调试哪一个项目，就把.vscode目录放在哪个项目下面，`--compile-commands-dir`配置的路径在哪一个目录，clangd生成的`.cache`的目录就在同级目录下。

如果出现 invalid AST 错误，将 .clangd 文件放到项目根目录，重启 clangd。

进入到项目目录下，执行 `git clone https://github.com/Dunky-Z/dot-vscode.git .vscode`，将本项目的配置文件克隆到 `.vscode` 目录下即可。具体配置文件说明可以参考下文进行修改。

generate_compdb.py 程序来自项目[amezin/vscode-linux-kernel](https://github.com/amezin/vscode-linux-kernel)。