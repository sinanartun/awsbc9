import json
import boto3
import os
def lambda_handler(event, context):
    sqs = boto3.client('sqs')
    SQS_URL = os.getenv('SQS_URL')

    data = [
  [
    "A1CAP",
    "a1cap-a1-capital-yatirim/"
  ],
  [
    "ACSEL",
    "acsel-acipayam-seluloz/"
  ],
  [
    "ADEL",
    "adel-adel-kalemcilik/"
  ],
  [
    "ADESE",
    "adese-adese-gayrimenkul/"
  ],
  [
    "ADGYO",
    "adgyo-adra-gmyo/"
  ],
  [
    "AEFES",
    "aefes-anadolu-efes/"
  ],
  [
    "AFYON",
    "afyon-afyon-cimento/"
  ],
  [
    "AGESA",
    "agesa-agesa-hayat-emeklilik/"
  ],
  [
    "AGHOL",
    "aghol-anadolu-grubu-holding/"
  ],
  [
    "AGROT",
    "agrot-agrotech-teknoloji/"
  ],
  [
    "AGYO",
    "agyo-atakule-gmyo/"
  ],
  [
    "AHGAZ",
    "ahgaz-ahlatci-dogalgaz/"
  ],
  [
    "AKBNK",
    "akbnk-akbank/"
  ],
  [
    "AKCNS",
    "akcns-akcansa/"
  ],
  [
    "AKENR",
    "akenr-ak-enerji/"
  ],
  [
    "AKFGY",
    "akfgy-akfen-gmyo/"
  ],
  [
    "AKFYE",
    "akfye-akfen-yen-enerji/"
  ],
  [
    "AKGRT",
    "akgrt-aksigorta/"
  ],
  [
    "AKMGY",
    "akmgy-akmerkez-gmyo/"
  ],
  [
    "AKSA",
    "aksa-aksa/"
  ],
  [
    "AKSEN",
    "aksen-aksa-enerji/"
  ],
  [
    "AKSGY",
    "aksgy-akis-gmyo/"
  ],
  [
    "AKSUE",
    "aksue-aksu-enerji/"
  ],
  [
    "AKYHO",
    "akyho-akdeniz-yatirim-holding/"
  ],
  [
    "ALARK",
    "alark-alarko-holding/"
  ],
  [
    "ALBRK",
    "albrk-albaraka-turk/"
  ],
  [
    "ALCAR",
    "alcar-alarko-carrier/"
  ],
  [
    "ALCTL",
    "alctl-alcatel-lucent-teletas/"
  ],
  [
    "ALFAS",
    "alfas-alfa-solar-enerji/"
  ],
  [
    "ALGYO",
    "algyo-alarko-gmyo/"
  ],
  [
    "ALKA",
    "alka-alkim-kagit/"
  ],
  [
    "ALKIM",
    "alkim-alkim-kimya/"
  ],
  [
    "ALMAD",
    "almad-altinyag-madencilik-ve-enerji/"
  ],
  [
    "ALTINS1",
    "altins1-darphane-altin-sertifikasi/"
  ],
  [
    "ANELE",
    "anele-anel-elektrik/"
  ],
  [
    "ANGEN",
    "angen-anatolia-tani-ve-biyoteknoloji/"
  ],
  [
    "ANHYT",
    "anhyt-anadolu-hayat-emek/"
  ],
  [
    "ANSGR",
    "ansgr-anadolu-sigorta/"
  ],
  [
    "ARASE",
    "arase-dogu-aras-enerji/"
  ],
  [
    "ARCLK",
    "arclk-arcelik/"
  ],
  [
    "ARDYZ",
    "ardyz-ard-bilisim-teknolojileri/"
  ],
  [
    "ARENA",
    "arena-arena-bilgisayar/"
  ],
  [
    "ARSAN",
    "arsan-arsan-tekstil/"
  ],
  [
    "ARZUM",
    "arzum-arzum-ev-aletleri/"
  ],
  [
    "ASELS",
    "asels-aselsan/"
  ],
  [
    "ASGYO",
    "asgyo-asce-gmyo/"
  ],
  [
    "ASTOR",
    "astor-astor-enerji/"
  ],
  [
    "ASUZU",
    "asuzu-anadolu-isuzu/"
  ],
  [
    "ATAGY",
    "atagy-ata-gmyo/"
  ],
  [
    "ATAKP",
    "atakp-atakey-patates/"
  ],
  [
    "ATATP",
    "atatp-atp-yazilim/"
  ],
  [
    "ATEKS",
    "ateks-akin-tekstil/"
  ],
  [
    "ATLAS",
    "atlas-atlas-yat-ort/"
  ],
  [
    "ATSYH",
    "atsyh-atlantis-yatirim-holding/"
  ],
  [
    "AVGYO",
    "avgyo-avrasya-gmyo/"
  ],
  [
    "AVHOL",
    "avhol-avrupa-yatirim-holding/"
  ],
  [
    "AVOD",
    "avod-avod-gida-ve-tarim/"
  ],
  [
    "AVPGY",
    "avpgy-avrupakent-gmyo/"
  ],
  [
    "AVTUR",
    "avtur-avrasya-petrol-ve-tur/"
  ],
  [
    "AYCES",
    "ayces-altinyunus-cesme/"
  ],
  [
    "AYDEM",
    "aydem-aydem-enerji/"
  ],
  [
    "AYEN",
    "ayen-ayen-enerji/"
  ],
  [
    "AYES",
    "ayes-ayes-celik-hasir-ve-cit/"
  ],
  [
    "AYGAZ",
    "aygaz-aygaz/"
  ],
  [
    "AZTEK",
    "aztek-aztek-teknoloji/"
  ]

]


    for item in data:
        sqs.send_message(QueueUrl=SQS_URL, MessageBody=json.dumps(item))

    return {
        'statusCode': 200,
        'body': 'Messages sent to SQS queue3'
    }