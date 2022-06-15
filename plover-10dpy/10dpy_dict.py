LONGEST_KEY = 1
from typing import Dict, Optional, List, Sequence, cast
import re
import regex

class TranslationError(Exception):
  pass

NOTHING = "{#}"

init_map = {
  '': '', 'G': 'g', 'HG': 'k', 'H': 'h',
  'SG': 'zh', 'SH': 'ch', 'S': 'sh', 'SHG': 'r',
  'D': 'd', 'SD': 't', 'SGD': 'n', 'GD': 'l',
  'HD': 'b', 'SHGD': 'p', 'HGD': 'm', 'SHD': 'f',
}

init_map_y = {
  'g': 'j', 'k': 'q', 'h': 'x',
}

init_remove_y = {
  'zh': 'z', 'ch': 'c', 'sh': 's',
}

default_final = {
  'b': 'u', 'p': 'u', 'f': 'u',
  'm': 'e',
  'd': 'e', 't': 'e', 'n': 'e', 'l': 'e',
  'g': 'e', 'k': 'e', 'h': 'e',
  'j': 'i', 'q': 'i', 'x': 'i',
  'z': 'i', 'c': 'i', 's': 'i',
  'zh': 'i', 'ch': 'i', 'sh': 'i', 'r': 'i'
}

# [subsequence of YWAINO]
open_map = {
  '':  '', 'AINO': 'er',

                'Y':    'yi',   'W':    'wu',   'YW':   'yu', 
  'A':   'a',   'YA':   'ya',   'WA':   'wa', 
  'IN':  'e',   'YIN':  'ye',   'WIN':  'wo',   'YWIN': 'yue', 
                'YI':   'ye',   'WO':   'wo',   'YWI':  'yue',
  'AI':  'ai',                  'WAI':  'wai', 
  'I':   'ei',                  'WI':   'wei',
  'AO':  'ao',  'YAO':  'yao', 
  'O':   'ou',  'YO':   'you',
  'AN':  'an',  'YAN':  'yan',  'WAN':  'wan',  'YWAN': 'yuan',
  'N':   'en',  'YN':   'yin',  'WN':   'wen',  'YWN':  'yun', 
  'ANO': 'ang', 'YANO': 'yang', 'WANO': 'wang',
  'NO':  'eng', 'YNO':  'ying', 'WNO':  'weng', 'YWNO': 'yong',
}

closed_map = {
  '':  '', 'AINO': 'er',

                'Y':    'i',    'W':    'u',   'YW':   'v', 
  'A':   'a',   'YA':   'ia',   'WA':   'ua', 
  'IN':  'e',   'YIN':  'ie',   'WIN':  'uo',  'YWIN': 've', 
                'YI':   'ie',   'WO':   'uo',  'YWI':  've', 
  'AI':  'ai',                  'WAI':  'uai', 
  'I':   'ei',                  'WI':   'ui',
  'AO':  'ao',  'YAO':  'iao', 
  'O':   'ou',  'YO':   'iu',
  'AN':  'an',  'YAN':  'ian',  'WAN':  'uan', 'YWAN': 'uan',
  'N':   'en',  'YN':   'in',   'WN':   'un',  'YWN':  'un', 
  'ANO': 'ang', 'YANO': 'iang', 'WANO': 'uang',
  'NO':  'eng', 'YNO':  'ing',  'WNO':  'ong', 'YWNO': 'iong',
}

