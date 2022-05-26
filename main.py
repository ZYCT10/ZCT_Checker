import re, sqlite3, hashlib
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

def search_by_info(dbpath, data):
    cdb = sqlite3.connect(dbpath)
    is_email = re.fullmatch(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+', data)
    is_nickname = re.fullmatch(r"[a-zA-Z0-9_\-\.]+", data)
    is_ip = re.fullmatch(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", data)
    
    if not cdb:
        return []
    
    result = []

    if is_email:
        get_by_email = cdb.execute("SELECT * FROM `Auth` WHERE `email`=?", [get_info])

        for get_row in get_by_email:
            result.append(get_row)

    elif is_ip:
        get_by_ip = cdb.execute("SELECT * FROM `Auth` WHERE `ip`=?", [get_info])

        for get_row in get_by_ip:
            result.append(get_row)

    elif is_nickname:
        get_by_nickname = cdb.execute("SELECT * FROM `Auth` WHERE `username`=?", [get_info])
            
        for get_row in get_by_nickname:
            result.append(get_row)
    
    cdb.close()

    return result


def unhash(salt, password):
    open_base = open("dicts/globalbase.txt", "r")
    bd_str = [element.strip() for element in open_base.readlines()]
    open_base.close()

    for line in bd_str:
        n_str = hashlib.sha256(line.encode("utf-8", errors="ignore")).hexdigest()
        n_2_str = hashlib.sha256((n_str + salt).encode("utf-8")).hexdigest()

        if n_2_str == password:
            return line

    return None


if __name__ == "__main__":
    TOKEN = "123"
    vk_session = vk_api.VkApi(token=TOKEN)

    longpoll = VkLongPoll(vk_session)
    vk = vk_session.get_api()
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            get_msg = event.text.split(" ")

            if event.from_chat:
                if get_msg[0].lower() == "пробив" and len(get_msg) == 2:
                    get_info = get_msg[1].lower()

                    result_msg = ""

                    get_bomjcraft_all_info = search_by_info("db/bomjcraft.db", get_info)
                    get_needmine_all_info = search_by_info("db/needmine.db", get_info)
                    get_lattycraft_all_info = search_by_info("db/lattycraft.db", get_info)
                    get_watermine_all_info = search_by_info("db/watermine.db", get_info)
                    get_fawemc_all_info = search_by_info("db/fawemc.db", get_info)

                    if len(get_bomjcraft_all_info) \
                        or len(get_needmine_all_info) \
                        or len(get_lattycraft_all_info) \
                        or len(get_watermine_all_info) \
                        or len(get_fawemc_all_info):

                        if len(get_bomjcraft_all_info):
                            for info in get_bomjcraft_all_info:
                                result_msg += f"Nickname: {info[1]}\n"
                                result_msg += f"Password: {info[2]}\n"
                                result_msg += f"IP: {info[3]}\n"
                                result_msg += f"Base: BomjCraft\n"
                                result_msg += "\n"

                        if len(get_needmine_all_info):
                            for info in get_needmine_all_info:
                                result_msg += f"Nickname: {info[2]}\n"
                                result_msg += f"Password: {info[3]}\n"
                                result_msg += f"IP: {info[4]}\n"
                                result_msg += f"Base: NeedMine\n"
                                result_msg += "\n"

                        if len(get_lattycraft_all_info):
                            for info in get_lattycraft_all_info:
                                result_msg += f"Nickname: {info[1]}\n"
                                result_msg += f"Password: {info[2]}\n"
                                result_msg += f"IP: {info[3]}\n"
                                result_msg += f"Base: LattyCraft\n"
                                result_msg += "\n"

                        if len(get_watermine_all_info):
                            for info in get_watermine_all_info:
                                result_msg += f"Nickname: {info[0]}\n"
                                result_msg += f"Password: {info[1]}\n"
                                result_msg += f"IP: {info[4]}\n"
                                result_msg += f"Base: WaterMine\n"
                                result_msg += "\n"

                        if len(get_fawemc_all_info):
                            for info in get_fawemc_all_info:
                                result_msg += f"Nickname: {info[1]}\n"
                                result_msg += f"Password: {info[2]}\n"
                                result_msg += f"IP: {info[3]}\n"
                                result_msg += f"Base: FaweMC\n"
                                result_msg += "\n"

                    else:
                        result_msg = "[!] Not found! :(\n"
                    
                    vk.messages.send(
                        chat_id=event.chat_id,
                        message=result_msg,
                        random_id=0
                    )
                
                elif get_msg[0].lower() == "вскрыть" and len(get_msg) == 2:
                    get_info = get_msg[1]

                    if re.fullmatch(r"\$SHA\$\w+\$\w+", get_info):
                        (_, _, salt, password) = get_info.split("$")

                        get_password = unhash(salt, password)

                        if get_password:
                            result_msg = f"[#] Found: {get_password}"

                        else:
                            result_msg = "[!] Not found" 
                    
                    else:
                        result_msg = "[!] Example: $SHA$hello$abc1234567890"
 
                    vk.messages.send(
                        chat_id=event.chat_id,
                        message=result_msg,
                        random_id=0
                    )
