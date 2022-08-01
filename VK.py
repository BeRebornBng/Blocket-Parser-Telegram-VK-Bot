import requests
import vk_api
import configparser

config = configparser.ConfigParser()
config.read('Config.ini')

token = str(config['VK']['token'])
group_id = int(config['VK']['group_id'])
app_id = int(config['VK']['app_id'])
album_id = int(config['VK']['album_id'])
session = vk_api.VkApi(token=token, app_id=app_id, api_version='5.131', scope='offline,wall,messages,photos,groups')
image = ''


def AddImageToDirectory(index, link):
    img = requests.get(link)
    out = open(f"Image\\{index}.png", 'wb')
    out.write(img.content)
    out.close()
    AddImageToVkAlbum(index)


def AddImageToVkAlbum(index):
    global image
    vk = vk_api.VkUpload(session)
    result = (vk.photo(album_id=album_id, group_id=group_id, photos=f'Image\\{index}.png'))
    image += 'photo' + str(result[0]['owner_id']) + '_' + str(result[0]['id']) + ','
    print(image)


def SendPostToVk(message):
    global image
    session.method('wall.post', {'owner_id': -group_id, 'from_group': 1, 'message': message,
                                 'attachments': [image]})
    image = ''