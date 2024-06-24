ADDFRIEND_MESSAGE = {
    "added": {"message": "你已经与对方是好友了，快去和他聊天吧！", "button": "聊天"},
    "notAdded": {"message": "你已经添加过对方了，请等待对方同意！", "button": "添加"},
}
a = {
    "status": True,
    "message": None,
    "is_friend": True,
    "button": None,
}
a.update(ADDFRIEND_MESSAGE["added"])
print(a)
