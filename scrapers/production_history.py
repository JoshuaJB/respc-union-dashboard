from bs4 import BeautifulSoup
from urllib import parse
import requests

enablement_data = "\
&ctl00%24ContentPlaceHolder1%24PublicPagePlaceholder1%24PageUserControl%24ctl00%24PublicPageLoadFixPage%24UserControlShowEnergyAndPower1%24SelectedIntervalID=5\
&ctl00%24ContentPlaceHolder1%24PublicPagePlaceholder1%24PageUserControl%24ctl00%24PublicPageLoadFixPage%24UserControlShowEnergyAndPower1%24PlantName=UNC%20Student%20Union\
&ctl00%24ContentPlaceHolder1%24PublicPagePlaceholder1%24PageUserControl%24ctl00%24PublicPageLoadFixPage%24UserControlShowEnergyAndPower1%24UseIntervalHour=1\
&ctl00%24ContentPlaceHolder1%24PublicPagePlaceholder1%24PageUserControl%24ctl00%24PublicPageLoadFixPage%24UserControlShowEnergyAndPower1%24_datePicker%24textBox=8%2F31%2F2016\
&ctl00%24ContentPlaceHolder1%24PublicPagePlaceholder1%24PageUserControl%24ctl00%24PublicPageLoadFixPage%24UserControlShowEnergyAndPower1%24DatePickerYear=2016\
&ctl00%24ContentPlaceHolder1%24PublicPagePlaceholder1%24PageUserControl%24ctl00%24PublicPageLoadFixPage%24UserControlShowEnergyAndPower1%24ImageButtonValues.x=8\
&ctl00%24ContentPlaceHolder1%24PublicPagePlaceholder1%24PageUserControl%24ctl00%24PublicPageLoadFixPage%24UserControlShowEnergyAndPower1%24ImageButtonValues.y=16"

TABLE_BASE_URL = "https://www.sunnyportal.com/Templates/PublicChartValues.aspx?ID=00000000-0000-0000-0000-000000000000&splang=en-US&plantTimezoneBias=-240&name="
TABLE_SETTINGS_PREFIX = "ctl00$ContentPlaceHolder1$PublicPagePlaceholder1$PageUserControl$ctl00$PublicPageLoadFixPage$UserControlShowEnergyAndPower1$"

def getHistory(base_url):#, interval_type, plant_name = "UNC Student Union", use_interval_hour = "1", start_date = "8/31/2016"):
	# Create session on the server
	base_page = requests.get(base_url)
	base_parser = BeautifulSoup(base_page.content, "html.parser")
	# Set server-side state
	table_settings = [("__VIEWSTATE", base_parser.find(id = "__VIEWSTATE")["value"])]
	pre_table_settings = [("ImageButtonValues.x", "8"), ("ImageButtonValues.y", "16"), ("SelectedIntervalID", 5), ("PlantName", "UNC Student Union"), ("UseIntervalHour", 1), ("_datePicker$textBox", "8/31/2016"), ("DatePickerYear","2016")]
	#table_settings = map(lambda setting: (TABLE_SETTING_PREFIX + setting[0], setting[1]), pre_table_settings)
	table_settings.extend(map(lambda setting: (TABLE_SETTINGS_PREFIX + setting[0], setting[1]), pre_table_settings))
	requests.post(base_url, parse.urlencode(table_settings), None, cookies = base_page.cookies, headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"})
	# Get table of history data
	detail_response = requests.get(TABLE_BASE_URL + "&endTime=12/31/2016%2011:59:59%20PM", cookies = base_page.cookies)
	# Perform some questionable parsing
	table_parser = BeautifulSoup(detail_response.content, "html.parser")
	table_entries = table_parser.find_all("td")[2:]
	stripped_table_entries = list(map(lambda entry: entry.string, table_entries))
	data = zip(stripped_table_entries[::2], stripped_table_entries[1::2])
	# Return a list of (date, reading) tuples
	return list(data)

def prefixSettings (settings_list):
	for idx in range(len(settings_list)):
		pre_table_settings[idx] = (TABLE_SETTINGS_PREFIX + pre_table_settings[idx][0], pre_table_settings[idx][1])
