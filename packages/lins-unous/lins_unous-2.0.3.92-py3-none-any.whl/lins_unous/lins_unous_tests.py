from random import randint

import pytest


def test_instancia_api_unous_deve_notificar_url_clean_up(
    api_unous,
    requisicao_get_positiva_mockada,
    resposta_positiva_requisicao,
    unous_token,
    mocker,
):
    resposta_positiva_requisicao._content = '{"StatusReply": 0}'.encode('UTF-8')
    mocker.patch('lins_unous.lins_unous.ApiUnous.get', return_value=resposta_positiva_requisicao)
    response = api_unous.notificar()
    saida_esperada = {'ok': True, 'notificou': True}
    assert response == saida_esperada


@pytest.mark.parametrize(
    'integracao',
    [
        'integrar_produtos',
        'integrar_produtos_tamanhos',
        'integrar_fornecedores',
        'integrar_pedidos',
        'integrar_lojas',
        'integrar_lojas_info',
        'integrar_metricas',
    ],
)
def test_integracao_deve_ser_efetuada_corretamente(
    integracao,
    api_unous,
    requisicao_post_positiva_mockada,
    capsys,
    mocked_sleep,
):
    dados = [{}] * randint(10000, 100000)
    integracao = getattr(api_unous, integracao)
    integracao(dados)
    log = capsys.readouterr()
    requisicao_post_positiva_mockada.assert_called()
    assert f'{len(dados)} REGISTROS INTEGRADOS' in log.out