all_legal = {"zhi","chi","shi","ri","zi","ci","si","a","ba","pa","ma","fa","da","ta","na","la","ga","ka","ha","zha","cha","sha","za","ca","sa","o","bo","po","mo","fo","lo","e","me","de","te","ne","le","ge","ke","he","zhe","che","she","re","ze","ce","se","ê","ai","bai","pai","mai","dai","tai","nai","lai","gai","kai","hai","zhai","chai","shai","zai","cai","sai","ei","bei","pei","mei","fei","dei","tei","nei","lei","gei","kei","hei","zhei","shei","zei","sei","ao","bao","pao","mao","dao","tao","nao","lao","gao","kao","hao","zhao","chao","shao","rao","zao","cao","sao","ou","pou","mou","fou","dou","tou","nou","lou","gou","kou","hou","zhou","chou","shou","rou","zou","cou","sou","an","ban","pan","man","fan","dan","tan","nan","lan","gan","kan","han","zhan","chan","shan","ran","zan","can","san","en","ben","pen","men","fen","den","nen","gen","ken","hen","zhen","chen","shen","ren","zen","cen","sen","ang","bang","pang","mang","fang","dang","tang","nang","lang","gang","kang","hang","zhang","chang","shang","rang","zang","cang","sang","eng","beng","peng","meng","feng","deng","teng","neng","leng","geng","keng","heng","zheng","cheng","sheng","reng","zeng","ceng","seng","er","yi","bi","pi","mi","di","ti","ni","li","ji","qi","xi","ya","dia","nia","lia","jia","qia","xia","yo","ye","bie","pie","mie","die","tie","nie","lie","jie","qie","xie","yai","yao","biao","piao","miao","fiao","diao","tiao","niao","liao","jiao","qiao","xiao","you","miu","diu","niu","liu","jiu","qiu","xiu","yan","bian","pian","mian","dian","tian","nian","lian","jian","qian","xian","yin","bin","pin","min","din","nin","lin","jin","qin","xin","yang","biang","diang","niang","liang","jiang","qiang","xiang","ying","bing","ping","ming","ding","ting","ning","ling","jing","qing","xing","wu","bu","pu","mu","fu","du","tu","nu","lu","gu","ku","hu","zhu","chu","shu","ru","zu","cu","su","wa","gua","kua","hua","zhua","chua","shua","rua","wo","duo","tuo","nuo","luo","guo","kuo","huo","zhuo","chuo","shuo","ruo","zuo","cuo","suo","wai","guai","kuai","huai","zhuai","chuai","shuai","wei","dui","tui","gui","kui","hui","zhui","chui","shui","rui","zui","cui","sui","wan","duan","tuan","nuan","luan","guan","kuan","huan","zhuan","chuan","shuan","ruan","zuan","cuan","suan","wen","dun","tun","nun","lun","gun","kun","hun","zhun","chun","shun","run","zun","cun","sun","wang","guang","kuang","huang","zhuang","chuang","shuang","weng","dong","tong","nong","long","gong","kong","hong","zhong","chong","shong","rong","zong","cong","song","yu","nv","lv","ju","qu","xu","yue","nve","lve","jue","que","xue","yuan","juan","quan","xuan","yun","jun","qun","xun","yong","jiong","qiong","xiong"}
check_rule = r"^([bpm])([iu]|a|i?e|o|[ae]i|i?ao|[oi]u|i?an|[ie]n|[ei]ng|ang|ong)|([fw])(u|a|o|[ae]i|ao|ou|an|en|eng|ang|ong)|([dt])([iu]|i?a|i?e|uo|[aeu]i|i?ao|[oi]u|[iu]?an|[ue]n|[ei]ng|ang|ong)|([nl])([iuv]|i?a|[iv]?e|u?o|[aeu]i|i?ao|[oi]u|[iu]?an|[iue]n|[ei]ng|i?ang|ong)|([gkh])(u|u?a|e|uo|u?ai|[ue]i|ao|ou|u?an|[ue]n|eng|u?ang|ong)|([zcs]h?|r)([iu]|u?a|e|uo|u?ai|[ue]i|ao|ou|u?an|[ue]n|eng|u?ang|ong)|([jqxy])([iu]|i?a|[iu]?e|o|i?ao|[oi]u|[iu]?an|[iu]n|ing|i?ang|i?ong)|([aeo]|[ae]i|ao|ou|[ae]ng?|er)$"

specials = {
  'jv': 'ju', 'qv': 'qu', 'xv': 'xu', 
  'jve': 'jue', 'qve': 'que', 'xve': 'xue',
  'buo': 'bo', 'puo': 'po', 'muo': 'mo', 'fuo': 'fo',
}

# input: S?H?G?D?Y?W?A?I?N?O?F?X?
def pm2py(s):
  if s == '':
    return ''
  if s == 'a':
    return '{^ ^}'

  (pm_initials, pm_finals, pm_functions) = regex.fullmatch(r"(S?H?G?D?)(Y?W?A?I?N?O?)(F?X?)", s).groups()
  initials = init_map.get(pm_initials)
  if initials == None:
    raise TranslationError()
  if pm_finals.startswith('Y'):
    if init_map_y.get(initials):
      initials = init_map_y.get(initials)
    elif init_remove_y.get(initials):
      initials = init_remove_y.get(initials)
      pm_finals = pm_finals[1:]
  
  finals = (closed_map if initials else open_map).get(pm_finals)
  if finals == "":
    finals = default_final.get(initials)
  if finals == None:
    raise TranslationError()
  
  pinyin = initials + finals
  pinyin = specials.get(pinyin, pinyin)
  if pinyin not in all_legal:
    raise TranslationError()

  return pinyin + "'"

def translate(s):
  (numL, numR, sL, sR, up, down) = regex.fullmatch(r"(#?)(:?)(S?H?G?D?Y?W?A?I?N?O?F?X?)-?(s?h?g?d?y?w?a?i?n?o?f?x?)(\^?)(_?)", s).groups()
  numL = bool(numL.strip())
  numR = bool(numR.strip())
  up = bool(up.strip())
  down = bool(down.strip())
  if numL or numR or up or down:
    return NOTHING
  sL = sL.upper()
  sR = sR.upper()
  try:
    return '{^}' + pm2py(sL) + pm2py(sR) + '{^}'
  except TranslationError:
    return NOTHING

# Lookup function: return the translation for <key> (a tuple of strokes)
# or raise KeyError if no translation is available/possible.
def lookup(key: List[str])->str:
  print("TEST: ", key)
  assert len(key) <= LONGEST_KEY
  form = translate(key[0])
  print('test: ', form)
  return form

# Optional: return an array of stroke tuples that would translate back
# to <text> (an empty array if not possible).
def reverse_lookup(text):
  return []
