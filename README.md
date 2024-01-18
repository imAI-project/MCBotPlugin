# MCBotPlugin

## 安装

配置完成 [QChatGPT](https://github.com/RockChinQ/QChatGPT) 主程序后使用管理员账号向机器人发送命令即可安装：

```
!plugin get https://github.com/RockChinQ/MCBotPlugin
```
或查看详细的[插件安装说明](https://github.com/RockChinQ/QChatGPT/wiki/5-%E6%8F%92%E4%BB%B6%E4%BD%BF%E7%94%A8)

### 数据库

需要使用数据库存储绑定信息和时长统计信息，目前支持 MongoDB。

首次启动后将生成一个 `mcbot.yaml`, 把 mongodb 的连接 URI 填进去。

## 使用

### 命令

- `!mcbot` - 查看帮助
- `!bind <server>` - 绑定服务器到此群
- `!unbind` - 解绑服务器
- `!status` - 查看服务器状态
- `!time` - 查看时长统计信息