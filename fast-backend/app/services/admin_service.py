import os

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

class AdminService:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_skater_stats_view(self):
        path = os.path.join(os.path.dirname(__file__), '..', 'db', 'sql', 'views', 'create_skater_stats_view.sql')
        with open(path) as f:
            view_query = f.read()

        path = os.path.join(os.path.dirname(__file__), '..', 'db', 'sql', 'views', 'create_skater_stats_indices.sql')
        with open(path) as f:
            indices_query = f.read().splitlines()
        
        await self.session.execute(text(view_query))
        for q in indices_query:
            await self.session.execute(text(q))

    async def create_goalie_stats_view(self):
        path = os.path.join(os.path.dirname(__file__), '..', 'db', 'sql', 'views', 'create_goalie_stats_view.sql')
        with open(path) as f:
            view_query = f.read()

        path = os.path.join(os.path.dirname(__file__), '..', 'db', 'sql', 'views', 'create_goalie_stats_indices.sql')
        with open(path) as f:
            indices_query = f.read().splitlines()
        
        await self.session.execute(text(view_query))
        for q in indices_query:
            await self.session.execute(text(q))

    async def refresh_views(self):
        await self.session.execute(text("REFRESH MATERIALIZED VIEW skater_stats"))
        await self.session.execute(text("REFRESH MATERIALIZED VIEW goalie_stats"))
