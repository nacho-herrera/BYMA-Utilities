from time import sleep
from typing import Any, Dict, Optional

import requests
from bs4 import BeautifulSoup

import constants
import file_utils
import urls
from exceptions import DADI_Exception


class DADI:
    """ 
        Libreria para descargar los informes disponibles en DADI para un rango de fechas. 
        Tiene un control para no volver a descargar informes ya descargados.
    """
    download_folder = constants.DADI_DOWNLOAD_FOLDER
    downloaded_files_list = constants.DADI_DOWNLOADED_FILES_PATH
    
    def __init__(self, username: str = "", password: str = ""):
        """_summary_

        Args:
            username (str, optional): _description_. Defaults to "".
            password (str, optional): _description_. Defaults to "".
        """
        self.username = username
        self.password = password
        self.session = requests.Session()
        self._update_headers()
        self._check_if_file_exists(self.save_path)

    def login(self) -> requests.Response:
        """_summary_

        Returns:
            requests.Response: _description_
        """
        url = urls.dadi_login
        data = {"user": self.username, "pass": self.password}
        response = self._request("post", url, data)
        return response

    def get_reports_in_range(self, date_start: str, date_end: str) -> requests.Response:
        """_summary_

        Args:
            date_start (str): _description_
            date_end (str): _description_

        Returns:
            requests.Response: _description_
        """
        url = urls.dadi_listado
        data = {"stringDesde": date_start, "stringHasta": date_end}
        response = self._request("post", url, data)
        return response

    def create_list_of_reports(
        self, report_range: requests.Response
    ) -> list[Dict[str, Any]]:
        """_summary_

        Args:
            report_range (requests.Response): _description_

        Returns:
            list[Dict[str, Any]]: _description_
        """
        soup = BeautifulSoup(report_range.content, "html.parser")
        table = soup.find("table", {"id": "tablaDocs"})
        links = table.find_all("a", {"id": "elNombre"})

        headers = [header.get_text().strip().lower() for header in table.find_all("th")]
        rows = table.find_all("tr")[1:]

        list_results = [
            {
                headers[column]: cell.get_text()
                .strip()
                .replace("\r", "")
                .replace("\n", "")
                .replace("\t", "")
                for column, cell in enumerate(row.find_all("td"))
            }
            | {"url": f'{urls.dadi_base}{link["href"]}'}
            for link, row in zip(links, rows)
        ]

        return list_results

    def download_new_files(self, new_files_list: list[Dict[str, Any]]) -> None:
        """_summary_

        Args:
            new_files_list (list[Dict[str, Any]]): _description_
        """
        with open(self.downloaded_files_list, "r") as file:
            downloaded_files = set(file.read().splitlines())

        for file in new_files_list:
            filename = file["nombre"]
            if filename not in downloaded_files:
                print(filename)
                url = file["url"]
                response = self.session.get(url)
                sleep(3)
                if response.status_code == 200:
                    with open(rf"{self.download_folder}/{filename}", "wb") as file:
                        file.write(response.content)
                    print(f"Downloaded: {filename}")
                else:
                    print(f"Failed to download: {filename}")

        downloaded_files.update(file["nombre"] for file in new_files_list)

        with open(self.downloaded_files_list, "w") as file:
            file.write("\n".join(downloaded_files))

    def _check_if_file_exists(self, file_path: str) -> None:
        """_summary_

        Args:
            file_path (str): _description_
        """
        file_utils.create_file_if_not_exists(file_path)

    def _update_headers(self) -> None:
        """_summary_
        """
        headers = {
            #"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            #"Accept-Language": "en-US,en;q=0.9,es-419;q=0.8,es;q=0.7,pt;q=0.6",
            #"Cache-Control": "max-age=0",
            #"Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded",
            #"Origin": "https://dadi.sba.com.ar",
            "Referer": "https://dadi.sba.com.ar/dadi/login.do",
            #"Sec-Fetch-Dest": "document",
            #"Sec-Fetch-Mode": "navigate",
            #"Sec-Fetch-Site": "same-origin",
            #"Sec-Fetch-User": "?1",
            #"Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
            #"sec-ch-ua": '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
            #"sec-ch-ua-mobile": "?0",
            #"sec-ch-ua-platform": '"Windows"',
        }
        self.session.headers.update(headers)

    def _request(
        self, method: str, url: str, data: Optional[Dict[str, Any]] = None
    ) -> requests.Response:
        """_summary_

        Args:
            method (str): _description_
            url (str): _description_
            data (Optional[Dict[str, Any]], optional): _description_. Defaults to None.

        Returns:
            Dict[str, Any]: _description_
        """
        try:
            if method == "get":
                response = self.session.get(url)
            elif method == "post":
                response = self.session.post(url, data)
            elif method == "put":
                response = self.session.put(url, data)
            else:
                raise ValueError(f"Invalid HTTP method: {method}")

            response.raise_for_status()  # Raise an exception if the response status is an error
            return response

        except requests.exceptions.RequestException as e:
            raise DADI_Exception(f"An error occurred during the request: {e}")
