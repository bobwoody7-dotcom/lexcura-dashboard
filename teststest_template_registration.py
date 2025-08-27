# tests/test_template_registration.py
# UI-REFACTOR-GOLD-2025: Template system tests

import pytest
import plotly.io as pio
from plotly_templates import register_gold_dark_template

def test_template_registration():
    """Test that gold_dark template registers correctly"""
    register_gold_dark_template()
    
    # Verify template exists
    assert "gold_dark" in pio.templates
    
    # Verify it's set as default
    assert pio.templates.default == "gold_dark"
    
    # Verify key properties
    template = pio.templates["gold_dark"]
    assert template.layout.paper_bgcolor == "#0F1113"
    assert template.layout.plot_bgcolor == "#0F1113"
    assert template.layout.font.color == "#F5F6F7"

def test_template_idempotent():
    """Test that multiple calls don't break anything"""
    register_gold_dark_template()
    register_gold_dark_template()  # Should not error
    
    assert pio.templates.default == "gold_dark"

if __name__ == "__main__":
    pytest.main([__file__])