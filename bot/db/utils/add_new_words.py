from loguru import logger
from random import shuffle

from db.core import Session
from db.models import Words
from bot.bot import translate_text


def add_new_text_to_db(words_en: str, level: int) -> None:
    logger.info('start add new words')

    words_ru = translate_text(text_on_en=words_en, language='RU').split(', ')
    words_es = translate_text(text_on_en=words_en, language='ES').split(', ')
    words_fr = translate_text(text_on_en=words_en, language='FR').split(', ')
    words_ge = translate_text(text_on_en=words_en, language='DE').split(', ')

    for index_word, word in enumerate(words_en.split(',')):

        with Session() as session:
            new_text = Words(
                level=level,
                words_en=word.strip(),
                words_ru=words_ru[index_word].strip(),
                words_ge=words_ge[index_word].strip(),
                words_es=words_es[index_word].strip(),
                words_fr=words_fr[index_word].strip(),
            )
            session.add(new_text)
            session.commit()
            session.refresh(new_text)


if __name__ == '__main__':
    words = """
    beach, forest, river, mountain, valley, city, village, country, desert, island, bridge, road, street, avenue, school, hospital, church, supermarket, restaurant, hotel, airport, station, bus, bicycle, taxi, plane, train, boat, car, motorcycle, morning, afternoon, evening, night, spring, summer, autumn, winter, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, today, tomorrow, yesterday, week, month, year, season, birthday, holiday, party, meeting, concert, movie, theater, museum, park, zoo, swimming pool, gym, library, office, factory, bank, post office, bakery, butcher, pharmacy, dentist, doctor, nurse, teacher, policeman, firefighter, engineer, pilot, driver, cook, waiter, farmer, painter, musician, actor, journalist, scientist, photographer, hairdresser, cashier, clerk, manager, secretary, cleaner, postman, lawyer, mechanic, receptionist, salesman, baker, family, father, mother, son, daughter, brother, sister, grandfather, grandmother, uncle, aunt, cousin, nephew, niece, husband, wife, friend, neighbor, colleague, boss, employee, partner, guest, host, customer, passenger, player, viewer, listener, reader, author, artist, speaker, winner, loser, beginner, expert, leader, follower, owner, guest, teacher, student, baby, child, teenager, adult, elderly, man, woman, boy, girl, human, animal, bird, fish, insect, plant, tree, flower, grass, fruit, vegetable, meat, fish, bread, milk, cheese, butter, sugar, salt, pepper, coffee, tea, juice, water, wine, beer, egg, rice, pasta, pizza, soup, salad, sandwich, breakfast, lunch, dinner, food, drink, plate, cup, glass, fork, knife, spoon, bottle, can, bag, box, basket, cart, trolley, chair, table, bed, sofa, cabinet, wardrobe, sink, shower, bathtub, toilet, mirror, lamp, window, door, floor, wall, ceiling, roof, stairs, elevator, chimney, balcony, garden, yard, garage, fence, gate, key, pen, pencil, eraser, paper, notebook, book, newspaper, magazine, letter, envelope, stamp, card, photo, picture, painting, map, flag, clock, watch, phone, radio, television, computer, camera, fridge, oven, stove, microwave, dishwasher, washing machine, dryer, vacuum cleaner, broom, mop, bucket, dustbin, hammer, screwdriver, nail, screw, rope, tape, glue, scissors, needle, thread, button, zip, pocket, sleeve, collar, hat, cap, helmet, scarf, glove, coat, jacket, sweater, shirt, blouse, dress, skirt, trousers, jeans, shorts, sock, shoe, boot, sandal, glasses, ring, bracelet, necklace, earring, lipstick, perfume, soap, shampoo, toothpaste, towel, sheet, blanket, pillow, curtain, carpet, wallpaper, paint, brush, ruler, calculator, stapler, clip, pin, sticker, stamp, coin, bill, wallet, purse, suitcase, backpack, umbrella, hat, helmet, mask, glove, ticket, card, letter, book, newspaper, magazine, picture, music, movie, game, toy, gift, flower, cake, candle
    """
    a = words.split(', ')
    shuffle(a)
    add_new_text_to_db(words_en=', '.join(a), level=0)
