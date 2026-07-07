import os

# Shared Chromium flags for confined / snap environments where GPU dma_buf fails.
WEBENGINE_CHROMIUM_FLAGS = (
    "--disable-gpu "
    "--disable-gpu-compositing "
    "--disable-vulkan "
    "--no-sandbox "
    "--disable-dev-shm-usage "
    "--disable-features=VizDisplayCompositor "
    "--use-gl=swiftshader"
)


def configure_webengine_env():
    """Must run before PyQt6 or QtWebEngine modules are imported."""
    os.environ.setdefault("QTWEBENGINE_CHROMIUM_FLAGS", WEBENGINE_CHROMIUM_FLAGS)

    if os.environ.get("SNAP"):
        os.environ.setdefault("QT_OPENGL", "software")
        os.environ.setdefault("QT_XCB_GL_INTEGRATION", "none")
        os.environ.setdefault("QTWEBENGINE_DISABLE_SANDBOX", "1")
