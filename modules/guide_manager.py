import time

from openai import AzureOpenAI

from config.setting import API_KEY, ENDPOINT, API_VERSION, MODEL
from modules.db_handler import get_description, get_last_updated, insert_object

system_message = """
Provide only the latest essential information about the given Minecraft object concisely for the player. 
For example, how to obtain and use it.
In about 30 to 50 words.
Use "\n" for line breaks.
Finally, count the number of characters and make sure it is between 30 and 50. If not, start over from the beginning.
Don't output character counts.
Answer in Japanese.
"""

def get_chat_response(input_object: str, update_flag: bool) -> str:
    """    
    Args:
        input_object (str): 物体認識の結果
        system_message (str): システムプロンプト
    
    Returns:
        str: オブジェクトの説明
    """
    client = AzureOpenAI(
        azure_endpoint=ENDPOINT,
        api_key=API_KEY,
        api_version=API_VERSION
    )
    
    if update_flag:
        description = get_description(input_object)
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": f"input_object:'{input_object}'\n description:'{description}'\n Update if necessary."},
        ]
    else:
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": "iron_ore"},
            {"role": "assistant", "content": "地表や洞窟で採掘でき\nかまどで精錬すると鉄のインゴットが得られる"},
            {"role": "user", "content": input_object},
        ]
    
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages
    )

    return response.choices[0].message.content

def generate_description(input_object: str) -> str:
    """ オブジェクトの説明を取得・生成し、DBに保存 """
    description = get_description(input_object)

    # 最終更新日時が1日以上前の場合、再取得
    if description == "Not found":
        description = get_chat_response(input_object, False)
        insert_object(input_object, description)
    else:
        last_updated = float(get_last_updated(input_object))
        if time.time() - last_updated >= 86400:
            description = get_chat_response(input_object, True)
            insert_object(input_object, description)

    return description
