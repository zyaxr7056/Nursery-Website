import logging
import razorpay
from decouple import config
# logging.basicConfig(level=logging.DEBUG)        # show requests
# logger = logging.getLogger("razorpay")          # razorpay logs

# client = razorpay.Client(auth=(os.environ.get('RAZORPAY_KEY_ID'),
#                                os.environ.get('RAZORPAY_KEY_SECRET')))
# # Try a minimal call

# print("→ [repr] Key:", repr(config('RAZORPAY_KEY_ID')))
# print("→ [repr] Secret:", repr(config('RAZORPAY_KEY_SECRET')))

# try:
#     client.order.create({ "amount": 100, "currency": "INR", "receipt": "test" })
# except Exception as e:
#     print("RAW ERROR:", repr(e))                # this will include status code & body
print("→ [repr] Key:", repr(config('RAZORPAY_KEY_ID')))
print("→ [repr] Secret:", repr(config('RAZORPAY_KEY_SECRET')))