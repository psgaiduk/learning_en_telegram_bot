from pytest import mark

from functions import decode_telegram_id, encode_telegram_id


class TestDecodingEncodingTelegramIdFunction:
    """Tests for create_keyboard_for_en_levels function."""

    @mark.parametrize('decode_id, encode_id', [(12345, 'rfu'), (12, 'l'), (1236724612874921, 'hstfhffmnta'), (-5, None), ('5', None)])
    @mark.asyncio
    async def test_encode_telegram_id(self, decode_id, encode_id):

        assert await encode_telegram_id(number=decode_id) == encode_id

    @mark.parametrize('decode_id, encode_id', [('rfu', 12345), ('l', 12), ('hstfhffmnta', 1236724612874921), (-5, None), ('5', None)])
    @mark.asyncio
    async def test_decode_telegram_id(self, encode_id, decode_id):
        assert await decode_telegram_id(encoded_str=decode_id) == encode_id
