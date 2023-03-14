import discord
import os
import time
import requests
import json
from discord.ext import tasks
from keep_alive import keep_alive
import numpy as np
import random
from bs4 import BeautifulSoup
import requests

client = discord.Client()
bad_words = ["plm","pula"," pl "]
cat = ["cat","pisica","mața"]

wall = "⬜"
innerWall = "⬛"
energy = "🍎"
snakeHead = "😍"
snakeBody = "🟨"
snakeLoose = "😵"

embedHouse=discord.Embed(title="titlu", description = "asd", color=0xff0000)
embedHouse.add_field(name="asd", value="⁣          🎈🎈    ☁️                                                                                     \n☁️           🎈🎈🎈  ☁️                                                                                \n☁️     🎈🎈🎈🎈                                                                              \n☁️     🎈🎈🎈🎈    ☁️                                                                           \n☁️         ⁣🎈🎈🎈                                                                                   \n☁️             \\|/                                                                       \n☁️     ☁️        🏠   ☁️    ☁️                                                                    \n☁️                                                                                               \n☁️              🌳🌹🏫🌳🏢🏢_🏢🏢🌳🌳", inline=True)
embedHouse.set_author(name="Geo")



def getGameGrid():
    str = ""

    for item in snakeMatrix:
        # print(item)
        for i in item:
            if(i == 0):
                str += wall
            elif i == 1:
                str += innerWall
            elif i == 2:
                str += snakeHead
            elif i == 3:
                str += snakeBody
            elif i == 4:
                str += energy
            else:
                str += snakeLoose
        str += "\n"
        
    return str

def generateRandomEnergy():
    snakeMatrix[random.randint(1,10)][random.randint(1,10)] = 4

def checkEnergy(i, j):
    # print("i : {}".format(i))
    # print("j : {}".format(j))
    # print("Pos Val : {}".format(snakeMatrix[i][j]))
    return snakeMatrix[i][j] == 4

def handleEnergy(i, j):
    global points
    # print(checkEnergy(i, j))
    if(checkEnergy(i, j)):
        generateRandomEnergy()
        points += 10

def updateSnakePosition(i, j, k, l):
    snakeMatrix[i][j] = 2
    snakeMatrix[k][l] = 1

def isOuterBoundary(i, j):
    global isOut
    if(i == 0 or j == 0 or i == 11 or j == 11):
        # print("Out")
        snakeHeadPos = np.argwhere(snakeMatrix == 2)[0]
        snakeMatrix[snakeHeadPos[0]][snakeHeadPos[1]] = 5
        isOut = True
        print("isOut : {}".format(isOut))
        return True
    return False

def moveUp():
    # print("Up")
    snakeHeadPos = np.argwhere(snakeMatrix == 2)[0]
    # print(snakeHeadPos)
    # print(snakeMatrix[snakeHeadPos[0]][snakeHeadPos[1]])
    if(not isOuterBoundary(snakeHeadPos[0]-1, snakeHeadPos[1])):
        handleEnergy(snakeHeadPos[0]-1, snakeHeadPos[1])
        updateSnakePosition(snakeHeadPos[0]-1, snakeHeadPos[1], snakeHeadPos[0], snakeHeadPos[1])
    # snakeMatrix[snakeHeadPos[0]-1][snakeHeadPos[1]] = 2
    # snakeMatrix[snakeHeadPos[0]][snakeHeadPos[1]] = 1


def moveLeft():
    # print("Left")
    snakeHeadPos = np.argwhere(snakeMatrix == 2)[0]
    if(not isOuterBoundary(snakeHeadPos[0], snakeHeadPos[1]-1)):
        handleEnergy(snakeHeadPos[0], snakeHeadPos[1]-1)
        updateSnakePosition(snakeHeadPos[0], snakeHeadPos[1]-1, snakeHeadPos[0], snakeHeadPos[1])
    # snakeMatrix[snakeHeadPos[0]][snakeHeadPos[1]-1] = 2
    # snakeMatrix[snakeHeadPos[0]][snakeHeadPos[1]] = 1


def moveRight():
    # print("Right")
    snakeHeadPos = np.argwhere(snakeMatrix == 2)[0]
    if(not isOuterBoundary(snakeHeadPos[0], snakeHeadPos[1]+1)):
        handleEnergy(snakeHeadPos[0], snakeHeadPos[1]+1)
        updateSnakePosition(snakeHeadPos[0], snakeHeadPos[1] + 1, snakeHeadPos[0], snakeHeadPos[1])
    # snakeMatrix[snakeHeadPos[0]][snakeHeadPos[1]+1] = 2
    # snakeMatrix[snakeHeadPos[0]][snakeHeadPos[1]] = 1


def moveDown():
    # print("Down")
    snakeHeadPos = np.argwhere(snakeMatrix == 2)[0]
    if(not isOuterBoundary(snakeHeadPos[0]+1, snakeHeadPos[1])):
        handleEnergy(snakeHeadPos[0]+1, snakeHeadPos[1])
        updateSnakePosition(snakeHeadPos[0]+1, snakeHeadPos[1], snakeHeadPos[0], snakeHeadPos[1])
    # snakeMatrix[snakeHeadPos[0]+1][snakeHeadPos[1]] = 2
    # snakeMatrix[snakeHeadPos[0]][snakeHeadPos[1]] = 1

def reset():
    global snakeMatrix, isOut, points
    isOut = False
    # print("Reset")
    snakeMatrix = np.array([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ])
    points = 0
    generateRandomEnergy()

