"""Smoke tests do Streamlit (executados pelo GitHub Actions, pois dependem do Streamlit)."""
from pathlib import Path
import pytest

streamlit = pytest.importorskip("streamlit")
from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]

@pytest.mark.skipif(not (ROOT / 'data' / 'clean' / 'dataset.csv').is_file(),
                    reason='CSV real é preparado no CI antes do teste.')
def test_app_ambos_dashboards_carregam():
    app = AppTest.from_file(str(ROOT / 'app.py')).run(timeout=90)
    assert not app.exception, [e.message for e in app.exception]
    assert len(app.tabs) == 2
    assert len(app.sidebar.multiselect) >= 3
    assert len(app.sidebar.slider) >= 1

@pytest.mark.skipif(not (ROOT / 'data' / 'clean' / 'dataset.csv').is_file(),
                    reason='CSV real é preparado no CI antes do teste.')
def test_app_zero_variaveis_nao_quebra():
    app = AppTest.from_file(str(ROOT / 'app.py')).run(timeout=90)
    app.sidebar.multiselect[0].set_value([]).run(timeout=90)
    assert not app.exception, [e.message for e in app.exception]
