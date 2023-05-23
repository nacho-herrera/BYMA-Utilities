import json
from typing import Any, Dict, Optional

import requests

import urls
from enums import Monedas, Movimientos, Segmentos, TipoMovimiento


class SLYC:
    """
        Libreria para consumir las APIS del sistema de Liquidacion y Compensacion de BYMA
    """
    
    def __init__(self, participante: str, username: str, password: str) -> None:
        """
        Inicializa la libreria, identificando participante, usuario y password para el ingreso al sistema

        Args:
            participante (str): nro de participante byma
            username (str): usuario
            password (str): password
        """
        self.participante: str = participante
        self.username: str = username
        self.password: str = password
        self.session: requests.Session = self._create_session()
        self.login()

    def login(self) -> None:
        """
        Loguea el usuario
        """
        data = json.dumps({"user": self.username, "password": self.password})
        response = self._request("post", urls.slyc_login, data)
        headers_update = {
            "Authorization": response["token"],
            "Referer": "https://liquidaciones.sba.com.ar/liquidaciones/liquidaciones/detalle-de-obligaciones/movimientos-y-obligaciones",
        }
        self._update_headers(headers_update)

    def get_bancos(self, usuario: str = "") -> Dict[str,Any]:
        """_summary_

        Args:
            usuario (str, optional): _description_. Defaults to "".

        Returns:
            Dict[str,Any]: _description_
        """
        if not usuario:
            usuario = self.username
        data = json.dumps(
            { 
            "IvAlta": "", 
            "IvEliminar": "", 
            "IvModificar": "", 
            "IvEsPpte": "X", 
            "IvUsuario": usuario, 
            "TtBancos": "" }
        )
        return self._request("post", urls.slyc_bancos, data)

    def get_conceptos(self, usuario: str = "") -> Dict[str,Any]:
        """_summary_

        Args:
            usuario (str, optional): _description_. Defaults to "".

        Returns:
            Dict[str,Any]: _description_
        """
        if not usuario:
            usuario = self.username
        data = json.dumps(
            {
             "IvUsuario": usuario 
            }
        )
        return self._request("post", urls.slyc_conceptos, data)
    
    def get_participantes(self, participante:str = "", usuario: str = "") -> Dict[str,Any]:
        """_summary_

        Args:
            usuario (str, optional): _description_. Defaults to "".

        Returns:
            Dict[str,Any]: _description_
        """
        if not participante:
            participante = self.participante
        if not usuario:
            usuario = self.username
        data = json.dumps(
            {
                "IvEsPpte": "X", 
                "IvPpte": participante, 
                "IvUsuario": usuario}
        )
        return self._request("post", urls.slyc_participantes, data)
    
    def get_reportes(self, participante:str = "", usuario: str = "") -> Dict[str,Any]:
        """_summary_

        Args:
            usuario (str, optional): _description_. Defaults to "".

        Returns:
            Dict[str,Any]: _description_
        """
        if not participante:
            participante = self.participante
        if not usuario:
            usuario = self.username
        data = json.dumps(
            {
                "IvEsPpte": "X", 
                "IvFecha": "", 
                "IvPpte": participante, 
                "IvUsuario": usuario
            }
        )
        return self._request("post", urls.slyc_reportes, data)
    
    def get_estado_de_liquidacion(
        self, fecha: str = "", participante: str = ""
    ) -> Dict[str, Any]:
        """_summary_

        Args:
            fecha (str, optional): _description_. Defaults to "".
            participante (str, optional): _description_. Defaults to "".

        Returns:
            Dict[str, Any]: _description_
        """
        if not participante:
            participante = self.participante
        data = json.dumps({"Ifecha": fecha, "IidPpte": participante})
        return self._request("post", urls.slyc_estado_liquidacion, data)

    def get_especie_participante(
        self,
        fecha: str = "",
        participante: str = "",
        segmento: Segmentos = Segmentos.TOTAL,
    ) -> Dict[str, Any]:
        """_summary_

        Args:
            fecha (str, optional): _description_. Defaults to "".
            participante (str, optional): _description_. Defaults to "".
            segmento (Segmentos, optional): _description_. Defaults to Segmentos.TOTAL.

        Returns:
            Dict[str, Any]: _description_
        """
        if not participante:
            participante = self.participante
        data = json.dumps(
            {"IFecha": fecha, "IIdPpte": participante, "ISegmento": segmento.value}
        )
        return self._request("post", urls.slyc_especie_participante, data)

    def get_estado_moneda(
        self, moneda: Monedas = Monedas.PESOS, fecha: str = "", participante: str = ""
    ) -> Dict[str, Any]:
        """_summary_

        Args:
            moneda (Monedas, optional): _description_. Defaults to Monedas.PESOS.
            fecha (str, optional): _description_. Defaults to "".
            participante (str, optional): _description_. Defaults to "".

        Returns:
            Dict[str, Any]: _description_
        """
        if not participante:
            participante = self.participante

        data = json.dumps(
            {
                "IFecha": fecha,
                "IvMoneda": moneda.value,
                "IvParticipante": participante,
            }
        )
        return self._request("post", urls.slyc_estado_moneda, data)

    def get_estado_especie(
        self, fecha: str = "", participante: str = "", especie: str = ""
    ) -> Dict[str, Any]:
        """_summary_

        Args:
            fecha (str, optional): _description_. Defaults to "".
            participante (str, optional): _description_. Defaults to "".
            especie (str, optional): _description_. Defaults to "".

        Returns:
            Dict[str, Any]: _description_
        """
        if not participante:
            participante = self.participante

        data = json.dumps(
            {"Icodespe": especie, "IidPpte": participante, "IvFecha": fecha}
        )
        return self._request("post", urls.slyc_estado_especie, data)
    
    def get_saldos_especie(self, especie: str = "", participante: str = "", subcuenta: str = "", usuario: str = "") -> Dict[str, Any]:
        if not participante:
            participante = self.participante
        if not usuario:
            usuario = self.username
        data = json.dumps(
            {
                "IvCodespe": especie, 
                "IvPpte": participante, 
                "IvSubcuenta": subcuenta, 
                "IvUsuario": usuario}
        )
        return self._request("post", urls.slyc_saldos_especie, data)
    
    def get_titulos_liq_contraparte(
        self,
        contraparte: str = "",
        fecha: str = "",
        moneda: Monedas = Monedas.PESOS,
        participante: str = "",
        usuario: str = "",
    ) -> Dict[str, Any]:
        """_summary_

        Args:
            contraparte (str, optional): _description_. Defaults to "".
            fecha (str, optional): _description_. Defaults to "".
            moneda (Monedas, optional): _description_. Defaults to Monedas.PESOS.
            participante (str, optional): _description_. Defaults to "".
            usuario (str, optional): _description_. Defaults to "".

        Returns:
            Dict[str, Any]: _description_
        """
        if not participante:
            participante = self.participante
        if not usuario:
            usuario = self.username

        data = json.dumps(
            {
                "IvContraparte": contraparte,
                "IvFecha": fecha,
                "IvMoneda": moneda.value,
                "IvParticipante": participante,
                "IvUsuario": usuario,
            }
        )
        return self._request("post", urls.slyc_titulos_liq_contraparte, data)    
    
    def get_obligaciones_contraparte_especie(
        self,
        contraparte: str = "",
        especie: str = "",
        fecha: str = "",
        participante: str = "",
    ) -> Dict[str, Any]:
        """_summary_

        Args:
            contraparte (str, optional): _description_. Defaults to "".
            especie (str, optional): _description_. Defaults to "".
            fecha (str, optional): _description_. Defaults to "".
            participante (str, optional): _description_. Defaults to "".

        Returns:
            Dict[str, Any]: _description_
        """
        if not participante:
            participante = self.participante

        data = json.dumps(
            {
                "IvCpte": contraparte,
                "IvEsPpte": "X",
                "IvEspea": especie,
                "IvFecha": fecha,
                "IvPpte": participante,
            }
        )
        return self._request("post", urls.slyc_obligaciones_contraparte_especie, data)   
    
    def get_movimientos_obligaciones(
        self,
        moneda: Monedas = Monedas.PESOS,
        fecha: str = "",
        participante: str = "",
        usuario: str = "",
        especie: str = "",
        concepto: str = "",
        tipo_movimiento: Movimientos = Movimientos.TODOS,
    ) -> Dict[str, Any]:
        """_summary_

        Args:
            moneda (Monedas, optional): _description_. Defaults to Monedas.PESOS.
            fecha (str, optional): _description_. Defaults to "".
            participante (str, optional): _description_. Defaults to "".
            usuario (str, optional): _description_. Defaults to "".
            especie (str, optional): _description_. Defaults to "".
            concepto (str, optional): _description_. Defaults to "".
            tipo_movimiento (Movimientos, optional): _description_. Defaults to Movimientos.TODOS.

        Returns:
            Dict[str, Any]: _description_
        """


        data = json.dumps(
            {
                "Icodespe": especie,
                "Iconcepto": concepto,
                "Itipmov": tipo_movimiento.value,
                "Imoneda": moneda.value,
                "IidPpte": participante,
                "IvFecha": fecha,
                "IvUsuario": usuario,
            }
        )
        return self._request("post", urls.slyc_movimientos_obligaciones, data)

    def get_fondos_aplicados(self, agente: str = None, moneda:Monedas=Monedas.PESOS, participante:str="", usuario:str="") -> Dict[str, Any]:
        if not participante:
            participante = self.participante
        if not usuario:
            usuario = self.username
        data = json.dumps(
            {
                "IvAgente": agente,
                "IvMoneda": moneda, 
                "IvPpte": participante, 
                "IvUsuario": usuario
            }
        )
        return self._request("post", urls.slyc_fondos_aplicados, data)

    def get_movimientos_registrado(
        self,
        agente: str = None,
        banco: str = "",
        fecha: str = "",
        moneda: Monedas = Monedas.PESOS,
        participante: str = "",
        tipo_movimiento: TipoMovimiento = TipoMovimiento.TODOS,
        usuario: str = "",
    ) -> Dict[str, Any]:
        """_summary_

        Args:
            agente (str, optional): _description_. Defaults to None.
            banco (str, optional): _description_. Defaults to "".
            fecha (str, optional): _description_. Defaults to "".
            moneda (Monedas, optional): _description_. Defaults to Monedas.PESOS.
            participante (str, optional): _description_. Defaults to "".
            tipo_movimiento (TipoMovimiento, optional): _description_. Defaults to TipoMovimiento.TODOS.
            usuario (str, optional): _description_. Defaults to "".

        Returns:
            Dict[str, Any]: _description_
        """
        if not participante:
            participante = self.participante
        if not usuario:
            usuario = self.username

        data = json.dumps(
            {
                "IvAgente": agente,
                "IvBanco": banco,
                "IvFecha": fecha,
                "IvMoneda": moneda.value,
                "IvPpte": participante,
                "IvTipoMov": tipo_movimiento.value,
                "IvUsuario": usuario,
            }
        )
        return self._request("post", urls.slyc_movimientos_registrados, data)

    def get_feriados(self) -> Dict[str, Any]:
        """_summary_

        Returns:
            Dict[str, Any]: _description_
        """
        data = json.dumps({"EtCalendario": None})
        return self._request("post", urls.slyc_feriados, data)
    
    def get_fecha_sistema(self) -> Dict[str, Any]:
        """_summary_

        Returns:
            Dict[str, Any]: _description_
        """
        data = json.dumps({"observe": "response"})
        return self._request("post", urls.slyc_fecha_sistema, data) 
        
    def get_mensajes_notificacion(self, participante: str = "") -> Dict[str, Any]:
        """_summary_

        Args:
            participante (str, optional): _description_. Defaults to "".

        Returns:
            Dict[str, Any]: _description_
        """
        if not participante:
            participante = self.participante
        data = json.dumps({"IvPpte": participante})
        return self._request("post", urls.slyc_mensajes, data)

    def _create_session(self) -> None:
        """_summary_

        Returns:
            _type_: _description_
        """
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36",
            "Content-Type": "application/json",
            "Referer": "https://liquidaciones.sba.com.ar/",
        }
        self.session = requests.Session()
        self._update_headers(headers)
        return self.session

    def _update_session_headers(self, headers: dict) -> None:
        """_summary_

        Args:
            headers (dict): _description_
        """
        self.session.headers.update(headers)

    def _request(
        self, method: str, url: str, data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
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
            return response.json()

        except requests.exceptions.RequestException as e:
            print(f"An error occurred during the request: {e}")
            return {}
