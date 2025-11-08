from .ROUTES import MAIN, DASHBOARD, ABOUT, require_auth
from nicegui.ui import page
from pages.PageWelcome import create as create_welcome
from pages.PageDashboard import create as create_dashboard
from pages.PageAbout import create as create_about

@page(MAIN)
async def render_main():
    await create_welcome()

@page(DASHBOARD)
@require_auth
async def render_dashboard():
    await create_dashboard()

@page(ABOUT)
async def render_about():
    await create_about()
