import sys
from pathlib import Path

# Add src to path for testing
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

def test_imports():
    import core.model_runner as mr
    import core.gdx_io as gi
    assert hasattr(mr, 'run_gams')
    assert hasattr(gi, 'read_gdx')
