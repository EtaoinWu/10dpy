# 10dpy - 10 Digit Pinyin

10dpy is an phono-coding scheme of Standard Mandarin Chinese. It uses 10 bits (binary **digits**) to encode a Standard Chinese syllable, and each of these bits can be input by a **digit** of the hand. This is loosely inspired by rime's [Combo Pinyin](https://github.com/rime/rime-combo-pinyin). The reference implementation works with the steno engine [Plover](https://github.com/openstenoproject/plover), and is supposed to be used **with another full-Pinyin IME**.

## Key Layout

This is the key layout I use for [georgi](https://www.gboards.ca/product/georgi):

```plain
       S  H  G  D  F | X  A  E  N  O  ^
       s  h  g  d  f | x  a  e  n  o  _
          #  Y  y    |    w  W  :
```

This is the minimal requirement of this layout:

```plain
       S  H  G  D   |   A  E  N  O  ^
          #  Y      |      W  :
```

Only ten keys (marked `SHGDYWAENO`) are used to encode Pinyin. Other keys are for punctuations, numbers, function keys, etc. You can, technically, use a 10-key layout for *10dpy*, and there are products like the [Ginny](https://www.gboards.ca/product/ginni). However, you need to redesign all the shortcuts for punctuation symbols.

## Design

Please refer to [this document](design.zh.md) (in Chinese).

<!--
### Syllable Structure

A regular Pinyin [syllable](https://en.wikipedia.org/wiki/Syllable#Chinese_model) has the following structure:

* The initial **ι** (optional onset, excluding sonorants)
* The final **φ**, which can be analyzed as
  * The medial **μ**: optional semivowel or liquid.
  * The nucleus **ν**: a vowel or syllabic consonant.
  * The coda **κ**: an optional final consonant. 

There are 22 initials in Pinyin (b, p, m, f, d, t, n, l, g, k, h, j, q, x, zh, ch, sh, r, z, c, s, ø). 

### Initial Chart

### Final Chart
-->
## Output

### Full Pinyin (default)

### Double Pinyin 

