"""
A cricket related python program that uses APIs to performs functions
related to cricket (like live score of matches, upcoming schedules,
ICC rankings, ICC standings in current tournaments and Latest News etc.)
"""

import requests
import sys
import pyfiglet
import textwrap3
import fontstyle
from tabulate import tabulate
from datetime import datetime

headers = {
    "X-RapidAPI-Key": "d57ba3d429msh115d998cb6ac452p12f5d4jsn9b88882cf596",
    "X-RapidAPI-Host": "cricbuzz-cricket.p.rapidapi.com"
}

teamIDs = {
		"australia" : 4,
		"india" : 2,
		"south africa" : 11,
		"england" : 9,
		"new zealand" : 13,
		"pakistan" : 3,
		"west indies" : 10,
		"srilanka" : 5,
		"bangladesh" : 6,
		"zimbabwe" : 12,
}

colors = {
		1: "green",
		2: "red",
		3: "blue",
		4: "yellow",
		5: "green",
		6: "red",
		7: "blue",
		8: "yellow",
}

wrapper = textwrap3.TextWrapper(width=100)

def getSchedule(team):

	url = f'https://cricbuzz-cricket.p.rapidapi.com/teams/v1/{teamIDs[team]}/schedule'

	response = requests.request("GET", url, headers=headers)
	teamData = response.json()
	dataList = []
	colorCounter = 1

	print(fontstyle.apply(f'UPCOMING FIXTURES OF {team.upper()} MENS CRICKET TEAM', 'bold/green/blink'))

	for _ in range(len(teamData["teamMatchesData"])):
		if list(teamData["teamMatchesData"][_].keys())[0] == "adDetail":
			continue

		for match in range(len(teamData["teamMatchesData"][_]["matchDetailsMap"]["match"])):
			x = []
			seriesName = fontstyle.apply(teamData["teamMatchesData"][_]["matchDetailsMap"]["match"][match]["matchInfo"]["seriesName"], f"bold/{colors[colorCounter]}")
			x.append(seriesName)
			x.append(teamData["teamMatchesData"][_]["matchDetailsMap"]["match"][match]["matchInfo"]["matchDesc"])
			team1 = teamData["teamMatchesData"][_]["matchDetailsMap"]["match"][match]["matchInfo"]["team1"]["teamName"]
			team2 = teamData["teamMatchesData"][_]["matchDetailsMap"]["match"][match]["matchInfo"]["team2"]["teamName"]
			x.append(f'{team1} VS {team2}')
			format = teamData["teamMatchesData"][_]["matchDetailsMap"]["match"][match]["matchInfo"]["matchFormat"]
			start = int(teamData["teamMatchesData"][_]["matchDetailsMap"]["match"][match]["matchInfo"]["startDate"])
			end = int(teamData["teamMatchesData"][_]["matchDetailsMap"]["match"][match]["matchInfo"]["endDate"])
			x.append(getDate(format, start, end))
			ground = teamData["teamMatchesData"][_]["matchDetailsMap"]["match"][match]["matchInfo"]["venueInfo"]["ground"]
			city = teamData["teamMatchesData"][_]["matchDetailsMap"]["match"][match]["matchInfo"]["venueInfo"]["city"]
			x.append(f"{ground}, {city}")

			dataList.append(x)

		colorCounter += 1

	head = ["Series Name", "Description", "Teams", "Date", "Venue"]
	print(tabulate(dataList, head, tablefmt="psql"))

	toExit()

