from gtts import gTTS
import os


def gtts_text2sound(text, mp3_filepath, language):  #参数说明:参数1是朗读的文字,参数2是保存路径,参数3是数字{0英文,1中文}
    if int(language) == 0:
        s = gTTS(text=text, lang='en', tld='com')
        # s = gTTS(text=text, lang='en', tld='co.uk')#我比较喜欢美音,但是如果你喜欢英国口音可以尝试这个
    elif int(language) == 1:
        s = gTTS(text=text, lang='zh-CN')  # 已知zh-tw版本违和感较高,所以我们用zh-CN来进行后续工作
    try:
        s.save(mp3_filepath)
    except:
        os.remove(mp3_filepath)
        s.save(mp3_filepath)
    print(mp3_filepath, "保存成功")
    # os.system(mp3_filepath)#调用系统自带的播放器播放MP3


if __name__ == '__main__':
    gtts_text2sound(text="I'm gtts library,from google Artificial Intelligence & Google Translate.",
                    mp3_filepath="gtts英文测试.mp3", language=0)
    gtts_text2sound(text="我是gtts库, 你想听听我的声音吗", mp3_filepath="gtts中文测试.mp3", language=1)