def getNormalEmbededData(title, description):
    return discord.Embed(title=title, description=description, color=discord.Color.green())

def getErrorEmbededData(title, description):
    return discord.Embed(title=title, description=description, color=discord.Color.red())

async def sendMessage(message):
    embedVar=getNormalEmbededData(title="Pick Apple Game", description="{}".format(getGameGrid()))
    embedVar.add_field(name="Your Score", value=points, inline=True)
    await message.channel.send(embed=embedVar)


def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)



@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    print('return')
    return
  
  print(message.content)

  if message.content.startswith('zt!ship @geo') or message.content.startswith('zt!ship @ana') or message.content.startswith('zt!ship geo') or message.content.startswith('zt!ship ana') :
    await message.channel.send('Cats calculation: ')
    await message.channel.send(file=discord.File('ship.png'))

  if message.content.startswith('^^whos the best ?'):
    print('got it :-j')
    await message.channel.send('Ana <3')
  
  if message.content.startswith('test'):
    print('got it :-j')
    await message.channel.send('ce testezi ma tu')

  if message.content.startswith('^^gimme inspiro'):
    quote = get_quote()
    await message.channel.send(quote)

  if message.content.startswith('t_hangman'):
    await message.channel.send('do you really wanna play this game? type y or n')

    time.sleep(5)
    print('asd')
    if message.content.startswith('n'):
      return False
    elif(message.content.startswith('y')):
      await message.channel.send(file=discord.file(''))
      await message.channel.send(file=discord.file(''))
      for i in range(10):
          await message.channel.send(file=discord.File('hangmanFrames/'+str(i+1)+'.jpg'))

  if message.content.startswith('^^pet Ana'):
    await message.channel.send('<3')
    await message.channel.send(file=discord.File('22.jpg'))
  if message.content.startswith('hangman'):
    await message.channel.send('yes')
    await message.channel.send(file=discord.File('4.jpg'))

  if(message.content.startswith('balloons')):  
    await message.channel.send(embed=embedHouse)
    await message.channel.send('cringe')
  
  

  if message.content.startswith('mananc'):
    await message.channel.send('mancare unde?')
  
  if message.content.startswith('plimba l pe qwerty'):
    await message.channel.send('t!tg')

  msg = message.content
  msg = msg.lower()

  if any(bw in msg for bw in bad_words):
    await message.channel.send('nu mai vb urat')
  
  if any(bw in msg for bw in cat):
    await message.channel.send('uh?')

  # print("Message Channel : {}".format(message.channel))
  # print(os.environ['CHANNEL_ID'])
  gameChannel = client.get_channel(int(os.environ['CHANNEL_ID']))
  # print("gameChannel Channel : {}".format(gameChannel))
  if(message.author == client.user):
        return
  if gameChannel == message.channel:
    if(message.content.startswith('play snake')):
        # print(message.channel)
        reset()
        embedVar = getNormalEmbededData(title="Welcome *{0.author}* to our Useless Game Channel ! Lets Play Game".format(message), description="⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜\n⬜⬛⬛⬛⬛⬛⬛⬛⬛⬛⬜\n⬜⬛⬛⬛⬛⬛⬛⬛🍎⬛⬜\n⬜⬛🟨🟨⬛⬛⬛⬛⬛⬛⬜\n⬜⬛⬛🟨🟨🟨🟨⬛⬛⬛⬜\n⬜⬛⬛⬛⬛⬛🟨🟨⬛⬛⬜\n⬜⬛⬛⬛⬛⬛⬛🟨🟨😵⬜\n⬜⬛⬛⬛⬛⬛⬛⬛⬛⬛⬜\n⬜⬛⬛⬛⬛⬛⬛⬛⬛⬛⬜\n⬜⬛⬛⬛⬛⬛⬛⬛⬛⬛⬜\n⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜\n\n` w ` -> Move Left\n` d ` -> Move Right\n` w ` -> Move Up\n` s ` -> Move Down\n` r ` -> Reset")
        await message.channel.send(embed=embedVar)
    elif(message.content.startswith('r')):
        print("Reset")
        reset()
        embedVar=getNormalEmbededData(title="Pick Apple Game", description="{}\nGame has been reset. You can start playing new game".format(getGameGrid()))
        embedVar.add_field(name="Your Score", value=points, inline=True)
        await message.channel.send(embed=embedVar)
    elif(isOut):
        embedVar=getErrorEmbededData(title="Game Over", description="Scored Point : {}".format(points))
        await message.channel.send(embed=embedVar)
    elif(message.content.startswith('w')):
        moveUp()
        await sendMessage(message)
    elif(message.content.startswith('a')):
        moveLeft()
        await sendMessage(message)
    elif(message.content.startswith('s')):
        moveDown()
        await sendMessage(message)
    elif(message.content.startswith('d')):
        moveRight()
        await sendMessage(message)
    else:
        embedVar = getErrorEmbededData(title="*Error*", description="Invalid Input Detected ! Please enter a valid input. \n ` w ` -> Move Left\n` d ` -> Move Right\n` w ` -> Move Up\n` s ` -> Move Down\n` r ` -> Reset")
        await message.channel.send(embed=embedVar)
  else:
    print("Wrong Channel")
        


keep_alive()
client.run(os.getenv('TOKEN'))

points = 0
isOut = False
snakeMatrix = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    ])
generateRandomEnergy()