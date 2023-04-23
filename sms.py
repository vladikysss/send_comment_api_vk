import re
import vk_api
import time

token_api_vk = ""


def get_urls_photo_comments():
    global url
    """Фукнция для сбора всех необходимых ссылок на фотки"""
    url = []
    while 1:
        url_photo = input("Введите ссылку на фотографию, где необходимо оставить комментарий:")
        print('Для того, чтоб остановить ввод ссылок введите "стоп"')
        if url_photo.lower() == "стоп":
            break
        elif "https://vk.com/" in url_photo:
            url.append(url_photo)
            print("##############################")
            print(f'Количество введенных ссылок: {len(url)}\nДля продолжения пришлите следующую ссылку')
            print("Ссылки на которые будет оставлен комментарий:")
            for url_ph in url:
                print(url_ph)
            print("##############################")
    return url


def get_photo_and_owner_id(photo_url):
    """Функция для получения айди фотки и айди группы"""
    if "https://vk.com/club" in photo_url:
        match_owner_id = re.search(r"(?<=photo-)\d+", photo_url)
        match_photo_id = re.search(r"photo-\d+_(\d+)", photo_url)
        if match_photo_id and match_owner_id:
            owner_id = "-" + match_owner_id.group()
            photo_id = match_photo_id.group(1)
            print(owner_id)
            print(photo_id)
    else:
        match_owner_id = re.search(r"photo(.+)_", photo_url)
        match_photo_id = re.search(r"\d+$", photo_url)
        if match_photo_id and match_owner_id:
            owner_id = match_owner_id.group(1)
            photo_id = match_photo_id.group()
            print(owner_id, photo_id)

    return owner_id, photo_id


def connect_vk_api(token):
    """Подключение к апи Вконтакте"""
    # авторизация пользователя
    vk_session = vk_api.VkApi(token=token)

    return vk_session.get_api()


def check_permissions_for_comments(vk, owner_id, photo_id):
    # получение информации о фотографии
    photo_info = vk.photos.getById(photos=f'{owner_id}_{photo_id}', extended=1)

    return photo_info


def get_count_comment_in_post(vk, owner_id, photo_id):
    # получение информации о фотографии
    photo_info = vk.photos.getById(photos=f'{owner_id}_{photo_id}', extended=1)

    # Получиние информации о кол-ве комментариев
    count_comment = photo_info[0]['comments']['count']

    return count_comment


def send_message(vk, owner_id, photo_id):
    """Отправка комментария для выбранного поста"""
    send_sms = vk.photos.createComment(owner_id=owner_id, photo_id=photo_id, message="Бронь")
    print(send_sms)


def send_message_comment_in_post():
    vk = connect_vk_api(token_api_vk)
    for photo_url in url:
        owner_id, photo_id = get_photo_and_owner_id(photo_url)
        for _ in range(60):
            photo_info = check_permissions_for_comments(vk, owner_id, photo_id)
            # Проверка доступности комментариев к фотографии
            if photo_info[0]['can_comment'] == 1:
                print('Комментарии к фотографии открыты')
                count_comment = get_count_comment_in_post(vk, owner_id, photo_id)
                if count_comment < 1:
                    send_message(vk, owner_id, photo_id)
                    break
                else:
                    print("К сожалению кто-то оказался быстрее нас (")
                    break

            else:
                print('Комментарии к фотографии закрыты')
                time.sleep(1)


if __name__ == "__main__":
    get_urls_photo_comments()
    send_message_comment_in_post()