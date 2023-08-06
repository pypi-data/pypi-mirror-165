"""Integration test for the etl service."""

from waylay.service import ETLService


def test_etl_import_get(waylay_etl: ETLService):
    """Test connectivity with the etl_import status endpoint."""
    assert waylay_etl.root_url is not None
    assert waylay_etl.root_url.endswith('/etl/v1')
    import_status_resp = waylay_etl.etl_import.get()
    assert import_status_resp is not None
    assert 'domain' in import_status_resp
    assert 'status' in import_status_resp
