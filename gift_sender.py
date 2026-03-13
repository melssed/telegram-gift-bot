from telethon import TelegramClient, errors
from telethon.tl.functions.payments import GetPaymentFormRequest, SendStarsFormRequest
from telethon.tl.types import InputInvoiceStarGift

API_ID = 32387059
API_HASH = "dfe69810dd9d13f88566c89f59f2eb51"

client = TelegramClient("gift_session", API_ID, API_HASH)


async def send_gift(gift_id, username):

    await client.start()

    try:

        if username.lstrip("@").isdigit():
            user = await client.get_entity(int(username.lstrip("@")))
        else:
            user = await client.get_entity(username)

        input_peer = await client.get_input_entity(user)

        invoice = InputInvoiceStarGift(
            peer=input_peer,
            gift_id=int(gift_id),
            message=None
        )

        form = await client(GetPaymentFormRequest(invoice=invoice))

        await client(SendStarsFormRequest(
            form_id=form.form_id,
            invoice=invoice
        ))

        return True

    except errors.RPCError as e:
        print("Telegram error:", e)
        return False

    except Exception as e:
        print("Error:", e)
        return False