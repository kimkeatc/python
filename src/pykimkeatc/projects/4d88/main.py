
from os.path import exists, join
from lxml import html
import datetime
import requests
import json
import os


class Parser4d88:

    def __init__(self):
        self.record_directory = "records"
        os.makedirs(self.record_directory, mode=0o777, exist_ok=True)
        self.record_filename = "raw_data.json"
        self.record_filepath = self.construct_output_file(self.record_filename)
        if not exists(self.record_filepath):
            self.records = {}
            with open(self.record_filepath, "w") as fh:
                json.dump(self.records, fh)
        else:
            with open(self.record_filepath, "r") as fh:
                self.records = json.load(fh)
        
        self.lotteries = {
            "DaMaCai 4D": {
                "filename": "damacai_4d.json",
            },
            "Toto 4D": {
                "filename": "toto_4d.json",
            },
            "Magnum 4D": {
                "filename": "magnum_4d.json",
            },
            "Magnum Life": {
                "filename": "magnum_life.json",
            },
            "Magnum Jackpot Gold": {
                "filename": "magnum_jackpot_gold.json",
            },
            "Toto 5D": {
                "filename": "toto_5d.json",
            },
            "Toto 6D": {
                "filename": "toto_6d.json",
            },
            "Toto Power 55": {
                "filename": "toto_power_55.json",
            },
            "Toto Supreme 58": {
                "filename": "toto_supreme_58.json",
            },
            "Toto Star 50": {
                "filename": "toto_star_50.json",
            },
            "CashSweep 4D": {
                "filename": "cashsweep_4d.json",
            },
            "Sandakan STC 4D": {
                "filename": "sandakan_stc_4d.json",
            },
            "Sabah Lotto88 4D": {
                "filename": "sabah_lotto88_4d.json",
            },
            "Sabah Lotto88 3D": {
                "filename": "sabah_lotto88_3d.json",
            },
            "Sabah Lotto88 6/45": {
                "filename": "sabah_lotto88_6_45.json",
            },
            "Singapore 4D": {
                "filename": "singapore_4d.json",
            },
            "Singapore 6/45": {
                "filename": "singapore_6_45.json",
            },
        }

        for _, lottery_info in self.lotteries.items():
            filepath = self.construct_output_file(lottery_info["filename"])
            if not exists(filepath):
                with open(filepath, "w") as fh:
                    fh.write(json.dumps({}, indent=4))

    def update_raw_data(self):
        counter = 0
        today = datetime.datetime.now()
        today = datetime.datetime(year=2025, month=1, day=10)
        while True:
            date = today - datetime.timedelta(days=counter)
            counter += 1
            day = date.strftime("%A")
            if day not in ["Tuesday", "Wednesday", "Saturday", "Sunday"]:
                continue
            date = date.strftime("%Y-%m-%d")
            if self.records.get(date, "") != "":
                continue
            try:
                print(f"[Counter {counter}] Query date {date} ({day}) {self.construct_url(date=date)}")
                content = self.download_specific_date_raw_html_content(date)
                self.records[date] = content
            except Exception:
                break
            finally:
                with open(self.record_filepath, "w") as fh:
                    fh.write(json.dumps(self.records, indent=4))

            if counter > 2905:
                break

    def construct_url(self, date: str):
        return f"https://app.4d88.asia/history/date?d={date}"

    def construct_output_file(self, filename: str):
        return join(self.record_directory, filename)

    def download_specific_date_raw_html_content(self, date: str):
        url = self.construct_url(date=date)
        response = requests.get(url=url)
        response.raise_for_status()
        content = response.content.decode()
        return content
    
    def parse_raw_data(self):
        for date, content in self.records.items():
            print(f"Parse content for date {date} {self.construct_url(date=date)}")
            content = html.fromstring(content)
            for tab_index, tab in enumerate(content.xpath("/html/body/div[4]/div[2]")[0].findall("div"), start=1):
                if tab_index == 1:
                    try:
                        filepath = self.construct_output_file(self.lotteries["DaMaCai 4D"]["filename"])
                        data = self.parse_lottery_damacai_4d(tab)
                        records = json.load(open(filepath, "r"))
                        records[data["id"]] = data
                        open(filepath, "w").write(json.dumps(records, indent=4))
                    except Exception as e:
                        print("Failed to parse DaMaCai 4D due to the following error:")
                        print(e)

                    try:
                        filepath = self.construct_output_file(self.lotteries["Toto 4D"]["filename"])
                        data = self.parse_lottery_toto_4d(tab)
                        records = json.load(open(filepath, "r"))
                        records[data["id"]] = data
                        open(filepath, "w").write(json.dumps(records, indent=4))
                    except Exception as e:
                        print("Failed to parse Toto 4D due to the following error:")
                        print(e)

                    try:
                        filepath = self.construct_output_file(self.lotteries["Magnum 4D"]["filename"])
                        data = self.parse_lottery_magnum_4d(tab)
                        records = json.load(open(filepath, "r"))
                        records[data["id"]] = data
                        open(filepath, "w").write(json.dumps(records, indent=4))
                    except Exception as e:
                        print("Failed to parse Magnum 4D due to the following error:")
                        print(e)

                    try:
                        filepath = self.construct_output_file(self.lotteries["Magnum Life"]["filename"])
                        data = self.parse_lottery_magnum_life(tab)
                        records = json.load(open(filepath, "r"))
                        records[data["id"]] = data
                        open(filepath, "w").write(json.dumps(records, indent=4))
                    except Exception as e:
                        print("Failed to parse Magnum Life due to the following error:")
                        print(e)

                    try:
                        filepath = self.construct_output_file(self.lotteries["Magnum Jackpot Gold"]["filename"])
                        data = self.parse_lottery_magnum_jackpot_gold(tab)
                        records = json.load(open(filepath, "r"))
                        records[data["id"]] = data
                        open(filepath, "w").write(json.dumps(records, indent=4))
                    except Exception as e:
                        print("Failed to parse Magnum Jackpot Gold due to the following error:")
                        print(e)

                    try:
                        filepath = self.construct_output_file(self.lotteries["Toto 5D"]["filename"])
                        data = self.parse_lottery_toto_5d(tab)
                        records = json.load(open(filepath, "r"))
                        records[data["id"]] = data
                        open(filepath, "w").write(json.dumps(records, indent=4))
                    except Exception as e:
                        print("Failed to parse Toto 5D due to the following error:")
                        print(e)

                    try:
                        filepath = self.construct_output_file(self.lotteries["Toto 6D"]["filename"])
                        data = self.parse_lottery_toto_6d(tab)
                        records = json.load(open(filepath, "r"))
                        records[data["id"]] = data
                        open(filepath, "w").write(json.dumps(records, indent=4))
                    except Exception as e:
                        print("Failed to parse Toto 6D due to the following error:")
                        print(e)

                    try:
                        filepath = self.construct_output_file(self.lotteries["Toto Power 55"]["filename"])
                        data = self.parse_lottery_toto_power_55(tab)
                        records = json.load(open(filepath, "r"))
                        records[data["id"]] = data
                        open(filepath, "w").write(json.dumps(records, indent=4))
                    except Exception as e:
                        print("Failed to parse Toto Power 55 due to the following error:")
                        print(e)

                    try:
                        filepath = self.construct_output_file(self.lotteries["Toto Supreme 58"]["filename"])
                        data = self.parse_lottery_toto_supreme_58(tab)
                        records = json.load(open(filepath, "r"))
                        records[data["id"]] = data
                        open(filepath, "w").write(json.dumps(records, indent=4))
                    except Exception as e:
                        print("Failed to parse Toto Supreme 58 due to the following error:")
                        print(e)

                    try:
                        filepath = self.construct_output_file(self.lotteries["Toto Star 50"]["filename"])
                        data = self.parse_lottery_toto_star_50(tab)
                        records = json.load(open(filepath, "r"))
                        records[data["id"]] = data
                        open(filepath, "w").write(json.dumps(records, indent=4))
                    except Exception as e:
                        print("Failed to parse Toto Star 50 due to the following error:")
                        print(e)

                elif tab_index == 2:
                    try:
                        filepath = self.construct_output_file(self.lotteries["CashSweep 4D"]["filename"])
                        data = self.parse_lottery_cashsweep_4d(tab)
                        records = json.load(open(filepath, "r"))
                        records[data["id"]] = data
                        open(filepath, "w").write(json.dumps(records, indent=4))
                    except Exception as e:
                        print("Failed to parse CashSweep 4D due to the following error:")
                        print(e)

                    try:
                        filepath = self.construct_output_file(self.lotteries["Sandakan STC 4D"]["filename"])
                        data = self.parse_lottery_sandaakan_stc_4d(tab)
                        records = json.load(open(filepath, "r"))
                        records[data["id"]] = data
                        open(filepath, "w").write(json.dumps(records, indent=4))
                    except Exception as e:
                        print("Failed to parse Sandakan STC 4D due to the following error:")
                        print(e)

                    try:
                        filepath = self.construct_output_file(self.lotteries["Sabah Lotto88 3D"]["filename"])
                        data = self.parse_lottery_sabah_lotto88_4d(tab)
                        records = json.load(open(filepath, "r"))
                        records[data["id"]] = data
                        open(filepath, "w").write(json.dumps(records, indent=4))
                    except Exception as e:
                        print("Failed to parse Sabah Lotto88 3D due to the following error:")
                        print(e)

                    try:
                        filepath = self.construct_output_file(self.lotteries["Sabah Lotto88 6/45"]["filename"])
                        data = self.parse_lottery_sabah_lotto88_3d(tab)
                        records = json.load(open(filepath, "r"))
                        records[data["id"]] = data
                        open(filepath, "w").write(json.dumps(records, indent=4))
                    except Exception as e:
                        print("Failed to parse Sabah Lotto88 6/45 due to the following error:")
                        print(e)

                    try:
                        filepath = self.construct_output_file(self.lotteries["Sabah Lotto88 4D"]["filename"])
                        data = self.parse_lottery_sabah_lotto88_6_45(tab)
                        records = json.load(open(filepath, "r"))
                        records[data["id"]] = data
                        open(filepath, "w").write(json.dumps(records, indent=4))
                    except Exception as e:
                        print("Failed to parse Sabah Lotto88 4D due to the following error:")
                        print(e)

                elif tab_index == 3:
                    try:
                        filepath = self.construct_output_file(self.lotteries["Singapore 4D"]["filename"])
                        data = self.parse_lottery_singapore_4d(tab)
                        records = json.load(open(filepath, "r"))
                        records[data["id"]] = data
                        open(filepath, "w").write(json.dumps(records, indent=4))
                    except Exception as e:
                        print("Failed to parse Singapore 4D due to the following error:")
                        print(e)

                    try:
                        filepath = self.construct_output_file(self.lotteries["Singapore 6/45"]["filename"])
                        data = self.parse_lottery_singapore_6_45(tab)
                        records = json.load(open(filepath, "r"))
                        records[data["id"]] = data
                        open(filepath, "w").write(json.dumps(records, indent=4))
                    except Exception as e:
                        print("Failed to parse Singapore 6/45 due to the following error:")
                        print(e)

    def parse_lottery_damacai_4d(self, tab):
        lottery = tab.xpath("div/div[1]/div[1]/div[1]/div[1]/span/span")[0].text.strip()
        if lottery != "DaMaCai 4D" or \
           tab.xpath("div/div[1]/div[1]/div[1]/div[2]/div/table/thead/tr[1]/th[1]")[0].attrib["class"].strip() not in ["firstLogo"] or \
           tab.xpath("div/div[1]/div[1]/div[1]/div[2]/div/table/thead/tr[2]/th[1]")[0].attrib["class"].strip() not in ["secondLogo"] or \
           tab.xpath("div/div[1]/div[1]/div[1]/div[2]/div/table/thead/tr[3]/th[1]")[0].attrib["class"].strip() not in ["thirdLogo"] or \
           tab.xpath("div/div[1]/div[1]/div[1]/div[2]/div/table/thead/tr[4]/th[1]/div")[0].text.strip() not in ["Special"] or \
           tab.xpath("div/div[1]/div[1]/div[1]/div[2]/div/table/thead/tr[4]/th[2]/div")[0].text.strip() not in ["Consolation"]:
               raise Exception("Fields are not in the correct format")
        data = {
            "lottery": lottery,
            "draw": tab.xpath("div/div[1]/div[1]/div[1]/div[1]/span/b[1]")[0].text.strip(),
            "id": tab.xpath("div/div[1]/div[1]/div[1]/div[1]/span/b[2]")[0].text.strip(),
            "1st": tab.xpath("div/div[1]/div[1]/div[1]/div[2]/div/table/thead/tr[1]/th[2]")[0].text.strip(),
            "2nd": tab.xpath("div/div[1]/div[1]/div[1]/div[2]/div/table/thead/tr[2]/th[2]")[0].text.strip(),
            "3rd": tab.xpath("div/div[1]/div[1]/div[1]/div[2]/div/table/thead/tr[3]/th[2]")[0].text.strip(),
            "special": [
                tab.xpath("div/div[1]/div[1]/div[1]/div[2]/div/table/tbody/tr[1]/td[1]")[0].text.strip(),
                tab.xpath("div/div[1]/div[1]/div[1]/div[2]/div/table/tbody/tr[1]/td[2]")[0].text.strip(),
                tab.xpath("div/div[1]/div[1]/div[1]/div[2]/div/table/tbody/tr[2]/td[1]")[0].text.strip(),
                tab.xpath("div/div[1]/div[1]/div[1]/div[2]/div/table/tbody/tr[2]/td[2]")[0].text.strip(),
                tab.xpath("div/div[1]/div[1]/div[1]/div[2]/div/table/tbody/tr[3]/td[1]")[0].text.strip(),
                tab.xpath("div/div[1]/div[1]/div[1]/div[2]/div/table/tbody/tr[3]/td[2]")[0].text.strip(),
                tab.xpath("div/div[1]/div[1]/div[1]/div[2]/div/table/tbody/tr[4]/td[1]")[0].text.strip(),
                tab.xpath("div/div[1]/div[1]/div[1]/div[2]/div/table/tbody/tr[4]/td[2]")[0].text.strip(),
                tab.xpath("div/div[1]/div[1]/div[1]/div[2]/div/table/tbody/tr[5]/td[1]")[0].text.strip(),
                tab.xpath("div/div[1]/div[1]/div[1]/div[2]/div/table/tbody/tr[5]/td[2]")[0].text.strip(),
            ],
            "consolation": [
                tab.xpath("div/div[1]/div[1]/div[1]/div[2]/div/table/tbody/tr[1]/td[3]")[0].text.strip(),
                tab.xpath("div/div[1]/div[1]/div[1]/div[2]/div/table/tbody/tr[1]/td[4]")[0].text.strip(),
                tab.xpath("div/div[1]/div[1]/div[1]/div[2]/div/table/tbody/tr[2]/td[3]")[0].text.strip(),
                tab.xpath("div/div[1]/div[1]/div[1]/div[2]/div/table/tbody/tr[2]/td[4]")[0].text.strip(),
                tab.xpath("div/div[1]/div[1]/div[1]/div[2]/div/table/tbody/tr[3]/td[3]")[0].text.strip(),
                tab.xpath("div/div[1]/div[1]/div[1]/div[2]/div/table/tbody/tr[3]/td[4]")[0].text.strip(),
                tab.xpath("div/div[1]/div[1]/div[1]/div[2]/div/table/tbody/tr[4]/td[3]")[0].text.strip(),
                tab.xpath("div/div[1]/div[1]/div[1]/div[2]/div/table/tbody/tr[4]/td[4]")[0].text.strip(),
                tab.xpath("div/div[1]/div[1]/div[1]/div[2]/div/table/tbody/tr[5]/td[3]")[0].text.strip(),
                tab.xpath("div/div[1]/div[1]/div[1]/div[2]/div/table/tbody/tr[5]/td[4]")[0].text.strip(),
            ],
        }
        return data

    def parse_lottery_toto_4d(self, tab):
        lottery = tab.xpath("div/div[1]/div[2]/div[1]/div[1]/span/span")[0].text.strip()
        if lottery != "Toto 4D" or \
           tab.xpath("div/div[1]/div[2]/div[1]/div[2]/div/table/thead/tr[1]/th[1]")[0].attrib["class"].strip() not in ["firstLogo"] or \
           tab.xpath("div/div[1]/div[2]/div[1]/div[2]/div/table/thead/tr[2]/th[1]")[0].attrib["class"].strip() not in ["secondLogo"] or \
           tab.xpath("div/div[1]/div[2]/div[1]/div[2]/div/table/thead/tr[3]/th[1]")[0].attrib["class"].strip() not in ["thirdLogo"] or \
           tab.xpath("div/div[1]/div[2]/div[1]/div[2]/div/table/thead/tr[4]/th[1]/div")[0].text.strip() not in ["Special"] or \
           tab.xpath("div/div[1]/div[2]/div[1]/div[2]/div/table/thead/tr[4]/th[2]/div")[0].text.strip() not in ["Consolation"]:
               raise Exception("Fields are not in the correct format")
        data = {
            "lottery": lottery,
            "draw": tab.xpath("div/div[1]/div[2]/div[1]/div[1]/span/b[1]")[0].text.strip(),
            "id": tab.xpath("div/div[1]/div[2]/div[1]/div[1]/span/b[2]")[0].text.strip(),
            "1st": tab.xpath("div/div[1]/div[2]/div[1]/div[2]/div/table/thead/tr[1]/th[2]")[0].text.strip(),
            "2nd": tab.xpath("div/div[1]/div[2]/div[1]/div[2]/div/table/thead/tr[2]/th[2]")[0].text.strip(),
            "3rd": tab.xpath("div/div[1]/div[2]/div[1]/div[2]/div/table/thead/tr[3]/th[2]")[0].text.strip(),
            "special": [
                tab.xpath("div/div[1]/div[2]/div[1]/div[2]/div/table/tbody/tr[1]/td[1]")[0].text.strip(),
                tab.xpath("div/div[1]/div[2]/div[1]/div[2]/div/table/tbody/tr[1]/td[2]")[0].text.strip(),
                tab.xpath("div/div[1]/div[2]/div[1]/div[2]/div/table/tbody/tr[2]/td[1]")[0].text.strip(),
                tab.xpath("div/div[1]/div[2]/div[1]/div[2]/div/table/tbody/tr[2]/td[2]")[0].text.strip(),
                tab.xpath("div/div[1]/div[2]/div[1]/div[2]/div/table/tbody/tr[3]/td[1]")[0].text.strip(),
                tab.xpath("div/div[1]/div[2]/div[1]/div[2]/div/table/tbody/tr[3]/td[2]")[0].text.strip(),
                tab.xpath("div/div[1]/div[2]/div[1]/div[2]/div/table/tbody/tr[4]/td[1]")[0].text.strip(),
                tab.xpath("div/div[1]/div[2]/div[1]/div[2]/div/table/tbody/tr[4]/td[2]")[0].text.strip(),
                tab.xpath("div/div[1]/div[2]/div[1]/div[2]/div/table/tbody/tr[5]/td[1]")[0].text.strip(),
                tab.xpath("div/div[1]/div[2]/div[1]/div[2]/div/table/tbody/tr[5]/td[2]")[0].text.strip(),
            ],
            "consolation": [
                tab.xpath("div/div[1]/div[2]/div[1]/div[2]/div/table/tbody/tr[1]/td[3]")[0].text.strip(),
                tab.xpath("div/div[1]/div[2]/div[1]/div[2]/div/table/tbody/tr[1]/td[4]")[0].text.strip(),
                tab.xpath("div/div[1]/div[2]/div[1]/div[2]/div/table/tbody/tr[2]/td[3]")[0].text.strip(),
                tab.xpath("div/div[1]/div[2]/div[1]/div[2]/div/table/tbody/tr[2]/td[4]")[0].text.strip(),
                tab.xpath("div/div[1]/div[2]/div[1]/div[2]/div/table/tbody/tr[3]/td[3]")[0].text.strip(),
                tab.xpath("div/div[1]/div[2]/div[1]/div[2]/div/table/tbody/tr[3]/td[4]")[0].text.strip(),
                tab.xpath("div/div[1]/div[2]/div[1]/div[2]/div/table/tbody/tr[4]/td[3]")[0].text.strip(),
                tab.xpath("div/div[1]/div[2]/div[1]/div[2]/div/table/tbody/tr[4]/td[4]")[0].text.strip(),
                tab.xpath("div/div[1]/div[2]/div[1]/div[2]/div/table/tbody/tr[5]/td[3]")[0].text.strip(),
                tab.xpath("div/div[1]/div[2]/div[1]/div[2]/div/table/tbody/tr[5]/td[4]")[0].text.strip(),
            ],
        }
        return data

    def parse_lottery_magnum_4d(self, tab):
        lottery = tab.xpath("div/div[1]/div[3]/div[1]/div[1]/span/span")[0].text.strip()
        if lottery != "Magnum 4D" or \
           tab.xpath("div/div[1]/div[3]/div[1]/div[2]/div/table/thead/tr[1]/th[1]")[0].attrib["class"].strip() not in ["firstLogo"] or \
           tab.xpath("div/div[1]/div[3]/div[1]/div[2]/div/table/thead/tr[2]/th[1]")[0].attrib["class"].strip() not in ["secondLogo"] or \
           tab.xpath("div/div[1]/div[3]/div[1]/div[2]/div/table/thead/tr[3]/th[1]")[0].attrib["class"].strip() not in ["thirdLogo"] or \
           tab.xpath("div/div[1]/div[3]/div[1]/div[2]/div/table/thead/tr[4]/th[1]/div")[0].text.strip() not in ["Special"] or \
           tab.xpath("div/div[1]/div[3]/div[1]/div[2]/div/table/thead/tr[4]/th[2]/div")[0].text.strip() not in ["Consolation"]:
               raise Exception("Fields are not in the correct format")
        data = {
            "lottery": lottery,
            "draw": tab.xpath("div/div[1]/div[3]/div[1]/div[1]/span/b[1]")[0].text.strip(),
            "id": tab.xpath("div/div[1]/div[3]/div[1]/div[1]/span/b[2]")[0].text.strip(),
            "1st": tab.xpath("div/div[1]/div[3]/div[1]/div[2]/div/table/thead/tr[1]/th[2]")[0].text.strip(),
            "2nd": tab.xpath("div/div[1]/div[3]/div[1]/div[2]/div/table/thead/tr[2]/th[2]")[0].text.strip(),
            "3rd": tab.xpath("div/div[1]/div[3]/div[1]/div[2]/div/table/thead/tr[3]/th[2]")[0].text.strip(),
            "special": [
                 tab.xpath("div/div[1]/div[3]/div[1]/div[2]/div/table/tbody/tr[1]/td[1]")[0].text.strip(),
                 tab.xpath("div/div[1]/div[3]/div[1]/div[2]/div/table/tbody/tr[1]/td[2]")[0].text.strip(),
                 tab.xpath("div/div[1]/div[3]/div[1]/div[2]/div/table/tbody/tr[2]/td[1]")[0].text.strip(),
                 tab.xpath("div/div[1]/div[3]/div[1]/div[2]/div/table/tbody/tr[2]/td[2]")[0].text.strip(),
                 tab.xpath("div/div[1]/div[3]/div[1]/div[2]/div/table/tbody/tr[3]/td[1]")[0].text.strip(),
                 tab.xpath("div/div[1]/div[3]/div[1]/div[2]/div/table/tbody/tr[3]/td[2]")[0].text.strip(),
                 tab.xpath("div/div[1]/div[3]/div[1]/div[2]/div/table/tbody/tr[4]/td[1]")[0].text.strip(),
                 tab.xpath("div/div[1]/div[3]/div[1]/div[2]/div/table/tbody/tr[4]/td[2]")[0].text.strip(),
                 tab.xpath("div/div[1]/div[3]/div[1]/div[2]/div/table/tbody/tr[5]/td[1]")[0].text.strip(),
                 tab.xpath("div/div[1]/div[3]/div[1]/div[2]/div/table/tbody/tr[5]/td[2]")[0].text.strip(),
            ],
            "consolation": [
                 tab.xpath("div/div[1]/div[3]/div[1]/div[2]/div/table/tbody/tr[1]/td[3]")[0].text.strip(),
                 tab.xpath("div/div[1]/div[3]/div[1]/div[2]/div/table/tbody/tr[1]/td[4]")[0].text.strip(),
                 tab.xpath("div/div[1]/div[3]/div[1]/div[2]/div/table/tbody/tr[2]/td[3]")[0].text.strip(),
                 tab.xpath("div/div[1]/div[3]/div[1]/div[2]/div/table/tbody/tr[2]/td[4]")[0].text.strip(),
                 tab.xpath("div/div[1]/div[3]/div[1]/div[2]/div/table/tbody/tr[3]/td[3]")[0].text.strip(),
                 tab.xpath("div/div[1]/div[3]/div[1]/div[2]/div/table/tbody/tr[3]/td[4]")[0].text.strip(),
                 tab.xpath("div/div[1]/div[3]/div[1]/div[2]/div/table/tbody/tr[4]/td[3]")[0].text.strip(),
                 tab.xpath("div/div[1]/div[3]/div[1]/div[2]/div/table/tbody/tr[4]/td[4]")[0].text.strip(),
                 tab.xpath("div/div[1]/div[3]/div[1]/div[2]/div/table/tbody/tr[5]/td[3]")[0].text.strip(),
                 tab.xpath("div/div[1]/div[3]/div[1]/div[2]/div/table/tbody/tr[5]/td[4]")[0].text.strip(),
            ],
        }
        return data

    def parse_lottery_magnum_life(self, tab):
        lottery = tab.xpath("div/div[2]/div[1]/div/div[1]/span/span")[0].text.strip()
        if lottery != "MAGNUM LIFE":
            raise Exception("Fields are not in the correct format")
        data = {
            "lottery": lottery,
            "draw": tab.xpath("div/div[2]/div[1]/div/div[1]/span/b[1]")[0].text.strip(),
            "id": tab.xpath("div/div[2]/div[1]/div/div[1]/span/b[2]")[0].text.strip(),
            "prize": tab.xpath("div/div[2]/div[1]/div/div[2]/div/table/tbody/tr[1]/td/span")[0].text.strip().split("\xa0") + [
                tab.xpath("div/div[2]/div[1]/div/div[2]/div/table/tbody/tr[1]/td/span/span")[0].text.strip(),
                tab.xpath("div/div[2]/div[1]/div/div[2]/div/table/tbody/tr[1]/td/span/span")[1].text.strip(),
            ],
        }
        return data

    def parse_lottery_magnum_jackpot_gold(self, tab):
        lottery = tab.xpath("div/div[2]/div[1]/div/div[2]/div/table/tbody/tr[2]/td/span")[0].text.strip()
        if lottery != "MAGNUM JACKPOT GOLD":
            raise Exception("Fields are not in the correct format")
        data = {
            "lottery": lottery,
            "draw": tab.xpath("div/div[2]/div[1]/div/div[1]/span/b[1]")[0].text.strip(),
            "id": tab.xpath("div/div[2]/div[1]/div/div[1]/span/b[2]")[0].text.strip(),
            "prize": [
                 tab.xpath("div/div[2]/div[1]/div/div[2]/div/table/tbody/tr[3]/td[1]/div")[0].text.strip(),
                 tab.xpath("div/div[2]/div[1]/div/div[2]/div/table/tbody/tr[3]/td[3]/div")[0].text.strip()
            ]
        }
        return data

    def parse_lottery_toto_5d(self, tab):
        lottery = tab.xpath("div/div[2]/div[2]/div[1]/div[1]/span/span")[0].text.strip()
        if lottery != "Toto 5D" or \
            tab.xpath("div/div[2]/div[2]/div[1]/div[2]/div/table/tbody/tr[1]/td[1]")[0].text.strip() not in ["1st"] or \
            tab.xpath("div/div[2]/div[2]/div[1]/div[2]/div/table/tbody/tr[2]/td[1]")[0].text.strip() not in ["2nd"] or \
            tab.xpath("div/div[2]/div[2]/div[1]/div[2]/div/table/tbody/tr[3]/td[1]")[0].text.strip() not in ["3rd"] or \
            tab.xpath("div/div[2]/div[2]/div[1]/div[2]/div/table/tbody/tr[1]/td[3]")[0].text.strip() not in ["4th"] or \
            tab.xpath("div/div[2]/div[2]/div[1]/div[2]/div/table/tbody/tr[2]/td[3]")[0].text.strip() not in ["5th"] or \
            tab.xpath("div/div[2]/div[2]/div[1]/div[2]/div/table/tbody/tr[3]/td[3]")[0].text.strip() not in ["6th"]:
               raise Exception("Fields are not in the correct format")
        data = {
            "lottery": lottery,
            "draw": tab.xpath("div/div[2]/div[2]/div[1]/div[1]/span/b[1]")[0].text.strip(),
            "id": tab.xpath("div/div[2]/div[2]/div[1]/div[1]/span/b[2]")[0].text.strip(),
            "prize": [
                tab.xpath("div/div[2]/div[2]/div[1]/div[2]/div/table/tbody/tr[1]/td[2]")[0].text.strip(),
                tab.xpath("div/div[2]/div[2]/div[1]/div[2]/div/table/tbody/tr[2]/td[2]")[0].text.strip(),
                tab.xpath("div/div[2]/div[2]/div[1]/div[2]/div/table/tbody/tr[3]/td[2]")[0].text.strip(),
                tab.xpath("div/div[2]/div[2]/div[1]/div[2]/div/table/tbody/tr[1]/td[4]")[0].text.strip(),
                tab.xpath("div/div[2]/div[2]/div[1]/div[2]/div/table/tbody/tr[2]/td[4]")[0].text.strip(),
                tab.xpath("div/div[2]/div[2]/div[1]/div[2]/div/table/tbody/tr[3]/td[4]")[0].text.strip(),
            ],
        }
        return data

    def parse_lottery_toto_6d(self, tab):
        lottery = tab.xpath("div/div[2]/div[2]/div[2]/div[1]/span/span")[0].text.strip()
        if lottery != "Toto 6D" or \
           tab.xpath("div/div[2]/div[2]/div[2]/div[2]/div/table/tbody/tr[1]/td[1]")[0].text.strip() not in ["2nd"] or \
           tab.xpath("div/div[2]/div[2]/div[2]/div[2]/div/table/tbody/tr[2]/td[1]")[0].text.strip() not in ["3rd"] or \
           tab.xpath("div/div[2]/div[2]/div[2]/div[2]/div/table/tbody/tr[3]/td[1]")[0].text.strip() not in ["4th"] or \
           tab.xpath("div/div[2]/div[2]/div[2]/div[2]/div/table/tbody/tr[4]/td[1]")[0].text.strip() not in ["5th"]:
               raise Exception("Fields are not in the correct format")
        data = {
            "lottery": lottery,
            "draw": tab.xpath("div/div[2]/div[2]/div[2]/div[1]/span/b[1]")[0].text.strip(),
            "id": tab.xpath("div/div[2]/div[2]/div[2]/div[1]/span/b[2]")[0].text.strip(),
            "1st": tab.xpath("div/div[2]/div[2]/div[2]/div[2]/div/table/thead/tr/th")[0].text.strip(),
            "2nd": [
                tab.xpath("div/div[2]/div[2]/div[2]/div[2]/div/table/tbody/tr[1]/td[2]")[0].text.strip(),
                tab.xpath("div/div[2]/div[2]/div[2]/div[2]/div/table/tbody/tr[1]/td[4]")[0].text.strip(),
            ],
            "3rd": [
                tab.xpath("div/div[2]/div[2]/div[2]/div[2]/div/table/tbody/tr[2]/td[2]")[0].text.strip(),
                tab.xpath("div/div[2]/div[2]/div[2]/div[2]/div/table/tbody/tr[2]/td[4]")[0].text.strip(),
            ],
            "4th": [
                tab.xpath("div/div[2]/div[2]/div[2]/div[2]/div/table/tbody/tr[3]/td[2]")[0].text.strip(),
                tab.xpath("div/div[2]/div[2]/div[2]/div[2]/div/table/tbody/tr[3]/td[4]")[0].text.strip(),
            ],
            "5th": [
                tab.xpath("div/div[2]/div[2]/div[2]/div[2]/div/table/tbody/tr[4]/td[2]")[0].text.strip(),
                tab.xpath("div/div[2]/div[2]/div[2]/div[2]/div/table/tbody/tr[4]/td[4]")[0].text.strip(),
            ],
        }
        return data

    def parse_lottery_toto_power_55(self, tab):
        lottery = tab.xpath("div/div[2]/div[3]/div[1]/div[1]/span/span")[0].text.strip()
        if lottery != "Toto POWER 55":
            raise Exception("Fields are not in the correct format")
        data = {
            "lottery": lottery,
            "draw": tab.xpath("div/div[2]/div[3]/div[1]/div[1]/span/b[1]")[0].text.strip(),
            "id": tab.xpath("div/div[2]/div[3]/div[1]/div[1]/span/b[2]")[0].text.strip(),
            "prize": [
                tab.xpath("div/div[2]/div[3]/div[1]/div[2]/div/table/tbody/tr/td[1]")[0].text.strip(),
                tab.xpath("div/div[2]/div[3]/div[1]/div[2]/div/table/tbody/tr/td[2]")[0].text.strip(),
                tab.xpath("div/div[2]/div[3]/div[1]/div[2]/div/table/tbody/tr/td[3]")[0].text.strip(),
                tab.xpath("div/div[2]/div[3]/div[1]/div[2]/div/table/tbody/tr/td[4]")[0].text.strip(),
                tab.xpath("div/div[2]/div[3]/div[1]/div[2]/div/table/tbody/tr/td[5]")[0].text.strip(),
                tab.xpath("div/div[2]/div[3]/div[1]/div[2]/div/table/tbody/tr/td[6]")[0].text.strip(),
            ],
        }
        return data

    def parse_lottery_toto_supreme_58(self, tab):
        lottery = tab.xpath("div/div[2]/div[3]/div[2]/div[1]/span/span")[0].text.strip()
        if lottery != "Toto SUPREME 58":
            raise Exception("Fields are not in the correct format")
        data = {
            "lottery": lottery,
            "draw": tab.xpath("div/div[2]/div[3]/div[2]/div[1]/span/b[1]")[0].text.strip(),
            "id": tab.xpath("div/div[2]/div[3]/div[2]/div[1]/span/b[2]")[0].text.strip(),
            "prize": [
                tab.xpath("div/div[2]/div[3]/div[2]/div[2]/div/table/tbody/tr/td[1]")[0].text.strip(),
                tab.xpath("div/div[2]/div[3]/div[2]/div[2]/div/table/tbody/tr/td[2]")[0].text.strip(),
                tab.xpath("div/div[2]/div[3]/div[2]/div[2]/div/table/tbody/tr/td[3]")[0].text.strip(),
                tab.xpath("div/div[2]/div[3]/div[2]/div[2]/div/table/tbody/tr/td[4]")[0].text.strip(),
                tab.xpath("div/div[2]/div[3]/div[2]/div[2]/div/table/tbody/tr/td[5]")[0].text.strip(),
                tab.xpath("div/div[2]/div[3]/div[2]/div[2]/div/table/tbody/tr/td[6]")[0].text.strip(),
            ],
        }
        return data

    def parse_lottery_toto_star_50(self, tab):
        lottery = tab.xpath("div/div[2]/div[3]/div[3]/div[1]/span/span")[0].text.strip()
        if lottery != "Toto STAR 50":
            raise Exception("Fields are not in the correct format")
        data = {
            "lottery": lottery,
            "draw": tab.xpath("div/div[2]/div[3]/div[3]/div[1]/span/b[1]")[0].text.strip(),
            "id": tab.xpath("div/div[2]/div[3]/div[3]/div[1]/span/b[2]")[0].text.strip(),
            "prize": [
                tab.xpath("div/div[2]/div[3]/div[3]/div[2]/div/table/tbody/tr/td[1]")[0].text.strip(),
                tab.xpath("div/div[2]/div[3]/div[3]/div[2]/div/table/tbody/tr/td[2]")[0].text.strip(),
                tab.xpath("div/div[2]/div[3]/div[3]/div[2]/div/table/tbody/tr/td[3]")[0].text.strip(),
                tab.xpath("div/div[2]/div[3]/div[3]/div[2]/div/table/tbody/tr/td[4]")[0].text.strip(),
                tab.xpath("div/div[2]/div[3]/div[3]/div[2]/div/table/tbody/tr/td[5]")[0].text.strip(),
                tab.xpath("div/div[2]/div[3]/div[3]/div[2]/div/table/tbody/tr/td[6]")[0].text.strip(),
                tab.xpath("div/div[2]/div[3]/div[3]/div[2]/div/table/tbody/tr/td[7]")[0].text.strip(),
            ],
        }
        return data

    def parse_lottery_cashsweep_4d(self, tab):
        lottery = tab.xpath("div/div[1]/div[1]/div[1]/div[1]/span/span")[0].text.strip()
        if lottery != "CashSweep 4D" or \
           tab.xpath("div/div[1]/div[1]/div[1]/div[2]/div/table/thead/tr[1]/th[1]")[0].attrib["class"].strip() not in ["firstLogo"] or \
           tab.xpath("div/div[1]/div[1]/div[1]/div[2]/div/table/thead/tr[2]/th[1]")[0].attrib["class"].strip() not in ["secondLogo"] or \
           tab.xpath("div/div[1]/div[1]/div[1]/div[2]/div/table/thead/tr[3]/th[1]")[0].attrib["class"].strip() not in ["thirdLogo"] or \
           tab.xpath("div/div[1]/div[1]/div[1]/div[2]/div/table/thead/tr[4]/th[1]/div")[0].text.strip() not in ["Special"] or \
           tab.xpath("div/div[1]/div[1]/div[1]/div[2]/div/table/thead/tr[4]/th[2]/div")[0].text.strip() not in ["Consolation"]:
               raise Exception("Fields are not in the correct format")
        data = {
            "lottery": lottery,
            "draw": tab.xpath("div/div[1]/div[1]/div[1]/div[1]/span/b[1]")[0].text.strip(),
            "id": tab.xpath("div/div[1]/div[1]/div[1]/div[1]/span/b[2]")[0].text.strip(),
            "1st": tab.xpath("div/div[1]/div[1]/div[1]/div[2]/div/table/thead/tr[1]/th[2]")[0].text.strip(),
            "2nd": tab.xpath("div/div[1]/div[1]/div[1]/div[2]/div/table/thead/tr[2]/th[2]")[0].text.strip(),
            "3rd": tab.xpath("div/div[1]/div[1]/div[1]/div[2]/div/table/thead/tr[3]/th[2]")[0].text.strip(),
            "special": [
                tab.xpath("div/div[1]/div[1]/div[1]/div[2]/div/table/tbody/tr[1]/td[1]")[0].text.strip(),
                tab.xpath("div/div[1]/div[1]/div[1]/div[2]/div/table/tbody/tr[1]/td[2]")[0].text.strip(),
                tab.xpath("div/div[1]/div[1]/div[1]/div[2]/div/table/tbody/tr[2]/td[1]")[0].text.strip(),
                tab.xpath("div/div[1]/div[1]/div[1]/div[2]/div/table/tbody/tr[2]/td[2]")[0].text.strip(),
                tab.xpath("div/div[1]/div[1]/div[1]/div[2]/div/table/tbody/tr[3]/td[1]")[0].text.strip(),
                tab.xpath("div/div[1]/div[1]/div[1]/div[2]/div/table/tbody/tr[3]/td[2]")[0].text.strip(),
                tab.xpath("div/div[1]/div[1]/div[1]/div[2]/div/table/tbody/tr[4]/td[1]")[0].text.strip(),
                tab.xpath("div/div[1]/div[1]/div[1]/div[2]/div/table/tbody/tr[4]/td[2]")[0].text.strip(),
                tab.xpath("div/div[1]/div[1]/div[1]/div[2]/div/table/tbody/tr[5]/td[1]")[0].text.strip(),
                tab.xpath("div/div[1]/div[1]/div[1]/div[2]/div/table/tbody/tr[5]/td[2]")[0].text.strip(),
            ],
            "consolation": [
                tab.xpath("div/div[1]/div[1]/div[1]/div[2]/div/table/tbody/tr[1]/td[3]")[0].text.strip(),
                tab.xpath("div/div[1]/div[1]/div[1]/div[2]/div/table/tbody/tr[1]/td[4]")[0].text.strip(),
                tab.xpath("div/div[1]/div[1]/div[1]/div[2]/div/table/tbody/tr[2]/td[3]")[0].text.strip(),
                tab.xpath("div/div[1]/div[1]/div[1]/div[2]/div/table/tbody/tr[2]/td[4]")[0].text.strip(),
                tab.xpath("div/div[1]/div[1]/div[1]/div[2]/div/table/tbody/tr[3]/td[3]")[0].text.strip(),
                tab.xpath("div/div[1]/div[1]/div[1]/div[2]/div/table/tbody/tr[3]/td[4]")[0].text.strip(),
                tab.xpath("div/div[1]/div[1]/div[1]/div[2]/div/table/tbody/tr[4]/td[3]")[0].text.strip(),
                tab.xpath("div/div[1]/div[1]/div[1]/div[2]/div/table/tbody/tr[4]/td[4]")[0].text.strip(),
                tab.xpath("div/div[1]/div[1]/div[1]/div[2]/div/table/tbody/tr[5]/td[3]")[0].text.strip(),
                tab.xpath("div/div[1]/div[1]/div[1]/div[2]/div/table/tbody/tr[5]/td[4]")[0].text.strip(),
            ],
        }
        return data

    def parse_lottery_sandaakan_stc_4d(self, tab):
        lottery = tab.xpath("div/div[1]/div[2]/div[1]/div[1]/span/span")[0].text.strip()
        if lottery != "Sandakan STC 4D" or \
           tab.xpath("div/div[1]/div[2]/div[1]/div[2]/div/table/thead/tr[1]/th[1]")[0].attrib["class"].strip() not in ["firstLogo"] or \
           tab.xpath("div/div[1]/div[2]/div[1]/div[2]/div/table/thead/tr[2]/th[1]")[0].attrib["class"].strip() not in ["secondLogo"] or \
           tab.xpath("div/div[1]/div[2]/div[1]/div[2]/div/table/thead/tr[3]/th[1]")[0].attrib["class"].strip() not in ["thirdLogo"] or \
           tab.xpath("div/div[1]/div[2]/div[1]/div[2]/div/table/thead/tr[4]/th[1]/div")[0].text.strip() not in ["Special"] or \
           tab.xpath("div/div[1]/div[2]/div[1]/div[2]/div/table/thead/tr[4]/th[2]/div")[0].text.strip() not in ["Consolation"]:
               raise Exception("Fields are not in the correct format")
        data = {
            "lottery": lottery,
            "draw": tab.xpath("div/div[1]/div[2]/div[1]/div[1]/span/b[1]")[0].text.strip(),
            "id": tab.xpath("div/div[1]/div[2]/div[1]/div[1]/span/b[2]")[0].text.strip(),
            "1st": tab.xpath("div/div[1]/div[2]/div[1]/div[2]/div/table/thead/tr[1]/th[2]")[0].text.strip(),
            "2nd": tab.xpath("div/div[1]/div[2]/div[1]/div[2]/div/table/thead/tr[2]/th[2]")[0].text.strip(),
            "3rd": tab.xpath("div/div[1]/div[2]/div[1]/div[2]/div/table/thead/tr[3]/th[2]")[0].text.strip(),
            "special": [
                tab.xpath("div/div[1]/div[2]/div[1]/div[2]/div/table/tbody/tr[1]/td[1]")[0].text.strip(),
                tab.xpath("div/div[1]/div[2]/div[1]/div[2]/div/table/tbody/tr[1]/td[2]")[0].text.strip(),
                tab.xpath("div/div[1]/div[2]/div[1]/div[2]/div/table/tbody/tr[2]/td[1]")[0].text.strip(),
                tab.xpath("div/div[1]/div[2]/div[1]/div[2]/div/table/tbody/tr[2]/td[2]")[0].text.strip(),
                tab.xpath("div/div[1]/div[2]/div[1]/div[2]/div/table/tbody/tr[3]/td[1]")[0].text.strip(),
                tab.xpath("div/div[1]/div[2]/div[1]/div[2]/div/table/tbody/tr[3]/td[2]")[0].text.strip(),
                tab.xpath("div/div[1]/div[2]/div[1]/div[2]/div/table/tbody/tr[4]/td[1]")[0].text.strip(),
                tab.xpath("div/div[1]/div[2]/div[1]/div[2]/div/table/tbody/tr[4]/td[2]")[0].text.strip(),
                tab.xpath("div/div[1]/div[2]/div[1]/div[2]/div/table/tbody/tr[5]/td[1]")[0].text.strip(),
                tab.xpath("div/div[1]/div[2]/div[1]/div[2]/div/table/tbody/tr[5]/td[2]")[0].text.strip(),
            ],
            "consolation": [
                tab.xpath("div/div[1]/div[2]/div[1]/div[2]/div/table/tbody/tr[1]/td[3]")[0].text.strip(),
                tab.xpath("div/div[1]/div[2]/div[1]/div[2]/div/table/tbody/tr[1]/td[4]")[0].text.strip(),
                tab.xpath("div/div[1]/div[2]/div[1]/div[2]/div/table/tbody/tr[2]/td[3]")[0].text.strip(),
                tab.xpath("div/div[1]/div[2]/div[1]/div[2]/div/table/tbody/tr[2]/td[4]")[0].text.strip(),
                tab.xpath("div/div[1]/div[2]/div[1]/div[2]/div/table/tbody/tr[3]/td[3]")[0].text.strip(),
                tab.xpath("div/div[1]/div[2]/div[1]/div[2]/div/table/tbody/tr[3]/td[4]")[0].text.strip(),
                tab.xpath("div/div[1]/div[2]/div[1]/div[2]/div/table/tbody/tr[4]/td[3]")[0].text.strip(),
                tab.xpath("div/div[1]/div[2]/div[1]/div[2]/div/table/tbody/tr[4]/td[4]")[0].text.strip(),
                tab.xpath("div/div[1]/div[2]/div[1]/div[2]/div/table/tbody/tr[5]/td[3]")[0].text.strip(),
                tab.xpath("div/div[1]/div[2]/div[1]/div[2]/div/table/tbody/tr[5]/td[4]")[0].text.strip(),
            ],
        }
        return data

    def parse_lottery_sabah_lotto88_4d(self, tab):
        lottery = tab.xpath("div/div[1]/div[3]/div[1]/div[1]/span/span")[0].text.strip()
        if lottery != "Sabah Lotto88 4D" or \
           tab.xpath("div/div[1]/div[3]/div[1]/div[2]/div/table/thead/tr[1]/th[1]")[0].attrib["class"].strip() not in ["firstLogo"] or \
           tab.xpath("div/div[1]/div[3]/div[1]/div[2]/div/table/thead/tr[2]/th[1]")[0].attrib["class"].strip() not in ["secondLogo"] or \
           tab.xpath("div/div[1]/div[3]/div[1]/div[2]/div/table/thead/tr[3]/th[1]")[0].attrib["class"].strip() not in ["thirdLogo"] or \
           tab.xpath("div/div[1]/div[3]/div[1]/div[2]/div/table/thead/tr[4]/th[1]/div")[0].text.strip() not in ["Special"] or \
           tab.xpath("div/div[1]/div[3]/div[1]/div[2]/div/table/thead/tr[4]/th[2]/div")[0].text.strip() not in ["Consolation"]:
               raise Exception("Fields are not in the correct format")
        data = {
            "lottery": lottery,
            "draw": tab.xpath("div/div[1]/div[3]/div[1]/div[1]/span/b[1]")[0].text.strip(),
            "id": tab.xpath("div/div[1]/div[3]/div[1]/div[1]/span/b[2]")[0].text.strip(),
            "1st": tab.xpath("div/div[1]/div[3]/div[1]/div[2]/div/table/thead/tr[1]/th[2]")[0].text.strip(),
            "2nd": tab.xpath("div/div[1]/div[3]/div[1]/div[2]/div/table/thead/tr[2]/th[2]")[0].text.strip(),
            "3rd": tab.xpath("div/div[1]/div[3]/div[1]/div[2]/div/table/thead/tr[3]/th[2]")[0].text.strip(),
            "special": [
                tab.xpath("div/div[1]/div[3]/div[1]/div[2]/div/table/tbody/tr[1]/td[1]")[0].text.strip(),
                tab.xpath("div/div[1]/div[3]/div[1]/div[2]/div/table/tbody/tr[1]/td[2]")[0].text.strip(),
                tab.xpath("div/div[1]/div[3]/div[1]/div[2]/div/table/tbody/tr[2]/td[1]")[0].text.strip(),
                tab.xpath("div/div[1]/div[3]/div[1]/div[2]/div/table/tbody/tr[2]/td[2]")[0].text.strip(),
                tab.xpath("div/div[1]/div[3]/div[1]/div[2]/div/table/tbody/tr[3]/td[1]")[0].text.strip(),
                tab.xpath("div/div[1]/div[3]/div[1]/div[2]/div/table/tbody/tr[3]/td[2]")[0].text.strip(),
                tab.xpath("div/div[1]/div[3]/div[1]/div[2]/div/table/tbody/tr[4]/td[1]")[0].text.strip(),
                tab.xpath("div/div[1]/div[3]/div[1]/div[2]/div/table/tbody/tr[4]/td[2]")[0].text.strip(),
                tab.xpath("div/div[1]/div[3]/div[1]/div[2]/div/table/tbody/tr[5]/td[1]")[0].text.strip(),
                tab.xpath("div/div[1]/div[3]/div[1]/div[2]/div/table/tbody/tr[5]/td[2]")[0].text.strip(),
            ],
            "consolation": [
                tab.xpath("div/div[1]/div[3]/div[1]/div[2]/div/table/tbody/tr[1]/td[3]")[0].text.strip(),
                tab.xpath("div/div[1]/div[3]/div[1]/div[2]/div/table/tbody/tr[1]/td[4]")[0].text.strip(),
                tab.xpath("div/div[1]/div[3]/div[1]/div[2]/div/table/tbody/tr[2]/td[3]")[0].text.strip(),
                tab.xpath("div/div[1]/div[3]/div[1]/div[2]/div/table/tbody/tr[2]/td[4]")[0].text.strip(),
                tab.xpath("div/div[1]/div[3]/div[1]/div[2]/div/table/tbody/tr[3]/td[3]")[0].text.strip(),
                tab.xpath("div/div[1]/div[3]/div[1]/div[2]/div/table/tbody/tr[3]/td[4]")[0].text.strip(),
                tab.xpath("div/div[1]/div[3]/div[1]/div[2]/div/table/tbody/tr[4]/td[3]")[0].text.strip(),
                tab.xpath("div/div[1]/div[3]/div[1]/div[2]/div/table/tbody/tr[4]/td[4]")[0].text.strip(),
                tab.xpath("div/div[1]/div[3]/div[1]/div[2]/div/table/tbody/tr[5]/td[3]")[0].text.strip(),
                tab.xpath("div/div[1]/div[3]/div[1]/div[2]/div/table/tbody/tr[5]/td[4]")[0].text.strip(),
            ],
        }
        return data

    def parse_lottery_sabah_lotto88_3d(self, tab):
        lottery = tab.xpath("div/div[1]/div[5]/div[1]/div[1]/span/span")[0].text.strip()
        if lottery != "Sabah Lotto88 3D" or \
           tab.xpath("div/div[1]/div[5]/div[1]/div[2]/div/table/thead/tr[1]/th[1]")[0].attrib["class"].strip() not in ["firstLogo"] or \
           tab.xpath("div/div[1]/div[5]/div[1]/div[2]/div/table/thead/tr[2]/th[1]")[0].attrib["class"].strip() not in ["secondLogo"] or \
           tab.xpath("div/div[1]/div[5]/div[1]/div[2]/div/table/thead/tr[3]/th[1]")[0].attrib["class"].strip() not in ["thirdLogo"]:
               raise Exception("Fields are not in the correct format")
        data = {
            "lottery": lottery,
            "draw": tab.xpath("div/div[1]/div[5]/div[1]/div[1]/span/b[1]")[0].text.strip(),
            "id": tab.xpath("div/div[1]/div[5]/div[1]/div[1]/span/b[2]")[0].text.strip(),
            "1st": tab.xpath("div/div[1]/div[5]/div[1]/div[2]/div/table/thead/tr[1]/th[2]")[0].text.strip(),
            "2nd": tab.xpath("div/div[1]/div[5]/div[1]/div[2]/div/table/thead/tr[2]/th[2]")[0].text.strip(),
            "3rd": tab.xpath("div/div[1]/div[5]/div[1]/div[2]/div/table/thead/tr[3]/th[2]")[0].text.strip(),
        }
        return data

    def parse_lottery_sabah_lotto88_6_45(self, tab):
        lottery = tab.xpath("div/div[1]/div[6]/div[1]/div[1]/span/span")[0].text.strip()
        if lottery != "Sabah Lotto88 6/45":
            raise Exception("Fields are not in the correct format")
        data = {
            "lottery": lottery,
            "draw": tab.xpath("div/div[1]/div[6]/div[1]/div[1]/span/b[1]")[0].text.strip(),
            "id": tab.xpath("div/div[1]/div[6]/div[1]/div[1]/span/b[2]")[0].text.strip(),
            "prize": [
                tab.xpath("div/div[1]/div[6]/div[1]/div[2]/div/table/tbody/tr/td[1]")[0].text.strip(),  
                tab.xpath("div/div[1]/div[6]/div[1]/div[2]/div/table/tbody/tr/td[2]")[0].text.strip(),
                tab.xpath("div/div[1]/div[6]/div[1]/div[2]/div/table/tbody/tr/td[3]")[0].text.strip(),
                tab.xpath("div/div[1]/div[6]/div[1]/div[2]/div/table/tbody/tr/td[4]")[0].text.strip(),
                tab.xpath("div/div[1]/div[6]/div[1]/div[2]/div/table/tbody/tr/td[5]")[0].text.strip(),
                tab.xpath("div/div[1]/div[6]/div[1]/div[2]/div/table/tbody/tr/td[6]")[0].text.strip(),
                tab.xpath("div/div[1]/div[6]/div[1]/div[2]/div/table/tbody/tr/td[7]")[0].text.strip(),
            ],
        }
        return data

    def parse_lottery_singapore_4d(self, tab):
        lottery = tab.xpath("div/div[1]/div[1]/div[1]/div[1]/span/span")[0].text.strip()
        if lottery != "Singapore 4D" or \
           tab.xpath("div/div[1]/div[1]/div[1]/div[2]/div/table/thead/tr[1]/th[1]")[0].attrib["class"].strip() not in ["firstLogo"] or \
           tab.xpath("div/div[1]/div[1]/div[1]/div[2]/div/table/thead/tr[2]/th[1]")[0].attrib["class"].strip() not in ["secondLogo"] or \
           tab.xpath("div/div[1]/div[1]/div[1]/div[2]/div/table/thead/tr[3]/th[1]")[0].attrib["class"].strip() not in ["thirdLogo"] or \
           tab.xpath("div/div[1]/div[1]/div[1]/div[2]/div/table/thead/tr[4]/th[1]/div")[0].text.strip() not in ["Special"] or \
           tab.xpath("div/div[1]/div[1]/div[1]/div[2]/div/table/thead/tr[4]/th[2]/div")[0].text.strip() not in ["Consolation"]:
               raise Exception("Fields are not in the correct format")
        data = {
            "lottery": lottery,
            "draw": tab.xpath("div/div[1]/div[1]/div[1]/div[1]/span/b[1]")[0].text.strip(),
            "id": tab.xpath("div/div[1]/div[1]/div[1]/div[1]/span/b[2]")[0].text.strip(),
            "1st": tab.xpath("div/div[1]/div[1]/div[1]/div[2]/div/table/thead/tr[1]/th[2]")[0].text.strip(),
            "2nd": tab.xpath("div/div[1]/div[1]/div[1]/div[2]/div/table/thead/tr[2]/th[2]")[0].text.strip(),
            "3rd": tab.xpath("div/div[1]/div[1]/div[1]/div[2]/div/table/thead/tr[3]/th[2]")[0].text.strip(),
            "special": [
                tab.xpath("div/div[1]/div[1]/div[1]/div[2]/div/table/tbody/tr[1]/td[1]")[0].text.strip(),
                tab.xpath("div/div[1]/div[1]/div[1]/div[2]/div/table/tbody/tr[1]/td[2]")[0].text.strip(),
                tab.xpath("div/div[1]/div[1]/div[1]/div[2]/div/table/tbody/tr[2]/td[1]")[0].text.strip(),
                tab.xpath("div/div[1]/div[1]/div[1]/div[2]/div/table/tbody/tr[2]/td[2]")[0].text.strip(),
                tab.xpath("div/div[1]/div[1]/div[1]/div[2]/div/table/tbody/tr[3]/td[1]")[0].text.strip(),
                tab.xpath("div/div[1]/div[1]/div[1]/div[2]/div/table/tbody/tr[3]/td[2]")[0].text.strip(),
                tab.xpath("div/div[1]/div[1]/div[1]/div[2]/div/table/tbody/tr[4]/td[1]")[0].text.strip(),
                tab.xpath("div/div[1]/div[1]/div[1]/div[2]/div/table/tbody/tr[4]/td[2]")[0].text.strip(),
                tab.xpath("div/div[1]/div[1]/div[1]/div[2]/div/table/tbody/tr[5]/td[1]")[0].text.strip(),
                tab.xpath("div/div[1]/div[1]/div[1]/div[2]/div/table/tbody/tr[5]/td[2]")[0].text.strip(),
            ],
            "consolation": [
                tab.xpath("div/div[1]/div[1]/div[1]/div[2]/div/table/tbody/tr[1]/td[3]")[0].text.strip(),
                tab.xpath("div/div[1]/div[1]/div[1]/div[2]/div/table/tbody/tr[1]/td[4]")[0].text.strip(),
                tab.xpath("div/div[1]/div[1]/div[1]/div[2]/div/table/tbody/tr[2]/td[3]")[0].text.strip(),
                tab.xpath("div/div[1]/div[1]/div[1]/div[2]/div/table/tbody/tr[2]/td[4]")[0].text.strip(),
                tab.xpath("div/div[1]/div[1]/div[1]/div[2]/div/table/tbody/tr[3]/td[3]")[0].text.strip(),
                tab.xpath("div/div[1]/div[1]/div[1]/div[2]/div/table/tbody/tr[3]/td[4]")[0].text.strip(),
                tab.xpath("div/div[1]/div[1]/div[1]/div[2]/div/table/tbody/tr[4]/td[3]")[0].text.strip(),
                tab.xpath("div/div[1]/div[1]/div[1]/div[2]/div/table/tbody/tr[4]/td[4]")[0].text.strip(),
                tab.xpath("div/div[1]/div[1]/div[1]/div[2]/div/table/tbody/tr[5]/td[3]")[0].text.strip(),
                tab.xpath("div/div[1]/div[1]/div[1]/div[2]/div/table/tbody/tr[5]/td[4]")[0].text.strip(),
            ],
        }
        return data

    def parse_lottery_singapore_6_45(self, tab):
        lottery = tab.xpath("div/div[1]/div[2]/div[1]/div[1]/span/span")[0].text.strip()
        if lottery != "Singapore 6/45":
            raise Exception("Fields are not in the correct format")
        data = {
            "lottery": lottery,
            "draw": tab.xpath("div/div[1]/div[2]/div[1]/div[1]/span/b[1]")[0].text.strip(),
            "id": tab.xpath("div/div[1]/div[2]/div[1]/div[1]/span/b[2]")[0].text.strip(),
            "prize": [
                tab.xpath("div/div/div[2]/div/div[2]/div/table[1]/tbody/tr/td[1]")[0].text.strip(),
                tab.xpath("div/div/div[2]/div/div[2]/div/table[1]/tbody/tr/td[2]")[0].text.strip(),
                tab.xpath("div/div/div[2]/div/div[2]/div/table[1]/tbody/tr/td[3]")[0].text.strip(),
                tab.xpath("div/div/div[2]/div/div[2]/div/table[1]/tbody/tr/td[4]")[0].text.strip(),
                tab.xpath("div/div/div[2]/div/div[2]/div/table[1]/tbody/tr/td[5]")[0].text.strip(),
                tab.xpath("div/div/div[2]/div/div[2]/div/table[1]/tbody/tr/td[6]")[0].text.strip(),
                tab.xpath("div/div/div[2]/div/div[2]/div/table[1]/tbody/tr/td[7]")[0].text.strip(),
            ],
        }
        return data


if __name__ == "__main__":
    parser = Parser4d88()
    parser.update_raw_data()
    parser.parse_raw_data()
