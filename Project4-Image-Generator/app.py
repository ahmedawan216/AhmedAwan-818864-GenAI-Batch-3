try:
    import streamlit as st  # type: ignore[import]
except ImportError as e:
    raise ImportError(
        "streamlit is required to run this app. Install it with `pip install streamlit`."
    ) from e
import requests
import io
from PIL import Image
from datetime import datetime
import os
from utils import generate_with_pollinations, generate_with_huggingface, save_image

# Page config
st.set_page_config(
    page_title="AI Image Generator",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .main {
        background-color: #0f0f1a;
    }

    .stApp {
        background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 100%);
    }

    .hero-title {
        font-size: 2.8rem;
        font-weight: 700;
        background: linear-gradient(90deg, #a78bfa, #38bdf8, #34d399);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.2rem;
    }

    .hero-subtitle {
        color: #94a3b8;
        font-size: 1.05rem;
        margin-bottom: 2rem;
    }

    .badge {
        display: inline-block;
        background: #1e1e3a;
        border: 1px solid #7c3aed44;
        border-radius: 20px;
        padding: 4px 14px;
        font-size: 0.78rem;
        color: #a78bfa;
        margin-right: 8px;
        margin-bottom: 12px;
    }

    .model-card {
        background: #1a1a2e;
        border: 1px solid #2d2d4e;
        border-radius: 12px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.8rem;
        cursor: pointer;
    }

    .model-card:hover {
        border-color: #7c3aed;
    }

    .stButton > button {
        background: linear-gradient(90deg, #7c3aed, #2563eb);
        color: white;
        border: none;
        border-radius: 10px;
        font-weight: 600;
        font-size: 1rem;
        padding: 0.6rem 2rem;
        width: 100%;
        transition: opacity 0.2s;
    }

    .stButton > button:hover {
        opacity: 0.88;
        color: white;
    }

    .stTextArea textarea {
        background: #1a1a2e !important;
        border: 1px solid #2d2d4e !important;
        color: #e2e8f0 !important;
        border-radius: 10px !important;
        font-size: 0.95rem !important;
    }

    .stTextArea textarea:focus {
        border-color: #7c3aed !important;
        box-shadow: 0 0 0 2px #7c3aed33 !important;
    }

    .stSelectbox > div > div {
        background: #1a1a2e !important;
        border: 1px solid #2d2d4e !important;
        color: #e2e8f0 !important;
        border-radius: 10px !important;
    }

    .stSlider > div > div {
        color: #a78bfa !important;
    }

    .image-result {
        border-radius: 14px;
        overflow: hidden;
        box-shadow: 0 8px 32px rgba(124, 58, 237, 0.25);
    }

    .tip-box {
        background: #1a1a2e;
        border-left: 3px solid #7c3aed;
        border-radius: 0 8px 8px 0;
        padding: 0.8rem 1rem;
        color: #94a3b8;
        font-size: 0.88rem;
        margin-top: 1rem;
    }

    .sidebar-section {
        background: #1a1a2e;
        border: 1px solid #2d2d4e;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
    }

    label, .stRadio label, .stSelectbox label {
        color: #94a3b8 !important;
        font-size: 0.9rem !important;
    }

    h3 {
        color: #e2e8f0 !important;
    }

    .success-badge {
        background: #064e3b;
        color: #34d399;
        border-radius: 6px;
        padding: 3px 10px;
        font-size: 0.8rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)


# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Settings")

    # API Backend
    st.markdown("**Backend**")
    backend = st.radio(
        "Choose backend",
        ["Pollinations.ai (No Key)", "Hugging Face (Free Token)"],
        label_visibility="collapsed"
    )

    hf_token = ""
    if backend == "Hugging Face (Free Token)":
        hf_token = st.text_input(
            "Hugging Face Token",
            type="password",
            placeholder="hf_xxxxxxxxxxxx",
            help="Get free token at huggingface.co → Settings → Access Tokens"
        )
        if not hf_token:
            st.warning("⚠️ Add your HF token above to use this backend.")

    st.divider()

    # Model selection
    st.markdown("**Model**")
    if backend == "Hugging Face (Free Token)":
        model = st.selectbox(
            "Model",
            [
                "black-forest-labs/FLUX.1-schnell",
                "black-forest-labs/FLUX.1-dev",
                "stabilityai/stable-diffusion-3.5-large",
                "stabilityai/stable-diffusion-xl-base-1.0",
            ],
            label_visibility="collapsed"
        )
    else:
        model = st.selectbox(
            "Model",
            ["flux", "turbo", "flux-realism"],
            label_visibility="collapsed"
        )

    st.divider()

    # Image settings
    st.markdown("**Image Size**")
    if backend == "Hugging Face (Free Token)":
        width = st.slider("Width", 256, 1024, 512, step=64)
        height = st.slider("Height", 256, 1024, 512, step=64)
    else:
        size_option = st.selectbox(
            "Size",
            ["1024×1024", "1280×720", "720×1280", "512×512"],
            label_visibility="collapsed"
        )
        w_h = size_option.split("×")
        width, height = int(w_h[0]), int(w_h[1])

    st.divider()
    st.markdown("""
    <div style='color:#475569;font-size:0.8rem;line-height:1.6'>
    💡 <b style='color:#7c3aed'>Pollinations</b> — No setup needed<br>
    🤗 <b style='color:#7c3aed'>Hugging Face</b> — Better quality, free token required
    </div>
    """, unsafe_allow_html=True)


# ── Main ─────────────────────────────────────────────────────────────────────
st.markdown('<div class="hero-title">🎨 AI Image Generator</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Generate stunning images for free using FLUX & Stable Diffusion</div>', unsafe_allow_html=True)

st.markdown("""
<span class="badge">✨ 100% Free</span>
<span class="badge">⚡ FLUX & SD Models</span>
<span class="badge">🔑 No Credit Card</span>
""", unsafe_allow_html=True)

# Prompt input
prompt = st.text_area(
    "Describe your image",
    placeholder="e.g. A majestic lion wearing a golden crown, sitting on a throne, dramatic lighting, hyperrealistic, 8K...",
    height=110,
    label_visibility="visible"
)

negative_prompt = st.text_input(
    "Negative prompt (optional)",
    placeholder="blurry, low quality, distorted, watermark...",
    help="Describe what you don't want in the image"
)

# Example prompts
st.markdown("**✨ Try an example:**")
examples = [
    "Cyberpunk city at night, neon lights, rain reflections, cinematic",
    "A cute robot reading a book in a cozy library, warm lighting, detailed",
    "Underwater palace with glowing corals, fantasy art, ultra detailed",
    "Portrait of an astronaut on Mars at golden hour, photorealistic",
]
cols = st.columns(2)
for i, ex in enumerate(examples):
    if cols[i % 2].button(f"💡 {ex[:42]}...", key=f"ex_{i}"):
        st.session_state["example_prompt"] = ex
        st.rerun()

if "example_prompt" in st.session_state:
    prompt = st.session_state.pop("example_prompt")

st.markdown("")

# Generate button
if st.button("🚀 Generate Image", use_container_width=True):
    if not prompt.strip():
        st.error("Please enter a prompt first.")
    elif backend == "Hugging Face (Free Token)" and not hf_token:
        st.error("Please add your Hugging Face token in the sidebar.")
    else:
        with st.spinner("🎨 Generating your image... this may take 10–30 seconds"):
            try:
                if backend == "Pollinations.ai (No Key)":
                    image, img_url = generate_with_pollinations(prompt, width, height, model)
                else:
                    image, img_url = generate_with_huggingface(
                        prompt, negative_prompt, hf_token, model, width, height
                    )

                if image:
                    st.success("✅ Image generated successfully!")

                    col1, col2 = st.columns([2, 1])
                    with col1:
                        st.image(image, use_container_width=True, caption=prompt[:80])

                    with col2:
                        st.markdown("### 📥 Download")
                        buf = io.BytesIO()
                        image.save(buf, format="PNG")
                        st.download_button(
                            label="⬇️ Download PNG",
                            data=buf.getvalue(),
                            file_name=f"generated_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
                            mime="image/png",
                            use_container_width=True
                        )

                        st.markdown("### 📊 Details")
                        st.markdown(f"**Size:** {image.width} × {image.height}px")
                        st.markdown(f"**Backend:** {backend.split('(')[0].strip()}")
                        st.markdown(f"**Model:** `{model.split('/')[-1] if '/' in model else model}`")

                        if img_url:
                            st.markdown(f"**[🔗 Direct URL]({img_url})**")

                else:
                    st.error("Failed to generate image. Please try again.")

            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.info("If using Hugging Face, the model may be loading (cold start). Wait 20 seconds and try again.")

# Tips
st.markdown("""
<div class="tip-box">
💡 <b>Prompt tips:</b> Add words like <i>hyperrealistic, cinematic, 8K, detailed, dramatic lighting, award-winning</i> for better results. 
Be specific about style: <i>oil painting, watercolor, 3D render, anime, photorealistic</i>.
</div>
""", unsafe_allow_html=True)