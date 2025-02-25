import math
import sys
from random import random

import requests
from secret_vars import SECRET_VARS

BASE = "QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm"

class Charset:
    def __init__(self, chars: str, char_len: int = 1):
        self.map = {
            BASE[i]: chars[i*char_len:(i+1)*char_len] for i in range(len(BASE))
        }

    def map_char(self, char: str) -> str:
        return self.map.get(char, char)

class TextFormatter:
    VARIANTS = [
        Charset("Q₩ɆⱤ₮ɎɄłØ₱₳₴Đ₣₲ⱧJ₭ⱠⱫӾ₵V฿₦₥Q₩ɆⱤ₮ɎɄłØ₱₳₴Đ₣₲ⱧJ₭ⱠⱫӾ₵V฿₦₥"),
        Charset("𝕼𝒲𝕰ℛ𝕿𝒴𝖀ℐ𝕺𝒫𝕬𝒮𝕯ℱ𝕲ℋ𝕵𝒦𝕷𝒵𝖃𝒞𝖁ℬ𝕹ℳ𝖖𝓌𝖊𝓇𝖙𝓎𝖚𝒾𝖔𝓅𝖆𝓈𝖉𝒻𝖌𝒽𝖏𝓀𝖑𝓏𝖝𝒸𝖛𝒷𝖓𝓂"),
        Charset("𝒬𝒲ℰℛ𝒯𝒴𝒰ℐ𝒪𝒫𝒜𝒮𝒟ℱ𝒢ℋ𝒥𝒦ℒ𝒵𝒳𝒞𝒱ℬ𝒩ℳ𝓆𝓌ℯ𝓇𝓉𝓎𝓊𝒾ℴ𝓅𝒶𝓈𝒹𝒻ℊ𝒽𝒿𝓀𝓁𝓏𝓍𝒸𝓋𝒷𝓃𝓂"),
        Charset("Ɋ山㠪尺ㄒㄚㄩ工ㄖ尸闩丂ᗪ千Ꮆ廾丿长㇄乙乂⼕ᐯ乃𝓝爪Ɋ山㠪尺ㄒㄚㄩ工ㄖ尸闩丂ᗪ千Ꮆ廾丿长㇄乙乂⼕ᐯ乃𝓝爪"),
        Charset("𐌒Ꮤ𐌄𐌐𐌕𐌙𐌵𐌉Ꝋ𐌓𐌀𐌔𐌃𐌅Ᏽ𐋅Ꮦ𐌊𐌋Ɀ𐋄𐌂ᕓ𐌁𐌍𐌌𐌒Ꮤ𐌄𐌐𐌕𐌙𐌵𐌉Ꝋ𐌓𐌀𐌔𐌃𐌅Ᏽ𐋅Ꮦ𐌊𐌋Ɀ𐋄𐌂ᕓ𐌁𐌍𐌌"),
        Charset("ⓆⓌⒺⓇⓉⓎⓊⒾⓄⓅⒶⓈⒹⒻⒼⒽⒿⓀⓁⓏⓍⒸⓋⒷⓃⓂⓠⓦⓔⓡⓣⓨⓤⓘⓞⓟⓐⓢⓓⓕⓖⓗⓙⓚⓛⓩⓧⓒⓥⓑⓝⓜ"),
        Charset("ዓሠቹዪፕሃ፱ጎዐየልነጋቻፏⶴፓኡረጊሸርህ፪ክጮዓሠቹዪፕሃ፱ጎዐየልነጋቻፏⶴፓኡረጊሸርህ፪ክጮ"),
        Charset("Q҉W҉E҉R҉T҉Y҉U҉I҉O҉P҉A҉S҉D҉F҉G҉H҉J҉K҉L҉Z҉X҉C҉V҉B҉N҉M҉q҉w҉e҉r҉t҉y҉u҉i҉o҉p҉a҉s҉d҉f҉g҉h҉j҉k҉l҉z҉x҉c҉v҉b҉n҉m҉", 2),
        Charset("𝝫𝗪𝝨𝝘𝝩𝝭𝗨𝝞𝝝𝝦𝝙𝗦𝗗𝗙𝗚𝝜𝗝𝝟𝗟𝝛𝝬𝗖𝝯𝝗𝝥𝝮𝞅𝞏𝝴𝝲𝞃𝞇𝝻𝗶𝝷𝞀𝝰𝘀𝝳𝗳𝗴𝝺𝗷𝝹𝝸𝘇𝞆𝞁𝝼𝝱𝝶𝗺"),
        Charset("ℚ𝕎𝔼ℝ𝕋𝕐𝕌𝕀𝕆ℙ𝔸𝕊𝔻𝔽𝔾ℍ𝕁𝕂𝕃ℤ𝕏ℂ𝕍𝔹ℕ𝕄𝕢𝕨𝕖𝕣𝕥𝕪𝕦𝕚𝕠𝕡𝕒𝕤𝕕𝕗𝕘𝕙𝕛𝕜𝕝𝕫𝕩𝕔𝕧𝕓𝕟𝕞"),
        Charset("🅀🅆🄴🅁🅃🅈🅄🄸🄾🄿🄰🅂🄳🄵🄶🄷🄹🄺🄻🅉🅇🄲🅅🄱🄽🄼🅀🅆🄴🅁🅃🅈🅄🄸🄾🄿🄰🅂🄳🄵🄶🄷🄹🄺🄻🅉🅇🄲🅅🄱🄽🄼"),
        Charset("🆀🆆🅴🆁🆃🆈🆄🅸🅾🅿🅰🆂🅳🅵🅶🅷🅹🅺🅻🆉🆇🅲🆅🅱🅽🅼🆀🆆🅴🆁🆃🆈🆄🅸🅾🅿🅰🆂🅳🅵🅶🅷🅹🅺🅻🆉🆇🅲🆅🅱🅽🅼"),
        Charset("𝐐𝐖𝐄𝐑𝐓𝐘𝐔𝐈𝐎𝐏𝐀𝐒𝐃𝐅𝐆𝐇𝐉𝐊𝐋𝐙𝐗𝐂𝐕𝐁𝐍𝐌𝐪𝐰𝐞𝐫𝐭𝐲𝐮𝐢𝐨𝐩𝐚𝐬𝐝𝐟𝐠𝐡𝐣𝐤𝐥𝐳𝐱𝐜𝐯𝐛𝐧𝐦"),
        Charset("𝕼𝖂𝕰𝕽𝕿𝖄𝖀𝕴𝕺𝕻𝕬𝕾𝕯𝕱𝕲𝕳𝕵𝕶𝕷𝖅𝖃𝕮𝖁𝕭𝕹𝕸𝖖𝖜𝖊𝖗𝖙𝖞𝖚𝖎𝖔𝖕𝖆𝖘𝖉𝖋𝖌𝖍𝖏𝖐𝖑𝖟𝖝𝖈𝖛𝖇𝖓𝖒"),
        Charset("🅠🅦🅔🅡🅣🅨🅤🅘🅞🅟🅐🅢🅓🅕🅖🅗🅙🅚🅛🅩🅧🅒🅥🅑🅝🅜🅠🅦🅔🅡🅣🅨🅤🅘🅞🅟🅐🅢🅓🅕🅖🅗🅙🅚🅛🅩🅧🅒🅥🅑🅝🅜"),
        Charset("ＱＷＥＲＴＹＵＩＯＰＡＳＤＦＧＨＪＫＬＺＸＣＶＢＮＭｑｗｅｒｔｙｕｉｏｐａｓｄｆｇｈｊｋｌｚｘｃｖｂｎｍ")
    ]

    @classmethod
    def random_variant(cls) -> Charset:
        return cls.VARIANTS[math.floor(random()*len(TextFormatter.VARIANTS))]

    @classmethod
    def format(cls, text: str) -> str:
        return "".join([
            cls.random_variant().map_char(c)
            for c in text
        ])
    

# Check if a message was provided
if len(sys.argv) < 2:
    print("Usage: python speak.py \"Your message here\"")
    sys.exit(1)

# Replace with your Discord webhook URL
response = requests.post(SECRET_VARS['heart'], json={
    "content": TextFormatter.format(" ".join(sys.argv[1:]))
})

# Check if the message was sent successfully
if response.status_code == 204:
    print("Message sent successfully!")
else:
    print(f"Failed to send message. Status code: {response.status_code}")
