import nltk
def auto_text_tilling(text,text_length=1000,paragraph_limit=20):
    """
    自动拆分文本，对文本进行自动分段
    """

    if len(text.split("\n"))>paragraph_limit or len(text.split(" "))>text_length:
        try:
            ttt = nltk.tokenize.TextTilingTokenizer()
            tiles = ttt.tokenize(text)
            # print("==================\n\n".join(tiles))
            items=[]
            for it in tiles:
                # print("================\n\n")
                # print(it.replace("\n"," "))
                items.append(it.replace("\n"," ").replace("<n>"," ").strip())

            text="\n".join(items)
        except:
            pass
    else:
        text=text.replace("<n>"," ").strip()
        pass
    return text

