import requests
from bs4 import BeautifulSoup
import re
import json


if __name__ == '__main__':

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
    }
    response = requests.get("https://www.zhihu.com/question/360515552", headers=headers)
    file_data = ""
    dict = {}

    if response.ok:
        html_data = response.text
        json_str = re.findall('<script id="js-initialData" type="text/json">(.*?)</script>', html_data)[0]
        json_data = json.loads(json_str)
        answers = json_data['initialState']['entities']['answers']
        next = json_data['initialState']['question']['answers']['360515552']['next']

        headers2 = {
            'cookie': '_zap=64f4d72c-cabe-4a01-9595-f1fde1e62847; d_c0=AEATDWLK0RWPTrUoU9kl2sp7vqly4Ckg-RQ=|1667636058; YD00517437729195%3AWM_TID=zur2UDuTXfFEQFQVFBPQcTR54t29lN%2FF; __snaker__id=ZtwRnXHzgABgp5cw; YD00517437729195%3AWM_NI=cW4RzYLgnZlDE%2BpAOMu%2F49DXYqzeDfYCpqgGwWi8Mx%2Fx7bgflXpRc9hoY2AdqBfaEC5LKg7xAhO5DjZc7DEh7piv3z5PBl5XucVm8w%2Bsjia8jAAjTze4U6b1xfm5Er9fRXo%3D; YD00517437729195%3AWM_NIKE=9ca17ae2e6ffcda170e2e6eeb6fb5bb1bb9a94e65b98ef8ab3c54e878b8a87c1478cbca38ec625fb908fb7e62af0fea7c3b92aa189fcb3f95390b9a2bbef5087f5c0a2ce47b7f1fcdac7549bafb686c76e9b9dc092e64db589a7d9d074eda8f983e66eb088c0b3e233acb197d3c470b39eaa82c849f7948588b67483b881d6c7629abdf9a5c864f5b0a797b272f7908e8db854b7bd9a8ebb7de9ada68ae434aa9f8f8bd772a7ec9bd7e13bbcbaa3d6c87afbba9eb9ee37e2a3; q_c1=9714ec3a05f24d9e9ebda7106642d22f|1668436399000|1668436399000; _xsrf=BbYZ5wZsIKQKxl4hm6cy9ToCUVNj7fXY; z_c0=2|1:0|10:1681974467|4:z_c0|80:MS4xN2psQUF3QUFBQUFtQUFBQVlBSlZUVEFFS1dWNkpnaFB3dmZVcFppek00RVZPVFZXZ05HMFB3PT0=|843d6d3ec484619688cbbbf886594220ae96f7c45e9ea8402d4e07998f4592bb; tst=r; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1682233950,1682255283,1682336031,1682385614; SESSIONID=mnGpSyItb7Wa0untyqmk7gjlzpU9Lt57RqwcfUjUgVR; JOID=UFwTBkj24Yf_2nBUbvFW1ZW7vYJ_nY3DiYgPHxmV0NKd7AQ8GD3KxZzddFVr9-974ESMAfEZWmxNo84umrMm2TE=; osd=V1sUBkPx5oD_0XdTafFd0pK8vYl4morDgo8IGBme19Wa7A87HzrKzpvac1Vg8Oh84E-LBvYZUWtKpM4lnbQh2To=; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1682406985; KLBRSID=4843ceb2c0de43091e0ff7c22eadca8c|1682407008|1682405603',
            'referer': 'https://www.zhihu.com/question/360515552',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
            'x-ab-pb': 'CkAbAD8ARwC0AGkBagF0ATsCzALXAtgCtwPWBFEFiwWMBZ4FMQbrBicHdAh5CGAJ9AlrCr4KcQuHC+UL5guPDPgMEiAJAAAAAgEAAQAAAAAEAQAAAQAAAAAGAQMAAAAAAAAAAA==',
            'x-requested-with': 'fetch',
            'x-zse-93': '101_3_3.0',
            'x-zse-96': '2.0_XNVtOHAJg127oFhChM9zgb0mJICqAqmueY=Ysy3dr9tikrKczdeUDekkFXg7ZA/2',
            'x-zst-81': '3_2.0aR_sn77yn6O92wOB8hPZnQr0EMYxc4f18wNBUgpTQ6nxERFZ8XY0-4Lm-h3_tufIwJS8gcxTgJS_AuPZNcXCTwxI78YxEM20s4PGDwN8gGcYAupMWufIoLVqr4gxrRPOI0cY7HL8qun9g93mFukyigcmebS_FwOYPRP0E4rZUrN9DDom3hnynAUMnAVPF_PhaueTFAuY-uV1eCOYhwO03DVOQGpxSiL18AL_3hCK3US_Ig38KqOOb6Cyr8exicSTV4xCkTLLnbN9eeXMU9oCCuVOShHBJLXqf7SY6eHCr0SfSu3KUh3KTcuyuG2fVgY0zcN_pqxy-GNmkvOmKQOOShrfQuFYxBO8l9xOQLp9-CFL_JN_5qV0Og_zCUpKVgV1mggMscCMkMwOJqXfE9HCBhrYygoXBuYMp9OOJTpqyDeMxULGUGxLQAxOHGgpivw0cCwmxrV_FUwso7OZdDHqarOMJDcmwwNLH9YYwJxCowts',
        }
        for key in list(answers.keys()):
            if dict.get(key) is not None:
                continue
            dict[key] = 0
            print(key)
            content = answers[key]['content']
            soup = BeautifulSoup(content, 'html.parser')
            markdown = soup.get_text(separator='\n')
            temp = "\n&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&" + "\n"+ "\n"+ "\n"
            file_data = file_data + f"\n{key}\n"+ markdown + temp

        next_res = requests.get(next, headers=headers2).text
        next_json_data = json.loads(next_res)
        while True:
            next_url = next_json_data['paging']['next']
            next_res = requests.get(next_url, headers=headers2).text
            next_json_data = json.loads(next_res)
            for i in range(len(next_json_data['data'])):
                next_content = next_json_data['data'][i]['target']['content']
                id = next_json_data['data'][i]['target']['id']
                if dict.get(id) is not None:
                    continue
                dict[id] = 0
                print(id)
                soup = BeautifulSoup(next_content, 'html.parser')
                markdown = soup.get_text(separator='\n')
                temp = "\n&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&" + "\n"+ "\n"+ "\n"
                file_data = file_data + f"\n{id}\n"+ markdown + temp
            if len(next_json_data['data']) < 5:
                break

        with open("2023 Fall.txt", "w", encoding="utf-8") as f:
            f.write(file_data)

else:
        print("请求失败")
