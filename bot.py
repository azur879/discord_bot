#new line
#two line
#three line 
import discord
import pygsheets
from discord.ext import commands
from datetime import datetime
import io

def num_to_col_letter(num):
	letters=''
	while num:
		mod = (num-1)%26
		letters +=chr(mod + 65)
		num = (num - 1) // 26
	return ''.join(reversed(letters))

def next_available_row(sheet,col_to_sample, max_row_range):
	col_letter = num_to_col_letter(col_to_sample)
	col_letter2 = num_to_col_letter(col_to_sample+1)
	for x in range(1, max_row_range):
		cell_coord = col_letter+ str(x)
		if sheet.cell(cell_coord).value =="":
			return cell_coord, col_letter2+str(x)
	print('reached end of for loop')
		
#get discord token
with open("api_file.bin", encoding="utf-8") as binary_file:
	discordKey = binary_file.read()



gc = pygsheets.authorize(service_file='serviceAccKey.json')
print(gc)
sh = gc.open('ss_losers')
wks = sh[0]

f = next_available_row(wks, 1, 100)
print(f)


#wks.update_value('A2', "derp")
first_row = wks.get_row(1, include_tailing_empty=False)
for item in first_row:
	print(item)

with open("sheet_url.bin", encoding="utf-8") as binary_file:
	sheet_url = binary_file.read()

description = f'sheet url: {sheet_url}\nRepository: github.com/azur879/discord_bot'
bot = commands.Bot(command_prefix='!', description=description)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.command()
async def hello(ctx):
    """Says world"""
    await ctx.send("world")

@bot.command()
async def W(ctx,*, arg: str = None):
	"""Adds your weight to the sheet. !W 80.5"""
	#print('TYPE ', type(arg))
	if arg == None:
		await ctx.send('bruh, no argument')
		return
	try: 
		float(arg)
	except:
		await ctx.send(f'`{arg}` can\'t be converted to a float')
		return
	counter=1
	userID_name = ctx.message.author.name
	userID = ctx.message.author.id
	first_row = wks.get_row(1, include_tailing_empty=False)
	print('user id is: ',userID)

	if str(userID) in first_row:
		await ctx.send(f'Sampled {userID_name}\'s weight of {arg}kg')
		for item in first_row:
			if item == str(userID):
				break
			else:
				counter+=1
		#letter_col = num_to_col_letter(counter)
		#find first emptry row of above col
		coord, coord2 = next_available_row(wks, counter, 1000)
		


		print('counter is ', counter, ' coord is: ', coord)
		valuess1=[]
		valuess2=[]
		valuess1.append(arg)
		print('value1 is ', valuess1)
		s = datetime.today()
		asd = "%a.%a.%a %a:%a" %(s.year, s.month, s.day, s.hour, s.minute)
		valuess2.append(asd)
		print('value2 is ', valuess2)
		#print('letter to col: ', letter_col,'. ', letter_col+
		#wks.append_table(values=valuess, start=letter_col+'3', end=None, dimension='ROWS', overwrite=True)
		wks.update_value(coord, str(arg))
		wks.update_value(coord2, str(asd))
		#await ctx.send(f'{userID_name}\'s weight today: {arg}kg')
		valuess1=[]
		valuess2=[]
			
		
	
	else:
		await ctx.send('you\'re not a loser (yet) :smug:')
	#await ctx.send(f'{userID_name}\'s wight today {arg}kg')
	print(arg)
	#wks.update_value('A2', arg)
	values=[]
	#values.append(datetime.now)
	#values.append(arg)
	#s = datetime.today()
	#asd = "%a.%a.%a %a:%a" %(s.year, s.month, s.day, s.hour, s.minute)
	#values.append(asd)
	#wks.append_table(values, start='A3', end=None, dimension='ROWS', overwrite=True)
	#values=[]
	

@bot.command()
async def pound(ctx,*, left : str=None):
	"""converts arg=pounds to kg. !pound 70"""
	if left == None:
		await ctx.send('bruh, no argument')
		return
	try: 
		float(left)
	except: 
		await ctx.send(f'`{left}` can\'t be converted to a float')
		return
	await ctx.send(f'{left} pounds is {float(left)*0.454} kg')

@bot.command()
async def info(ctx, user: discord.Member=None):
	"""Gets usernames unique discord id. !info @Azur"""
	if user == None:
		await ctx.send('bruh, no argument')
		return
	await ctx.send(f'{user}\'s id is: `{user.id}`')

@bot.command()
async def new_loser(ctx,*, arg:str=None):
	"""Adds new loser: !new_loser id"""
	if arg==None:
		await ctx.send('no')
		return
	userID = ctx.message.author.id
	if userID == 328851738142703627:
		print('MATCH')
		try:
			usr = await bot.fetch_user(arg)
			#print('USR IS: ',str(usr))
			first_row = wks.get_row(1,include_tailing_empty=False)
			if arg in first_row:				
				await ctx.send(f'{usr} is already a loser')
			else:
				values=[]
				values2=[]
				values.append(arg)
				values2.append(str(usr))
				#print(values)
				col_nr = len(first_row)+1
				letter_col = num_to_col_letter(col_nr)
				letter_col2 = num_to_col_letter(col_nr+1)
				wks.append_table(values, start=letter_col+'1', end=None, dimension='COLUMNS', overwrite=True)
				wks.append_table(values2, start=letter_col2+'1', end=None, dimension='COLUMNS', overwrite=True)
				await ctx.send(f'{usr} added.')
			
		except:
			await ctx.send('something went wrong')
	else:
		print(userID, ' tried adding')
		await ctx.send('no')

@info.error
async def info_error(ctx,error):
	if isinstance(error,commands.BadArgument):
		await ctx.send('error, try @<user>')



bot.run(discordKey)
