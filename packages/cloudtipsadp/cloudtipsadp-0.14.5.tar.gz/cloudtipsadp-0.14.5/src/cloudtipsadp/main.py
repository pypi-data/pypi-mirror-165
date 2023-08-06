from cloudtipsadp.accumulations.services import (
    accum_payout_receiver, accum_summary)
from cloudtipsadp.cards.services import (
    card_auth, card_default, card_delete, card_get, card_add, card_3ds,
    token_connect, token_refresh, headers_get)
from cloudtipsadp.payouts.services import payout
from cloudtipsadp.places.services import (
    place_confirm, place_list, place_send)
from cloudtipsadp.receivers.services import (
    photo_load, receiver_create, receiver_detach_agent, receiver_get,
    receiver_pages)


class Cloudtipsadp:
    __link = None

    def __init__(self):
        self.accums_summary = accum_summary
        self.accums_payout_receiver = accum_payout_receiver
        self.cards_3ds = card_3ds
        self.cards_add = card_add
        self.cards_auth = card_auth
        self.cards_delete = card_delete
        self.cards_default = card_default
        self.cards_get = card_get
        self.get_token = token_connect
        self.refresh_token = token_refresh
        self.get_headers = headers_get
        self.payouts = payout
        self.places_confirm = place_confirm
        self.places_get = place_list
        self.places_send_sms = place_send
        self.receivers_create = receiver_create
        self.receivers_get = receiver_get
        self.receivers_detach_agent = receiver_detach_agent
        self.receivers_pages = receiver_pages
        self.receivers_photo = photo_load


if __name__ == '__main__':
    cta = Cloudtipsadp()
