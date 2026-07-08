# DJMAX_HoshinoBot

DJMAX Respect V 查分插件，适用于 **HoshinoBot / Nonebot**。
数据来源于 [`V-Archive`](https://v-archive.net/)，可以生成玩家 **Best100 分表图**。

---
## 功能
* 查询**DJMAX Respect V**玩家成绩，涵盖以下内容
* b100分表
* 指定难度等级分表
* 指定曲包分表
* 新曲目（NEW）分表
* PP(Perfect Play)分表
* 当前版本理论值b100分表
---
## 
<p align="center">
  <img width="321" height="520" src="https://github.com/user-attachments/assets/6fc3e532-f5cd-47f0-832f-a75d5e6f2980" />
  <img width="321" height="520" src="https://github.com/user-attachments/assets/d0cb3540-8976-4556-88b4-32763e66ec4f" />
  <img width="321" height="300" src="https://github.com/user-attachments/assets/afb051d4-c48e-4413-9edf-c71fe1b2f622" />
</p>

---

## 快速开始

本项目依赖 `git submodule`。

在`modules`目录下克隆本仓库项目，并在`__bot__.py`的`module`中添加`DJMAX_HoshinoBot`
```
git clone --recurse-submodules https://github.com/AmamiyaAkina/DJMAX_HoshinoBot.git
```

## 更新

```
git submodule update --remote
```

---

## 使用方法

### b100查分

```
djmax <V-Archive ID> b100 <4/5/6/8>
```

### 指定难度分表

```
djmax <V-Archive ID> list <4/5/6/8> <难度等级>
```

### 指定曲包分表

```
djmax <V-Archive ID> pack <4/5/6/8> <NM/HD/MX/SC> <曲包代码>
```
如需查询曲包代码，可以输入
```
djmax listdlc
```

### 新曲目（NEW）分表
```
djmax <V-Archive ID> new <4/5/6/8> <NM/HD/MX/SC>
```

### PP(Perfect Play)分表
```
djmax <V-Archive ID> pp <4/5/6/8>
```

### 当前版本理论值的b100分表
```
djmax max <4/5/6/8>
```

### 绑定与解绑

#### 自动绑定
在第一次使用或QQ号未绑定V-Archive ID时，通过第一次使用`b100` `list` `pack` `new` `pp`等指令查分，将会自动静默将二者绑定，绑定数据存放于`djmax_bind_data.json`中

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
在机器人第一次运行的时候，会在生成分表之前缓存DJMAX每首歌的曲绘，总共有800多张图，建议在第一次运行或者DJMAX更新后跑一遍预缓存脚本
```
cd deps/djmax_bests_generate
python prefetch_covers.py
```

---

## 更新日志

### 2026-07-08
* 已适配完成`djmax_bests_generate`的所有查分功能
* 重写并精简了使用方法部分
* 为`list` `pack` `new` `pp`指令适配了自动绑定QQ号与V-Archive ID的功能
	
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

* 如有issue或者建议，再考虑更新
* ~~QQ 账号绑定 V-Archive（完成）~~
* ~~指令优化(完成)~~
* ~~同步更新`djmax_bests_generate`的一些其他出图指令（更完了）~~
* ~~撰写V-Archive与VArchiveMacro的传分教程（老教程很麻烦，懒得写了）~~

---

## 致谢


本项目基于开源项目[`djmax_bests_generate`](https://github.com/SoreHait/djmax_bests_generate)二次开发

代码级指导：[@SoreHait](https://github.com/SoreHait)

## 友链DJMAX查分群
如有需要，可加入该QQ群寻求查分相关帮助：[群聊链接](https://qm.qq.com/q/TnMtgPUyau)

<p align="center">
  <img width="321" height="573" alt="qrcode_1783503964991" src="https://github.com/user-attachments/assets/ee5785d7-bc1e-4c54-972d-d242d835124e" /
</p>

>

---

## License

本项目使用 **MIT License**。
