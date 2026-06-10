# DJMAX_HoshinoBot

DJMAX Respect V 查分插件，适用于 **HoshinoBot / Nonebot**。
数据来源于 [V-Archive](https://v-archive.net/)，可以生成玩家 **Best100 分表图**。

---
## 功能
* 查询 **DJMAX Respect V** 玩家成绩
* 生成**4 / 5 / 6 / 8b **的**Bests 100**分表图片
* 生成指定难度的所有曲目的分表图片
* 生成指定曲包难度的所有曲目的分表图片
* 数据来源：V-Archive
---
## 生成分表图示例
<p align="center">
  <img src="https://github.com/user-attachments/assets/6fc3e532-f5cd-47f0-832f-a75d5e6f2980" />
  <img src="https://github.com/user-attachments/assets/d0cb3540-8976-4556-88b4-32763e66ec4f" />
  <img src="https://github.com/user-attachments/assets/afb051d4-c48e-4413-9edf-c71fe1b2f622" />
</p>

---

## 安装

本项目依赖 `git submodule`。

在`modules`目录下克隆本仓库项目：
```
git clone --recurse-submodules https://github.com/AmamiyaAkina/DJMAX_HoshinoBot.git
```

如果已经`clone`过仓库，可以执行该指令更新：

```
git submodule update --remote
```

并在`__bot__.py`的`module`中添加`DJMAX_HoshinoBot`

---

## 使用方法

### Best100 查分指令：

```
djmax <V-Archive ID> b100 <4/5/6/8>
```
机器人会返回对应键位的 **Best100分表图**。并且同时会在**第一次自动绑定该QQ号**。后续查分可直接输入：
```
djmax b100 4
```


### 指定难度分表查分指令

#### 普通难度：
```
djmax <V-Archive ID> list 4 9
```
#### SC难度：
```
djmax <V-Archive ID> list 4 sc9
```
机器人会返回对应键位的 **指定难度分表图**。并且同时会在**第一次自动绑定该QQ号**。后续查分可直接输入：
```
djmax list 4 sc9
```
### 指定曲包查分指令

```
djmax <V-Archive ID> pack 4 <NM/HD/MX/SC> <曲包ID>
```
查找曲包列表指令
```
djmax listdlc
```


### 绑定与解绑

#### 手动绑定
```
djmax bind <V-Archive ID>
```
#### 解绑
```
djmax unbind
```

以上指令相关帮助均可输入`djmax help`查阅

---

## 注意事项
在机器人第一次运行的时候，会在生成分表之前缓存DJMAX每首歌的曲绘，合计大约有700多张图，建议在第一次查分之前提前运行一遍预缓存脚本
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

### 2026-06-10
* 更新了`djmax help`指令

### 2026-05-25
* 更新了`generate_scorelist_pack`指定曲包与难度查分的功能
* 更新了`send_dlc_list`发送全部曲包列表的功能

### 2026-05-18
* 更新了`generate_scorelist`指定难度分表查分的功能

### 2026-05-06
* 纠正并优化了一些命名上的低级错误，并加入了绑定QQ号功能

### 2026-03-12
* 修复旧版本 coroutine `.save()` 语法遗留问题

### 2025-12-20
* 项目首次可用版本
---

## 未来计划

* ~~QQ 账号绑定 V-Archive~~
* ~~指令优化~~
* 同步更新`djmax_bests_generate`的一些其他出图指令（在更了在更了）
* 撰写V-Archive与VArchiveMacro的传分教程

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
