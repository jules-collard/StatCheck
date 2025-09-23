import { Routes } from "@angular/router";
import { PlayerPage, resolvePlayer, resolvePostSeasonStats, resolveRegSeasonStats } from "./player-page/player-page";
import { SearchPage } from "./search-page/search-page";
import { HomePage } from "./home-page/home-page";

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
        path: 'search',
        component: SearchPage
    }
]