def getResults(team):

	url = f'https://cricbuzz-cricket.p.rapidapi.com/teams/v1/{teamIDs[team]}/results'

	response = requests.request("GET", url, headers=headers)
	teamData = response.json()
	dataList = []
	colorCounter = 1

	print(fontstyle.apply(f'RECENT COMPLETED MATCHES OF {team.upper()} MENS CRICKET TEAM', 'bold/green'))

	for _ in range(len(teamData["teamMatchesData"])):
		if list(teamData["teamMatchesData"][_].keys())[0] == "adDetail":
			continue


		for match in range(len(teamData["teamMatchesData"][_]["matchDetailsMap"]["match"])):
			x = []
			seriesName = fontstyle.apply(teamData["teamMatchesData"][_]["matchDetailsMap"]["match"][match]["matchInfo"]["seriesName"], f"bold/{colors[colorCounter]}")
			x.append(seriesName)
			x.append(teamData["teamMatchesData"][_]["matchDetailsMap"]["match"][match]["matchInfo"]["matchDesc"])
			team1 = teamData["teamMatchesData"][_]["matchDetailsMap"]["match"][match]["matchInfo"]["team1"]["teamSName"]
			team2 = teamData["teamMatchesData"][_]["matchDetailsMap"]["match"][match]["matchInfo"]["team2"]["teamSName"]
			x.append(f'{team1} VS {team2}')
			state = teamData["teamMatchesData"][_]["matchDetailsMap"]["match"][match]["matchInfo"]["status"]

			if team.upper() in state.upper():
				status = fontstyle.apply(state, "bold/blink/green")
			elif "drawn".upper() in state.upper() or "no".upper() in state.upper():
				status = fontstyle.apply(state, "bold/blink/yellow")
			else:
				status = fontstyle.apply(state, "bold/blink/red")

			x.append(status)
			format = teamData["teamMatchesData"][_]["matchDetailsMap"]["match"][match]["matchInfo"]["matchFormat"]
			start = int(teamData["teamMatchesData"][_]["matchDetailsMap"]["match"][match]["matchInfo"]["startDate"])
			end = int(teamData["teamMatchesData"][_]["matchDetailsMap"]["match"][match]["matchInfo"]["endDate"])
			x.append(getDate(format, start, end))
			ground = teamData["teamMatchesData"][_]["matchDetailsMap"]["match"][match]["matchInfo"]["venueInfo"]["city"]
			x.append(f"{ground}")

			dataList.append(x)

		colorCounter += 1

	head = ["Series Name", "Description", "Teams","Result", "Date", "Venue"]
	print(tabulate(dataList, head, tablefmt="psql"))

	toExit()


def news():

	url = "https://cricbuzz-cricket.p.rapidapi.com/news/v1/index"

	response = requests.request("GET", url, headers=headers)
	newsData = response.json()

	print(fontstyle.apply("LATEST NEWS", 'bold/green'))

	counter = 0
	newsIDs = {}

	for _ in range(len(newsData["storyList"])):

		if list(newsData["storyList"][_].keys())[0] == "ad":
			continue

		counter += 1
		print(fontstyle.apply(f'{counter}.  {newsData["storyList"][_]["story"]["hline"]}', "italic/bold/blue"))
		newsIDs[counter] = newsData["storyList"][_]["story"]["id"]
		print()

	id = int(input(fontstyle.apply("\nEnter ID to get details: ", "red")))
	print()
	newsDetails(newsIDs, id)

def newsDetails(nIDs, x):
	thisID = nIDs.get(x)
	url = f"https://cricbuzz-cricket.p.rapidapi.com/news/v1/detail/{thisID}"
	response = requests.request("GET", url, headers=headers)
	details = response.json()
	print(fontstyle.apply(f'{details["headline"]}', "italic/bold/blue"))
	print()
	for _ in range(len(details["content"])):
		if list(details["content"][_])[0] == "ad":
			continue
		print(wrapper.fill(f'\t{details["content"][_]["content"]["contentValue"]}'))

	print()
	toExit()

def playerRankings():
	format = input("Enter Format (Test, ODI, t20): ").strip().lower()
	category = input("Enter Category (Batsmen, Bowlers, AllRounders): ").strip().lower().replace("-", "")
	gender = input("Men's or Women's: ").strip().lower().replace("'","")

	url = f"https://cricbuzz-cricket.p.rapidapi.com/stats/v1/rankings/{category}"

	if gender == "men" or gender == "mens":
		querystring = {"formatType":format}
	elif gender == "women" or gender == "womens":
		querystring = {"formatType":format,"isWomen":"1"}

	response = requests.request("GET", url, headers=headers, params=querystring)

	ranksData = response.json()

	rankingList = []

	print(fontstyle.apply(f"ICC {gender.upper()} PLAYERS RANKINGS ({format.upper()} - {category.upper()})", 'bold/green'))

	for _ in range(10):
		player = []

		for key in ["rank", "name", "country", "points"]:
			player.append(ranksData["rank"][_][key])

		rankingList.append(player)

	head = ["Rank", "Name", "Country", "Points"]

	print(tabulate(rankingList, head, tablefmt="psql"))

	toExit()

def teamRankings():
	format = input("Enter Format (Test, ODI, t20): ").strip().lower()
	gender = input("Men's or Women's: ").strip().lower().replace("'","")

	url = "https://cricbuzz-cricket.p.rapidapi.com/stats/v1/rankings/teams"

	if gender == "men" or gender == "mens":
		querystring = {"formatType":format}
	elif gender == "women" or gender == "womens":
		querystring = {"formatType":format, "isWomen":"1"}

	response = requests.request("GET", url, headers=headers, params=querystring)

	ranksData = response.json()

	rankingList = []

	print(fontstyle.apply(f"ICC {gender.upper()} TEAMS RANKINGS ({format.upper()})", 'bold/green'))

	for _ in range(10):
		player = []

		for key in ["rank", "name", "matches", "points", "rating"]:
			player.append(ranksData["rank"][_][key])

		rankingList.append(player)

	head = ["Rank", "Name", "Matches", "Points", "Rating"]

	print(tabulate(rankingList, head, tablefmt="psql"))

	toExit()

