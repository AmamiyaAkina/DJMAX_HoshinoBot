# DJMAX_HoshinoBot

DJMAX Respect V 查分插件，适用于 **HoshinoBot / Nonebot**。
数据来源于 [V-Archive](https://v-archive.net/)，可以生成玩家 **Bests 分表图**。

---
## 功能
* 查询 **DJMAX Respect V** 玩家成绩
* 指令生成 **Bests 分表图片**
* 支持 **4 / 5 / 6 / 8 键模式**
* 数据来源：V-Archive
---
## 生成分表图示例
![preview](https://github.com/user-attachments/assets/6fc3e532-f5cd-47f0-832f-a75d5e6f2980)

---

## 安装

本项目依赖 `git submodule`。

在`modules`目录下克隆本仓库项目：
```
git clone --recurse-submodules https://github.com/AmamiyaAkina/DJMAX_HoshinoBot.git
```

如果已经`clone`过仓库，可以执行：

```
git submodule update --init --recursive
```

并在`__bot__.py`的`module`中添加`DJMAX_HoshinoBot`

---

## 使用方法

机器人指令：

```
djmax <V-Archive ID> <4/5/6/8>
```

示例：

```
djmax Amamiya_Akina 4
```

机器人会返回对应键位的 **Bests 分表图**。

---

## 注意事项
在机器人第一次运行的时候，会在生成分表之前缓存DJMAX每首歌的曲绘，建议在第一次查分之前提前运行一遍预缓存脚本
```
cd deps/djmax_bests_generate
python prefetch_covers.py
```
---

## 依赖项目
本项目使用以下开源项目：<br>

[djmax_bests_generate](https://github.com/SoreHait/djmax_bests_generate)<br>

同时感谢 [V-Archive](https://v-archive.net/) 提供的公开数据

---

## 更新日志

### 2026-03-12

* 修复旧版本 coroutine `.save()` 语法遗留问题

### 2025-12-20

* 项目首次可用版本

---

## 未来计划

* QQ 账号绑定 V-Archive
* 指令优化

---

## 致谢
代码级指导：[@SoreHait](https://github.com/SoreHait)

感谢以下项目和网站：
* V-Archive
* djmax_bests_generate

推荐使用该工具以自动化捕获分表：
* [VArchiveMacro](https://github.com/johypark97/VArchiveMacro.git)
---

## License

本项目使用 **MIT License**。
