from PIL import Image
import numpy as np
import os

png_name = str(input())
folder_path = "{}".format(png_name)
if not os.path.exists(folder_path):
    os.makedirs(folder_path)
image = Image.open("{}.png".format(png_name))
class allblock:
    blocks = [
        [247,233,163,"sand"],
        [255,255,255,"white_wool"],
        [112,112,112,"stone"],
        [143, 119, 72,"planks"],
        [216, 127, 51,"orange_wool"],
        [178, 76, 216,"magenta_wool"],
        [102, 153, 216,"light_blue_wool"],
        [229, 229, 51,"yellow_wool"],
        [127, 204, 25,"lime_wool"],
        [242, 127, 165,"pink_wool"],
        [76, 76, 76,"gray_wool"],
        [153, 153, 153,"light_gray_wool"],
        [76, 127, 153,"cyan_wool"],
        [127, 63, 178,"purple_wool"],
        [51, 76, 178,"blue_wool"],
        [102, 76, 51,"brown_wool"],
        [102, 127, 51,"green_wool"],
        [153, 51, 51,"red_wool"],
        [25, 25, 25,"black_wool"],
        [250, 238, 77,"gold_block"],
        [92, 219, 213,"diamond_block"],
        [74, 128, 255,"lapis_block"],
        [0, 217, 58,"emerald_block"],
        [100, 100, 100,"deepslate"]
    ]


def printblock(image_array,x,y):
    image_block_index = [[0 for j in range(len(image_array[0]))] for i in range(len(image_array))]
    for i in range(len(image_array)):
        for j in range(len(image_array[0])):
            min_sum = 65535
            min_index = 0
            for k in range(23):
                sum = 0
                sum = sum + np.power(np.abs(image_array[i][j][0] - allblock.blocks[k][0]),2)
                sum = sum + np.power(np.abs(image_array[i][j][1] - allblock.blocks[k][1]),2)
                sum = sum + np.power(np.abs(image_array[i][j][2] - allblock.blocks[k][2]),2)
                if(sum < min_sum):
                    min_sum = sum
                    min_index = k
            image_block_index[i][j] = min_index
    with open("{0}/x{1}y{2}.mcfunction".format(png_name,x,y),"w") as file:
        for i in range(len(image_array)):
            for j in range(len(image_array[0])):
                file.write("setblock ~{1}~~{0} {2} \n".format(i,j,allblock.blocks[image_block_index[i][j]][3]))   

x = 0
y = 0

for y in range(1+int(image.height/64)):

    if(image.height - 64 * y < 64):
        y1 = image.height
    else:
        y1 = 64 + 64 * y
    
    for x in range(1+int(image.width/64)):
        if(image.width - 64 * x < 64):
            x1 = image.width
        else:
            x1 = 64 + 64 * x
        

        crop_box = (x*64,y*64,x1,y1)
        cropped_image = image.crop(crop_box)
        image_array = np.array(cropped_image)
        printblock(image_array,x,y)



k = 0
with open("print.mcfunction".format(png_name),"w") as file:
    file.write("scoreboard objectives add print dummy\n") 
    file.write("scoreboard objectives add printcool dummy\n") 
    file.write("scoreboard players set @p[tag=!printing] printcool 0\n") 
    file.write("scoreboard players set @p[tag=!printing] print 0\n") 
    file.write("tag @p[tag=!printing] add printing\n") 
    for y in range(1+int(image.height/64)):
        k = k + 4
        for x in range(1+int(image.width/64)):
            k = k + 1
            file.write("execute @p[scores={{print={3}}},tag=printing] ~~~ function {0}/x{1}y{2}\n".format(png_name,x,y,k)) 
            if(x != int(image.width/64)):
                file.write("tp @p[scores={{print={}}},tag=printing] ~64~~\n".format(k))
        file.write("tp @p[scores={{print={1}}},tag=printing] ~-{0}~~64\n".format((x)*64,k)) 
    k = k + 1
    file.write("tag @p[scores={{print={}..}},tag=printing] remove printing\n".format(k)) 