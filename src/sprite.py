from emo import AmadeusEmo
from dotenv import load_dotenv
import os
from PIL import Image
import glob
import random

load_dotenv()

class AmadeusSprite:

    def __init__(self):
        """
        class to process the emotions and produce the sprite
        """
        self.emo = AmadeusEmo()
        self.base_path = os.path.dirname(os.path.abspath(__file__))[:-4]
        self.data_path = os.path.join(self.base_path, os.getenv("DATA_PATH"))
        self.save_path = "asset/sprite.gif"

        # initialize class of sprites
        self.DEF = {"D":"D_40000", "E":"E_40000", "F":"F_00000"}
        self.D_dat = ["a","b","c","1","2","3","4","5","6","7","8",""]
        self.E_dat = ["1","2","3","4","5","6","7","0"]
        self.size = {"Large":"L","Medium":"M","Small":"S"}

    def __call__(self, emotion, distance="Medium", duration=200):
        return self.make_sprite(emotion, distance)
    
    def make_sprite(self, emotion, distance="Medium", duration=200):
        sprite_imgs = self._get_sprite(emotion, distance)

        single_sprite_duration = 150 # this is a hyperparam
        duration += single_sprite_duration # add one more sprite
        multiplier = max(1, duration // (single_sprite_duration * len(sprite_imgs)))
        sprite_imgs *= multiplier
        sprite_imgs.append(sprite_imgs[0])
        # random.shuffle(sprite_imgs)
        
        sprite_imgs[0].save(
                self.save_path, 
                save_all=True, 
                append_images=sprite_imgs[1:], 
                optimize=False, 
                duration=single_sprite_duration, 
                # loop=0
            )

    def _get_sprite_class(self, emotion, distance="Medium"):
        assert emotion in self.emo.emotions, f"Emotion {emotion} not recognized"

        index = self.emo.emotions.index(emotion)
        pref = "CRS_J" + self.size[distance]
        if index == 19:
            return pref + self.DEF['F'] + self.E_dat[7]
        elif index >= 12:
            return pref + self.DEF['E'] + self.E_dat[index-12]
        else:
            return pref + self.DEF['D'] + self.D_dat[index]
    
    def _get_sprite(self, emotion, distance="Medium"):
        """
        get sprite
        """

        sprite_class = self._get_sprite_class(emotion, distance)
        sprite_group_path = os.path.join(self.data_path, f"{sprite_class}*.png")
        # get related sprites
        sprites = glob.glob(sprite_group_path)

        # create sprite images
        sprite_imgs = []
        for sprite in sprites:
            img = Image.open(sprite)
            new_width  = 300
            new_height = new_width * img.height // img.width
            img = img.resize((new_width, new_height), Image.LANCZOS)
            new_image = Image.new("RGBA", img.size, (255,255,255))
            new_image.paste(img, (0, 0), img)
            new_image.convert('RGB')

            sprite_imgs.append(new_image)
    
        return sprite_imgs

