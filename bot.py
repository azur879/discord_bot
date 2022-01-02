
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
	for x in range(3, max_row_range):
		cell_coord = col_letter+ str(x)
		if sheet.cell(cell_coord).value =="":
			return cell_coord, col_letter2+str(x)
	print('reached end of for loop')
		
#get discord token
with open("api_file.bin", encoding="utf-8") as binary_file:
	discordKey = binary_file.read()


#authorize to google
gc = pygsheets.authorize(service_file='serviceAccKey.json')
sh = gc.open('ss_losers')
wks = sh[0]

#f = next_available_row(wks, 1, 100)
#print(f)


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
		print('wrong 123')
	col_counter = 1
	userID_name = ctx.message.author.name
	userID = ctx.message.author.id
	first_row = wks.get_row(1, include_tailing_empty=False)
	print('user id is: ', userID)

	if str(userID) in first_row:
		# look for loser's column
		for item in first_row:
			if item == str(userID):
				break
			else:
				col_counter += 1


		# copy entry counter
		entries_string = wks.cell((2, col_counter)).value
		# cast number to int
		entries_int = int(entries_string.split()[1])

		# sample now's time
		now = datetime.today()

		if entries_int > 0:
			# get prev. weigh in val.
			prev_val = float(wks.cell((entries_int + 3, col_counter)).value)
			# get prev. time
			prev_time_str = wks.cell((entries_int + 3, col_counter + 1)).value
			prev_time_datetime = datetime.strptime(prev_time_str, '%Y.%m.%d %H:%M')
			print('prev_time_datetime is: ', prev_time_datetime)

			# calc. weight difference
			val_diff = arg - prev_val
			print("val_diff is: %.1f" % val_diff)

			# calc. time difference
			time_diff = (now - prev_time_datetime).days
			print('time_diff in days is: ', time_diff)

		# announce in disc channel
			await ctx.send(f'{userID_name}\'s weight today: {arg}kg\n{val_diff}kg in {time_diff} days.')

		else:
			print('doe something eslse')
			await ctx.send(f'{userID_name}\'s weight today: {arg}kg\n1st entry, gambate!')

		# today string val for insertion in sheet
		now_string = "%a.%a.%a %a:%a" % (now.year, now.month, now.day, now.hour, now.minute)

		# define range for new entry
		new_entry_range = pygsheets.datarange.DataRange(start=(entries_int + 3 + 1, col_counter),
														end=(entries_int + 3 + 1, col_counter + 1), worksheet=wks)
		print('new_entry_range is: ', new_entry_range)
		# update range with new entry
		new_entry_range.update_values(values=[[str(arg), now_string]])  # row matrix. [[1, 2, 3]]=col matrix

		# update entry counter cell
		wks.update_value((2, col_counter), 'entries ' + str(entries_int + 1))
			
		
	
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
async def new_loser(ctx, usr: discord.Member=None):
	"""Adds new loser: !new_loser id"""
	if usr==None:
		await ctx.send('bruh, no argument')
		return
	userid_sender = ctx.message.author.id
	print('user is:', usr)
	if userid_sender == 328851738142703627:
		print('MATCH')
		try:
			#usr = await bot.fetch_user(user)
			arg = str(usr.id)
			#print('USR IS: ',str(usr))
			first_row = wks.get_row(1,include_tailing_empty=False)
			if arg in first_row:				
				await ctx.send(f'{usr} is already a loser')
			else:
				#start column of range
				col_nr = len(first_row) + 1
				# define range of header for new loser
				newHeader_range = pygsheets.datarange.DataRange(start=(1, col_nr), end=(3, col_nr+1), worksheet=wks)
				#update range with values
				newHeader_range.update_values(values=[[str(usr.id), str(usr)], ['entries 0', ''],
											 ['Weight [kg]', 'Datetime']])  # row matrix. [[1, 2, 3]]=col matrix

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
