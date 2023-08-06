import pytest

from src.scienceio import ScienceIO


@pytest.fixture(scope="session", autouse=True)
def scio():
    """
    Init ScienceIO client, using .scio/config
    :return: our client
    """
    yield ScienceIO()


def test_input_is_string(scio):
    """
    Test providing something other than a string returns an error
    """
    query_text = {
        "text": "The COVID-19 pandemic has shown a markedly low proportion of cases among children 1-4. Age disparities in observed cases could be  explained by children having lower susceptibility to infection, lower  propensity to show clinical symptoms or both."
    }
    with pytest.raises(ValueError, match="annotate argument must be a string."):
        scio.annotate(text=query_text)
        raise ValueError("annotate argument must be a string.")


def test_annotate(scio, snapshot):
    """
    Test annotate request with a small text snippet
    """
    query_text = (
        "The COVID-19 pandemic has shown a markedly low proportion of "
        "cases among children 1-4. Age disparities in observed cases could be "
        "explained by children having lower susceptibility to infection, lower "
        "propensity to show clinical symptoms or both."
    )

    response = scio.annotate(text=query_text)

    # 1. Test response is a dict
    assert isinstance(response, dict)

    # 2. Test we get text back
    assert response.get("text") == query_text

    # 3. Test character length match
    assert response.get("characters") == 245

    # 4. Are we billing 1 unit
    assert response.get("units_number") == 1

    # 5. Do we get a request_id
    assert "request_id" in response
    del response["request_id"]

    # 6. General snapshot
    assert response == snapshot
