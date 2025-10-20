import { Routes } from "@angular/router";
import { PlayerPage, resolvePlayer, resolvePostSeasonStats, resolveRegSeasonStats } from "./player-page/player-page";
import { SearchPage } from "./search-page/search-page";
import { HomePage } from "./home-page/home-page";
import { SkaterLeaderboardPage } from "./skater-leaderboard-page/skater-leaderboard-page";

export const routes: Routes = [
    {
        path: '',
        component: HomePage
    },
    {
        path: 'players/:playerID',
        component: PlayerPage,
        resolve: {
            playerInfoResource: resolvePlayer,
            regSeasonResource: resolveRegSeasonStats,
            postSeasonResource: resolvePostSeasonStats
        }
    },
    {
        path: 'leaderboards/:season',
        component: SkaterLeaderboardPage
    },
    {
        path: 'search',
        component: SearchPage
    }
]