import os

# Chromium flags for WebEngine only — do not disable Qt/X11 GLX (needed for QRhi).
WEBENGINE_CHROMIUM_FLAGS = (
    "--disable-gpu "
    "--disable-gpu-compositing "
    "--disable-vulkan "
    "--no-sandbox "
    "--disable-dev-shm-usage"
)


def configure_webengine_env():
    """Must run before PyQt6 or QtWebEngine modules are imported."""
    os.environ.setdefault("QTWEBENGINE_CHROMIUM_FLAGS", WEBENGINE_CHROMIUM_FLAGS)

    if os.environ.get("SNAP"):
        os.environ.setdefault("QTWEBENGINE_DISABLE_SANDBOX", "1")
