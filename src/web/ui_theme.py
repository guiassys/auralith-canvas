"""
Custom Gradio theme for Auralith with a metallic, industrial aesthetic.
"""
import gradio as gr
from gradio.themes.base import Base
from gradio.themes.utils import colors, fonts, sizes

class AuralithMetalTheme(Base):
    def __init__(self):
        super().__init__(
            primary_hue=colors.slate,
            secondary_hue=colors.gray,
            neutral_hue=colors.zinc,
            spacing_size=sizes.spacing_md,
            radius_size=sizes.radius_sm,
            font=fonts.GoogleFont("Inter"),
        )
        self.name = "auralith_metal_theme"
        self.set(
            # --- Base (Metal Dark) ---
            body_background_fill="#0f1114",
            body_background_fill_dark="#0f1114",
            body_text_color="#d1d5db",
            body_text_color_dark="#d1d5db",

            # --- Panels ---
            background_fill_primary="#1a1d21",
            background_fill_primary_dark="#1a1d21",
            background_fill_secondary="#2a2f36",
            background_fill_secondary_dark="#2a2f36",

            # --- Borders (Steel look) ---
            border_color_primary="#3f4650",
            border_color_primary_dark="#3f4650",
            border_color_accent="#8b949e",
            border_color_accent_dark="#8b949e",

            # --- Soft accent ---
            color_accent_soft="#2f3742",
            color_accent_soft_dark="#2f3742",

            # --- Buttons (Brushed Metal Effect) ---
            button_primary_background_fill="""
                linear-gradient(180deg, #5a616b 0%, #2f343b 50%, #1c1f24 100%)
            """,
            button_primary_background_fill_dark="""
                linear-gradient(180deg, #5a616b 0%, #2f343b 50%, #1c1f24 100%)
            """,
            button_primary_text_color="#e5e7eb",
            button_primary_text_color_dark="#e5e7eb",

            # --- Sliders ---
            slider_color="#9aa4af",
            slider_color_dark="#9aa4af",

            # --- Inputs ---
            input_background_fill="#1c1f24",
            input_background_fill_dark="#1c1f24",
            input_border_color="#3f4650",
            input_border_color_dark="#3f4650",
            input_placeholder_color="#6b7280",
            input_placeholder_color_dark="#6b7280",
        )

auralith_theme = AuralithMetalTheme()

custom_css = """
/* --- Inputs --- */
textarea, input, select {
    color: #e5e7eb !important;
}

/* --- Terminal (Industrial Green Phosphor, mais sutil) --- */
.terminal-box textarea {
    background-color: #0a0d0f !important;
    color: #6ee7b7 !important;
    font-family: 'Courier New', monospace !important;
    border: 1px solid #2f343b !important;
}

/* --- Header --- */
.main-header {
    text-align: center;
    margin-bottom: 20px;
    font-size: 2.5em;
    color: #e5e7eb;
    font-weight: 600;
    letter-spacing: 0.5px;
}

/* --- Slider Glow (Cold Metal) --- */
.glowing-progress .track-fill {
    background: linear-gradient(90deg, #9aa4af, #c0c6cf) !important;
    box-shadow: 0 0 4px rgba(192,198,207,0.4);
}

/* --- Metallic subtle highlight (top light reflection) --- */
.gradio-container {
    background-image: linear-gradient(
        180deg,
        rgba(255,255,255,0.04) 0%,
        rgba(255,255,255,0.00) 40%
    );
}

/* --- Button hover (metal shine) --- */
button:hover {
    filter: brightness(1.15);
}
"""