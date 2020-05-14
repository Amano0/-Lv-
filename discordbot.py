import os

import discord
client=discord.Client()
token="put your bots token"


@client.event
async def on_message(message):

    # userのデータが書かれているtextファイルのpath (ファイル名はuser.id)
    USER_DATA_FILE_PATH=f'/MemberData/{message.author.id}.txt'

    # messageの文字数
    mozi_num=len(list(message.content))

    # userの初期データとして新規userのファイルに書き込む内容
    userdatalist=[
        message.author.display_name,
        "0",  # 総メッセージ文字数
        "0",  # 文字数を消費してLvを上げた後に残った文字数
        "1",  # 現在のLv (初期から1Lvは有る)
    ]

    # 自分は拒否
    if message.author != client.user:

        # userのデータのファイルの有無を確認
        if os.path.isfile(USER_DATA_FILE_PATH):

            # 読み込みモード
            with open(USER_DATA_FILE_PATH, mode="r") as f:

                # txt内の文字列を行分けにして data_list というリストにする
                data_list=f.readlines()

                # 読み込んだデータをもとに再度更新するために書き込みモードで読み込む
                with open(USER_DATA_FILE_PATH, mode="w") as f:
                    # そのままでは\nがあるため、\nをforで回して消す
                    data_list=[i.replace('\n','') for i in data_list]
                    # 今までの発言の総文字数に今回の発言の文字数を加える (実際このデータいらないかも)
                    data_list[1]=int(data_list[1]) + mozi_num
                    # 前回のLvUPで消費した残りの文字数に今回の発言の文字数を加える
                    data_list[2]=int(data_list[2]) + mozi_num

                    #残りの文字数がLvUPに必要な文字数を超えたかどうか
                    if int(data_list[3])*200<=data_list[2]:  # 1LvUPに必要な文字数は 現在のレベル*200

                        # 必要量を下回るまでLvをあげる
                        while int(data_list[3])*200<=data_list[2]:
                            # 残りの文字数から必要量を引く
                            data_list[2]-=int(data_list[3])*200
                            # 引いたので、Lvを1上げる
                            data_list[3]=int(data_list[3])+1

                        text=("おめでとう！\n{message.author.mention}のレベルが **__{data_list[3]}__** に上がったよ！")
                        # LvUPしたらメッセージを送信
                        await message.channel.send(text)

                    # ログとして更新後のデータをprint
                    data_list=[str(i) for i in data_list]
                    print(
                        "　＊　＊　＊　＊\n"
                        + f"UserName:{data_list[0]}\n"
                        + f"AllExp:{data_list[1]}\n"
                        + f"Level:{data_list[3]}\n"
                        + f"ExcessExp:{data_list[2]}"
                    )
                    f.write('\n'.join(data_list))

        # userのデータtxtファイルが無かった→つまり新規userだった
        else:

            # データファイルを新規作成
            with open(USER_DATA_FILE_PATH, mode="x") as f:

                # 書き込みモードで開く
                with open(USER_DATA_FILE_PATH, mode="w") as f:
                    # 初期データを書き込む
                    f.write('\n'.join(userdatalist))

client.run(token)
