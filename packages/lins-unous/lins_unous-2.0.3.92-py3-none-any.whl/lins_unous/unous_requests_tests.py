from re import findall

import pytest

from .unous_requests import UnousRequests


@pytest.mark.parametrize('method', ['GET', 'POST'])
def test_requisicao_deve_ser_efetuada_corretamente(
    method,
    requisicao_get_positiva_mockada,
    requisicao_post_positiva_mockada,
):
    ur = UnousRequests()
    request_method = getattr(ur, method.lower())
    response = request_method('http://requestb.in')
    assert response.ok is True


@pytest.mark.parametrize('method', ['GET', 'POST'])
def test_log_deve_ser_exibido_se_requisicao_gerar_excecao(
    method,
    capsys,
    requisicao_get_negativa_mockada,
    requisicao_post_negativa_mockada,
):
    ur = UnousRequests()
    method = getattr(ur, method.lower())
    method('http://requestb.in', timeout=000.1)
    read_timeout = capsys.readouterr()
    regex = r'Um\s\w+\socorreu\sao\sexecutar\sum\s(?:GET|POST)\sna\surl\shtt(?:ps|p):\W+\w+.\w+'
    assert findall(regex, read_timeout.out)


@pytest.mark.parametrize('method', ['GET', 'POST'])
def test_requisicao_get_deve_falhar_se_o_tempo_resposta_exceder(
    method,
    requisicao_get_negativa_mockada,
    requisicao_post_negativa_mockada,
):
    ur = UnousRequests()
    method = getattr(ur, method.lower())
    response = method('http://requestb.in', timeout=000.1)
    assert not response.ok


