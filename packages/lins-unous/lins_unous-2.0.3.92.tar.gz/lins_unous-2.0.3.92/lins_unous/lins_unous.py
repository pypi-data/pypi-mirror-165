import decimal
import json
import os
import time

from .unous_requests import UnousRequests


class ApiUnous(UnousRequests):
    _grant_type = 'password'
    _client_id = 'userIntegration'
    _mindset_user = os.environ.get('MINDSET_USER')
    _mindset_pass = os.environ.get('MINDSET_PASS')
    _mindset_url = os.environ.get('MINDSET_URL')
    _mindset_notify_url = os.environ.get('MINDSET_NOTIFY_URL')
    show_log = True

    @property
    def headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self._get_token()}',
        }

    def integrar_produtos(self, dados):
        return self._integrar(dados, '/StageContent/api/Product/Post')

    def integrar_produtos_tamanhos(self, dados):
        return self._integrar(dados, '/StageContent/api/ProductSize/Post')

    def integrar_fornecedores(self, dados):
        return self._integrar(dados, '/StageContent/api/Supplier/Post')

    def integrar_pedidos(self, dados):
        return self._integrar(dados, '/StageMetrics/api/OpenOrder/Post')

    def integrar_lojas(self, dados):
        return self._integrar(dados, '/StageContent/api/Location/Post')

    def integrar_lojas_info(self, dados):
        return self._integrar(dados, '/StageContent/api/StoreInfo/Post')

    def integrar_metricas(self, dados):
        return self._integrar(dados, '/StageMetrics/api/Metric/Post')

    def integrar_pedidos_sku(self, dados):
        return self._integrar(dados, '/StageAllocation/api/OrderSkuData/Post')

    def integrar_cluster_pedidos_sku(self, dados):
        return self._integrar(dados, '/StageAllocation/api/OrderClusterSkuData/Post')

    def integrar_grade_pedidos_sku(self, dados):
        return self._integrar(dados, '/StageAllocation/api/GridAllocationModelOpenOrderDcSku/Post')

    def integrar_grade_disponiveis_cd(self, dados):
        return self._integrar(dados, '/StageAllocation/api/GridAllocationModelDcSku/Post')

    def integrar_sku_disponiveis_cd(self, dados):
        return self._integrar(dados, '/StageAllocation/api/DCPositionSKUAlloc/Post')

    def integrar_pedidos_packs_serem_alocados(self, dados):
        return self._integrar(dados, '/StageAllocation/api/OrderPackData/Post')

    def integrar_cluster_pedidos_packs_serem_alocados(self, dados):
        return self._integrar(dados, '/StageAllocation/api/OrderPackClusterData/Post')

    def integrar_produtos_atendimento_cd(self, dados):
        return self._integrar(dados, '/StageAllocation/api/OrderInDistribution/Post')

    def integrar_grade_pedidos_pack(self, dados):
        return self._integrar(dados, '/StageAllocation/api/GridAllocationModelOpenOrderPack/Post')

    def integrar_posicao_estoque_sku(self, dados):
        return self._integrar(dados, '/StageAllocation/api/DCPositionSKUAlloc/Post')

    def notificar(self):
        params = {
            'EnterpriseKey': self._mindset_user,
            'enterprisePwd': self._mindset_pass,
            'jobName': 'CleanUpJob',
        }
        response = self.get(url=self._mindset_notify_url, params=params)
        return {
            'ok': response.ok,
            'notificou': response.json().get('StatusReply', '') == 0,
        }

    def _integrar(self, dados, url_endpoint):
        url, total_registros = self._mindset_url + url_endpoint, 0
        for lote in self.cria_lotes(dados):
            while not self.posta_lote_na_unous(url=url, lote=lote).ok:
                time.sleep(5)
                continue
            total_registros += len(lote)
        print(f'{total_registros} REGISTROS INTEGRADOS')
        print('-'*42)

    def limpar_pedidos(self):
        url = self._mindset_url + '/StageMetrics/api/OpenOrder/GetClearAllData'
        self.get(url=url, headers=self.headers)

    def _get_token(self):
        response = self.get(
            url=self._mindset_url + '/Auth/token',
            data={
                'grant_type': self._grant_type,
                'username': self._mindset_user,
                'password': self._mindset_pass,
                'client_id': self._client_id,
            }
        )
        if not response.ok:
            raise ValueError(f'Erro ao obter o token de acesso! Status: {response.status_code}')
        return json.loads(response.text).get('access_token')

    def posta_lote_na_unous(self, url, lote):
        return self.post(url=url, data=json.dumps(lote, cls=DecimalEncoder), headers=self.headers)

    def cria_lotes(self, dados, tamanho=int(os.environ.get('TAMANHO_LOTE_PARA_POSTAGEM_UNOUS', 10000))):
        for i in range(0, len(dados), tamanho):
            yield dados[i:i + tamanho]


class DecimalEncoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)
