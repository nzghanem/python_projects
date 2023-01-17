from bs4 import BeautifulSoup
import requests


class data:
    def __init__(self, url):
        self.url = url

    def __iter__(self):
        return iter(self.get_specializations_info())

    def get_specializations_urls(self, url):
        soup = BeautifulSoup(requests.get(
            url).content, 'html.parser')

        items = soup.find_all(class_='link', href=True)

        available_specializations = [
            "https://fit.cvut.cz"+item['href']+"/study-plan" for item in items]

        return available_specializations

    def get_specializations_info(self):
        specializations = self.get_specializations_urls(self.url)
        specializations_details = []
        for specialization in range(len(specializations)):
            soup = BeautifulSoup(requests.get(
                specializations[specialization]).content, 'html.parser')

            specializations_details.append([str(soup.title).replace(
                "<title>", "").replace(" - FIT CTU</title>", ""), []])

            for t in range(6):
                semesters = soup.find_all(class_='entry')
                semesters = [str(item.find('h2')).replace(
                    "<h2>", "").replace("</h2>", "") for item in semesters]
                semesters = semesters[:6]
                for i, item in enumerate(semesters):
                    semesters[i] = item.split(" ")[1].title() + f" {i+1}"
                specializations_details[-1][-1].append([semesters[t]])

            subjects_details = soup.find_all(class_='subjects')
            subjects_details = [str(subject.find_all('td')).replace(
                "<td>", "").replace("</td>", "") for subject in subjects_details]
            subjects_details = subjects_details[:6]

            for item in range(len(subjects_details)):
                sub_item = [[]]
                subjects_details[item] = subjects_details[item] .replace(
                    "[", "").replace("]", "").split(", ")
                for i in range(len(subjects_details[item])):
                    if "<a" in subjects_details[item][i]:
                        lis = subjects_details[item][i].split("=")
                        subjects_details[item][i] = [lis[1][1:].replace(
                            '" target', ''), lis[-1].split(">")[0][1:].replace('"', '')]
                    try:
                        if int(subjects_details[item][i]):
                            sub_item[-1].append(subjects_details[item][i])
                            sub_item.append([])
                    except:
                        sub_item[-1].append(subjects_details[item][i])
                specializations_details[specialization][1][item].append(
                    sub_item[:6])
        return specializations_details
