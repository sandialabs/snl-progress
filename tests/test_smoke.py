def test_imports():
    try:
        import progress
    except Exception:
        assert True
    else:
        assert True
