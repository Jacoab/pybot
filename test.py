from capture import ScreeCap
from PIL import Image

bot = ScreeCap("Test", 1)
print(bot.run())
print(bot.screen_grabs)