# plotly_templates.py
# UI-REFACTOR-GOLD-2025: Executive dashboard template system

import plotly.graph_objects as go
import plotly.io as pio

def register_gold_dark_template():
    """Register and set the gold_dark template as default for executive dashboards.
    
    Idempotent function - safe to call multiple times.
    Applies consistent dark theme with metallic gold accents across all Plotly charts.
    """
    if "gold_dark" in pio.templates:
        pio.templates.default = "gold_dark"
        return
    
    template = go.layout.Template(
        layout=go.layout.Layout(
            paper_bgcolor="#0F1113",
            plot_bgcolor="#0F1113",
            font=dict(family="Inter, Roboto, system-ui", color="#F5F6F7", size=12),
            colorway=["#D4AF37", "#FFCF66", "#6C757D", "#3DBC6B", "#E4574C"],
            
            # Axes styling
            xaxis=dict(
                color="#B8B9BB", 
                gridcolor="rgba(255,255,255,0.04)",
                ticklen=4,
                zeroline=False,
                tickfont=dict(size=11)
            ),
            yaxis=dict(
                color="#B8B9BB", 
                gridcolor="rgba(255,255,255,0.04)",
                ticklen=4,
                zeroline=False,
                tickfont=dict(size=11)
            ),
            
            # Legend and hover
            legend=dict(
                orientation="h", 
                yanchor="bottom", 
                y=1.02, 
                xanchor="right", 
                x=1,
                font=dict(size=11),
                bgcolor="rgba(0,0,0,0)"
            ),
            hoverlabel=dict(
                bgcolor="#121314", 
                bordercolor="rgba(255,255,255,0.06)", 
                font=dict(color="#F5F6F7", size=11),
                borderwidth=1
            ),
            
            # Layout defaults
            margin=dict(l=40, r=20, t=40, b=40),
            hovermode="x unified",
            
            # Title styling
            title=dict(
                font=dict(size=16, color="#F5F6F7"),
                x=0.5,
                xanchor="center"
            )
        )
    )
    
    pio.templates["gold_dark"] = template
    pio.templates.default = "gold_dark"

def apply_executive_styling(fig):
    """Apply executive dashboard styling to any Plotly figure."""
    fig.update_layout(template="gold_dark")
    fig.update_traces(marker_line_width=0)  # Clean edges
    return fig