def getDate(format, start, end):
	if format == "TEST":
		return f'{datetime.fromtimestamp(start/1000).strftime("%B, %d %Y")} to {datetime.fromtimestamp(end/1000).strftime("%B, %d %Y")}'
	else:
		return datetime.fromtimestamp(start/1000).strftime('%A - %B, %d %Y')

def getStandings():

	url = "https://cricbuzz-cricket.p.rapidapi.com/stats/v1/iccstanding/team/matchtype/1"
	response = requests.request("GET", url, headers=headers)

	standingsData = response.json()
	pointsList = []

	print(fontstyle.apply(standingsData["seasonStandings"][0]["name"], "bold/green"))

	for _ in range(len(standingsData["values"])):
		team = []
		team.append(standingsData["values"][_]["value"][0])
		team.append(standingsData["values"][_]["value"][2])
		team.append(standingsData["values"][_]["value"][3])

		pointsList.append(team)

	head = ["Rank", "Name", "PCT",]

	print(tabulate(pointsList, head, tablefmt="psql"))
	print(wrapper.fill(text=f'{standingsData["subText"]}\n'))

	toExit()

def getLive(x):

	url = f"https://cricbuzz-cricket.p.rapidapi.com/matches/v1/{x}"

	response = requests.request("GET", url, headers=headers)

	liveData = response.json()
	liveMList = []

	print(fontstyle.apply(f"CURRENT {x.upper()} MATCHES", 'bold/green'))

	for k in range(len(liveData["typeMatches"])):

		if (len(liveData["typeMatches"])) == 0:
			print(fontstyle.apply("\n No Live Match Currently","bold/red"))
			return
		
		for _ in range(len(liveData["typeMatches"][k]["seriesMatches"])):

			if list(liveData["typeMatches"][k]["seriesMatches"][_].keys())[0] == "adDetail":
				continue

			for i in range(len(liveData["typeMatches"][k]["seriesMatches"][_]["seriesAdWrapper"]["matches"])):

				liveCurr = []

				name = fontstyle.apply(liveData["typeMatches"][k]["seriesMatches"][_]["seriesAdWrapper"]["matches"][i]["matchInfo"]["seriesName"], "bold/italic/blue")
				state = fontstyle.apply(liveData["typeMatches"][k]["seriesMatches"][_]["seriesAdWrapper"]["matches"][i]["matchInfo"]["state"], "bold/blink/red")

				desc = liveData["typeMatches"][k]["seriesMatches"][_]["seriesAdWrapper"]["matches"][i]["matchInfo"]["matchDesc"]
				format = liveData["typeMatches"][k]["seriesMatches"][_]["seriesAdWrapper"]["matches"][i]["matchInfo"]["matchFormat"]
				
				status = liveData["typeMatches"][k]["seriesMatches"][_]["seriesAdWrapper"]["matches"][i]["matchInfo"]["status"]
				team1 = fontstyle.apply(liveData["typeMatches"][k]["seriesMatches"][_]["seriesAdWrapper"]["matches"][i]["matchInfo"]["team1"]["teamSName"], "green")

				team2 = fontstyle.apply(liveData["typeMatches"][k]["seriesMatches"][_]["seriesAdWrapper"]["matches"][i]["matchInfo"]["team2"]["teamSName"], "yellow")
				city = liveData["typeMatches"][k]["seriesMatches"][_]["seriesAdWrapper"]["matches"][i]["matchInfo"]["venueInfo"]["city"]

				try:
					team1wickets = liveData["typeMatches"][k]["seriesMatches"][_]["seriesAdWrapper"]["matches"][i]["matchScore"]["team1Score"]["inngs1"]["wickets"]
				except:
					team1wickets = 0

				try:
					team1runs = liveData["typeMatches"][k]["seriesMatches"][_]["seriesAdWrapper"]["matches"][i]["matchScore"]["team1Score"]["inngs1"]["runs"]
					team1overs = liveData["typeMatches"][k]["seriesMatches"][_]["seriesAdWrapper"]["matches"][i]["matchScore"]["team1Score"]["inngs1"]["overs"]
					team1score = f"{team1runs}/{team1wickets} ({team1overs})"
				except:
					team1score = "Yet to Bat"

				try:
					team2wickets = liveData["typeMatches"][k]["seriesMatches"][_]["seriesAdWrapper"]["matches"][i]["matchScore"]["team2Score"]["inngs1"]["wickets"]
				except:
					team2wickets = 0

				try:
					team2runs = liveData["typeMatches"][k]["seriesMatches"][_]["seriesAdWrapper"]["matches"][i]["matchScore"]["team2Score"]["inngs1"]["runs"]
					team2overs = liveData["typeMatches"][k]["seriesMatches"][_]["seriesAdWrapper"]["matches"][i]["matchScore"]["team2Score"]["inngs1"]["overs"]
					team2score = f"{team2runs}/{team2wickets} ({team2overs})"
				except:
					team2score = "Yet to Bat"

				if format == "TEST":
					try:
						team1wickets2 = liveData["typeMatches"][k]["seriesMatches"][_]["seriesAdWrapper"]["matches"][i]["matchScore"]["team1Score"]["inngs2"]["wickets"]
					except:
						team1wickets2 = 0

					try:
						team1runs2 = liveData["typeMatches"][k]["seriesMatches"][_]["seriesAdWrapper"]["matches"][i]["matchScore"]["team1Score"]["inngs2"]["runs"]
						team1overs2 = liveData["typeMatches"][k]["seriesMatches"][_]["seriesAdWrapper"]["matches"][i]["matchScore"]["team1Score"]["inngs2"]["overs"]
						team1score2 = f"{team1runs2}/{team1wickets2} ({team1overs2})"
					except:
						team1score2 = "Yet to Bat"

					try:
						team2wickets2 = liveData["typeMatches"][k]["seriesMatches"][_]["seriesAdWrapper"]["matches"][i]["matchScore"]["team2Score"]["inngs2"]["wickets"]
					except:
						team2wickets2 = 0

					try:
						team2runs2 = liveData["typeMatches"][k]["seriesMatches"][_]["seriesAdWrapper"]["matches"][i]["matchScore"]["team2Score"]["inngs2"]["runs"]
						team2overs2 = liveData["typeMatches"][k]["seriesMatches"][_]["seriesAdWrapper"]["matches"][i]["matchScore"]["team2Score"]["inngs2"]["overs"]
						team2score2 = f"{team2runs2}/{team2wickets2} ({team2overs2})"
					except:
						team2score2 = "Yet to Bat"

					score = f"1st Inngs: {team1} {team1score} & {team2} {team2score}\n2nd Inngs: {team1} {team1score2} & {team2} {team2score2}"

					
					
				else:
					score = f"{team1} {team1score} & {team2} {team2score}"
				
				liveCurr.append(f"{team1} VS {team2}")
				liveCurr.append(f"{name} - {desc}")
				liveCurr.append(state)
				liveCurr.append(status)
				liveCurr.append(score)
				liveCurr.append(city)

				liveMList.append(liveCurr)

	head = ["Matches", "Description", "State","Status", "Score", "Live From"]

	print(tabulate(liveMList, head, tablefmt="psql"))

	timestamp = int(liveData["responseLastUpdated"])
	updateTime = datetime.fromtimestamp(timestamp).strftime('%A - %B, %d %Y at %I:%M:%S %p')
	if x == "upcoming":
		print(f"Updated on {updateTime}.\n")

