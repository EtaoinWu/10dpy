# 10dpy 设计文档

## 按键方案

10dpy 将拼音音节编码为 10bit，在本文中标记为字符串 `SHGDYWAINO` 的一个子序列。例如，拼音音节 dai 被编码为 `DAI`。

这 10 个字符分别对应左手的第五指至第一指、右手的第一指至第五指（遵循钢琴惯例，“第一指”为拇指，“第二指”为食指，以此类推），即双手大拇指放在 `Y W` 两键上。在输入时，手指只需考虑是否按下，不需考虑上下左右移动。例如音节 guan 编码为 `GWAN`，需要左手中指、左手拇指、右手食指、右手无名指同时按下。

## 音节结构

每个汉语拼音音节可以分为声母、韵母、音调三部分，韵母又可以分为介母、韵腹、韵尾。以音节「双」shuāng 为例，声母为 sh-，介母为 -u-，韵腹为 a，韵尾为 -ng，音调为阴平。按大部分拼音输入法的规律，10dpy 中我们不考虑音调。

## 韵母编码

韵母采用左手大拇指、右手五指，一共六个手指对应的 6 bit 进行编码。

### 介母

介母有 -ø-, -i-, -u-, -ü- 四种。我们可以分出两个维度：

|        | 洪音 | 细音 |
| :----: | :--: | :--: |
| 不圆唇 | -ø-  | -i-  |
|  圆唇  | -u-  | -ü-  |

我们用两个比特 Y 和 W 表达“是否细音”和“是否圆唇”，即上表被编码为

|        | 洪音 | 细音 |
| :----: | :--: | :--: |
| 不圆唇 | (空) | `Y`  |
|  圆唇  | `W`  | `YW` |

### 韵腹

韵腹有三种：空（仅在介母非空时存在）、央（o 或 e）、低（a）。我们使用 `A` 这一比特来编码“低”的韵腹。介母非空时，为了区分韵腹为空或央（lie/li, tuo/tu），默认韵腹为空，占用韵尾的编码 `IN` 来表达介母为央。

### 韵尾

韵尾有五种：-ø、-i、-u、-n、-ng。使用最后三个比特 `INO` 来编码韵尾，上述五种韵尾分别用空、`I`、`O`、`N`、`NO` 来编码。

### 音节例外与简化

ong 与 ueng 互补，均视作后者进行编码。

拼音音节 bo、po、mo、fo 视作 buo、puo、muo、fuo 进行编码。

不符合上述音系的音节 er 采用特殊编码 `AINO`。

表达拼音 ie、üe 的组合 `YIN`、`YWIN` 可以简化为 `YI`、`YWI`，表达拼音 `uo` 的组合 `WIN` 可以输入为 `WO`。

### 韵母总表

| 零声母 |      |      |      | 编码 |          |          |            |
| ------ | ---- | ---- | ---- | ---- | -------- | -------- | ---------- |
| er     |      |      |      | AINO |          |          |            |
|        | yi   | wu   | yü   |      | Y        | W        | YW         |
| a      | ya   | wa   |      | A    | YA       | WA       |            |
| e      | ye   | wo   | yüe  | IN   | YIN / YI | WIN / WO | YWIN / YWI |
| ai     |      | wai  |      | AI   |          | WAI      |            |
| ei     |      | wei  |      | I    |          | WI       |            |
| ao     | yao  |      |      | AO   | YAO      |          |            |
| ou     | you  |      |      | O    | YO       |          |            |
| an     | yan  | wan  | yüan | AN   | YAN      | WAN      | YWAN       |
| en     | yin  | wen  | yün  | N    | YN       | WN       | YWN        |
| ang    | yang | wang |      | ANO  | YANO     | WANO     |            |
| eng    | ying | weng | yong | NO   | YNO      | WNO      | YWNO       |

| 有声母 |      |      |      | 编码 |          |          |            |
| ------ | ---- | ---- | ---- | ---- | -------- | -------- | ---------- |
|        |      |      |      | AINO |          |          |            |
|        | i    | u    | ü    |      | Y        | W        | YW         |
| a      | ia   | ua   |      | A    | YA       | WA       |            |
| e      | ie   | uo   | üe   | IN   | YIN / YI | WIN / WO | YWIN / YWI |
| ai     |      | uai  |      | AI   |          | WAI      |            |
| ei     |      | ui   |      | I    |          | WI       |            |
| ao     |      | iao  |      | AO   | YAO      |          |            |
| ou     |      | iu   |      | O    | YO       |          |            |
| an     | ian  | uan  | üan  | AN   | YAN      | WAN      | YWAN       |
| en     | in   | un   | ün   | N    | YN       | WN       | YWN        |
| ang    | iang | uang |      | ANO  | YANO     | WANO     |            |
| eng    | ing  | ong  | iong | NO   | YNO      | WNO      | YWNO       |

## 声母编码

拼音一共有 22 个声母：ø, b, p, m, f, d, t, n, l, g, k, h, j, q, x, zh, ch, sh, r, z, c, s。为了把它们编码到 4 bit 中，我们需要做一些权衡。首先可以发现龈颚声母 j, q, x 与软腭声母 g, k, h 互补，前三个只配合细音韵腹、后三个只配合洪音韵腹。因此我们使用 g、k、h + `Y` 来表达 j、q、x。

同理，我们可以发现 zh ch sh z c s 都只出现洪音，我们也将其合并。由于词频统计中 z c s 的频率相比于 zh ch sh 更低，我们将 zh ch sh 设为默认，用它们加 `Y` 来表达 z c s。

最后的 4 bit 声母表为：

```plain
  G : g
 HG : k
 H  : h
  
S   : zh
 HGD: ch
  GD: sh
SH  : r
 
   D: d
SHG : t
S G : n
 H D: l
 
SHGD: b
S GD: p
S  D: m
SH D: f
```

每个声母具有零韵母简码。分别为：bu、pu、me、fu、de、te、ne、le、ge、ke、he、ji、qi、xi、zhi、chi、shi、ri、zi、ci、si。

## 范例

| 汉字 | 拼音  | 10dpy   |
| ---- | ----- | ------- |
| 有   | you   | `YO`    |
| 一   | yi    | `Y`     |
| 次   | ci    | `SHY`   |
| 北   | bei   | `SHGDI` |
| 风   | feng  | `SHDNO` |
| 和   | he    | `H`     |
| 太   | tai   | `SHGAI` |
| 阳   | yang  | `YANO`  |
| 正   | zheng | `SNO`   |
| 在   | zai   | `SYAI`  |
| 争   | zheng | `SNO`   |
| 论   | lun   | `HDWN`  |
| 谁   | shei  | `GDI`   |
| 比   | bi    | `SHGDY` |
| 较   | jiao  | `GYAO`  |
| 有   | you   | `YO`    |
| 本   | ben   | `SHGDN` |
| 事   | shi   | `GD`    |