def toExit():
	print(fontstyle.apply("Enter 1 to return to MAIN MENU ↙️", "red/bold"))
	print(fontstyle.apply("Enter 0 to exit the program ↙️", "bold/red"))
	choice = int(input("\n?  "))

	if choice == 1:
		main()
	else:
		sys.exit("\nCopyright © 2022 Bold Cricket Inc\n".center(100))


def main():

	getLive("live")
	# getLive("recent")
	# getLive("upcoming")
	print(fontstyle.apply("CHOOSE DESIRED OPTION", 'bold/green'))
	print()
	print("Enter 1 to refresh LIVE SCORE ↙️")
	print("Enter 2 to get Results or Upcoming Fixtures ↙️")
	print("Enter 3 to get ICC Player Rankings ↙️")
	print("Enter 4 to get ICC Team Rankings ↙️")
	print("Enter 5 to get Cricket Related News ↙️")
	print("Enter 6 to get ICC Current Tournaments Points Table ↙️")
	print("Enter 0 to exit program ↙️")
	choice = int(input("\n?  "))

	if choice == 1:
		main()

	elif choice == 2:

		team = input("Enter Team Name: ").lower().strip()
		form = input("Upcoming Fixtures or Recent Results: ").lower().strip()

		if "upcoming" in form:
			getSchedule(team)
		elif "recent" in form:
			getResults(team)

	elif choice == 3:
		playerRankings()

	elif choice == 4:
		teamRankings()

	elif choice == 5:
		news()

	elif choice == 6:
		getStandings()

	else:
		sys.exit("\nCopyright © 2022 Cricket 365 Inc\n".center(100))


if __name__ == "__main__":
    
	print()
	print(pyfiglet.figlet_format("CRICKET  365"))
	main()

